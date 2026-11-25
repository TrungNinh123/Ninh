"""Đưa danh sách tiệm (JSON từ nghiên cứu web) vào CRM, chấm sơ bộ và soạn sẵn tin Zalo + email.

Chạy: python scripts/import_leads.py file1.json [file2.json ...]
Tạo sheet 'Duyệt đợt 1' để anh Ninh duyệt từng tin trước khi gửi.
"""
import datetime as dt
import json
import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
CRM = ROOT / "crm" / "CRM_Tiem.xlsx"
FIRST, LAST = 5, 1004
CONG_TY, NGUOI_GUI = "MREAL", "Phương Thư"

GOI_Y = {
    "Nail": ("chị", "khách tìm \"nail đẹp quận 1\" để làm móng đón Noel, Tết", "lưới ảnh mẫu theo mùa Noel – Tết, video 15 giây quá trình làm móng và trang đặt lịch mẫu", "500.000đ", "48 giờ"),
    "Spa / Nail / Thẩm mỹ": ("chị", "khách tìm \"spa gần đây\"", "ảnh trước–sau, video 15 giây và trang đặt lịch mẫu", "500.000đ", "48 giờ"),
    "Nha khoa": ("anh/chị", "bệnh nhân tìm \"nha khoa gần đây\"", "ảnh phòng khám sắp xếp lại, video giới thiệu 15 giây và trang đặt lịch hẹn mẫu", "1.000.000đ", "72 giờ"),
    "Rửa xe / Gara ô tô": ("anh", "khách tìm \"rửa xe gần đây\", \"bảo dưỡng ô tô\" trước Tết", "ảnh gara sắp xếp lại, bảng giá dịch vụ, video 15 giây và trang đặt lịch mẫu", "500.000đ", "48 giờ"),
    "Nhà hàng / Quán ăn": ("anh/chị", "khách tìm \"quán ăn gần đây\" mùa tất niên", "ảnh món sắp xếp lại, video 15 giây và trang đặt bàn mẫu", "500.000đ", "48 giờ"),
}


def score(l):
    s = {"I": 10 if l.get("website") else 0,
         "J": (10 if "202" in str(l.get("fanpage_hoat_dong", "")) and "không" not in str(l.get("fanpage_hoat_dong", "")) else 4) if l.get("fanpage") else 0,
         "K": 10 if l.get("co_dat_lich_online") else 0}
    return s


