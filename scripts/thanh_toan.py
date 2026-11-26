"""Nailmark – thanh toán VietQR tự xác nhận và giao hàng ngay (không cần người).

Luồng: tạo đơn (mã NMxxxxxx) -> QR VietQR có sẵn số tiền + nội dung = mã đơn -> khách chuyển khoản
-> cổng (SePay/payOS...) gọi webhook -> khớp mã + số tiền -> đánh dấu ĐÃ TRẢ (chống trùng) -> giao hàng tự động.
Đơn từ 3.000.000đ: giao hàng sau bước xác minh (một cuộc gọi), theo nguyên tắc đã chốt.

Cấu hình (biến môi trường, CHƯA CÓ tài khoản thật thì chạy chế độ mẫu):
  NAILMARK_BANK_BIN   mã BIN ngân hàng nhận (6 số, theo danh sách NAPAS)    – mẫu: 970436
  NAILMARK_BANK_ACC   số tài khoản nhận                                     – mẫu: 0000000000 (TÀI KHOẢN MẪU)
  NAILMARK_BANK_NAME  tên chủ tài khoản hiển thị
  SEPAY_API_KEY       khoá xác thực webhook (header "Authorization: Apikey <khoá>") – ĐỐI CHIẾU tài liệu SePay khi mở tài khoản
  NAILMARK_DEV=1      bật nút "giả lập đã thanh toán" để chạy thử
Đơn hàng lưu ở du_lieu/don_hang.json (KHÔNG đưa lên git: có tên tiệm, số điện thoại).
"""
import json
import os
import random
import string
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KHO = ROOT / "du_lieu" / "don_hang.json"
KHOA = threading.Lock()

SAN_PHAM = {
    "bo-tet-99k": dict(ten="Bộ Tết mang tên tiệm", gia=99_000),
    "khoi-dau": dict(ten="Web Khởi đầu", gia=999_000),
    "chuan": dict(ten="Web Chuẩn", gia=1_990_000),
    "dang-cap": dict(ten="Web Đẳng cấp", gia=2_990_000),
    "goi-mua": dict(ten="Gói Mùa", gia=1_490_000),
    "chuyen-giao": dict(ten="Chuyển giao cho nhân viên", gia=4_990_000),
    "lam-ho": dict(ten="Làm hộ trọn gói", gia=9_990_000),
}
MA_GIAM = {"KHAUTRU99": dict(tru=99_000, ap_dung={"khoi-dau", "chuan", "dang-cap"})}
NGUONG_XAC_MINH = 3_000_000
# Giới thiệu (affiliate) – anh Ninh chốt 26/11/2026:
#   đơn ≤ 5.000.000đ: người giới thiệu nhận 15%; đơn > 5.000.000đ: nhận 20%; tiệm dùng link giới thiệu giảm 5%.
#   Hoa hồng tính trên số tiền tiệm thực trả. Chỉ ghi nhận khi đơn đã trả tiền. Không tự giới thiệu chính mình.
NGUONG_HH = 5_000_000
HH_THAP, HH_CAO, GIAM_GT = 0.15, 0.20, 0.05


def _doc():
    try:
        return json.loads(KHO.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _ghi(d):
    KHO.parent.mkdir(parents=True, exist_ok=True)
    KHO.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def crc16(s: str) -> str:
    crc = 0xFFFF
    for ch in s.encode("utf-8"):
        crc ^= ch << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) if crc & 0x8000 else (crc << 1)
            crc &= 0xFFFF
    return f"{crc:04X}"


def tlv(tag, val):
    return f"{tag}{len(val):02d}{val}"


def vietqr(bin_nh, stk, so_tien, noi_dung):
    """Chuỗi VietQR (chuẩn EMVCo/NAPAS) có sẵn số tiền và nội dung chuyển khoản."""
    tk = tlv("00", "A000000727") + tlv("01", tlv("00", bin_nh) + tlv("01", stk)) + tlv("02", "QRIBFTTA")
    s = (tlv("00", "01") + tlv("01", "12") + tlv("38", tk) + tlv("53", "704") + tlv("54", str(int(so_tien)))
         + tlv("58", "VN") + tlv("62", tlv("08", noi_dung)) + "6304")
    return s + crc16(s)


def tai_khoan():
    return dict(bin=os.environ.get("NAILMARK_BANK_BIN", "970436"), stk=os.environ.get("NAILMARK_BANK_ACC", "0000000000"),
                ten=os.environ.get("NAILMARK_BANK_NAME", "TÀI KHOẢN MẪU – CHƯA NHẬN TIỀN THẬT"),
                mau="NAILMARK_BANK_ACC" not in os.environ)


