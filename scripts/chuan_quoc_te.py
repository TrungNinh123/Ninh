"""Trang "Tiệm X so với chuẩn quốc tế" (gửi riêng cho từng chủ tiệm).

Hai phần đặt cạnh nhau theo 7 hạng mục của bản khám:
  1) Chuẩn 9–10: điểm mạnh nhất của từng hạng mục, lấy từ tiệm dẫn đầu thế giới (và Việt Nam cho Google Maps), có nguồn.
  2) Tiệm hiện tại (điểm + bằng chứng) và phần MREAL đã làm sẵn theo đúng khung đó.
Hai mốc điểm: "Ngày bật" = hạ tầng làm sẵn (ước tính MREAL); "3–6 tháng" = độ phủ (người theo dõi, đánh giá) cần thời gian.

Chạy:  python scripts/chuan_quoc_te.py Q1S051 Q1S041 Q1S059   ->  reports/chuan_qt_<id>.html
"""
import sys
from html import escape as e
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ban_kham import DEMO_URL, KHAM, LEADS, tinh_diem  # noqa: E402
from demo import DEMO  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LISA = LEADS["Q1S022"]

# (chuẩn 9–10, nguồn [(tên, url)], MREAL làm sẵn, cách tính điểm ngày bật từ điểm hiện tại)
CHUAN = [
    ("Vanity Projects (New York, Miami): khoảng 130.000 người theo dõi Instagram, mỗi bài là một bộ móng vẽ tay chụp cận. "
     "Paintbox (New York): feed chính là menu, mẫu nào đăng cũng đặt được.",
     [("Beauty Launchpad", "https://www.beautylaunchpad.com/business/nail-news/article/21809218/savvy-salon-vanity-projects"),
      ("Foursquare", "https://lv.foursquare.com/paintbox9261795")],
     "Lưới Instagram 9 ô đầu tiên và 4 bảng Pinterest theo dịp, cùng một nền và một nguồn sáng.", lambda d: max(d, 6)),
    ("Paintbox đăng video theo mùa và theo trend, kèm hashtag địa phương. NYC Polished quay quy trình từng bước, ghi tên thợ. "
     "Khách du lịch tự quay trải nghiệm ở 5x5 Nail Studio (Seoul).",
     [("TikTok Paintbox", "https://www.tiktok.com/@paintboxnails"), ("TikTok NYC Polished", "https://www.tiktok.com/@nycpolished")],
     "Danh sách video đầu tiên theo 3 dạng quốc tế: quy trình, theo mùa, khách thật. Cần 10 clip quay bằng điện thoại của tiệm.", lambda d: max(d, 5)),
    ("Lisa Nail & Spa (dẫn đầu Quận 1): " + str(LISA["sao"]).replace(".", ",") + "★ với "
     + f"{LISA['so_danh_gia']:,}".replace(",", ".") + " đánh giá Google, hạng 1 khi tìm tiệm nail Quận 1.",
     [("Google Maps", LISA["maps"])],
     "Bài mô tả Google Maps, 3 mẫu trả lời đánh giá, mã QR xin đánh giá (viết sẵn bên dưới).", lambda d: max(d, 7)),
    ("Sundays (New York): mỗi dịch vụ ghi giá và số phút, đặt online, mỗi chi nhánh có trang riêng. "
     "Chillhouse giữ thẻ khi đặt để chống bỏ hẹn.",
     [("Sundays menu", "https://dearsundays.com/pages/nycstudiomenu"), ("Chillhouse FAQ", "https://chillhouse.com/pages/faq")],
     "Trang đặt lịch một nút, gắn được vào Google Maps, Facebook, Instagram, TikTok.", lambda d: 9),
    ("Chillhouse: gói thành viên Club Chill (ví dụ 125 USD/tháng), gift card dùng 5 năm, tạo doanh thu đều mỗi tháng.",
     [("Club Chill", "https://chillhouse.com/pages/club-chill")],
     "Tin Zalo nhắc làm lại sau 3 tuần, thẻ 10 lần, gift card theo dịp (viết sẵn bên dưới).", lambda d: 8),
    ("Vanity Projects hợp tác bộ sưu tập với Pleasing (thương hiệu của Harry Styles, 2023). "
     "Unistella (Seoul) tạo trend có tên riêng, gắn với nghệ sĩ K-pop.",
     [("Hypebae", "https://hypebae.com/2023/7/harry-styles-pleasing-manicure-pollinators-collection-vanity-projects-miami-new-york-collab"),
      ("Fashion Magazine", "https://fashionmagazine.com/beauty-grooming/park-eunkyung-unistella-nail-artist/")],
     "Giới thiệu thợ chính trên trang và lưới (cần tên, ảnh thợ). Hạng mục này cần thời gian, không tăng ngay.", lambda d: d),
    ("Paintbox: nút Book a Manicure và Gift Cards ngay trang chủ, menu mẫu theo mùa giá trọn gói, FAQ rõ ràng.",
     [("paint-box.com", "https://paint-box.com/"), ("Menu", "https://paint-box.com/menu")],
     "Landing page theo khung Paintbox: đặt lịch, lookbook đánh số, bảng giá, gift card.", lambda d: 9),
]


