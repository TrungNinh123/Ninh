"""Nailmark – sản phẩm 99.000đ "Bộ Tết mang tên tiệm": giao NGAY sau khi thanh toán, tự động 100%.

Giá trị (so với quà miễn phí chỉ có 1 poster + 1 thẻ QR + 1 video):
  - 3 poster đăng Facebook/Zalo (1080x1350) · 3 story Facebook/Zalo/TikTok (1080x1920)
  - 2 thẻ quà tặng Tết (300.000đ, 500.000đ) để tiệm bán cho khách tặng nhau
  - 1 bảng giá Tết in quầy (A5) · 1 thẻ QR đặt lịch in quầy (A6)
  - 10 câu đăng bài soạn sẵn (copy dán là dùng) + lịch đăng 4 tuần trước Tết
  - Mã KHAUTRU99: trừ 99.000đ khi lên gói web (Khởi đầu, Chuẩn, Đẳng cấp)
Ảnh: dùng ảnh tiệm gửi (nếu có) hoặc ảnh minh hoạ Nailmark (ghi rõ trên ảnh).
Chạy: python scripts/bo_99k.py --ten "Sơn Mài Nail" --zalo 0900000000 [--gia bang_gia.txt] [--anh anh1.jpg ...]
Kết quả: nailmark/bo99/<slug>/ (index.html + ảnh + bo-tet.zip)
"""
import argparse
import re
import shutil
import sys
import zipfile
from html import escape as e
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qua_tang import FONT, chup, qr_svg  # noqa: E402
from scan_vn import khong_dau  # noqa: E402
from tao_web import doc_gia_chu  # noqa: E402
from web_tiem import ROOT  # noqa: E402

TET = "Thứ Bảy 6/2/2027"
TIEU_DE = [("BỘ SƯU TẬP TẾT 2027", "Móng đỏ son đón năm mới", "Đặt lịch sớm, không phải chờ"),
           ("ĐẶT LỊCH TRƯỚC TẾT", "Còn ít khung giờ đẹp", "Nhắn Zalo giữ chỗ ngay hôm nay"),
           ("QUÀ TẾT CHO NÀNG", "Thẻ quà tặng làm móng", "Tặng mẹ, tặng chị, tặng bạn thân")]
CAP = [
    "Tết này diện móng đỏ son 💅 Bộ sưu tập Tết 2027 đã có tại {ten}. Nhắn Zalo {zalo} để giữ lịch sớm, không phải chờ.",
    "Cận Tết tiệm rất đông. Chị em đặt lịch trước để có khung giờ đẹp nhé! Zalo {zalo}.",
    "Móng đẹp đón Tết không cần chờ: chọn mẫu theo số trên web, nhắn Zalo {zalo} là xong.",
    "Thẻ quà tặng làm móng: món quà Tết tinh tế cho mẹ, chị, bạn thân. Hỏi {ten} qua Zalo {zalo}.",
    "Giá rõ ràng, không phát sinh. Xem bảng giá Tết của {ten} trong ảnh nhé!",
    "Đỏ son, vàng ánh kim, nhũ nhẹ: 3 tông móng được chọn nhiều nhất mùa Tết. Chị thích tông nào?",
    "Tiệm mở cửa xuyên Tết theo lịch đã thông báo. Đặt trước để tiệm sắp xếp thợ cho chị nhé. Zalo {zalo}.",
    "Đi làm cả năm vất vả, Tết này tự thưởng một bộ móng thật xinh. {ten} chờ chị!",
    "Dụng cụ sạch, mở túi trước mặt khách: chị yên tâm làm đẹp ngày Tết tại {ten}.",
    "Còn vài ngày nữa là Tết. Khung giờ đẹp sắp kín, nhắn Zalo {zalo} ngay để giữ chỗ!"]
LICH = ["4 tuần trước Tết: câu 1, 2 + poster 1", "3 tuần trước: câu 3, 4 + thẻ quà tặng", "2 tuần trước: câu 5, 6 + bảng giá Tết",
        "1 tuần trước: câu 7, 8 + story 2", "3 ngày trước: câu 9, 10 + story 1"]


def nen(img):
    return f"background:#7d0f13 url({img}) center/cover"


