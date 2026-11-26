"""Nailmark – chi hoa hồng giới thiệu TỰ ĐỘNG, không người duyệt từng đơn.

Nguyên tắc (anh Ninh chốt 26/11/2026):
- Người giới thiệu là CỘNG TÁC VIÊN, không phải nhân viên. Nailmark chỉ chuyển tiền; người nhận tự lo phần thuế
  của mình (điều khoản họ bấm đồng ý khi đăng ký tài khoản nhận tiền).
- Đơn ≤ 5tr: 15%; đơn > 5tr: 20% (tính trong thanh_toan.py). Người mua qua link giảm 5%.

Bảo vệ quyền lợi người gửi link:
1. Khách đã mua qua link của ai thì GẮN với người đó 12 tháng: gia hạn, lên gói, mua thêm trong 12 tháng
   vẫn tính hoa hồng cho người giới thiệu đầu tiên, kể cả khi khách quên mở lại link.
2. Link được nhớ trên máy khách 60 ngày; khách cũng có ô tự gõ mã giới thiệu khi thanh toán.
3. Mỗi đơn được chi riêng ngay khi qua hạn giữ, không chờ cuối tháng, không mức tối thiểu.
4. Trang Giới thiệu (link riêng có khoá) hiện từng đơn: trạng thái, ngày dự kiến nhận, mã giao dịch đã chi.

Kiểm tra tự động trước khi chi (máy tự làm, không ai phải xem):
- đơn đã nhận đủ tiền, chưa hoàn tiền;
- qua HẠN GIỮ (mặc định 7 ngày, bằng thời hạn hoàn tiền – chỉnh HH_GIU_NGAY);
- không tự giới thiệu: khác số Zalo, khác tên tiệm (so sau khi bỏ dấu, khoảng trắng);
- người giới thiệu đã đăng ký tài khoản nhận và đồng ý điều khoản cộng tác viên;
- tài khoản nhận không vừa bị đổi trong 3 ngày (chống chiếm tài khoản);
- mỗi đơn chỉ chi một lần (khoá chống trùng = mã đơn, gửi kèm cổng chi làm idempotency key).
Đơn không qua kiểm tra không bị "treo chờ người": nó tự chi khi điều kiện đủ (vd người nhận nhập tài khoản),
hoặc tự huỷ (đơn hoàn tiền).

Cổng chi: payOS Payouts API (POST /v1/payouts, có x-idempotency-key) – theo SDK chính thức `payos` 1.1.1.
Cần anh mở payOS và bật chi hộ; khoá đặt qua biến môi trường PAYOS_PAYOUT_CLIENT_ID / _API_KEY / _CHECKSUM_KEY.
Chưa có khoá: NAILMARK_DEV=1 -> chi giả lập; không DEV -> đơn ở trạng thái "chờ cổng chi", tự chi khi có khoá.

Thuế: Nailmark không khai thuế thay cộng tác viên. Nếu luật buộc bên trả khấu trừ khi một lần chi từ ngưỡng
trở lên, hệ thống tự trừ (HH_THUE_NGUONG, HH_THUE_TY_LE). Ngưỡng 5.000.000đ/lần theo NĐ 253/2026 (nguồn thứ cấp,
CẦN kế toán xác nhận). Với bảng giá hiện tại, hoa hồng mỗi đơn cao nhất ≈ 1,9tr nên chưa chạm ngưỡng.
"""
import hashlib
import hmac
import os
import re
import time
import unicodedata

import thanh_toan as tt

NGAY = 86_400
HH_GIU_NGAY = int(os.environ.get("HH_GIU_NGAY", "7"))
DOI_TK_CHO_NGAY = 3
GAN_KHACH_NGAY = 365
HH_THUE_NGUONG = int(os.environ.get("HH_THUE_NGUONG", "5000000"))
HH_THUE_TY_LE = float(os.environ.get("HH_THUE_TY_LE", "0.10"))
DIEU_KHOAN = ("Tôi là cộng tác viên giới thiệu độc lập, không phải nhân viên Nailmark. Nailmark chuyển hoa hồng vào tài "
              "khoản tôi đăng ký; tôi tự chịu trách nhiệm kê khai và nộp thuế thu nhập của mình. Nếu pháp luật buộc bên "
              "trả khấu trừ thuế, Nailmark khấu trừ đúng quy định và báo trên trang này. Không tự giới thiệu chính mình, "
              "không dùng số Zalo khác để mua qua link của mình; đơn vi phạm không được tính hoa hồng.")