def msgs(l):
    xung, tim, mau, gia, tg = GOI_Y[l["nganh"]]
    dy = " ".join(l.get("diem_yeu", [])).lower()
    thieu = []
    if "website" in dy:
        thieu.append("website riêng")
    if "fanpage" in dy:
        thieu.append("fanpage chính thức")
    thieu.append("nút đặt lịch online" if l["nganh"] != "Nhà hàng / Quán ăn" else "nút đặt bàn online")
    yeu_txt = ", ".join(thieu[:-1]) + (" và " if len(thieu) > 1 else "") + thieu[-1]
    khen = l.get("diem_khen") or "được khách đánh giá tốt"
    if l["nganh"] == "Nail" and l.get("diem"):
        y = [v.replace('"spa quận 1"', '"spa, nail quận 1"') for v in l.get("yeu_maps", [])][:1]
        mo = f"{l['ten'].split('|')[0].split(' - ')[0].strip()} đang có {khen}, tay nghề đã được khách công nhận ạ."
        thay = f" Em thấy hiện tiệm {y[0]}." if y else ""
        zalo = (f"Chào chị, em là {NGUOI_GUI} bên {CONG_TY}. {mo}{thay}\n"
                f"Mùa Noel – Tết – cưới là mùa làm móng đông nhất năm, nên em đã làm sẵn một bản khám marketing riêng cho tiệm: "
                f"so sánh với các tiệm nail dẫn đầu Quận 1, kèm lộ trình 3 ngày – 1 tháng và chi phí từ 500.000đ: {{Link bản khám}}\n"
                f"Chị xem thử, thấy hợp thì bên em làm luôn 3 ngày đầu rồi chị mới thanh toán. "
                f"Không cần thì chị nhắn \"không\", em sẽ không làm phiền nữa ạ.")
        subj = f"{l['ten']} – bản khám marketing mùa Noel – Tết (miễn phí)"
        return zalo, subj, zalo
    lon = l.get("diem") and ((l.get("so_danh_gia") or 0) >= 300 or l.get("tong", 0) > 70)
    if lon:
        y = l["yeu_maps"][:1]
        them = f"Em xem hồ sơ Google Maps của tiệm thì thấy {y[0]}. " if y else ""
        zalo = (f"Chào {xung}, em là {NGUOI_GUI} bên {CONG_TY}. {l['ten']} đang có {khen}, thuộc nhóm tiệm mạnh nhất Quận 1 ạ.\n"
                f"{them}Với lượng khách như vậy, nếu khách vẫn phải nhắn tin, gọi điện mới đặt được lịch thì mỗi ngày tiệm có thể đang mất khách.\n"
                f"Em đã làm sẵn trang đặt lịch mẫu mang tên {l['ten']} để {xung} xem thử: {{Link mẫu}}\n"
                f"Bên em có thể làm trọn hệ thống: trang đặt lịch, danh sách khách, tự nhắn nhắc lịch và chăm khách cũ qua Zalo. Nếu {xung} quan tâm, em gửi báo giá theo quy mô tiệm ạ. "
                f"Không cần thì {xung} nhắn \"không\", em sẽ không làm phiền nữa.")
    elif l.get("yeu_maps"):
        y = l["yeu_maps"][:2]
        yeu_txt = " và ".join(y)
        mo = f"{l['ten']} đang có {khen}, rất đáng quý ạ." if l.get("sao") else f"Em có tìm hiểu {l['ten']} trên Google Maps ạ."
        zalo = (f"Chào {xung}, em là {NGUOI_GUI} bên {CONG_TY}. {mo}\n"
                f"Em xem hồ sơ Google Maps của tiệm thì thấy {yeu_txt}, nên {tim} rất dễ chọn tiệm khác.\n"
                f"Em đã làm sẵn bản mẫu riêng cho {l['ten']} ({mau}) để {xung} xem trước, miễn phí: {{Link mẫu}}\n"
                f"Nếu thấy ổn, bên em làm hoàn chỉnh trong {tg}, chỉ {gia}. "
                f"{xung.capitalize()} không cần thì nhắn \"không\" giúp em, em sẽ không làm phiền nữa ạ.")
    else:
      zalo = (f"Chào {xung}, em là {NGUOI_GUI} bên {CONG_TY}. Em có tìm hiểu {l['ten']}, thấy tiệm mình {khen[0].lower() + khen[1:]} ạ.\n"
            f"Em tìm thử {l['ten']} trên mạng thì chưa thấy {yeu_txt}, nên {tim} rất dễ chọn tiệm khác.\n"
            f"Em đã làm sẵn bản mẫu riêng cho {l['ten']} ({mau}) để {xung} xem trước, miễn phí: {{Link mẫu}}\n"
            f"Nếu thấy ổn, bên em làm hoàn chỉnh trong {tg}, chỉ {gia}. "
            f"{xung.capitalize()} không cần thì nhắn \"không\" giúp em, em sẽ không làm phiền nữa ạ.")
    subj = f"{l['ten']} – bản mẫu Google Maps và trang đặt lịch em làm sẵn (miễn phí)"
    body = (f"Chào {xung},\n\nEm là {NGUOI_GUI} bên {CONG_TY}. Em có tìm hiểu kênh online của {l['ten']}.\n"
            f"• Điểm tốt: {khen}\n• Cần cải thiện: {'; '.join(l.get('yeu_maps') or [yeu_txt])}\n\n"
            f"Em đã làm sẵn bản mẫu riêng cho tiệm ({mau}): {{Link mẫu}}\n\n"
            f"Gói hoàn chỉnh {gia}, giao trong {tg}, không hài lòng hoàn tiền. "
            f"{xung.capitalize()} chỉ cần trả lời email này.\n\n"
            f"Nếu không muốn nhận thêm email, {xung} trả lời \"không\", em sẽ dừng ngay.\n\n{NGUOI_GUI} – {CONG_TY}")
    return zalo, subj, body


