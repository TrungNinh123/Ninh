"""Tạo bộ demo cho tiệm nail theo mẫu demo My Doris (reports/demo_Q1S044.html).

Mỗi tiệm có một cấu hình trong DEMO bên dưới. Phần "Hiện tại" chỉ ghi điều đã có bằng chứng
trong crm/kham_nail_v1.json, crm/leads_q1_nail.json, crm/audit_web_v1.json (khám ngày 25/11/2026).
Giá: chỉ ghi giá tiệm tự công bố; giá từ nguồn bên thứ ba ghi rõ "chờ tiệm xác nhận".

Chạy:  python scripts/demo.py            (tạo mọi tiệm)
       python scripts/demo.py Q1S079     (một tiệm)
"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAU = ROOT / "reports" / "demo_Q1S044.html"

DEMO = {
    "Q1S079": dict(
        title="Demo Dami Nail", ten="Dami Nail — 8B Nguyễn Văn Thủ, Tân Định",
        mo_dau="Ngày 25/11/2026, Dami Nail có 4,8★ với 52 đánh giá Google và video TikTok lan vào các trang khám phá "
               "\"korean nails\", nhưng chưa có website, bảng giá hay nút đặt lịch. Fanpage ghi địa chỉ chi nhánh 2 (157 Cô Bắc) "
               "trong khi Google Maps ghi 8B Nguyễn Văn Thủ.",
        tag="Ảnh thật của tiệm · nail chuẩn Hàn", sao="★ 4,8 Google · 52 đánh giá",
        hero="Nail chuẩn Hàn, bảo hành 7 ngày", hero_phu="Nailbox thiết kế theo yêu cầu · 2 chi nhánh Quận 1 · 9h–21h",
        nut="Đặt lịch hoặc đặt nailbox online", lien_he=["TikTok", "Zalo · 0909 430 018"],
        look_ten="Korean Lookbook · Noel – Tết", look_mo="Chọn mẫu theo số, chọn chi nhánh, giữ chỗ trước.",
        tang=[("Sơn gel trơn", "giá của tiệm"), ("Nail art chuẩn Hàn", "giá của tiệm"), ("Nailbox theo yêu cầu", "giá của tiệm")],
        note="Bảo hành 7 ngày ghi ngay cạnh giá. Nailbox đặt online, nhận tại tiệm: bán được cả cho khách ở xa.",
        dia_chi="CN1: 8B Nguyễn Văn Thủ, Tân Định · CN2: 157 Cô Bắc, Cô Giang · Chỉ đường từng chi nhánh",
        so_sanh=[
            ("Không có website; Google Maps không gắn link nào", "Trang đặt lịch riêng, gắn vào Google Maps, TikTok, Facebook"),
            ("Fanpage ghi 157 Cô Bắc, Maps ghi 8B Nguyễn Văn Thủ: khách dễ đi nhầm", "Hai chi nhánh tách rõ, mỗi nơi một nút chỉ đường"),
            ("Hotline khác nhau giữa các nguồn", "Một số Zalo duy nhất trên mọi kênh"),
            ("Video TikTok được xem nhiều nhưng không dẫn về đâu", "Mỗi video có link đặt đúng mẫu trong video"),
            ("Không có bảng giá công khai", "Bảng giá 3 mức, ghi kèm bảo hành 7 ngày"),
        ],
        ig=["Video 20s: làm mẫu Hàn 01", "Mẫu Noel 02 · giá trọn gói", "Khách thật · đánh giá 5★", "Bảng giá 3 mức",
            "Nailbox mở hộp", "Video: bảo hành 7 ngày là gì", "Thợ của tiệm", "Mẫu Tết đỏ – vàng", "Hai chi nhánh, chọn nơi gần bạn"],
        pins=[("Korean Nails Saigon", "Mẫu chuẩn Hàn đánh số"), ("Custom Nailbox", "Nailbox theo yêu cầu, giao tại tiệm"),
              ("Christmas Nails – Dami", "Mẫu Noel"), ("Lunar New Year Nails", "Tết đỏ – vàng")],
        ap_dung=["Lookbook chuẩn Hàn đánh số theo mùa", "Bảng giá 3 mức, bảo hành ghi rõ", "Thẻ 10 lần, nailbox làm quà tặng", "Mỗi dịch vụ ghi giá và số phút"],
    ),
    "Q1S041": dict(
        title="Demo February Nails", ten="February Nails — 18A/62 Nguyễn Thị Minh Khai, Quận 1",
        mo_dau="Ngày 25/11/2026, February Nails có 4,9★ với 335 đánh giá Google, 5,0 trên Tripadvisor, dòng sơn gel mang tên riêng "
               "và được nhiều trang top tiệm nail Quận 1 nhắc tên. Nhưng Google Maps dẫn về Facebook, chưa có bảng giá chính thức, "
               "chưa đặt lịch online được và chưa thấy TikTok.",
        tag="Ảnh thật của tiệm · pastel Hàn", sao="★ 4,9 Google · 335 đánh giá · 5,0 Tripadvisor",
        hero="Artful nails, cozy vibes", hero_phu="Sơn gel độc quyền February 100 màu · Quận 1 và Thảo Điền",
        nut="Chọn màu và đặt lịch", lien_he=["Instagram", "Zalo · 0343 636 161"],
        look_ten="Bảng màu February · Noel – Tết", look_mo="Chọn màu trong 100 màu độc quyền trước khi đến.",
        tang=[("Sơn gel trơn", "~100–140k*"), ("Đắp gel / hard gel", "~250–380k*"), ("Nail art", "~20–70k/móng*")],
        note="* Giá từ trang bên thứ ba (ubeauty, wikithammy), chờ tiệm xác nhận. Gift card 8/3, 20/10, Valentine.",
        dia_chi="Quận 1: Hẻm 18A/62 Nguyễn Thị Minh Khai · Thảo Điền: 14M Quốc Hương · Một giờ mở cửa thống nhất",
        so_sanh=[
            ("Google Maps dẫn về Facebook, không có website", "Trang riêng tải nhanh, gắn vào Maps và Instagram"),
            ("Dòng sơn gel riêng 100 màu nhưng khách không xem trước được", "Bảng màu số hoá: chọn màu ngay trên điện thoại"),
            ("Không có bảng giá chính thức", "Bảng giá 3 mức do tiệm xác nhận"),
            ("Giờ mở cửa ghi khác nhau giữa các nguồn (9–20h và 9–21h)", "Một giờ mở cửa thống nhất trên mọi kênh"),
            ("Instagram 1.359 người theo dõi dù đã có 424 bài; chưa thấy TikTok", "Lưới Instagram đồng bộ và video ngắn đăng theo lịch"),
        ],
        ig=["Video 20s: phối màu February", "Màu mới tháng 12", "Khách nước ngoài · Tripadvisor 5,0", "Bảng giá 3 mức",
            "Mẫu Noel pastel", "Video: hard gel bền bao lâu", "Góc tiệm ấm cúng", "Mẫu Tết", "Thảo Điền hay Quận 1?"],
        pins=[("February Color Card", "100 màu độc quyền"), ("Pastel Korean Nails", "Mẫu pastel đánh số"),
              ("Christmas Nails Saigon", "Mẫu Noel"), ("Hard Gel Natural Look", "Hard gel tự nhiên")],
        ap_dung=["Bảng màu độc quyền làm \"menu\" theo mùa", "Bảng giá 3 mức, không phát sinh", "Thẻ 10 lần, gift card dịp lễ", "Mỗi dịch vụ ghi giá và số phút"],
    ),
    "Q1S051": dict(
        title="Demo Nail Districts", ten="Nail Districts & Spa — Lầu 1, 158/4 Nguyễn Công Trứ, Quận 1",
        mo_dau="Ngày 25/11/2026, Nail Districts có 5,0★ với 1.113 đánh giá Google, mức uy tín hiếm có ở Quận 1. "
               "Nhưng tiệm chưa có website, Facebook vẫn để \"Opening Soon\", Instagram 572 người theo dõi dù đã có 439 bài, "
               "và tên tiệm trùng nhiều tài khoản nước ngoài nên khó tìm.",
        tag="Ảnh thật của tiệm · nail xinh theo mùa", sao="★ 5,0 Google · 1.113 đánh giá",
        hero="1.113 khách chấm 5 sao", hero_phu="Nail · gội đầu · nối mi · massage · Lầu 1 trong hẻm Nguyễn Công Trứ",
        nut="Đặt combo nail + gội đầu", lien_he=["Instagram", "Zalo · 0333 947 341"],
        look_ten="Fall – Holiday Collection", look_mo="Chọn mẫu theo số, chọn cơ sở, giữ chỗ trước.",
        tang=[("Nail", "giá của tiệm"), ("Nail + gội đầu", "giá của tiệm"), ("Nail + mi", "giá của tiệm")],
        note="Combo theo dịp: cưới, Noel, Tết. Thẻ 10 lần cho khách văn phòng quanh Bến Thành.",
        dia_chi="Q1: Lầu 1, 158/4 Nguyễn Công Trứ · Cơ sở 2: 269/1 Nguyễn Trãi · 10h–20h · Hướng dẫn lên lầu",
        so_sanh=[
            ("Không có website; 1.113 đánh giá 5★ chỉ nằm trên Google Maps", "Đánh giá thật đưa lên trang đầu, kèm nút đặt lịch"),
            ("Facebook để \"Opening Soon\", 2 đánh giá", "Fanpage cập nhật, mọi bài dẫn về một nút đặt lịch"),
            ("Instagram 572 người theo dõi dù 439 bài", "Lưới đồng bộ, video ngắn, hashtag tiếng Việt + Quận 1"),
            ("Tên trùng nhiều tài khoản nước ngoài", "Tên tìm kiếm thống nhất \"Nail Districts Sài Gòn\" trên mọi kênh"),
            ("Không bảng giá, không đặt lịch online", "Bảng giá theo combo, đặt chỗ trong 30 giây"),
        ],
        ig=["Video 20s: một bộ móng từ đầu", "Fall Collection 02", "Khách thật · 5,0★", "Bảng giá combo",
            "Gội đầu thư giãn", "Video: đường lên Lầu 1", "Thợ của tiệm", "Mẫu Noel", "Combo cô dâu"],
        pins=[("Nail Districts Saigon", "Mẫu theo mùa đánh số"), ("Nail + Head Spa", "Combo thư giãn"),
              ("Christmas Nails", "Mẫu Noel"), ("Bridal Nails Saigon", "Nail cô dâu")],
        ap_dung=["Bộ sưu tập theo mùa đánh số", "Combo theo thời lượng, giá trọn gói", "Thẻ 10 lần, gift card", "Mỗi combo ghi giá và số phút"],
    ),
    "Q1S042": dict(
        title="Demo A+ Nail Studio", ten="A+ Nail Studio — 55/8 Lê Thị Hồng Gấm, Quận 1",
        mo_dau="Ngày 25/11/2026, A+ có 4,8★ với 705 đánh giá Google, khoảng 11.000 người theo dõi Facebook, và đứng số 3 "
               "trong một danh sách top tiệm nail TP.HCM. Website hiện là trang WordPress miễn phí: không có giá, nút gọi/Zalo hay bản đồ; "
               "tên Instagram ghi hai kiểu khác nhau.",
        tag="Ảnh thật của tiệm · Y2K đính đá", sao="★ 4,8 Google · 705 đánh giá",
        hero="Làm 1 kèm 1, theo trend", hero_phu="Nail · nối mi · chân mày · Quận 1 và Bình Thạnh · 9h–21h",
        nut="Giữ giờ làm 1 kèm 1", lien_he=["Instagram", "Zalo · 0565 195 109"],
        look_ten="Y2K & Holiday Lookbook", look_mo="Chọn mẫu theo số, chọn thợ, giữ giờ trước.",
        tang=[("Nail trơn", "giá của tiệm"), ("Y2K đính đá / charm", "180–350k"), ("Nail + mi", "giá của tiệm")],
        note="Giá Y2K theo bài Threads của tiệm (04/2026). Làm 1 kèm 1 nên giữ giờ trước, nhắc lịch qua Zalo.",
        dia_chi="CN1: 55/8 Lê Thị Hồng Gấm, Bến Thành · CN2: 69/7 Nguyễn Gia Trí, Bình Thạnh · Chỉ đường",
        so_sanh=[
            ("Website WordPress miễn phí: không giá, không nút gọi/Zalo, không bản đồ", "Trang riêng có giá, nút Zalo và bản đồ hai chi nhánh"),
            ("Hai tên Instagram: @acongnails và @acong.nail.studio", "Một tên duy nhất trên mọi kênh"),
            ("Instagram 4.327 người theo dõi dù 621 bài; chưa thấy TikTok", "Video ngắn theo trend, đăng đều theo lịch"),
            ("Bảo hành ghi 7 ngày ở nơi này, 5 ngày ở nơi khác", "Chính sách bảo hành ghi một lần, rõ ràng"),
            ("Làm 1 kèm 1 nhưng phải nhắn hỏi giờ trống", "Chọn thợ và giờ trống ngay trên trang"),
        ],
        ig=["Video 20s: đính đá Y2K", "Mẫu Noel 02 · giá trọn gói", "Khách thật · 705 đánh giá", "Bảng giá 3 mức",
            "Nối mi tự nhiên", "Video: làm 1 kèm 1 là gì", "Thợ của tiệm", "Mẫu Tết", "Hai chi nhánh"],
        pins=[("Y2K Nails Saigon", "Đính đá, charm, xà cừ"), ("Christmas Nails – A+", "Mẫu Noel"),
              ("Lunar New Year Nails", "Tết đỏ – vàng"), ("Natural Lashes", "Mi tự nhiên")],
        ap_dung=["Lookbook theo trend đánh số", "Bảng giá 3 mức theo độ cầu kỳ", "Thẻ 10 lần, gift card", "Chọn thợ, ghi giá và số phút"],
    ),
    "Q1S059": dict(
        title="Demo Ther Nail", ten="Ther Nail Space & Headspa — 135/12 Trần Hưng Đạo, Quận 1",
        mo_dau="Ngày 25/11/2026, Ther Nail đang mở cửa (Google Maps) với 4,8★ từ 336 đánh giá và khoảng 16.000 người theo dõi Facebook. "
               "Nhưng website thernailspace.com không truy cập được và cũng chưa gắn vào Google Maps; Instagram 1.971 người theo dõi dù 490 bài; "
               "khách chưa đặt lịch online được.",
        tag="Ảnh thật của tiệm · nail và headspa", sao="★ 4,8 Google · 336 đánh giá",
        hero="Nail, gội đầu dưỡng sinh, mi", hero_phu="Mẫu Hàn – Nhật – Âu Mỹ · Nailbox by Ther · cạnh Trần Hưng Đạo",
        nut="Đặt combo nail + headspa", lien_he=["Facebook", "Zalo · 0777 922 699"],
        look_ten="Holiday Lookbook · Noel – Tết", look_mo="Chọn mẫu theo số, giá trọn gói, giữ chỗ trước.",
        tang=[("Gội đầu thư giãn", "429k–799k"), ("Nail theo mẫu", "giá của tiệm"), ("Combo nail + headspa", "giá của tiệm")],
        note="Giá gội đầu theo website của tiệm (bản lưu trong kết quả tìm kiếm). Nailbox và khoá học nghề có trang riêng.",
        dia_chi="135/12 Trần Hưng Đạo, Cầu Ông Lãnh, Q1 · Giờ mở cửa theo Google Maps · Chỉ đường",
        so_sanh=[
            ("Website thernailspace.com không truy cập được (kiểm tra 25/11/2026)", "Trang mở trong 1 giây, chạy tốt trên điện thoại"),
            ("Google Maps không gắn website", "Trang đặt lịch gắn vào Maps, Facebook, Instagram"),
            ("Instagram 1.971 người theo dõi dù 490 bài; Facebook khoảng 16.000", "Kéo người theo dõi Facebook sang đặt lịch bằng một nút"),
            ("Tripadvisor chỉ 1 đánh giá dù tiệm nhắm khách du lịch", "Mã QR xin đánh giá Google và Tripadvisor sau mỗi lượt"),
            ("Không đặt lịch online", "Combo nail + headspa đặt trong 30 giây"),
        ],
        ig=["Video 20s: gội đầu dưỡng sinh", "Mẫu Noel 02 · giá trọn gói", "Khách thật · 4,8★", "Bảng giá combo",
            "Nailbox by Ther", "Video: một bộ móng Hàn", "Thợ của tiệm", "Mẫu Tết", "Combo cho khách du lịch"],
        pins=[("Ther Nail Lookbook", "Hàn – Nhật – Âu Mỹ đánh số"), ("Head Spa Saigon", "Gội đầu dưỡng sinh"),
              ("Nailbox by Ther", "Móng úp theo yêu cầu"), ("Christmas Nails", "Mẫu Noel")],
        ap_dung=["Lookbook theo mùa đánh số", "Combo theo thời lượng, giá trọn gói", "Thẻ 10 lần, gift card nail + headspa", "Mỗi dịch vụ ghi giá và số phút"],
    ),
}

HINH_MAU = [
    ("Paintbox", "https://paint-box.com", "New York", "Menu mẫu theo mùa, giá trọn gói; nút \"Book a Manicure\" và gift card ngay trang chủ"),
    ("Vanity Projects", "https://vanityprojectsnyc.com", "New York, Miami", "Nail art 3 cấp theo thời gian (60/90/120 phút), phụ phí ghi rõ"),
    ("Chillhouse", "https://chillhouse.com", "New York", "Gói thành viên hằng tháng, gift card dùng 5 năm"),
    ("Sundays", "https://dearsundays.com", "New York", "Dịch vụ ghi rõ giá và thời lượng, đặt lịch online"),
]


def tao(id_, c):
    e = escape
    style = re.search(r"<style>.*?</style>", MAU.read_text(encoding="utf-8"), re.S).group(0)
    look = "".join(f"<div>Ảnh thật<b>{i:02d}</b></div>" for i in range(1, 7))
    tang = "".join(f"<div><span>{e(a)}</span><span>{e(b)}</span></div>" for a, b in c["tang"])
    so = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in c["so_sanh"])
    ig = "".join(f"<div>{e(x)}</div>" for x in c["ig"])
    pins = "".join(f"<div class=pin><div class=cov><i></i><i></i><i></i></div><p><b>{e(a)}</b><br>{e(b)}</p></div>" for a, b in c["pins"])
    hm = "".join(f"<tr><td><a href=\"{u}\" target=\"_blank\" rel=\"noopener\">{e(n)}</a> ({e(noi)})</td><td>{e(lam)}</td><td>{e(ad)}</td></tr>"
                 for (n, u, noi, lam), ad in zip(HINH_MAU, c["ap_dung"]))
    ten_ngan = c["title"].removeprefix("Demo ")
    return f"""<title>{e(c['title'])}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Be+Vietnam+Pro:wght@400;500;600&display=swap">
{style}
<main>
<header><div class=k>Bản demo MREAL dựng riêng cho</div><h1>{e(c['ten'])}</h1>
<p class=m>{e(c['mo_dau'])} Đây là bản xem trước nếu MREAL làm lại: mọi khung ảnh sẽ dùng <b>ảnh thật của tiệm</b> (chỉ chỉnh sáng bằng AI, không đổi màu móng); mọi giá điền theo bảng giá của tiệm.</p></header>
<section class=two>
<div class=phone><div class=ph>
  <div class=hero><span class=ph-tag>{e(c['tag'])}</span>
    <div class=stars>{e(c['sao'])}</div>
    <h3>{e(c['hero'])}</h3><div class=m style="color:#5a4a44">{e(c['hero_phu'])}</div></div>
  <div class=btns><div class="btn main">{e(c['nut'])}</div><div class=btn>{e(c['lien_he'][0])}</div><div class=btn>{e(c['lien_he'][1])}</div></div>
  <div><h3>{e(c['look_ten'])}</h3><p class=m style="margin:2px 0 8px">{e(c['look_mo'])}</p>
  <div class=look>{look}</div></div>
  <div><h3>Bảng giá</h3><div class=tier>{tang}</div></div>
  <div class=note>{e(c['note'])}</div>
  <div class=m>{e(c['dia_chi'])}</div>
