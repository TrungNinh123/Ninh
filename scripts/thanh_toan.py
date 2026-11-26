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


def tao_don(goi, ten_tiem, zalo, ma_giam="", them=None):
    if goi not in SAN_PHAM:
        raise ValueError("Gói không có.")
    gia = SAN_PHAM[goi]["gia"]
    mg = MA_GIAM.get((ma_giam or "").strip().upper())
    tru = mg["tru"] if mg and goi in mg["ap_dung"] else 0
    ma = "NM" + "".join(random.choices(string.digits, k=6))
    tk = tai_khoan()
    don = dict(ma=ma, goi=goi, ten_goi=SAN_PHAM[goi]["ten"], so_tien=gia - tru, giam=tru, ten_tiem=ten_tiem, zalo=zalo,
               trang_thai="cho_thanh_toan", tao_luc=int(time.time()), xac_minh=gia - tru >= NGUONG_XAC_MINH,
               qr=vietqr(tk["bin"], tk["stk"], gia - tru, ma), them=them or {})
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
