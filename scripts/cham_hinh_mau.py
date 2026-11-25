"""Chấm điểm hình mẫu nail theo research/TIEU_CHI_CHON_HINH_MAU.md (5 tiêu chí × 20%).
Dữ liệu: research/hinh_mau_toan_cau.md, hinh_mau_dong_nam_a.md, hinh_mau_dong_a.md (25/11/2026).
Chạy: python scripts/cham_hinh_mau.py  -> research/cham_diem_hinh_mau.json + bảng in ra
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def diem_cua_hang(n):
    return 10 if n >= 500 else 8 if n >= 100 else 6 if n >= 30 else 4 if n >= 10 else 2 if n >= 2 else 0


# A: hạng doanh thu trong vùng (1 -> 10, top3 -> 8, có số -> 4, không rõ -> 0)
# E: mỗi mục có bằng chứng = 2 điểm: dat_lich, menu_gia, thanh_vien, followers, danh_gia
HM = [
    # tên, nước, vùng, doanh thu (chữ), hạng DT trong vùng, số cửa hàng, vùng khí hậu, E-items, độ tin cậy, ghi chú
    ("FASTNAIL", "Nhật", "Đông Á", "¥3,25 tỷ mảng nail (FY 3/2026, báo cáo công ty niêm yết)", 1, 73, "khác", ["dat_lich", "menu_gia"], "cao", "500–700 mẫu, giá cố định, 60 phút, app đặt lịch"),
    ("Heart Nail", "Nhật", "Đông Á", "không rõ", None, 280, "khác", ["dat_lich", "menu_gia"], "trung bình", "Mọi mẫu đồng giá ¥4.400, hơn 80.000 lượt đặt/tháng"),
    ("Nail Quick", "Nhật", "Đông Á", "không rõ", None, 50, "khác", ["dat_lich"], "trung bình", "Thành lập 1996"),
    ("Qiaoxiang 瞧享", "Trung Quốc", "Đông Á", "không rõ", None, 1000, "khác", [], "thấp (tự công bố)", "Tự nhận hơn 1.000 tiệm"),
    ("MiniLuxe", "Mỹ", "Toàn cầu", "~$28 triệu (FY2025, báo cáo công khai)", 1, 24, "khác", [], "cao", "Doanh thu TB mỗi studio $1,3 triệu"),
    ("Townhouse", "Anh", "Toàn cầu", "£19,4 triệu (2025); định giá £130 triệu", 2, 44, "khác", ["dat_lich", "menu_gia", "thanh_vien"], "trung bình", "Một hệ đặt lịch: app + web + Instagram"),
    ("Frenchies", "Mỹ", "Toàn cầu", "~$21 triệu toàn hệ thống (ước tính từ hồ sơ nhượng quyền)", 3, 26, "khác", ["dat_lich", "thanh_vien"], "trung bình", "Polish Pass $50/tháng, phí chưa dùng cộng dồn"),
    ("Regal Nails", "Mỹ", "Toàn cầu", "không rõ", None, 584, "khác", ["dat_lich", "thanh_vien"], "trung bình", "Tiệm trong Walmart"),
    ("DaVi Nails", "Mỹ", "Toàn cầu", "không rõ", None, 399, "khác", [], "trung bình", "Tiệm trong Walmart"),
    ("Tips & Toes", "UAE", "Toàn cầu", "không rõ", None, 35, "nóng", ["dat_lich"], "trung bình", "Salon tổng hợp"),
    ("Nails Dot Glow", "Philippines", "Đông Nam Á", "không rõ", None, 100, "ĐNÁ", [], "trung bình", "Nhượng quyền US$20.000, phí bản quyền US$200/tháng"),
    ("Nail Palace", "Singapore", "Đông Nam Á", "không rõ", None, 23, "ĐNÁ", ["dat_lich", "thanh_vien"], "trung bình", "Bị cảnh cáo vì ép bán gói trả trước"),
    ("Nail-a-holics", "Philippines", "Đông Nam Á", "không rõ", None, 63, "ĐNÁ", [], "thấp (số 2018)", ""),
    ("N.I.C Nail Salon", "Thái Lan", "Đông Nam Á", "không rõ", None, 25, "ĐNÁ", [], "trung bình", "Mở từ 1991, trong mall và ga tàu"),
    ("Shimmer & Shine", "Singapore", "Đông Nam Á", "không rõ", None, 9, "ĐNÁ", ["menu_gia"], "trung bình", "Bảng giá cho khách mới công khai"),
    ("Lisa Nail & Spa", "Việt Nam", "Đông Nam Á", "không rõ", None, 6, "ĐNÁ", ["dat_lich", "danh_gia"], "cao (dữ liệu MREAL)", "4,9★ với 9.141 đánh giá Google"),
    ("Nail Room – Mit's House", "Việt Nam", "Đông Nam Á", "không rõ", None, 15, "ĐNÁ", [], "thấp", ""),
]

rows = []
for ten, nuoc, vung, dt, hang, ch, kh, e_items, tin_cay, ghi in HM:
    A = 10 if hang == 1 else 8 if hang and hang <= 3 else 6 if hang and hang <= 10 else 0
    B = diem_cua_hang(ch)
    C = 10 if vung in ("Đông Á", "Đông Nam Á") else 2
    D = 10 if kh == "ĐNÁ" else 6 if kh == "nóng" else 2
    E = 2 * len(e_items)
    rows.append(dict(ten=ten, nuoc=nuoc, vung=vung, doanh_thu=dt, so_cua_hang=ch, A=A, B=B, C=C, D=D, E=E,
                     tong=2 * (A + B + C + D + E), do_tin_cay=tin_cay, ghi_chu=ghi))
rows.sort(key=lambda r: -r["tong"])
(ROOT / "research" / "cham_diem_hinh_mau.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
for i, r in enumerate(rows, 1):
    print(f"{i:2} {r['ten']:24} {r['vung']:11} A{r['A']:>3} B{r['B']:>3} C{r['C']:>3} D{r['D']:>3} E{r['E']:>3}  = {r['tong']}")