def tao_don(goi, ten_tiem, zalo, ma_giam="", them=None, ma_gt=""):
    if goi not in SAN_PHAM:
        raise ValueError("Gói không có.")
    gia = SAN_PHAM[goi]["gia"]
    mg = MA_GIAM.get((ma_giam or "").strip().upper())
    # KHAUTRU99 chỉ dành cho tiệm (theo số Zalo) đã mua và trả tiền bộ 99k
    da_mua_99 = any(x.get("goi") == "bo-tet-99k" and x.get("zalo") == zalo and x.get("trang_thai") == "da_tra" for x in _doc().values())
    tru = mg["tru"] if mg and goi in mg["ap_dung"] and da_mua_99 else 0
    ma = "NM" + "".join(random.choices(string.digits, k=6))
    tk = tai_khoan()
    nguoi_gt = tim_nguoi_gt(ma_gt, zalo)
    giam_gt = round((gia - tru) * GIAM_GT / 1000) * 1000 if nguoi_gt else 0
    tien = gia - tru - giam_gt
    don = dict(ma=ma, goi=goi, ten_goi=SAN_PHAM[goi]["ten"], so_tien=tien, giam=tru + giam_gt, giam_gt=giam_gt,
               ma_gt=nguoi_gt["ma_gt"] if nguoi_gt else "", ten_tiem=ten_tiem, zalo=zalo,
               trang_thai="cho_thanh_toan", tao_luc=int(time.time()), xac_minh=tien >= NGUONG_XAC_MINH,
               hoa_hong=round(tien * (HH_CAO if tien > NGUONG_HH else HH_THAP)) if nguoi_gt else 0,
               qr=vietqr(tk["bin"], tk["stk"], tien, ma), them=them or {})
    with KHOA:
        d = _doc(); d[ma] = don; _ghi(d)
    return don


def lay_don(ma):
    return _doc().get(ma)


def ghi_nhan_tien(noi_dung, so_tien, ma_gd):
    """Gọi từ webhook. Khớp mã đơn trong nội dung CK + đủ tiền. Trả về đơn nếu vừa chuyển sang ĐÃ TRẢ."""
    with KHOA:
        d = _doc()
        if any(x.get("ma_gd") == str(ma_gd) for x in d.values()):
            return None  # tin báo trùng (cổng gửi lại) -> bỏ qua
        for ma, don in d.items():
            if ma in (noi_dung or "").upper().replace(" ", "") and don["trang_thai"] == "cho_thanh_toan":
                if int(so_tien) < don["so_tien"]:
                    don["trang_thai"] = "thieu_tien"; don["da_nhan"] = int(so_tien)
                else:
                    don["trang_thai"] = "cho_xac_minh" if don["xac_minh"] else "da_tra"
                don["ma_gd"] = str(ma_gd); don["tra_luc"] = int(time.time())
                _ghi(d)
                return don
    return None


def cap_nhat(ma, **kv):
    with KHOA:
        d = _doc()
        if ma in d:
            d[ma].update(kv); _ghi(d)
            return d[ma]


# ---------------- Giới thiệu (affiliate) ----------------
def ma_gioi_thieu(zalo):
    """Mỗi tiệm (theo số Zalo) có một mã giới thiệu cố định, cấp khi đã có ít nhất một đơn trả tiền."""
    import hashlib
    return "GT" + hashlib.sha256(("nailmark-gt-" + zalo).encode()).hexdigest()[:6].upper()


def tim_nguoi_gt(ma_gt, zalo_nguoi_mua):
    ma_gt = (ma_gt or "").strip().upper()
    if not ma_gt:
        return None
    for don in _doc().values():
        if don.get("trang_thai") in ("da_tra", "cho_xac_minh") and ma_gioi_thieu(don["zalo"]) == ma_gt:
            if don["zalo"] == zalo_nguoi_mua:
                return None  # không tự giới thiệu chính mình
            return dict(ma_gt=ma_gt, zalo=don["zalo"], ten_tiem=don["ten_tiem"])
    return None


def thong_ke_gt(ma_gt):
    ma_gt = (ma_gt or "").upper()
    d = _doc()
    chu = next((x for x in d.values() if x.get("trang_thai") in ("da_tra", "cho_xac_minh") and ma_gioi_thieu(x["zalo"]) == ma_gt), None)
    if not chu:
        return None
    don_gt = [x for x in d.values() if x.get("ma_gt") == ma_gt and x.get("trang_thai") in ("da_tra", "cho_xac_minh")]
    return dict(ma_gt=ma_gt, ten_tiem=chu["ten_tiem"], so_don=len(don_gt), tong_hoa_hong=sum(x["hoa_hong"] for x in don_gt),
                don=[dict(ngay=time.strftime("%d/%m/%Y", time.localtime(x["tra_luc"])), goi=x["ten_goi"], so_tien=x["so_tien"],
                          hoa_hong=x["hoa_hong"]) for x in sorted(don_gt, key=lambda x: x["tra_luc"], reverse=True)])