def poster(t, so, i, w, h, img):
    k, a, b = TIEU_DE[i]
    s = min(w / 1080, h / 1350)
    return f"""<!doctype html><meta charset=utf-8>{FONT}<style>
*{{box-sizing:border-box}}body{{margin:0;width:{w}px;height:{h}px;{nen(img)};font-family:"Be Vietnam Pro";color:#f5eee3;overflow:hidden;position:relative}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(23,16,14,.1),rgba(125,15,19,.55) 42%,#7d0f13 76%)}}
.in{{position:absolute;left:{80*s:.0f}px;right:{80*s:.0f}px;bottom:{80*s:.0f}px}}.k{{font-size:{30*s:.0f}px;letter-spacing:.2em;color:#e9c977;font-weight:700}}
h1{{font-family:"Noto Serif Display";font-size:{100*s:.0f}px;line-height:1;margin:{16*s:.0f}px 0 {10*s:.0f}px}}h2{{font-family:"Noto Serif Display";font-style:italic;font-weight:600;font-size:{54*s:.0f}px;margin:0 0 {26*s:.0f}px;color:#e9c977}}
.row{{display:flex;justify-content:space-between;align-items:flex-end;gap:30px}}.cta{{font-size:{34*s:.0f}px;font-weight:700}}.sub{{font-size:{27*s:.0f}px;margin-top:8px;color:#f7e6d6}}
.qr{{background:#fff;border-radius:22px;padding:12px;width:{230*s:.0f}px}}.qr svg{{width:100%;height:auto;display:block}}.ft{{position:absolute;top:{40*s:.0f}px;left:{80*s:.0f}px;font-size:{20*s:.0f}px;opacity:.85}}
</style><div class=sh></div><div class=ft>{e(t['nguon_anh'])}</div>
<div class=in><div class=k>{k}</div><h1>{e(t['ten'])}</h1><h2>{a}</h2>
<div class=row><div><div class=cta>{b}</div><div class=sub>Zalo {so[:4]} {so[4:7]} {so[7:]}</div></div><div class=qr>{qr_svg(so)}</div></div></div>"""


def the_qua(t, so, menh_gia):
    return f"""<!doctype html><meta charset=utf-8>{FONT}<style>
*{{box-sizing:border-box}}body{{margin:0;width:1500px;height:900px;background:#17100e;font-family:"Be Vietnam Pro";color:#f5eee3;display:flex;align-items:center;justify-content:center}}
.c{{width:1400px;height:800px;border-radius:48px;background:linear-gradient(135deg,#a3161a,#5c0b0e);border:6px solid #c9a14a;position:relative;padding:80px;overflow:hidden}}
.c:after{{content:"";position:absolute;right:-120px;top:-120px;width:520px;height:520px;border-radius:50%;border:40px solid rgba(233,201,119,.18)}}
.k{{font-size:34px;letter-spacing:.25em;color:#e9c977;font-weight:700}}h1{{font-family:"Noto Serif Display";font-size:110px;margin:20px 0 0}}
.v{{font-family:"Noto Serif Display";font-size:150px;color:#e9c977;line-height:1;margin-top:30px}}.f{{position:absolute;left:80px;right:80px;bottom:70px;display:flex;justify-content:space-between;font-size:30px}}
</style><div class=c><div class=k>THẺ QUÀ TẶNG TẾT 2027</div><h1>{e(t['ten'])}</h1><div class=v>{menh_gia}</div>
<div class=f><span>Tặng: ……………………</span><span>Zalo {so[:4]} {so[4:7]} {so[7:]}</span></div></div>"""


def bang_gia(t, so, gia):
    rows = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in gia[:12])
    return f"""<!doctype html><meta charset=utf-8>{FONT}<style>
*{{box-sizing:border-box}}body{{margin:0;width:1748px;height:2480px;background:#17100e;font-family:"Be Vietnam Pro";color:#f5eee3;padding:110px}}
.c{{border:5px solid #c9a14a;border-radius:60px;height:100%;padding:120px 130px;display:flex;flex-direction:column}}
.k{{text-align:center;color:#e9c977;font-weight:700;letter-spacing:.2em;font-size:44px}}h1{{text-align:center;font-family:"Noto Serif Display";font-size:140px;margin:20px 0 70px}}
table{{width:100%;border-collapse:collapse;font-size:76px;margin:auto 0}}td{{padding:44px 0;border-bottom:2px solid rgba(233,201,119,.25)}}td:last-child{{text-align:right;color:#e9c977;font-weight:700}}
.f{{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:40px}}.qr{{background:#fff;border-radius:24px;padding:16px;width:300px}}.qr svg{{width:100%;height:auto;display:block}}
</style><div class=c><div class=k>BẢNG GIÁ TẾT 2027 · KHÔNG PHÁT SINH</div><h1>{e(t['ten'])}</h1><table>{rows}</table>
<div class=f><div>Đặt lịch trước Tết<br><b>Zalo {so[:4]} {so[4:7]} {so[7:]}</b></div><div class=qr>{qr_svg(so)}</div></div></div>"""


