"""Mẫu website chuẩn Nailmark cho từng tiệm nail.

Điền thông tin tiệm (TIEM bên dưới hoặc file JSON) -> nailmark/tiem/<slug>.html, dùng ảnh trong nailmark/img.
Chỉ đăng công khai trang của một tiệm khi tiệm đã đồng ý; trước đó chỉ gửi riêng cho chủ tiệm.
Chạy: python scripts/web_tiem.py mau            (tiệm mẫu hư cấu)
      python scripts/web_tiem.py nail-districts  (bản riêng, không đăng công khai)
"""
import json
import sys
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIEM = {
    "mau": dict(ten="Sơn Mài Nail", khau_hieu="Móng đẹp như sơn mài, bền qua mùa nóng ẩm", dia_chi=["Quận 1, TP.HCM (địa chỉ mẫu)"],
                gio="9:00–21:00 mỗi ngày", zalo="0900 000 000", sao="", danh_gia="", maps="",
                dich_vu=["Sơn gel", "Đắp gel, nối móng", "Nail art", "Chà gót, chăm sóc chân"], ghi_chu="Trang mẫu: tên, địa chỉ, số điện thoại là ví dụ.", cam_ket=True),
    "nail-districts": dict(ten="Nail Districts & Spa", khau_hieu="1.113 khách chấm 5 sao giữa lòng Quận 1",
                           dia_chi=["Lầu 1, 158/4 Nguyễn Công Trứ, Bến Thành, Quận 1", "269/1 Nguyễn Trãi, Cầu Ông Lãnh, Quận 1"],
                           gio="10:00–20:00 mỗi ngày", zalo="0333 947 341", sao="5,0", danh_gia="1.113",
                           maps="https://maps.google.com/?cid=", dich_vu=["Nail", "Gội đầu dưỡng sinh", "Nối mi", "Massage"],
                           ghi_chu="Bản demo Nailmark dựng riêng cho tiệm, chưa phải trang chính thức."),
    # Đợt 1 TP.HCM (25/11/2026). Số liệu lấy từ Google Places. Giờ mở cửa ELIZ và Charming lấy từ Places; các tiệm khác chưa có.
    "eliz": dict(ten="ELIZ Nail Beauty", khau_hieu="2.374 khách chấm 4,9 sao, tiệm được đánh giá nhiều nhất trong danh sách của Nailmark",
                 dia_chi=["47b Hẻm 69 Nguyễn Gia Trí, Thạnh Mỹ Tây (Bình Thạnh cũ)"], gio="09:30–20:30 mỗi ngày",
                 zalo="0388 767 096", sao="4,9", danh_gia="2.374", maps="https://maps.google.com/?cid=4031066148165843456",
                 dich_vu=["Sơn gel", "Nail art", "Đắp gel, nối móng", "Chăm sóc tay chân"],
                 ghi_chu="Bản demo Nailmark dựng riêng cho tiệm, chưa phải trang chính thức."),
    "salin": dict(ten="Salin Beauty", khau_hieu="Hai cơ sở, 3.178 đánh giá, cả hai đều 5,0 sao",
                  dia_chi=["06 Lam Sơn, Gia Định (Bình Thạnh cũ)", "305 Huỳnh Văn Bánh, Phú Nhuận"], gio="Giờ mở cửa: tiệm bổ sung",
                  zalo="0367 296 783", sao="5,0", danh_gia="3.178", maps="https://maps.google.com/?cid=1847432760038863650",
                  dich_vu=["Sơn gel", "Nail art", "Đắp gel, nối móng", "Học viện nail"],
                  ghi_chu="Bản demo Nailmark dựng riêng cho tiệm, chưa phải trang chính thức."),
    "quyt": dict(ten="Quýt Nail", khau_hieu="Hai cơ sở Gò Vấp và Phú Nhuận, 2.105 đánh giá 4,9 sao",
                 dia_chi=["255 Quang Trung, Gò Vấp · Zalo 0932 066 116", "214 Lê Văn Sỹ, Phú Nhuận · Zalo 0773 895 566"],
                 gio="Giờ mở cửa: tiệm bổ sung", zalo="0932 066 116", sao="4,9", danh_gia="2.105",
                 maps="https://maps.google.com/?cid=9100402491226512413",
                 dich_vu=["Vẽ nail art", "Sơn gel", "Đắp gel, nối móng", "Chăm sóc tay chân"],
                 ghi_chu="Bản demo Nailmark dựng riêng cho tiệm, chưa phải trang chính thức."),
    "charming": dict(ten="Charming Nail Studio", khau_hieu="1.025 khách chấm 5,0 sao tại Bình Thạnh",
                     dia_chi=["30 Mai Xuân Thưởng, Bình Lợi Trung (Bình Thạnh cũ)"], gio="09:00–21:00 mỗi ngày",
                     zalo="0867 546 247", sao="5,0", danh_gia="1.025", maps="https://maps.google.com/?cid=17816716868794614151",
                     dich_vu=["Sơn gel", "Nail art", "Đắp gel, nối móng", "Chăm sóc tay chân"],
                     ghi_chu="Bản demo Nailmark dựng riêng cho tiệm, chưa phải trang chính thức."),
}
DIP = [("tet", "Tết"), ("cuoi-nam", "Tiệc cuối năm"), ("thang-chuc", "Thăng chức"), ("sinh-nhat", "Sinh nhật"),
       ("cuoi", "Mùa cưới"), ("valentine", "Valentine"), ("8-3", "8/3"), ("20-10", "20/10")]