def _bi_mat():
    return os.environ.get("NAILMARK_SECRET", "dev-chi-de-thu-nghiem").encode()


def khoa_ctv(ma_gt):
    """Khoá riêng của cộng tác viên (chỉ hiện ở trang cảm ơn của chính họ). Không lưu, tính lại từ bí mật máy chủ."""
    return hmac.new(_bi_mat(), ("ctv-" + ma_gt.upper()).encode(), hashlib.sha256).hexdigest()[:16]


def dung_khoa(ma_gt, khoa):
    return bool(khoa) and hmac.compare_digest(khoa_ctv(ma_gt), str(khoa))


def chuan_ten(s):
    s = unicodedata.normalize("NFD", (s or "").lower()).replace("đ", "d")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"\b(tiem|nail|nails|spa|salon|beauty)\b", "", s)
    return re.sub(r"[^a-z0-9]", "", s)


# ---------------- dữ liệu cộng tác viên (lưu cùng kho đơn, khoá "_ctv" và "_gan") ----------------
def _kho():
    d = tt._doc()
    d.setdefault("_ctv", {}); d.setdefault("_gan", {})
    return d


def don_cua(d):
    return {k: v for k, v in d.items() if not k.startswith("_")}


def nguoi_gt_da_gan(zalo, d=None, now=None):
    """Khách đã từng mua qua link ai trong 12 tháng -> trả mã người đó."""
    d = d or _kho(); now = now or time.time()
    g = d["_gan"].get(zalo)
    if g and now - g["luc"] < GAN_KHACH_NGAY * NGAY:
        return g["ma_gt"]
    return None


def gan_khach(zalo, ma_gt, now=None):
    with tt.KHOA:
        d = _kho()
        if not nguoi_gt_da_gan(zalo, d, now):
            d["_gan"][zalo] = dict(ma_gt=ma_gt, luc=int(now or time.time()))
            tt._ghi(d)


def dang_ky_tai_khoan(ma_gt, khoa, bin_nh, stk, ten_tk, dong_y):
    ma_gt = (ma_gt or "").upper()
    if not dung_khoa(ma_gt, khoa):
        raise ValueError("Link quản lý không đúng. Chị mở lại link riêng ở trang cảm ơn sau khi thanh toán.")
    if not dong_y:
        raise ValueError("Chị cần đồng ý điều khoản cộng tác viên.")
    bin_nh, stk = re.sub(r"\D", "", bin_nh or ""), re.sub(r"\D", "", stk or "")
    ten_tk = re.sub(r"\s+", " ", (ten_tk or "").strip().upper())
    if len(bin_nh) != 6 or not 6 <= len(stk) <= 19 or len(ten_tk) < 4:
        raise ValueError("Kiểm tra lại ngân hàng, số tài khoản (6–19 số) và tên chủ tài khoản.")
    with tt.KHOA:
        d = _kho()
        cu = d["_ctv"].get(ma_gt, {})
        doi = bool(cu.get("stk")) and (cu.get("stk"), cu.get("bin")) != (stk, bin_nh)
        d["_ctv"][ma_gt] = dict(bin=bin_nh, stk=stk, ten_tk=ten_tk, dong_y_luc=int(time.time()),
                                doi_tk_luc=int(time.time()) if doi else cu.get("doi_tk_luc", 0))
        tt._ghi(d)
    return dict(ok=True, doi_tk=doi)