</div></div>
<div class=panel><h2>Landing page này khác gì hiện tại</h2>
<div class=wrap><table><tr><th>Hiện tại (bằng chứng, khám 25/11/2026)</th><th>Bản demo</th></tr>{so}</table></div>
<p class=m>Chi phí dựng: nằm trong gói Khởi động 500.000đ (landing page). Website đầy đủ nằm trong gói Hệ thống.</p></div>
</section>
<section class=panel><h2>Lưới Instagram 9 ô đầu tiên (kế hoạch)</h2><p class=m>Một nền, một nguồn sáng cho mọi ảnh, để lưới đồng bộ như các tiệm dẫn đầu thế giới.</p>
<div class=ig>{ig}</div></section>
<section class=panel><h2>Bảng Pinterest cho khách chọn mẫu trước khi đến</h2><div class=pins>{pins}</div></section>
<section class=panel><h2>Học từ tiệm nail dẫn đầu thế giới, áp dụng với chi phí thấp</h2><div class=wrap><table>
<tr><th>Hình mẫu</th><th>Họ làm gì</th><th>{e(ten_ngan)} áp dụng</th></tr>{hm}
</table></div><p class=m>Nguồn: website các thương hiệu và bài tổng hợp (tra cứu 25/11/2026). MREAL học cách làm, không sao chép thiết kế.</p></section>
</main>
"""


if __name__ == "__main__":
    for id_ in (sys.argv[1:] or DEMO):
        out = ROOT / "reports" / f"demo_{id_}.html"
        out.write_text(tao(id_, DEMO[id_]), encoding="utf-8")
        print("Đã tạo", out.relative_to(ROOT))