def main(paths):
    leads = [x for p in paths for x in json.loads(Path(p).read_text(encoding="utf-8"))]
    wb = load_workbook(CRM)
    ds, cd = wb["Danh sách tiệm"], wb["Chấm điểm"]
    row = next(r for r in range(FIRST, LAST + 1) if not ds[f"A{r}"].value)
    crow = next(r for r in range(FIRST, LAST + 1) if not cd[f"A{r}"].value)
    if "Duyệt đợt 1" in wb.sheetnames:
        del wb["Duyệt đợt 1"]
    dv = wb.create_sheet("Duyệt đợt 1", 1)
    heads = ["ID", "Tên tiệm", "Ngành", "Khu vực", "SĐT", "Link Zalo", "Email", "Tin Zalo soạn sẵn",
             "Tiêu đề email", "Nội dung email", "Duyệt (Có / Sửa / Bỏ)", "Ghi chú của anh Ninh"]
    widths = [8, 26, 18, 10, 12, 24, 24, 70, 40, 70, 14, 30]
    thin = Side(style="thin", color="BFBFBF")
    for i, (h, w) in enumerate(zip(heads, widths), start=1):
        c = dv.cell(row=1, column=i, value=h)
        c.font, c.fill = Font(name="Arial", bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F3864")
        c.alignment = Alignment(wrap_text=True, vertical="center")
        dv.column_dimensions[c.column_letter].width = w
    dv.freeze_panes = "C2"
    val = DataValidation(type="list", formula1='"Có,Sửa,Bỏ"', allow_blank=True)
    dv.add_data_validation(val)
    for i, l in enumerate(leads, start=2):
        sdt = (l.get("sdt") or "").replace(" ", "").replace(".", "")
        vals = {"A": l["id"], "B": dt.date.today(), "C": l["nganh"], "D": l["ten"], "E": l.get("khu_vuc", ""),
                "F": l.get("dia_chi", ""), "G": sdt, "I": l.get("email", ""), "K": l.get("website", ""),
                "L": l.get("fanpage", ""), "J": l.get("maps", ""), "M": l.get("sao"), "N": l.get("so_danh_gia"), "R": "; ".join(l.get("diem_yeu", [])), "T": "2. Đã chấm điểm",
                "U": "Zalo + Email" if l.get("email") else "Zalo",
                "AF": ("CHUỖI – chào gói lớn. " if l.get("chuoi") else "") + "Nguồn: " + " | ".join(l.get("nguon", []))[:500]}
        for col, v in vals.items():
            ds[f"{col}{row}"] = v
        cd[f"A{crow}"] = l["id"]
        for col, v in (l.get("diem") or score(l)).items():
            cd[f"{col}{crow}"] = v
        cd[f"N{crow}"] = ("Tự chấm từ Google Maps" + (f", thứ hạng tìm kiếm #{l['hang']}" if l.get("hang") else ", ngoài top tìm kiếm")) if l.get("diem") else ("Sơ bộ từ web (website, fanpage, đặt lịch). Chưa có dữ liệu Google Maps – chấm bổ sung khi có khoá API.")
        row, crow = row + 1, crow + 1
        zalo, subj, body = msgs(l)
        rowvals = [l["id"], l["ten"], l["nganh"], l.get("khu_vuc", ""), sdt,
                   ("SĐT bàn – gọi điện, không có Zalo" if sdt.startswith("02") else f"https://zalo.me/{sdt}") if sdt else "KHÔNG CÓ SĐT – cần tìm thêm", l.get("email", ""), zalo,
                   subj if l.get("email") else "", body if l.get("email") else "", "",
                   f"Điểm {l['tong']}/100 – dữ liệu Google Maps" if l.get("diem") else "CẦN KIỂM TRA điểm yếu trước khi gửi (dữ liệu từ danh bạ, chưa mở được trang của tiệm)"]
        for j, v in enumerate(rowvals, start=1):
            c = dv.cell(row=i, column=j, value=v)
            c.font = Font(name="Arial", size=10, color="0000FF" if j >= 11 else "000000")
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(left=thin, right=thin, top=thin, bottom=thin)
        dv.cell(row=i, column=11).fill = PatternFill("solid", fgColor="FFF2CC")
        dv.cell(row=i, column=12).fill = PatternFill("solid", fgColor="FFF2CC")
        val.add(f"K{i}")
    wb.save(CRM)
    print(f"Đã thêm {len(leads)} tiệm và tạo sheet 'Duyệt đợt 1'")


if __name__ == "__main__":
    main(sys.argv[1:])