def viet_san(c, ten):
    zalo = c["lien_he"][1].split("·")[-1].strip()
    mo_ta = (f"{ten}: {c['hero'][0].lower() + c['hero'][1:]}. {c['hero_phu']}. "
             "Giá trọn gói, chọn mẫu theo số, đặt lịch online trong 30 giây. "
             f"{c['dia_chi'].split(' · ')[0]}. Zalo {zalo}.")
    return [
        ("Bài mô tả Google Maps", mo_ta),
        ("Trả lời đánh giá 5 sao", f"Cảm ơn chị đã chọn {ten}! Bộ móng hợp với chị lắm. Khoảng 3 tuần nữa chị ghé dặm lại nhé, đặt lịch nhanh qua Zalo {zalo}."),
        ("Trả lời đánh giá 4 sao", f"Cảm ơn chị đã góp ý. {ten} ghi nhận để lần sau chị hài lòng trọn vẹn. Chị nhắn Zalo {zalo} để tiệm giữ giờ đẹp cho lần tới."),
        ("Trả lời đánh giá 1–3 sao", f"{ten} rất tiếc vì trải nghiệm chưa tốt. Chị nhắn Zalo {zalo} để chủ tiệm trực tiếp hỗ trợ chị ngay."),
        ("Tin Zalo nhắc làm lại (sau 3 tuần)", f"Chào chị, đã 3 tuần từ lần làm móng ở {ten}. Mẫu Noel – Tết mới đã có, chị chọn mẫu và đặt lịch qua link này để giữ giờ đẹp nhé."),
        ("Thẻ 10 lần và gift card", "Thẻ 10 lần: mua 10 tặng 1. Gift card 8/3, 20/10, Valentine: khách mua tặng, tiệm có doanh thu trước."),
    ]


