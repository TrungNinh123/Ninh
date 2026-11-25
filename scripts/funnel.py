"""Phễu chọn tiệm 100 → 30 → 10 → 3 (+5 đối chứng), phiên bản thang điểm v1.

Tầng 2 (tự động, 100 điểm): khả năng chi trả 25 · khoảng trống 25 · liên hệ được 20 · quan tâm uy tín 15 · tự quyết 15.
Tầng 3 (đọc 5 đánh giá Google gần nhất của từng tiệm, 100 điểm):
    phàn nàn về đặt lịch / chờ / phản hồi 40 · tiệm đang hoạt động sôi nổi (đánh giá trong 60 ngày) 30 · tiệm độc lập 30.
Điểm chọn = 50% tầng 2 + 50% tầng 3.
Kết quả: crm/du_doan_v1.json (chốt trước khi gửi) + sheet "Phễu v1" trong CRM.
"""
import datetime as dt
import json
import random
import re
import urllib.request
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
import sys
_NAIL = "--nail" in sys.argv
LEADS = ROOT / ("crm/leads_q1_nail.json" if _NAIL else "crm/leads_q1_spa.json")
CRM, OUT = ROOT / "crm/CRM_Tiem.xlsx", ROOT / ("crm/du_doan_nail_v1.json" if _NAIL else "crm/du_doan_v1.json")
SHEET = "Phễu Nail v1" if _NAIL else "Phễu v1"
CHUOI = re.compile(r"bệnh viện|chi nhánh|hệ thống|cơ sở|branch|\(chuỗi\)", re.I)
PHAN_NAN = re.compile(r"chờ|đợi|đặt lịch|book|hẹn|gọi không|nhắn tin|không trả lời|phản hồi chậm|trễ|kín lịch|wait|appointment|reservation|late|no one answer", re.I)


def phan_khuc(ten):
    t = ten.lower()
    if "nail" in t or "móng" in t:
        return "Nail"
    if re.search(r"thẩm mỹ|clinic|bệnh viện|da liễu|derma", t):
        return "Thẩm mỹ viện"
    return "Spa / Massage / Headspa"


def tang2(l):
    n, s, sdt, web, h = l["so_danh_gia"] or 0, l["sao"] or 0, l["sdt"], l["website"], l["hang"]
    a = 25 if 100 <= n <= 600 else 18 if 600 < n <= 1500 else 15 if 30 <= n < 100 else 10 if n > 1500 else 5
    b = (10 if not web else 7 if "facebook" in web else 0) + (8 if not h or h > 20 else 5 if h > 10 else 0) \
        + (5 if l["diem"]["G"] == 0 or l["diem"]["I"] == 0 else 0)
    c = 20 if sdt and not sdt.startswith("02") else 8 if sdt else 0
    d = 15 if s >= 4.8 else 12 if s >= 4.5 else 7 if s >= 4.0 else 3
    e = 5 if CHUOI.search(l["ten"]) else 15
    return a + min(b, 25) + c + d + e


def reviews(maps_url, ten):
    """Tìm lại place id theo tên rồi lấy 5 đánh giá (Place Details)."""
    def call(url, body=None, mask=""):
        req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                     headers={"Content-Type": "application/json", "X-Goog-Api-Key": "proxy-injects-key",
                                              "X-Goog-FieldMask": mask})
        return json.load(urllib.request.urlopen(req, timeout=30))
    r = call("https://places.googleapis.com/v1/places:searchText",
             {"textQuery": ten + " quận 1 TP.HCM", "pageSize": 1, "languageCode": "vi"}, "places.id")
    pid = r["places"][0]["id"]
    d = call(f"https://places.googleapis.com/v1/places/{pid}?languageCode=vi", mask="reviews")
    return d.get("reviews", [])


def tang3(l, rv):
    texts = [(x.get("text") or {}).get("text", "") + " " + (x.get("originalText") or {}).get("text", "") for x in rv]
    phan_nan = sum(1 for t in texts if PHAN_NAN.search(t))
    now = dt.datetime.now(dt.timezone.utc)
    moi = sum(1 for x in rv if x.get("publishTime") and
              (now - dt.datetime.fromisoformat(x["publishTime"].replace("Z", "+00:00"))).days <= 60)
    a = min(40, phan_nan * 20)
    b = 30 if moi >= 2 else 15 if moi == 1 else 0
    c = 10 if CHUOI.search(l["ten"]) else 30
    ghi = [t.strip()[:160] for t in texts if PHAN_NAN.search(t)][:2]
    return a + b + c, phan_nan, moi, ghi