# ---------------- kiểm tra tự động ----------------
def kiem_tra(don, d, now):
    """Trả về (trạng thái hoa hồng, lý do, ngày dự kiến). Không có trạng thái nào cần người xem."""
    if not don.get("ma_gt") or not don.get("hoa_hong"):
        return "khong_co", "", None
    if don.get("hh_trang_thai") in ("da_chi", "dang_chi"):
        return don["hh_trang_thai"], "", None
    if don["trang_thai"] in ("hoan_tien", "huy"):
        return "huy", "Đơn đã hoàn tiền", None
    if don["trang_thai"] not in ("da_tra", "cho_xac_minh"):
        return "cho_thanh_toan", "Tiệm bạn chưa thanh toán", None
    chu = next((x for x in don_cua(d).values() if tt.ma_gioi_thieu(x["zalo"]) == don["ma_gt"]), None)
    if chu and (chu["zalo"] == don["zalo"] or chuan_ten(chu["ten_tiem"]) == chuan_ten(don["ten_tiem"])):
        return "huy", "Tự giới thiệu chính mình", None
    het_giu = don["tra_luc"] + HH_GIU_NGAY * NGAY
    if now < het_giu:
        return "cho_het_han_giu", f"Giữ {HH_GIU_NGAY} ngày theo thời hạn hoàn tiền", het_giu
    ctv = d["_ctv"].get(don["ma_gt"])
    if not ctv or not ctv.get("stk"):
        return "cho_tai_khoan", "Chị nhập tài khoản nhận tiền là hệ thống chi ngay", None
    if ctv.get("doi_tk_luc") and now < ctv["doi_tk_luc"] + DOI_TK_CHO_NGAY * NGAY:
        return "cho_het_han_giu", "Tài khoản nhận vừa đổi, chờ 3 ngày để an toàn", ctv["doi_tk_luc"] + DOI_TK_CHO_NGAY * NGAY
    return "san_sang", "", now


def thue_cua(so):
    return round(so * HH_THUE_TY_LE) if so >= HH_THUE_NGUONG else 0


# ---------------- cổng chi ----------------
class CongPayOS:
    """payOS Payouts API theo SDK chính thức `payos` (POST /v1/payouts, header x-idempotency-key, ký HMAC)."""
    ten = "payos"

    def __init__(self):
        from payos import PayOS  # pip install payos
        self.c = PayOS(client_id=os.environ["PAYOS_PAYOUT_CLIENT_ID"], api_key=os.environ["PAYOS_PAYOUT_API_KEY"],
                       checksum_key=os.environ["PAYOS_PAYOUT_CHECKSUM_KEY"])

    def chi(self, ref, so_tien, bin_nh, stk, noi_dung):
        from payos.types import PayoutRequest
        p = self.c.payouts.create(PayoutRequest(reference_id=ref, amount=so_tien, description=noi_dung,
                                                to_bin=bin_nh, to_account_number=stk, category=["hoa-hong"]),
                                  idempotency_key=ref)
        return dict(ma_gd=p.id, trang_thai=p.approval_state)


class CongGiaLap:
    ten = "gia_lap"

    def chi(self, ref, so_tien, bin_nh, stk, noi_dung):
        return dict(ma_gd="GL-" + ref, trang_thai="COMPLETED")


def cong_chi():
    if os.environ.get("PAYOS_PAYOUT_CLIENT_ID"):
        return CongPayOS()
    if os.environ.get("NAILMARK_DEV") == "1":
        return CongGiaLap()
    return None


def chay_chi(now=None, cong=None):
    """Chạy định kỳ (mỗi giờ). Tự kiểm tra từng đơn, chi đơn đủ điều kiện. Trả về danh sách đã chi."""
    now = now or time.time()
    cong = cong if cong is not None else cong_chi()
    da_chi = []
    with tt.KHOA:
        d = _kho()
        viec = []
        for ma, don in don_cua(d).items():
            tt_hh, ly_do, du_kien = kiem_tra(don, d, now)
            if tt_hh == "san_sang" and cong is None:
                tt_hh, ly_do = "cho_cong_chi", "Hệ thống chi đang kết nối ngân hàng"
            don["hh_trang_thai"], don["hh_ly_do"], don["hh_du_kien"] = tt_hh, ly_do, du_kien
            if tt_hh == "san_sang":
                don["hh_trang_thai"] = "dang_chi"
                viec.append(ma)
        tt._ghi(d)
    for ma in viec:  # gọi cổng ngoài khoá; chống trùng nhờ idempotency key = mã đơn
        d = _kho(); don = d[ma]; ctv = d["_ctv"][don["ma_gt"]]
        thue = thue_cua(don["hoa_hong"]); thuc = don["hoa_hong"] - thue
        try:
            kq = cong.chi("HH" + ma, thuc, ctv["bin"], ctv["stk"], f"Nailmark hoa hong {ma}")
            tt.cap_nhat(ma, hh_trang_thai="da_chi", hh_chi_luc=int(now), hh_ma_gd=kq["ma_gd"], hh_thue=thue,
                        hh_thuc_nhan=thuc, hh_cong=cong.ten, hh_ly_do="")
            da_chi.append(ma)
        except Exception as e:  # lỗi cổng: tự thử lại lần chạy sau, cùng idempotency key nên không chi trùng
            tt.cap_nhat(ma, hh_trang_thai="san_sang", hh_ly_do="Ngân hàng chưa nhận lệnh, hệ thống tự thử lại",
                        hh_loi=str(e)[:200])
    return da_chi