def tao(pid):
    c = DEMO[pid]
    ten = c["title"].removeprefix("Demo ")
    _, _, _, hm, tong = tinh_diem(pid)
    k = KHAM[pid]
    van_de = k.get("van_de") or []
    rows, bat = [], []
    for (ten_hm, d, _, _, w), (chuan, nguon, lam, f_bat) in zip(hm, CHUAN):
        b = f_bat(d)
        bat.append(b * w)
        rows.append((ten_hm, d, b, w, chuan, nguon, lam))
    ngay_bat = str(round(sum(bat) / 100, 1)).replace(".", ",")
    tong = str(tong).replace(".", ",")

    def cham(v, cls):
        return f'<i class="{cls}" style="left:{v * 10}%"></i>'
    bars = "".join(
        f'<div class=row><div class=lb>{e(t.split(" (")[0])}<span>{d} → {b}</span></div>'
        f'<div class=track><b class=goal></b><s style="left:{d * 10}%;width:{max(b - d, 0) * 10}%"></s>{cham(d, "now")}{cham(b, "day")}</div></div>'
        for t, d, b, *_ in rows)
    bang = "".join(
        f'<tr><td data-l="Hạng mục"><b>{e(t)}</b><br><span class=m>Trọng số {w}%</span></td>'
        f'<td data-l="Chuẩn 9–10">{e(ch)}<br><span class=src>{" · ".join(f"<a href={chr(34)}{u}{chr(34)} target=_blank rel=noopener>{e(n)}</a>" for n, u in ng)}</span></td>'
        f'<td data-l="Tiệm hiện tại" class=num><b>{d}/10</b></td>'
        f'<td data-l="MREAL làm sẵn">{e(l)}<br><b class=up>Ngày bật: {b}/10</b></td></tr>'
        for t, d, b, w, ch, ng, l in rows)
    vs = "".join(f"<div class=card><h3>{e(t)}</h3><p>{e(x)}</p></div>" for t, x in viet_san(c, ten))
    vd = "".join(f"<li>{e(x)}</li>" for x in van_de[:3])
    demo = DEMO_URL.get(pid, "")
    return f"""<title>{e(ten)} và chuẩn quốc tế</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Be+Vietnam+Pro:wght@400;500;600&display=swap">
<style>
/* VOICE work, gửi riêng chủ tiệm
   IDEA phiếu so màu móng: mỗi hạng mục là một thanh màu từ hiện tại tới chuẩn quốc tế
   PICTURE 7 thanh dumbbell: chấm hiện tại, chấm ngày bật, vùng 9–10 tô hồng
   COLOUR nền kem hồng, mực nâu đậm, hồng đậm dẫn, xanh lá cho mức đạt được
   TYPE Fraunces + Be Vietnam Pro (cùng bộ demo)
   LAYOUT laptop: kết luận + 3 con số trên, thanh so sánh dưới; điện thoại xếp dọc */
:root{{color-scheme:light dark;--bg:light-dark(#f7f1ee,#171312);--card:light-dark(#fff,#211b19);--ink:light-dark(#2a2220,#f2e9e5);--mut:light-dark(#6f625d,#b5a7a1);--line:light-dark(#e7dfda,#3a312e);--rose:light-dark(#b8405f,#ec8aa3);--blush:light-dark(#f6dfe5,#43262e);--ok:light-dark(#1f7a52,#6fd3a0)}}
:root[data-theme=light]{{color-scheme:light}}:root[data-theme=dark]{{color-scheme:dark}}
*{{box-sizing:border-box;min-width:0}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 "Be Vietnam Pro",system-ui,sans-serif;overflow-x:clip}}
.band{{padding-block:clamp(24px,4vw,48px);padding-left:max(5vw,16px,env(safe-area-inset-left,0px));padding-right:max(5vw,16px,env(safe-area-inset-right,0px))}}
.in{{max-width:1080px;margin:0 auto}}
h1{{font:600 clamp(30px,4.5vw,46px)/1.08 Fraunces,Georgia,serif;letter-spacing:-.02em;margin:0 0 12px;max-width:22ch}}
h2{{font:600 24px/1.2 Fraunces,Georgia,serif;margin:0 0 6px}}h3{{font:600 16px/1.3 "Be Vietnam Pro",sans-serif;margin:0 0 6px}}
.m{{color:var(--mut);font-size:14px}}a{{color:var(--rose)}}
.lead{{font-size:17px;max-width:62ch;margin:0}}
.nums{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:22px 0}}
.nums div{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}}
.nums b{{display:block;font:600 clamp(30px,4vw,40px)/1 Fraunces,serif;white-space:nowrap}}.nums .a b{{color:var(--mut)}}.nums .c b{{color:var(--ok)}}.nums .d b{{color:var(--rose)}}
.chart{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px}}
.key{{display:flex;flex-wrap:wrap;gap:16px;font-size:14px;color:var(--mut);margin-bottom:10px}}.key i{{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-1px;margin-right:6px}}
.row{{display:grid;grid-template-columns:minmax(0,15em) minmax(0,1fr);gap:14px;align-items:center;padding:9px 0;border-top:1px solid var(--line)}}
.lb{{font-size:15px}}.lb span{{display:block;font-size:13px;color:var(--mut);font-variant-numeric:tabular-nums}}
.track{{position:relative;height:22px;border-radius:99px;background:linear-gradient(90deg,var(--line),var(--line)) center/100% 4px no-repeat}}
.track .goal{{position:absolute;left:90%;right:0;top:0;bottom:0;background:var(--blush);border-radius:99px}}
.track s{{position:absolute;top:9px;height:4px;background:var(--ok);opacity:.55}}
.track i{{position:absolute;top:3px;width:16px;height:16px;margin-left:-8px;border-radius:50%;border:2px solid var(--card)}}
.now{{background:var(--mut)}}.day{{background:var(--ok)}}.k1{{background:var(--mut)}}.k2{{background:var(--ok)}}.k3{{background:var(--blush);border:1px solid var(--rose)}}
.scale{{display:flex;justify-content:space-between;font-size:13px;color:var(--mut);margin-left:calc(15em + 14px)}}
.scroll{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:15px}}
th,td{{text-align:left;vertical-align:top;padding:12px 10px;border-bottom:1px solid var(--line)}}th{{font-size:13px;color:var(--mut);font-weight:600}}
td.num{{white-space:nowrap;font-variant-numeric:tabular-nums}}.src{{font-size:13px}}.up{{color:var(--ok);font-size:14px;white-space:nowrap}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:12px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}}.card p{{margin:0;font-size:15px}}
.cta{{background:var(--rose);color:#fff}}.cta h2{{color:#fff}}.cta a{{color:#fff;font-weight:600}}.cta .m{{color:rgba(255,255,255,.85)}}
.btn{{display:inline-block;background:#fff;color:var(--rose)!important;border-radius:12px;padding:12px 18px;text-decoration:none;margin-top:8px}}
@media(max-width:640px){{.nums{{gap:8px}}.nums div{{padding:10px;font-size:13px}}.row{{grid-template-columns:1fr;gap:6px}}.scale{{margin-left:0}}table{{font-size:14px}}thead{{display:none}}tr{{display:grid;padding:10px 0;border-bottom:1px solid var(--line)}}td{{border:0;padding:4px 0}}td::before{{content:attr(data-l);display:block;font-size:12px;color:var(--mut)}}}}
</style>
<section class=band><div class=in>
<p class=m>MREAL · gửi riêng {e(ten)} · số liệu kiểm tra ngày 25/11/2026</p>
<h1>{e(ten)}: từ {tong}/10 lên chuẩn quốc tế</h1>
<p class=lead>Tiệm dẫn đầu thế giới đạt 9–10 điểm vì làm đúng 7 việc, không phải vì có ngân sách lớn. MREAL đã làm sẵn cho {e(ten)} theo đúng 7 việc đó: bật lên là hạ tầng đạt chuẩn ngay; người theo dõi và đánh giá cần 3–6 tháng để lên 9.</p>
<div class=nums><div class=a><b>{tong}</b>Hiện tại</div><div class=c><b>{ngay_bat}</b>Ngày bật bản làm sẵn</div><div class=d><b>9–10</b>Chuẩn quốc tế, sau 3–6 tháng</div></div>
<div class=chart><div class=key><span><i class=k1></i>Hiện tại</span><span><i class=k2></i>Ngày bật bản làm sẵn</span><span><i class=k3></i>Vùng chuẩn quốc tế 9–10</span></div>
{bars}<div class=scale><span>0</span><span>5</span><span>10</span></div></div>
</div></section>

<section class=band style="padding-top:0"><div class=in>
<h2>7 việc: chuẩn quốc tế, {e(ten)} hôm nay, và phần đã làm sẵn</h2>
<p class=m>Chuẩn 9–10 ghép từ điểm mạnh nhất của từng hạng mục ở các tiệm dẫn đầu; không tiệm nào đứng đầu cả 7. Điểm "ngày bật" là ước tính của MREAL.</p>
<div class=scroll><table><thead><tr><th>Hạng mục</th><th>Chuẩn 9–10 (ví dụ thật)</th><th>Hôm nay</th><th>MREAL đã làm sẵn</th></tr></thead><tbody>{bang}</tbody></table></div>
<p class=m>Ba điểm cần xử lý trước:</p><ul class=m>{vd}</ul>
</div></section>

<section class=band style="padding-top:0"><div class=in>
<h2>Đã viết sẵn, dùng được ngay</h2>
<div class=grid>{vs}</div>
</div></section>

<section class="band cta"><div class=in>
<h2>Anh chị đồng ý là bật trong 24 giờ</h2>
<p>Landing page, trang đặt lịch, lưới Instagram, bảng Pinterest đã dựng sẵn. Anh chị chỉ cần gửi 10 clip làm móng quay bằng điện thoại và xác nhận bảng giá.</p>
{f'<a class=btn href="{demo}" target=_blank rel=noopener>Xem bản làm sẵn cho {e(ten)}</a>' if demo else ''}
<p class=m>Phương Thư · MREAL</p>
</div></section>
"""


if __name__ == "__main__":
    for pid in sys.argv[1:]:
        out = ROOT / "reports" / f"chuan_qt_{pid}.html"
        out.write_text(tao(pid), encoding="utf-8")
        print("Đã tạo", out.relative_to(ROOT))