def trang(t, so):
    caps = "".join(f"<li>{e(c.format(ten=t['ten'], zalo=f'{so[:4]} {so[4:7]} {so[7:]}'))}</li>" for c in CAP)
    lich = "".join(f"<li>{e(x)}</li>" for x in LICH)
    fig = lambda f, cap: f'<figure><img src="{f}" alt="{e(cap)}" loading=lazy><figcaption>{e(cap)}</figcaption></figure>'
    return f"""<!doctype html><html lang=vi><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Bộ Tết của {e(t['ten'])}</title>{FONT}
<style>:root{{color-scheme:light dark;--bg:light-dark(#f5eee3,#120c0b);--ink:light-dark(#17100e,#f3eadf);--card:light-dark(#fff,#1d1513);--line:light-dark(#e3d5c3,#3a2c26);--acc:light-dark(#a3161a,#ff6b5e)}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Be Vietnam Pro",system-ui}}.w{{max-width:980px;margin:0 auto;padding:28px 16px 60px}}
.ok{{background:#17100e;color:#f5eee3;border-radius:22px;padding:24px}}.ok h1{{font-family:"Noto Serif Display";font-size:clamp(30px,6vw,44px);margin:6px 0}}.ok b{{color:#e9c977}}
h2{{font-family:"Noto Serif Display";margin:34px 0 12px}}.g{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.g2{{grid-template-columns:repeat(2,minmax(0,1fr))}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:10px}}figure img{{width:100%;height:auto;border-radius:10px;display:block}}figcaption{{font-size:13px;margin-top:6px}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px}}ol li,ul li{{margin:6px 0}}a{{color:var(--acc)}}.dl{{display:inline-block;background:#a3161a;color:#fff;border-radius:999px;padding:12px 20px;font-weight:700;text-decoration:none}}
.code{{font-family:monospace;font-size:20px;background:#e9c977;color:#17100e;border-radius:8px;padding:2px 10px}}@media(max-width:700px){{.g{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}</style>
<div class=w><div class=ok><div style="color:#e9c977;font-weight:700;letter-spacing:.1em;font-size:13px">ĐÃ THANH TOÁN · CẢM ƠN CHỊ</div>
<h1>Bộ Tết của {e(t['ten'])} đã sẵn sàng</h1><p>Nailmark cảm ơn chị đã tin tưởng. Toàn bộ <b>10 ảnh và 10 câu đăng bài</b> bên dưới là của tiệm, dùng ngay, không cần làm gì thêm.</p>
<a class=dl href="bo-tet.zip">Tải trọn bộ (.zip)</a></div>
<h2>1. Đăng bài và story</h2><div class=g>{fig("poster-1.png","Poster 1 · Bộ sưu tập Tết")}{fig("poster-2.png","Poster 2 · Đặt lịch trước Tết")}{fig("poster-3.png","Poster 3 · Quà Tết cho nàng")}
{fig("story-1.png","Story 1")}{fig("story-2.png","Story 2")}{fig("story-3.png","Story 3")}</div>
<h2>2. In ở quầy</h2><div class="g g2">{fig("bang-gia-tet.png","Bảng giá Tết · in A5")}{fig("the-qr.png","Thẻ QR đặt lịch · in A6")}</div>
<h2>3. Bán thẻ quà tặng</h2><div class="g g2">{fig("the-qua-300.png","Thẻ quà tặng 300.000đ")}{fig("the-qua-500.png","Thẻ quà tặng 500.000đ")}</div>
<h2>4. 10 câu đăng bài (chép là dùng)</h2><div class=box><ol>{caps}</ol></div>
<h2>5. Lịch đăng 4 tuần trước Tết ({TET})</h2><div class=box><ul>{lich}</ul></div>
<h2>Bước tiếp theo (nếu chị muốn)</h2><div class=box><p>Có web đặt lịch riêng để khách chọn mẫu và nhắn Zalo: gói Khởi đầu <b>999.000đ</b>. Nhập mã <span class=code>KHAUTRU99</span> để <b>trừ 99.000đ đã trả</b>, chỉ còn 900.000đ.</p>
<p><b>Giới thiệu tiệm bạn, chị nhận hoa hồng:</b> 15% với đơn đến 5 triệu, 20% với đơn trên 5 triệu. Tiệm bạn dùng link của chị được giảm 5%. Hoa hồng tự chuyển vào tài khoản của chị sau 7 ngày. Link của chị nằm ở trang cảm ơn sau khi thanh toán. Lần sau chị mua thêm gói nào cũng được giảm 10% vì là khách quen.</p></div></div></html>"""