NHAN = dict(cho_thanh_toan="Chờ tiệm bạn thanh toán", cho_het_han_giu="Đang giữ, sẽ tự chi", cho_tai_khoan="Cần tài khoản nhận",
            cho_cong_chi="Chờ hệ thống chi", san_sang="Đang chi", dang_chi="Đang chi", da_chi="Đã chuyển", huy="Không tính")


def bao_cao(ma_gt, khoa=None, now=None):
    """Số liệu cho trang Giới thiệu. Không có khoá: chỉ tổng. Có khoá đúng: chi tiết từng đơn, tài khoản nhận."""
    ma_gt = (ma_gt or "").upper(); now = now or time.time()
    d = _kho()
    chu = next((x for x in don_cua(d).values() if x.get("trang_thai") in ("da_tra", "cho_xac_minh")
                and tt.ma_gioi_thieu(x["zalo"]) == ma_gt), None)
    if not chu:
        return None
    ds = [x for x in don_cua(d).values() if x.get("ma_gt") == ma_gt and x.get("trang_thai") not in ("cho_thanh_toan",)]
    hang = []
    for x in sorted(ds, key=lambda x: x.get("tra_luc", 0), reverse=True):
        # Trạng thái do vòng chi tự động ghi lại là chuẩn; đơn chưa qua vòng nào thì tính ngay.
        st, ly_do, du_kien = (x["hh_trang_thai"], x.get("hh_ly_do", ""), x.get("hh_du_kien")) if x.get("hh_trang_thai") else kiem_tra(x, d, now)
        if x["trang_thai"] == "thieu_tien":
            st, ly_do, du_kien = "cho_thanh_toan", "Tiệm bạn chuyển chưa đủ tiền", None
        hang.append(dict(ngay=time.strftime("%d/%m/%Y", time.localtime(x.get("tra_luc", x["tao_luc"]))), goi=x["ten_goi"],
                         so_tien=x["so_tien"], hoa_hong=x["hoa_hong"], trang_thai=st, nhan=NHAN.get(st, st), ly_do=ly_do,
                         du_kien=time.strftime("%d/%m/%Y", time.localtime(du_kien)) if du_kien and st != "da_chi" else "",
                         ma_gd=x.get("hh_ma_gd", "") if khoa else "", thuc_nhan=x.get("hh_thuc_nhan")))
    tinh = [h for h in hang if h["trang_thai"] not in ("huy", "cho_thanh_toan", "khong_co")]
    out = dict(ma_gt=ma_gt, ten_tiem=chu["ten_tiem"], so_don=len(tinh), tong_hoa_hong=sum(h["hoa_hong"] for h in tinh),
               da_nhan=sum(h["thuc_nhan"] or 0 for h in hang if h["trang_thai"] == "da_chi"), quan_ly=False,
               giu_ngay=HH_GIU_NGAY, dieu_khoan=DIEU_KHOAN)
    if dung_khoa(ma_gt, khoa):
        ctv = d["_ctv"].get(ma_gt, {})
        out.update(quan_ly=True, don=hang, tai_khoan=dict(bin=ctv.get("bin", ""), stk=("•••" + ctv["stk"][-4:]) if ctv.get("stk") else "",
                                                          ten_tk=ctv.get("ten_tk", "")))
    return out