CAM_KET = """<section class=band><div class=in><h2>Cam kết <em>của tiệm</em></h2><div class=grid3>
<div class=box><b>Giá trọn gói</b>Đã gồm tháo gel cũ, không phát sinh.</div><div class=box><b>Vệ sinh thấy được</b>Dụng cụ hấp tiệt trùng, khui trước mặt chị.</div><div class=box><b>Bảo hành 10 ngày</b>Bong, hở gel: tiệm sửa miễn phí.</div></div>
<ul style="margin-top:18px">{dv}</ul></div></section>"""
LOOK = ["s1", "m0", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "s3", "s4"]


def tao(slug):
    """slug là khoá trong TIEM, hoặc truyền thẳng một dict cùng cấu trúc (dùng cho scripts/tu_dong_demo.py)."""
    t = slug if isinstance(slug, dict) else TIEM[slug]
    dv = "".join(f"<li>{e(x)}</li>" for x in t["dich_vu"])
    dc = "".join(f"<p><b>Cơ sở {i}</b><br>{e(x)}</p>" for i, x in enumerate(t["dia_chi"], 1))
    bst = "".join(f'<figure><img src="img/bst-{k}.jpg" alt="Bộ móng {e(n)}" loading=lazy width=720 height=900><figcaption>{e(n)}</figcaption></figure>' for k, n in DIP)
    # Phiên bản 2: dùng ảnh thật của tiệm nếu có (t["anh"] = danh sách đường dẫn tương đối), không thì ảnh mẫu
    anh = t.get("anh") or [f"img/{k}.jpg" for k in LOOK]
    lb = "".join(f'<figure><img src="{e(k)}" alt="Mẫu số {i}" loading=lazy><figcaption><b>{i:02d}</b></figcaption></figure>' for i, k in enumerate(anh, 1))
    hero = t.get("hero") or (anh[0] if t.get("anh") else "img/hero.jpg")
    opts = "".join(f"<option>Mẫu {i:02d}</option>" for i in range(1, 13))
    # Bảng giá thật của tiệm nếu có (t["gia"] = [(tên dịch vụ, giá)]), không thì 3 mức mẫu
    if t.get("gia"):
        bang_gia = ('<h2 style="margin-top:36px">Bảng giá <em>trọn gói</em></h2><div class=box><table class=gia>' +
                    "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in t["gia"]) + "</table></div>")
    else:
        bang_gia = ('<div class=grid3 style="margin-top:16px"><div class=box><b>Đơn giản</b>45 phút · giá của tiệm</div>'
                    '<div class=box><b>Vừa</b>60 phút · giá của tiệm</div><div class=box><b>Cầu kỳ</b>90 phút · giá của tiệm</div></div>')
    # Mục "Cam kết" CHỈ hiện khi tiệm đã xác nhận (t["cam_ket"] is True). Nailmark không hứa thay tiệm.
    dv_html = dv
    cam_ket = CAM_KET.replace("{dv}", dv_html) if t.get("cam_ket") is True else ""
    rv = (f'<div class=rv><b>{e(t["sao"])}★</b><span>{e(t["danh_gia"])} đánh giá Google</span></div>' if t["sao"] else
          '<div class=rv><b>★</b><span>Số sao và đánh giá Google của tiệm hiển thị ở đây</span></div>')
    return f"""<title>{e(t['ten'])}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Display:ital,wght@0,700;1,600&family=Be+Vietnam+Pro:wght@400;600;700&display=swap">
<style>
/* Mẫu website tiệm chuẩn Nailmark: hero vòm ảnh, bộ sưu tập theo dịp, lookbook đánh số, bảng giá, cam kết, đặt lịch qua Zalo */
:root{{color-scheme:light dark;--son:#a3161a;--son2:#7d0f13;--den:#17100e;--vang:#c9a14a;--vang2:#e9c977;--trung:#f5eee3;--bg:light-dark(#fbf7f1,#120c0b);--card:light-dark(#fff,#1d1513);--ink:light-dark(#1c1210,#f3eadf);--mut:light-dark(#6f6259,#bcae9f);--line:light-dark(#e8dccd,#3a2c26);--accent:light-dark(#a3161a,#ff6b5e)}}
:root[data-theme=light]{{color-scheme:light}}:root[data-theme=dark]{{color-scheme:dark}}
*{{box-sizing:border-box;min-width:0}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Be Vietnam Pro",system-ui,sans-serif;overflow-x:clip}}img{{display:block;max-width:100%}}
.band{{padding-block:clamp(40px,6vw,84px);padding-left:max(5vw,16px,env(safe-area-inset-left,0px));padding-right:max(5vw,16px,env(safe-area-inset-right,0px))}}.in{{max-width:1180px;margin:0 auto}}
h1,h2{{font-family:"Noto Serif Display",serif;font-weight:700;margin:0;letter-spacing:-.015em}}h1{{font-size:clamp(38px,5.4vw,66px);line-height:1.04}}h2{{font-size:clamp(28px,3.6vw,44px);line-height:1.1;margin-bottom:22px}}h2 em{{font-style:italic;font-weight:600}}
.nav{{position:sticky;top:0;z-index:9;background:rgba(23,16,14,.88);backdrop-filter:blur(8px);color:var(--trung);padding:12px max(5vw,16px);padding-top:calc(env(safe-area-inset-top,0px) + 12px);display:flex;justify-content:space-between;align-items:center;gap:12px}}
.nav b{{font-family:"Noto Serif Display",serif;font-size:21px}}.cta{{background:var(--vang);color:var(--den);border-radius:999px;padding:9px 18px;font-weight:700;text-decoration:none;white-space:nowrap}}
.hero{{background:radial-gradient(110% 90% at 80% 30%,#c4231f,var(--son) 45%,var(--son2));color:var(--trung)}}
.hero .in{{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:36px;align-items:center}}
.hero p{{font-size:19px;color:#f7e6d6;max-width:40ch}}
.arch{{aspect-ratio:4/5;border-radius:999px 999px 26px 26px;overflow:hidden;border:5px solid var(--vang);box-shadow:0 30px 60px rgba(40,0,0,.4);max-width:420px;justify-self:center;width:100%}}.arch img{{width:100%;height:100%;object-fit:cover}}
.rv{{display:inline-flex;gap:12px;align-items:baseline;border:1.5px solid rgba(233,201,119,.6);border-radius:999px;padding:8px 18px;margin:6px 0 20px}}.rv b{{font-family:"Noto Serif Display",serif;font-size:26px;color:var(--vang2)}}
.btn{{display:inline-block;background:var(--vang);color:var(--den);border-radius:999px;padding:14px 26px;font-weight:700;text-decoration:none;margin-right:10px}}.btn.g{{background:transparent;color:var(--trung);border:1.5px solid rgba(245,238,227,.6)}}
.rail{{display:grid;grid-auto-flow:column;grid-auto-columns:clamp(200px,22vw,260px);gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px}}
.rail figure{{margin:0;scroll-snap-align:start;position:relative;border-radius:18px;overflow:hidden}}.rail img{{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover}}
.rail figcaption{{position:absolute;left:12px;top:12px;background:var(--vang);color:var(--den);font-weight:700;font-size:13px;border-radius:999px;padding:4px 12px}}
.lb{{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px}}.lb figure{{margin:0;position:relative;border-radius:999px 999px 12px 12px;overflow:hidden;aspect-ratio:3/4}}.lb img{{width:100%;height:100%;object-fit:cover}}
.lb figcaption{{position:absolute;left:10px;bottom:8px;font-family:"Noto Serif Display",serif;color:var(--vang2);font-size:20px;text-shadow:0 2px 8px rgba(0,0,0,.6)}}
.gia{{width:100%;border-collapse:collapse}}.gia td{{padding:10px 4px;border-bottom:1px solid var(--line)}}.gia tr:last-child td{{border-bottom:0}}.gia td:last-child{{text-align:right;font-weight:700;color:var(--accent);white-space:nowrap}}
.tint{{background:light-dark(#f3e9dc,#18100e)}}
.grid3{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}}.box{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px}}.box b{{display:block;font-family:"Noto Serif Display",serif;font-size:22px;color:var(--accent)}}
.book{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:36px;align-items:start}}
form{{display:grid;gap:12px}}label{{font-size:14px;font-weight:600}}select,input{{font:inherit;font-size:16px;padding:12px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--ink);width:100%}}
form button{{font:inherit;font-weight:700;background:var(--son);color:#fff;border:0;border-radius:999px;padding:14px;cursor:pointer}}
.msg{{background:var(--card);border:1px dashed var(--vang);border-radius:14px;padding:14px;font-size:15px}}
footer{{background:var(--den);color:#bcae9f;font-size:13px;text-align:center}}footer b{{color:var(--trung)}}
.note{{background:var(--vang2);color:var(--den);text-align:center;font-size:13px;padding:6px 16px}}
@media(max-width:860px){{.hero .in,.book{{grid-template-columns:1fr}}.lb{{grid-template-columns:repeat(3,minmax(0,1fr))}}.grid3{{grid-template-columns:1fr}}.arch{{max-width:320px}}}}
</style>
<div class=note>{e(t['ghi_chu'])}</div>
<header class=nav><b>{e(t['ten'])}</b><a class=cta href="#dat-lich">Đặt lịch</a></header>
<section class="band hero"><div class=in>
<div><h1>{e(t['ten'])}</h1><p>{e(t['khau_hieu'])}</p>{rv}<br><a class=btn href="#dat-lich">Chọn mẫu và đặt lịch</a><a class="btn g" href="#bo-suu-tap">Bộ sưu tập</a></div>
<div class=arch><img src="{e(hero)}" alt="Bàn tay sơn gel đỏ" width=900 height=1125></div></div></section>
<section class=band id=bo-suu-tap><div class=in><h2>Bộ sưu tập <em>theo dịp</em></h2><div class=rail>{bst}</div></div></section>
<section class="band tint"><div class=in><h2>Lookbook <em>đánh số</em></h2><div class=lb>{lb}</div>
{bang_gia}</div></section>
{cam_ket}
<section class="band tint" id=dat-lich><div class="in book">
<div><h2>Đặt lịch <em>trong 30 giây</em></h2>{dc}<p>{e(t['gio'])} · Zalo {e(t['zalo'])}</p></div>
<form id=f><label for=mau>Mẫu</label><select id=mau>{opts}</select><label for=ngay>Ngày</label><input id=ngay type=date><label for=gio>Giờ</label><select id=gio><option>10:00</option><option>13:00</option><option>15:00</option><option>17:00</option><option>19:00</option></select><button type=submit>Tạo tin đặt lịch</button><div class=msg id=msg hidden></div></form>
</div></section>
<footer class=band><b>{e(t['ten'])}</b> · Trang theo bộ tiêu chuẩn Nailmark · {e(t.get('nguon_anh', 'Ảnh minh hoạ: Pexels'))}</footer>
<script>{{const f=document.getElementById("f"),m=document.getElementById("msg");f.addEventListener("submit",ev=>{{ev.preventDefault();const t=`Chào tiệm, em muốn đặt ${{document.getElementById("mau").value}} ngày ${{document.getElementById("ngay").value||"(chọn ngày)"}} lúc ${{document.getElementById("gio").value}}.`;m.hidden=false;m.textContent="Gửi tin này qua Zalo {e(t['zalo'])}: "+t;}});}}</script>
"""


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "mau"
    out = ROOT / "nailmark" / f"tiem-{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(tao(slug), encoding="utf-8")
    print("Đã tạo", out.relative_to(ROOT))