def main():
    L = json.loads(LEADS.read_text(encoding="utf-8"))
    for l in L:
        l["phan_khuc"], l["t2"] = phan_khuc(l["ten"]), tang2(l)
    xep = sorted(L, key=lambda l: (-l["t2"], -(l["so_danh_gia"] or 0)))
    di_dong = [l for l in xep if l["sdt"] and not l["sdt"].startswith("02")]
    top30 = di_dong[:30]
    for l in top30:  # tầng 3 chấm bằng phiếu kiểm tra (Google không trả đánh giá/ảnh qua API)
        l["t3"], l["so_phan_nan"], l["trich_dan"] = None, None, []
        l["diem_chon"] = l["t2"]
    top30.sort(key=lambda l: (-l["t2"], -(l["sao"] or 0), abs((l["so_danh_gia"] or 0) - 350)))
    top10, top3 = top30[:10], top30[:3]
    con_lai = [l for l in di_dong if l not in top30]
    random.seed(2026)
    if len(con_lai) < 5:  # danh sách nhỏ (vd. 31 tiệm nail): lấy đối chứng từ hạng 11 trở đi
        con_lai = top30[10:]
    doi_chung = random.sample(con_lai, min(5, len(con_lai)))
    for l in L:
        l["tang"] = ("Top 3" if l in top3 else "Top 10" if l in top10 else "Đối chứng" if l in doi_chung
                     else "Top 30" if l in top30 else "Ngoài phễu")
    snap = {"phien_ban": "v1", "ngay_chot": dt.date.today().isoformat(),
            "thang_diem": __doc__, "tiem": [{k: l.get(k) for k in
            ("id", "ten", "phan_khuc", "sdt", "so_danh_gia", "sao", "hang", "website", "t2", "t3", "so_phan_nan",
             "dg_moi", "trich_dan", "diem_chon", "tang")} for l in L]}
    OUT.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")

    wb = load_workbook(CRM)
    if SHEET in wb.sheetnames:
        del wb[SHEET]
    ws = wb.create_sheet(SHEET, 1)
    ws["A1"] = f"Phễu 100 → 30 → 10 → 3 · thang điểm v1 · chốt dự đoán ngày {snap['ngay_chot']}"
    ws["A1"].font = Font(name="Arial", size=13, bold=True)
    heads = ["Tầng (tạm)", "ID", "Tên tiệm", "Phân khúc", "SĐT", "Số đánh giá", "Sao", "Điểm tầng 2", "Điểm tầng 3",
             "Điểm chọn", "Hạng trong Top 30", "FB/IG đăng ≤30 ngày (25)", "Có TikTok (15)",
             "Đặt lịch chỉ qua tin nhắn/gọi (25)", "Chủ trả lời đánh giá (15)", "Đang chạy khuyến mãi (10)",
             "Kết quả (điền sau)", "Mua? (Có/Không)", "Lý do khách nói"]
    for i, h in enumerate(heads, 1):
        c = ws.cell(row=3, column=i, value=h)
        c.font, c.fill = Font(name="Arial", bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F3864")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[3].height = 45
    for col, w in zip("ABCDEFGHIJKLMNOPQRS", [11, 9, 34, 20, 12, 9, 6, 9, 9, 9, 9, 11, 9, 12, 11, 11, 18, 10, 30]):
        ws.column_dimensions[col].width = w
    ws["A2"] = ("Tầng 3: người kiểm tra điền Có/Không ở 5 cột vàng L–P cho 30 tiệm đầu (2–3 phút/tiệm). "
                "Điểm tầng 3, điểm chọn và hạng tự tính lại. Sau khi đủ, chốt Top 10 / Top 3 theo cột 'Hạng'.")
    ws["A2"].font = Font(name="Arial", size=9, italic=True)
    thu_tu = {"Top 3": 0, "Top 10": 1, "Top 30": 2, "Đối chứng": 3, "Ngoài phễu": 4}
    rows = sorted(L, key=lambda l: (thu_tu[l["tang"]], -(l.get("diem_chon") or l["t2"])))
    dv = DataValidation(type="list", formula1='"Có,Không"', allow_blank=True)
    ws.add_data_validation(dv)
    yellow = PatternFill("solid", fgColor="FFF2CC")
    n30 = sum(1 for l in rows if l["tang"] in ("Top 3", "Top 10", "Top 30"))
    for r, l in enumerate(rows, start=4):
        vals = [l["tang"], l["id"], l["ten"], l["phan_khuc"], l["sdt"], l["so_danh_gia"], l["sao"], l["t2"]]
        for i, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=i, value=v)
            c.font = Font(name="Arial", size=10, bold=l["tang"] == "Top 3" and i <= 3)
            c.alignment = Alignment(wrap_text=i == 3, vertical="top")
        doc_lap = 10 if not CHUOI.search(l["ten"]) else 0
        ws[f"I{r}"] = (f'=IF(COUNTA(L{r}:P{r})=0,"",IF(L{r}="Có",25,0)+IF(M{r}="Có",15,0)+IF(N{r}="Có",25,0)'
                       f'+IF(O{r}="Có",15,0)+IF(P{r}="Có",10,0)+{doc_lap})')
        ws[f"J{r}"] = f'=IF(I{r}="",H{r},0.5*H{r}+0.5*I{r})'
        if r < 4 + n30:
            ws[f"K{r}"] = f"=RANK(J{r},$J$4:$J${3 + n30})"
            for col in "LMNOP":
                ws[f"{col}{r}"].fill = yellow
                dv.add(f"{col}{r}")
        for col in "QRS":
            ws[f"{col}{r}"].fill = yellow
            ws[f"{col}{r}"].font = Font(name="Arial", size=10, color="0000FF")
        dv.add(f"R{r}")
    last = 3 + len(rows)
    rng = lambda c: f"${c}$4:${c}${last}"  # noqa: E731
    co = lambda t: f'COUNTIFS({rng("A")},"{t}",{rng("R")},"Có")'  # noqa: E731
    hoc = [
        ("Số tiệm đã mua", f'=COUNTIF({rng("R")},"Có")', "0"),
        ("Độ chính xác Top 3 (số mua / 3)", f"={co('Top 3')}/3", "0%"),
        ("Top 10 bắt trúng (khách mua nằm trong Top 10)", f"=IF(V4=0,0,({co('Top 3')}+{co('Top 10')})/V4)", "0%"),
        ("Top 30 bắt trúng", f"=IF(V4=0,0,({co('Top 3')}+{co('Top 10')}+{co('Top 30')})/V4)", "0%"),
        ("Khách mua thuộc nhóm đối chứng", f"={co('Đối chứng')}", "0"),
        ("Điểm tầng 2 TB – nhóm mua", f'=IFERROR(AVERAGEIFS({rng("H")},{rng("R")},"Có"),"-")', "0.0"),
        ("Điểm tầng 2 TB – nhóm không mua", f'=IFERROR(AVERAGEIFS({rng("H")},{rng("R")},"Không"),"-")', "0.0"),
        ("Điểm tầng 3 TB – nhóm mua", f'=IFERROR(AVERAGEIFS({rng("I")},{rng("R")},"Có"),"-")', "0.0"),
        ("Điểm tầng 3 TB – nhóm không mua", f'=IFERROR(AVERAGEIFS({rng("I")},{rng("R")},"Không"),"-")', "0.0"),
    ]
    ws["U3"], ws["V3"] = "Học sau mỗi vòng", "Giá trị"
    for c in ("U3", "V3"):
        ws[c].font, ws[c].fill = Font(name="Arial", bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F3864")
    ws.column_dimensions["U"].width, ws.column_dimensions["V"].width = 44, 12
    for i, (k, f, fmt) in enumerate(hoc, start=4):
        ws[f"U{i}"], ws[f"V{i}"] = k, f
        ws[f"V{i}"].number_format = fmt
    ws.freeze_panes = "D4"
    wb.save(CRM)
    print("TOP 3:", [(l["ten"][:35], l["diem_chon"]) for l in top3])
    print("TOP 10:", [(l["ten"][:30], l["diem_chon"], l["so_phan_nan"]) for l in top10[3:]])
    print("Đối chứng:", [l["ten"][:30] for l in doi_chung])
    print("Lỗi:", [l["ten"][:20] for l in top30 if l.get("loi")])


if __name__ == "__main__":
    main()
