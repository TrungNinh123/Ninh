"""Tạo file CRM (Excel) cho chương trình tiếp cận tiệm trên Google Maps.

Chạy:  python scripts/build_crm.py  ->  crm/CRM_Tiem.xlsx
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parent.parent / "crm" / "CRM_Tiem.xlsx"
FIRST, LAST = 5, 1004  # dòng dữ liệu (1.000 tiệm)

F = "Arial"
TITLE = Font(name=F, size=14, bold=True, color="1F3864")
SUB = Font(name=F, size=9, italic=True, color="595959")
HEAD = Font(name=F, size=10, bold=True, color="FFFFFF")
BODY = Font(name=F, size=10)
INPUT = Font(name=F, size=10, color="0000FF")
HEAD_FILL = PatternFill("solid", fgColor="1F3864")
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
FORMULA_FILL = PatternFill("solid", fgColor="F2F2F2")
EX_FILL = PatternFill("solid", fgColor="E2EFDA")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

NGANH = ["Spa / Nail / Thẩm mỹ", "Nha khoa", "Rửa xe / Gara ô tô", "Nhà hàng / Quán ăn", "Khác"]
KHU_VUC = ["Quận 1", "Quận 3", "Quận 10", "Quận 2", "Phú Nhuận", "Bình Thạnh", "Tân Bình", "Gò Vấp", "Khác"]
TRANG_THAI = [
    "1. Mới", "2. Đã chấm điểm", "3. Đã làm mẫu", "4. Đã gửi lần 1", "5. Đã nhắc",
    "6. Phản hồi - quan tâm", "7. Đang tư vấn", "8. Đã chốt", "9. Đã bàn giao",
    "10. Duy trì", "Từ chối", "Không phản hồi", "Dừng liên hệ",
]
KENH = ["Zalo", "Email", "Zalo + Email", "Điện thoại"]
CO_KHONG = ["Có", "Chưa"]
GOI = ["Lên hình", "Lên hạng", "Duy trì Cơ bản", "Duy trì Tăng trưởng", "Duy trì Toàn diện", "Đặt lịch",
       "Chuyển giao tự làm", "Hệ thống trọn gói", "App riêng"]


def header(ws, row, cols, widths):
    for i, (name, w) in enumerate(zip(cols, widths), start=1):
        c = ws.cell(row=row, column=i, value=name)
        c.font, c.fill, c.border = HEAD, HEAD_FILL, BOX
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 32
    ws.freeze_panes = ws.cell(row=row + 1, column=3)


def title(ws, text, sub):
    ws["A1"] = text
    ws["A1"].font = TITLE
    ws["A2"] = sub
    ws["A2"].font = SUB


def style_range(ws, cols_input, cols_formula, ncols):
    for r in range(FIRST, LAST + 1):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=r, column=c)
            cell.border = BOX
            if c in cols_formula:
                cell.font, cell.fill = BODY, FORMULA_FILL
            elif c in cols_input:
                cell.font = INPUT


def add_list(ws, ref, source):
    dv = DataValidation(type="list", formula1=source, allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(ref)


wb = Workbook()

# ---------------- Danh mục (ẩn) ----------------
dm = wb.active
dm.title = "DanhMuc"
for col, (name, items) in enumerate(
    [("Ngành", NGANH), ("Khu vực", KHU_VUC), ("Trạng thái", TRANG_THAI),
     ("Kênh", KENH), ("Có/Chưa", CO_KHONG), ("Gói", GOI)], start=1):
    dm.cell(row=1, column=col, value=name).font = Font(name=F, bold=True)
    for i, v in enumerate(items, start=2):
        dm.cell(row=i, column=col, value=v).font = BODY
LISTS = {
    "nganh": f"DanhMuc!$A$2:$A${len(NGANH)+1}",
    "khu": f"DanhMuc!$B$2:$B${len(KHU_VUC)+1}",
    "tt": f"DanhMuc!$C$2:$C${len(TRANG_THAI)+1}",
    "kenh": f"DanhMuc!$D$2:$D${len(KENH)+1}",
    "ck": f"DanhMuc!$E$2:$E${len(CO_KHONG)+1}",
    "goi": f"DanhMuc!$F$2:$F${len(GOI)+1}",
}

# ---------------- Hướng dẫn ----------------
hd = wb.create_sheet("Hướng dẫn", 0)
hd.column_dimensions["A"].width = 26
hd.column_dimensions["B"].width = 100
title(hd, "CRM tiếp cận tiệm trên Google Maps", "Một dòng = một tiệm. Mọi liên hệ ghi vào 'Nhật ký liên hệ'.")
rows = [
    ("Ô nền vàng, chữ xanh", "Ô nhập tay (hoặc AI điền khi quét danh sách)."),
    ("Ô nền xám", "Công thức tự tính – không sửa: Link Zalo, Điểm, Nhóm, Gói đề xuất, Ngày nhắc, Tên tiệm."),
    ("Dòng nền xanh lá", "Dòng VÍ DỤ ở mỗi bảng. Xoá khi bắt đầu dùng thật."),
    ("", ""),
    ("QUY TRÌNH MỖI TIỆM", ""),
    ("1. Mới", "Tiệm vừa được quét từ Google Maps."),
    ("2. Đã chấm điểm", "Đã chấm 10 hạng mục ở bảng 'Chấm điểm' (xem Maps, website, fanpage)."),
    ("3. Đã làm mẫu", "Đã có ảnh trước–sau / video 15 giây / trang đặt lịch mẫu. Dán link vào cột 'Link mẫu'."),
    ("4. Đã gửi lần 1", "Gửi tin đầu (mẫu Z1-… hoặc E1). Ghi 'Ngày gửi lần 1' → CRM tự tính ngày nhắc."),
    ("5. Đã nhắc", "Ngày +2: mẫu Z2. Ngày +7: mẫu Z3 (tin cuối). Sau đó → 'Không phản hồi'."),
    ("6–7. Quan tâm / Tư vấn", "Trả lời bằng bộ R1–R6. Mục tiêu: chốt gói và gửi mã QR thanh toán (P1)."),
    ("8. Đã chốt", "Gửi hướng dẫn thêm quản lý Google Maps (H1). Ghi gói, giá trị, đã thanh toán."),
    ("9. Đã bàn giao", "Giao trong 48–72 giờ, gửi báo cáo trước–sau (B1)."),
    ("10. Duy trì", "Ngày 14 chào gói tháng (U1). Ghi số tiền/tháng ở cột 'Duy trì (đ/tháng)'."),
    ("Từ chối / Dừng liên hệ", "Tiệm nói 'không' → dừng ngay, không nhắn lại."),
    ("", ""),
    ("NHÓM THEO ĐIỂM", ""),
    ("A (dưới 40)", "Ưu tiên. Chào Lên hình (500.000đ) / Lên hạng (1.000.000đ)."),
    ("B (40–70)", "Chào Duy trì + trang đặt lịch."),
    ("C (trên 70)", "Để sau. Chỉ chào trang đặt lịch hoặc gói sư tử."),
    ("", ""),
    ("QUY TẮC", "Chỉ dùng thông tin công khai của tiệm. Mỗi tin nhắn phải có tên tiệm + điểm yếu cụ thể + mẫu riêng. "
               "Tối đa 3 lần liên hệ nếu không phản hồi. Không đánh giá ảo. Không đăng mẫu khi chưa được đồng ý."),
]
for i, (a, b) in enumerate(rows, start=4):
    hd.cell(row=i, column=1, value=a).font = Font(name=F, size=10, bold=a.isupper() or a[:2].strip(".").isdigit())
    c = hd.cell(row=i, column=2, value=b)
    c.font, c.alignment = BODY, WRAP
hd["A4"].fill, hd["A4"].font = INPUT_FILL, INPUT
hd["A5"].fill = FORMULA_FILL
hd["A6"].fill = EX_FILL

# ---------------- Danh sách tiệm ----------------
ds = wb.create_sheet("Danh sách tiệm", 1)
title(ds, "Danh sách tiệm", "Chữ xanh = nhập tay · nền xám = công thức · dòng xanh lá = ví dụ")
cols = ["ID", "Ngày thêm", "Ngành", "Tên tiệm", "Khu vực", "Địa chỉ", "SĐT", "Link Zalo",
        "Email", "Link Google Maps", "Website", "Fanpage", "Số sao", "Số đánh giá",
        "Điểm (/100)", "Nhóm", "Gói đề xuất", "Điểm yếu chính", "Link mẫu", "Trạng thái",
        "Kênh", "Ngày gửi lần 1", "Ngày nhắc 1", "Ngày nhắc cuối", "Liên hệ gần nhất",
        "Bước tiếp theo", "Phụ trách", "Gói đã chốt", "Giá trị (đ)", "Đã thanh toán",
        "Duy trì (đ/tháng)", "Ghi chú"]
widths = [9, 11, 18, 26, 12, 30, 13, 24, 22, 22, 22, 22, 7, 9, 9, 7, 18, 34, 22, 18,
          12, 12, 12, 12, 12, 26, 12, 16, 13, 10, 13, 26]
header(ds, 4, cols, widths)
FORMULA_COLS = {8, 15, 16, 17, 23, 24}
style_range(ds, set(range(1, 33)) - FORMULA_COLS, FORMULA_COLS, 32)
for r in range(FIRST, LAST + 1):
    ds[f"H{r}"] = f'=IF(G{r}="","","https://zalo.me/"&SUBSTITUTE(SUBSTITUTE(G{r}," ",""),".",""))'
    ds[f"O{r}"] = f"=IF(A{r}=\"\",\"\",IFERROR(INDEX('Chấm điểm'!$M:$M,MATCH(A{r},'Chấm điểm'!$A:$A,0)),\"\"))"
    ds[f"P{r}"] = f'=IF(O{r}="","",IF(O{r}<40,"A",IF(O{r}<=70,"B","C")))'
    ds[f"Q{r}"] = (f'=IF(P{r}="","",IF(N(N{r})>=300,"KHÁCH LỚN: Hệ thống / App",'
                   f'IF(P{r}="A","Lên hình / Lên hạng",IF(P{r}="B","Duy trì + Đặt lịch","Đặt lịch / Sư tử"))))')
    ds[f"W{r}"] = f'=IF(V{r}="","",V{r}+2)'
    ds[f"X{r}"] = f'=IF(V{r}="","",V{r}+7)'
    for col in ("B", "V", "W", "X", "Y"):
        ds[f"{col}{r}"].number_format = "dd/mm/yyyy"
    ds[f"M{r}"].number_format = "0.0"
    for col in ("AC", "AE"):
        ds[f"{col}{r}"].number_format = "#,##0;-#,##0;-"
    ds[f"G{r}"].number_format = "@"
rng = f"{FIRST}:{LAST}"
add_list(ds, f"C{FIRST}:C{LAST}", LISTS["nganh"])
add_list(ds, f"E{FIRST}:E{LAST}", LISTS["khu"])
add_list(ds, f"T{FIRST}:T{LAST}", LISTS["tt"])
add_list(ds, f"U{FIRST}:U{LAST}", LISTS["kenh"])
add_list(ds, f"AB{FIRST}:AB{LAST}", LISTS["goi"])
add_list(ds, f"AD{FIRST}:AD{LAST}", LISTS["ck"])
ds.auto_filter.ref = f"A4:AF{LAST}"
ds["T4"].comment = Comment("Chọn từ danh sách. Xem quy trình ở sheet 'Hướng dẫn'.", "CRM")
ds["V4"].comment = Comment("Nhập ngày gửi tin đầu. Ngày nhắc 1 (+2) và nhắc cuối (+7) tự tính.", "CRM")

import datetime as _dt
ex = {"A": "VD-001", "B": _dt.date(2026, 11, 25), "C": "Spa / Nail / Thẩm mỹ",
      "D": "Spa Mẫu (VÍ DỤ – xoá dòng này)", "E": "Quận 1",
      "F": "12 Đường Ví Dụ, Phường Ví Dụ, TP.HCM", "G": "0900000000",
      "J": "https://maps.google.com/?cid=0", "M": 4.6, "N": 87,
      "R": "Chưa có ảnh bìa; chưa có nút đặt lịch; 30 đánh giá chưa trả lời",
      "S": "(link mẫu)", "T": "4. Đã gửi lần 1", "U": "Zalo",
      "V": _dt.date(2026, 11, 26), "Y": _dt.date(2026, 11, 26),
      "Z": "Nhắc lần 1 bằng mẫu Z2", "AA": "Người gửi 1"}
for col, v in ex.items():
    ds[f"{col}{FIRST}"] = v
for c in range(1, 33):
    ds.cell(row=FIRST, column=c).fill = EX_FILL

# ---------------- Chấm điểm ----------------
cd = wb.create_sheet("Chấm điểm", 2)
title(cd, "Chấm điểm hiện diện Google Maps (100 điểm)", "Tự chấm từ dữ liệu Google Maps theo thang cố định (xem chú thích ở tiêu đề cột). Fanpage và Đặt lịch chấm tay nếu tìm thấy.")
crit = [("Số đánh giá", 20), ("Điểm sao", 15), ("Website riêng", 15), ("Fanpage", 5),
        ("Giờ mở cửa", 10), ("SĐT", 5), ("Mô tả", 5), ("Thứ hạng tìm kiếm", 15),
        ("Đặt lịch online", 5), ("Ảnh (chấm tay)", 5)]
cols = ["ID", "Tên tiệm"] + [f"{n} ({m})" for n, m in crit] + ["Tổng", "Ghi chú chấm"]
header(cd, 4, cols, [9, 28] + [11] * 10 + [8, 40])
style_range(cd, set(range(1, 15)) - {2, 13}, {2, 13}, 14)
notes = ["≥300: 20 · 100–299: 16 · 30–99: 10 · 10–29: 5 · dưới 10: 1",
         "≥4,8: 15 · 4,5–4,79: 12 · 4,0–4,49: 7 · dưới 4: 3 · chưa có: 0",
         "Website riêng: 15 · chỉ dẫn về Facebook: 5 · không có: 0",
         "Có fanpage liên kết: 5 (chấm tay nếu tìm thấy)",
         "Có giờ mở cửa trên Maps: 10", "Có SĐT trên Maps: 5", "Có mô tả trên Maps: 5",
         "Vị trí khi tìm 'spa / nail / thẩm mỹ viện quận 1': top 5: 15 · 6–10: 10 · 11–20: 6 · sau 20: 0",
         "Có đặt lịch online: 5 (chấm tay)",
         "Ảnh đẹp, đủ, có ảnh bìa: 5 (chấm tay – Google không trả số ảnh qua API)"]
for i, ((n, m), note) in enumerate(zip(crit, notes), start=3):
    cd.cell(row=4, column=i).comment = Comment(f"Tối đa {m} điểm. {note}.", "CRM")
    dv = DataValidation(type="whole", operator="between", formula1="0", formula2=str(m),
                        showErrorMessage=True, error=f"Điểm từ 0 đến {m}")
    cd.add_data_validation(dv)
    L = get_column_letter(i)
    dv.add(f"{L}{FIRST}:{L}{LAST}")
for r in range(FIRST, LAST + 1):
    cd[f"B{r}"] = f"=IF(A{r}=\"\",\"\",IFERROR(INDEX('Danh sách tiệm'!$D:$D,MATCH(A{r},'Danh sách tiệm'!$A:$A,0)),\"(chưa có trong danh sách)\"))"
    cd[f"M{r}"] = f'=IF(A{r}="","",SUM(C{r}:L{r}))'
for col, v in zip("ACDEFGHIJKLN", ["VD-001", 10, 12, 0, 0, 10, 5, 0, 6, 0, 0,
                                   "Ví dụ: 9 ảnh tối, không ảnh bìa; 87 đánh giá nhưng chủ không trả lời"]):
    cd[f"{col}{FIRST}"] = v
for c in range(1, 15):
    cd.cell(row=FIRST, column=c).fill = EX_FILL

# ---------------- Nhật ký liên hệ ----------------
nk = wb.create_sheet("Nhật ký liên hệ", 3)
title(nk, "Nhật ký liên hệ", "Mỗi lần gửi hoặc nhận tin = một dòng. Dán nguyên văn tin của tiệm vào cột 'Nội dung'.")
cols = ["Ngày", "ID", "Tên tiệm", "Kênh", "Chiều", "Mẫu đã dùng", "Nội dung", "Kết quả", "Bước tiếp theo", "Người thực hiện"]
header(nk, 4, cols, [11, 9, 28, 12, 11, 12, 60, 22, 30, 14])
style_range(nk, set(range(1, 11)) - {3}, {3}, 10)
for r in range(FIRST, LAST + 1):
    nk[f"C{r}"] = f"=IF(B{r}=\"\",\"\",IFERROR(INDEX('Danh sách tiệm'!$D:$D,MATCH(B{r},'Danh sách tiệm'!$A:$A,0)),\"\"))"
    nk[f"A{r}"].number_format = "dd/mm/yyyy"
    nk[f"G{r}"].alignment = WRAP
add_list(nk, f"D{FIRST}:D{LAST}", LISTS["kenh"])
dv = DataValidation(type="list", formula1='"Gửi đi,Nhận về"', allow_blank=True)
nk.add_data_validation(dv)
dv.add(f"E{FIRST}:E{LAST}")
for col, v in zip("ABDEFGHIJ", [_dt.date(2026, 11, 26), "VD-001", "Zalo", "Gửi đi", "Z1-SPA",
                               "Gửi tin đầu kèm link mẫu", "Đã xem", "Nhắc ngày 28/11 (Z2)", "Người gửi 1"]):
    nk[f"{col}{FIRST}"] = v
for c in range(1, 11):
    nk.cell(row=FIRST, column=c).fill = EX_FILL

# ---------------- Mẫu tin nhắn ----------------
mt = wb.create_sheet("Mẫu tin nhắn", 4)
title(mt, "Mẫu tin nhắn", "Thay mọi {…} bằng thông tin riêng của tiệm. Không gửi tin thiếu tên tiệm, điểm yếu cụ thể và link mẫu.")
header(mt, 4, ["Mã", "Kênh", "Ngành", "Khi nào dùng", "Nội dung"], [11, 10, 18, 26, 110])
T = [
 ("Z1-SPA", "Zalo", "Spa / Nail / Thẩm mỹ", "Tin đầu tiên",
  "Chào chị, em là {Tên người gửi} bên {Công ty}. Em thấy {Tên tiệm} trên Google Maps được {Số sao} sao, khách khen {Điểm khen} nhiều lắm ạ.\n"
  "Em có chấm thử hồ sơ của tiệm: {Điểm}/100. Hai chỗ đang làm mất khách: {Điểm yếu 1} và {Điểm yếu 2}.\n"
  "Em làm sẵn bản mẫu riêng cho tiệm để chị xem trước, miễn phí: {Link mẫu}\n"
  "Nếu chị thấy ổn, bên em làm hoàn chỉnh trong 48 giờ, chỉ 500.000đ, kịp đón khách Tết. Chị không cần thì nhắn \"không\" giúp em, em sẽ không làm phiền nữa ạ."),
 ("Z1-NHAKHOA", "Zalo", "Nha khoa", "Tin đầu tiên",
  "Chào anh/chị, em là {Tên người gửi} bên {Công ty}. Phòng khám {Tên tiệm} đang có {Số đánh giá} đánh giá, {Số sao} sao trên Google Maps ạ.\n"
  "Em chấm thử hồ sơ: {Điểm}/100. Bệnh nhân tìm \"nha khoa gần đây\" đang khó chọn phòng khám vì {Điểm yếu 1}, {Điểm yếu 2}.\n"
  "Em đã làm sẵn bản mẫu (ảnh phòng khám sắp xếp lại, video giới thiệu 15 giây, trang đặt lịch hẹn): {Link mẫu}\n"
  "Gói hoàn chỉnh 1.000.000đ, giao trong 72 giờ. Anh/chị không quan tâm thì nhắn \"không\", em sẽ không nhắn lại ạ."),
 ("Z1-GARA", "Zalo", "Rửa xe / Gara ô tô", "Tin đầu tiên",
  "Chào anh, em là {Tên người gửi} bên {Công ty}. {Tên tiệm} được khách đánh giá tốt về {Điểm khen} ạ.\n"
  "Em chấm thử hồ sơ Google Maps của gara được {Điểm}/100: {Điểm yếu 1}, {Điểm yếu 2}.\n"
  "Em làm sẵn bản mẫu để anh xem: {Link mẫu}. Trước Tết người ta tìm \"rửa xe gần đây\", \"bảo dưỡng ô tô\" rất nhiều, hồ sơ đẹp lên là có khách ngay.\n"
  "Làm hoàn chỉnh 500.000đ, giao trong 48 giờ. Anh không quan tâm thì nhắn \"không\", em sẽ không nhắn lại ạ."),
 ("Z1-NHAHANG", "Zalo", "Nhà hàng / Quán ăn", "Tin đầu tiên",
  "Chào anh/chị, em là {Tên người gửi} bên {Công ty}. {Tên tiệm} được khách khen {Điểm khen} trên Google Maps ạ.\n"
  "Em chấm thử hồ sơ: {Điểm}/100. Khách tìm \"quán ăn gần đây\" đang bỏ qua quán vì {Điểm yếu 1}, {Điểm yếu 2}.\n"
  "Em làm sẵn ảnh món sắp xếp lại, video 15 giây và trang đặt bàn mẫu: {Link mẫu}\n"
  "Gói hoàn chỉnh 500.000đ, kịp mùa tất niên. Anh/chị không cần thì nhắn \"không\" giúp em ạ."),
 ("Z2", "Zalo", "Tất cả", "Ngày +2, chưa phản hồi",
  "Dạ em gửi thêm {Tên tiệm} video 15 giây em dựng thử từ ảnh của tiệm: {Link video}. Chị/anh xem thử, thấy hợp thì em làm luôn bản đầy đủ ạ."),
 ("Z3", "Zalo", "Tất cả", "Ngày +7, tin cuối",
  "Dạ đây là tin cuối em nhắn ạ. Bên em còn {Số suất} suất làm trước Tết, giá 500.000đ, không hài lòng hoàn tiền. Mẫu của {Tên tiệm} em vẫn giữ ở đây: {Link mẫu}. Chúc tiệm mình mùa Tết đông khách!"),
 ("E1", "Email", "Tất cả", "Email đầu tiên",
  "Tiêu đề: {Tên tiệm} – bản mẫu Google Maps em làm sẵn (miễn phí)\n\n"
  "Chào anh/chị,\n\nEm là {Tên người gửi} bên {Công ty}. Em đã chấm thử hồ sơ Google Maps và kênh online của {Tên tiệm}: {Điểm}/100.\n"
  "• Điểm tốt: {Điểm khen}\n• Cần cải thiện: {Điểm yếu 1}; {Điểm yếu 2}; {Điểm yếu 3}\n\n"
  "Em làm sẵn bản mẫu riêng cho tiệm (ảnh trước–sau, video 15 giây, trang đặt lịch): {Link mẫu}\n\n"
  "Gói Lên hình 500.000đ / Lên hạng 1.000.000đ, giao trong 48–72 giờ, không hài lòng hoàn tiền. "
  "Anh/chị chỉ cần trả lời email này hoặc nhắn Zalo {SĐT công ty}.\n\n"
  "Nếu không muốn nhận thêm email, anh/chị trả lời \"không\", em sẽ dừng ngay.\n\n{Tên người gửi} – {Công ty}"),
 ("R1", "Cả hai", "Tất cả", "Hỏi: có hiệu quả không?",
  "Dạ, ảnh trước–sau của tiệm mình đây ạ: {Link}. Sau 30 ngày em gửi báo cáo số lượt gọi, lượt chỉ đường, lượt bấm website từ chính Google. Không hài lòng bản giao thì bên em hoàn tiền."),
 ("R2", "Cả hai", "Tất cả", "Hỏi: tiệm phải làm gì?",
  "Dạ tiệm gần như không phải làm gì: chỉ thêm bên em làm người quản lý hồ sơ Google Maps (3 bước, em gửi hướng dẫn có hình), và gửi thêm vài ảnh nếu có. Phần còn lại bên em làm hết."),
 ("R3", "Cả hai", "Tất cả", "Nghi ngờ / sợ lừa",
  "Dạ chị/anh không phải trả trước. Xem bản mẫu thấy ưng mới chuyển khoản, bên em xuất thông tin công ty đầy đủ. Bản giao không ưng thì hoàn tiền ạ."),
 ("R4", "Cả hai", "Tất cả", "Đã có người làm",
  "Dạ vậy tốt quá ạ. Em gửi bảng chấm điểm để bên mình đối chiếu: {Link phiếu chấm}. Phần {Điểm yếu} hiện chưa có, bên em có thể làm riêng phần đó, ví dụ trang đặt lịch {giá}/tháng."),
 ("R5", "Cả hai", "Tất cả", "Chê đắt",
  "Dạ, thuê 2–3 người làm marketing tốn từ 12–15 triệu/tháng trở lên. Bên em làm trọn ảnh, video, Google Maps, chăm khách chỉ 1–3 triệu/tháng, và gói đầu chỉ 500.000đ để tiệm thử trước."),
 ("R6", "Cả hai", "Tất cả", "Để suy nghĩ",
  "Dạ vâng ạ. Em giữ bản mẫu cho tiệm đến {Ngày}. Chị/anh cần chỉnh gì trong mẫu cứ nhắn em, em sửa miễn phí để mình xem cho chắc."),
 ("P1", "Cả hai", "Tất cả", "Chốt – gửi thanh toán",
  "Dạ em xác nhận gói {Gói} – {Giá}đ cho {Tên tiệm}. Chị/anh chuyển khoản theo mã QR này: {QR}, nội dung: {ID} {Tên tiệm}. Em bắt đầu làm ngay khi nhận được ạ."),
 ("H1", "Cả hai", "Tất cả", "Sau khi chốt – xin quyền quản lý",
  "Dạ để bên em cập nhật hồ sơ, chị/anh thêm email {Email công ty} làm người quản lý theo 3 bước: (1) mở Google Maps → hồ sơ của tiệm, (2) Cài đặt → Người dùng và quyền truy cập, (3) Thêm → nhập email → Quản lý. Em gửi kèm ảnh hướng dẫn: {Link}."),
 ("B1", "Cả hai", "Tất cả", "Bàn giao",
  "Dạ hồ sơ của {Tên tiệm} đã cập nhật xong ạ. Trước–sau: {Link}. Video: {Link}. Trang đặt lịch: {Link}. Mã QR xin đánh giá để ở quầy: {Link}. 14 ngày nữa em gửi số liệu đầu tiên."),
 ("U1", "Cả hai", "Tất cả", "Ngày 14 – chào gói tháng",
  "Dạ sau 14 ngày, {Tên tiệm} có {Số lượt gọi} lượt gọi, {Số lượt chỉ đường} lượt chỉ đường, {Số đánh giá mới} đánh giá mới. Để giữ và tăng tiếp, bên em có gói duy trì {Giá}/tháng: {Nội dung gói}. Dừng được theo tháng ạ."),
]
for i, row in enumerate(T, start=FIRST):
    for j, v in enumerate(row, start=1):
        c = mt.cell(row=i, column=j, value=v)
        c.font, c.alignment, c.border = BODY, WRAP, BOX
mt.freeze_panes = "B5"

# ---------------- Bảng giá ----------------
bg = wb.create_sheet("Bảng giá", 5)
title(bg, "Bảng giá", "Giá đề xuất – chỉnh ở cột 'Giá (đ)' sau khi chạy thử.")
header(bg, 4, ["Gói", "Loại", "Giá (đ)", "Nội dung"], [22, 12, 14, 100])
P = [("Lên hình", "Một lần", 500000, "Chuẩn hoá hồ sơ Google Maps: ảnh bìa, sắp xếp ảnh, 3 video ngắn, mô tả, danh mục, giờ, dịch vụ & giá, bộ QR xin đánh giá"),
     ("Lên hạng", "Một lần", 1000000, "Lên hình + landing page 1 trang + 1 tháng đăng bài, trả lời đánh giá + báo cáo thứ hạng trước–sau"),
     ("Duy trì Cơ bản", "Tháng", 1000000, "4 bài Maps, 2 video, trả lời đánh giá, chương trình xin đánh giá, báo cáo"),
     ("Duy trì Tăng trưởng", "Tháng", 2000000, "8 bài, 6 video, danh sách khách, chăm khách cũ, 1 khuyến mãi/tháng, fanpage, trang đặt lịch, báo cáo"),
     ("Duy trì Toàn diện", "Tháng", 3000000, "12 bài, 12 video, chăm khách, 2 khuyến mãi + 1 sự kiện/tháng, quản lý fanpage, website, trang đặt lịch, báo cáo + đề xuất"),
     ("Đặt lịch (lẻ)", "Tháng", 400000, "Trang đặt lịch riêng của tiệm, gắn nút trên Google Maps, báo lịch mới cho chủ tiệm"),
     ("Chuyển giao tự làm", "Một lần", 7000000, "Đào tạo chủ tiệm/nhân viên tự làm: bộ công cụ AI, mẫu nội dung, lịch đăng 90 ngày, 4 buổi kèm 1:1, 30 ngày hỗ trợ (5–10 triệu)"),
     ("Hệ thống trọn gói", "Một lần", 20000000, "Website + trang đặt lịch + danh sách khách + tự động chăm khách qua Zalo OA, bàn giao quyền sở hữu, kèm đào tạo (15–30 triệu)"),
     ("App riêng", "Một lần", 50000000, "App đặt lịch + thành viên, tích điểm + quản lý nhiều chi nhánh cho chuỗi (30–100 triệu, tuỳ phạm vi)"),
     ("Bảo trì hệ thống/app", "Tháng", 500000, "Lưu trữ, cập nhật, sửa lỗi cho khách đã mua Hệ thống hoặc App")]
for i, row in enumerate(P, start=FIRST):
    for j, v in enumerate(row, start=1):
        c = bg.cell(row=i, column=j, value=v)
        c.font, c.border, c.alignment = (INPUT if j == 3 else BODY), BOX, WRAP
    bg.cell(row=i, column=3).number_format = "#,##0"
    bg.cell(row=i, column=3).fill = INPUT_FILL
bg["A16"] = "Nguồn giá: đề xuất đã thống nhất với anh Ninh trong buổi lên phương án (25/11/2026)."
bg["A16"].font = SUB

# ---------------- Báo cáo ----------------
bc = wb.create_sheet("Báo cáo", 1)
title(bc, "Báo cáo tiến độ", "Tự tính từ 'Danh sách tiệm'. Chỉ sửa ô nền vàng (mục tiêu).")
bc.column_dimensions["A"].width = 32
bc.column_dimensions["B"].width = 16
bc.column_dimensions["C"].width = 14
bc.column_dimensions["E"].width = 26
bc.column_dimensions["F"].width = 12
DSR = f"'Danh sách tiệm'!$T${FIRST}:$T${LAST}"
for c, h in zip("ABC", ["Phễu theo trạng thái", "Số tiệm", "% trên tổng"]):
    bc[f"{c}4"] = h
    bc[f"{c}4"].font, bc[f"{c}4"].fill = HEAD, HEAD_FILL
for i, s in enumerate(TRANG_THAI, start=5):
    bc[f"A{i}"] = s
    bc[f"B{i}"] = f'=COUNTIF({DSR},A{i})'
    bc[f"C{i}"] = f'=IF($B${5+len(TRANG_THAI)}=0,0,B{i}/$B${5+len(TRANG_THAI)})'
    bc[f"C{i}"].number_format = "0.0%"
tot = 5 + len(TRANG_THAI)
bc[f"A{tot}"] = "Tổng số tiệm"
bc[f"B{tot}"] = f'=COUNTA(\'Danh sách tiệm\'!$A${FIRST}:$A${LAST})'
bc[f"A{tot}"].font = Font(name=F, bold=True)

DS = "'Danh sách tiệm'!"
kpi = [
    ("Mục tiêu doanh thu đến 31/12/2026 (đ)", 100000000, "#,##0"),
    ("Doanh thu đã chốt (đ)", f"=SUM({DS}$AC${FIRST}:$AC${LAST})", "#,##0"),
    ("Doanh thu đã thanh toán (đ)", f'=SUMIFS({DS}$AC${FIRST}:$AC${LAST},{DS}$AD${FIRST}:$AD${LAST},"Có")', "#,##0"),
    ("Doanh thu duy trì hằng tháng (đ)", f"=SUM({DS}$AE${FIRST}:$AE${LAST})", "#,##0"),
    ("% đạt mục tiêu (đã thanh toán)", "=IF(F5=0,0,F7/F5)", "0.0%"),
    ("Đã gửi tin (từ bước 4 trở đi)", f'=COUNT({DS}$V${FIRST}:$V${LAST})', "0"),
    ("Tỷ lệ phản hồi quan tâm", f"=IF(F10=0,0,SUM(B10:B14)/F10)", "0.0%"),
    ("Tỷ lệ chốt / đã gửi", f"=IF(F10=0,0,SUM(B12:B14)/F10)", "0.0%"),
    ("Cần nhắc lần 1 hôm nay", f'=COUNTIFS({DS}$W${FIRST}:$W${LAST},TODAY(),{DS}$T${FIRST}:$T${LAST},"4. Đã gửi lần 1")', "0"),
    ("Cần gửi tin cuối hôm nay", f'=COUNTIFS({DS}$X${FIRST}:$X${LAST},TODAY(),{DS}$T${FIRST}:$T${LAST},"5. Đã nhắc")', "0"),
]
bc["E4"], bc["F4"] = "Chỉ số", "Giá trị"
for c in ("E4", "F4"):
    bc[c].font, bc[c].fill = HEAD, HEAD_FILL
for i, (name, val, fmt) in enumerate(kpi, start=5):
    bc[f"E{i}"] = name
    bc[f"F{i}"] = val
    bc[f"F{i}"].number_format = fmt
    bc[f"E{i}"].font = BODY
bc["F5"].font, bc["F5"].fill = INPUT, INPUT_FILL
bc["F5"].comment = Comment("Mục tiêu do anh Ninh đặt cho giai đoạn 25/11–31/12/2026.", "CRM")
bc["F11"].comment = Comment("Gồm các trạng thái từ 6. Phản hồi - quan tâm đến 10. Duy trì.", "CRM")
bc["F12"].comment = Comment("Gồm 8. Đã chốt, 9. Đã bàn giao, 10. Duy trì.", "CRM")

r0 = tot + 2
bc[f"A{r0}"], bc[f"B{r0}"], bc[f"C{r0}"] = "Theo ngành", "Số tiệm", "Đã chốt+"
for c in "ABC":
    bc[f"{c}{r0}"].font, bc[f"{c}{r0}"].fill = HEAD, HEAD_FILL
for i, n in enumerate(NGANH, start=r0 + 1):
    bc[f"A{i}"] = n
    bc[f"B{i}"] = f'=COUNTIF({DS}$C${FIRST}:$C${LAST},A{i})'
    bc[f"C{i}"] = (f'=COUNTIFS({DS}$C${FIRST}:$C${LAST},A{i},{DS}$T${FIRST}:$T${LAST},"8. Đã chốt")'
                   f'+COUNTIFS({DS}$C${FIRST}:$C${LAST},A{i},{DS}$T${FIRST}:$T${LAST},"9. Đã bàn giao")'
                   f'+COUNTIFS({DS}$C${FIRST}:$C${LAST},A{i},{DS}$T${FIRST}:$T${LAST},"10. Duy trì")')
for row in bc.iter_rows(min_row=5, max_row=r0 + len(NGANH), max_col=3):
    for c in row:
        if c.row not in (4, r0):
            c.font = BODY

dm.sheet_state = "hidden"
wb.active = 1
OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT)
print(OUT)