def tao(t, so, gia, anh_tiem=None):
    slug = re.sub(r"[^a-z0-9]+", "-", khong_dau(t["ten"])).strip("-")[:40] or "tiem"
    out = ROOT / "nailmark" / "bo99" / slug
    out.mkdir(parents=True, exist_ok=True)
    tmp = out / "_tmp"; tmp.mkdir(exist_ok=True)
    nguon = [Path(a) for a in (anh_tiem or [])][:3]
    t = dict(t, nguon_anh="Ảnh của tiệm" if nguon else "Ảnh minh hoạ · quà tặng của Nailmark")
    anh = []
    for i in range(3):
        src = nguon[i % len(nguon)] if nguon else ROOT / "nailmark" / "img" / ["bst-tet.jpg", "bst-cuoi-nam.jpg", "bst-tet.jpg"][i]
        dst = tmp / f"nen-{i}{src.suffix}"; shutil.copy(src, dst); anh.append(dst.name)
    viec = []
    for i in range(3):
        (tmp / f"p{i}.html").write_text(poster(t, so, i, 1080, 1350, anh[i]), encoding="utf-8")
        (tmp / f"s{i}.html").write_text(poster(t, so, i, 1080, 1920, anh[i]), encoding="utf-8")
        viec += [[str(tmp / f"p{i}.html"), str(out / f"poster-{i+1}.png"), 1080, 1350], [str(tmp / f"s{i}.html"), str(out / f"story-{i+1}.png"), 1080, 1920]]
    for mg in (300, 500):
        (tmp / f"q{mg}.html").write_text(the_qua(t, so, f"{mg}.000đ"), encoding="utf-8")
        viec.append([str(tmp / f"q{mg}.html"), str(out / f"the-qua-{mg}.png"), 1500, 900])
    (tmp / "bg.html").write_text(bang_gia(t, so, gia), encoding="utf-8")
    viec.append([str(tmp / "bg.html"), str(out / "bang-gia-tet.png"), 1748, 2480])
    from qua_tang import the_qr
    (tmp / "qr.html").write_text(the_qr(t, so), encoding="utf-8")
    viec.append([str(tmp / "qr.html"), str(out / "the-qr.png"), 1240, 1748])
    chup(dict(tmp=str(tmp), anh=viec, video=None))
    shutil.rmtree(tmp, ignore_errors=True)
    (out / "index.html").write_text(trang(t, so), encoding="utf-8")
    caps = "\n".join(f"{i+1}. " + c.format(ten=t["ten"], zalo=f"{so[:4]} {so[4:7]} {so[7:]}") for i, c in enumerate(CAP))
    with zipfile.ZipFile(out / "bo-tet.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(out.glob("*.png")):
            z.write(f, f.name)
        z.writestr("10-cau-dang-bai.txt", caps + "\n\nLịch đăng:\n" + "\n".join(LICH))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ten", required=True); ap.add_argument("--zalo", required=True)
    ap.add_argument("--gia"); ap.add_argument("--anh", nargs="*")
    g = ap.parse_args()
    so = re.sub(r"\D", "", g.zalo)
    gia = doc_gia_chu(Path(g.gia).read_text(encoding="utf-8"))[0] if g.gia else [
        ("Sơn gel trơn", "150.000đ"), ("Sơn gel + vẽ Tết", "190.000đ"), ("Đắp gel, nối móng", "350.000đ"), ("Chăm sóc chân", "120.000đ")]
    out = tao(dict(ten=g.ten), so, gia, g.anh)
    print("Đã tạo", out.relative_to(ROOT), "·", len(list(out.glob("*.png"))), "ảnh · zip", (out / "bo-tet.zip").stat().st_size // 1024, "KB")
