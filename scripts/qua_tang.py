"""Nailmark – GÓI QUÀ MIỄN PHÍ cho từng tiệm: cho giá trị trước, không cần tiệm hỏi hay trả tiền.

Tạo trong nailmark/qua/<slug>/:
  1. web-mau/index.html  – web đặt lịch mẫu mang tên tiệm (dữ liệu Google Maps)
  2. poster-tet.png      – poster Tết 2027 1080x1350 mang tên tiệm + QR Zalo (đăng Facebook/Zalo được ngay)
  3. qr-quay.png         – thẻ QR in để ở quầy (A6, 1240x1748) mang tên tiệm
  4. video-web.mp4       – video 12 giây lướt web mẫu trên điện thoại (đăng TikTok/Reels được)
  5. index.html          – trang mở quà: xem, tải về, và "bước tiếp theo" (không cần hỏi ai)
Ảnh móng trong quà là ẢNH MINH HOẠ (Pexels) cho tới khi tiệm gửi ảnh thật – ghi rõ trên quà.

Chạy: python scripts/qua_tang.py --maps "Tên tiệm + quận"     (1 lượt Google Places)
      python scripts/qua_tang.py --ten "Sơn Mài Nail" --zalo 0900000000 [--sao 4,9 --danh-gia 1.250]
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from html import escape as e
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_vn import khong_dau  # noqa: E402
from web_tiem import ROOT, DIP, tao  # noqa: E402

FONT = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Display:ital,wght@0,700;1,600'
        '&family=Be+Vietnam+Pro:wght@400;600;700&display=swap">')
ANH_TET = ROOT / "nailmark" / "img" / "bst-tet.jpg"


def qr_svg(so):
    import segno
    return segno.make(f"https://zalo.me/{so}", error="m").svg_inline(scale=8, border=1, dark="#17100e", omitsize=True)


def poster(t, so):
    sao = f'<div class=rv>{e(t["sao"])}★ · {e(t["danh_gia"])} đánh giá Google</div>' if t.get("sao") else ""
    return f"""<!doctype html><meta charset=utf-8>{FONT}<style>
*{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1350px;background:#7d0f13;font-family:"Be Vietnam Pro";color:#f5eee3;overflow:hidden}}
.bg{{position:absolute;inset:0;background:url(anh-tet.jpg) center/cover}}.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(23,16,14,.15),rgba(125,15,19,.55) 45%,#7d0f13 78%)}}
.in{{position:absolute;left:80px;right:80px;bottom:80px}}.k{{font-size:30px;letter-spacing:.2em;color:#e9c977;font-weight:700}}
h1{{font-family:"Noto Serif Display";font-size:104px;line-height:1;margin:18px 0 10px}}h2{{font-family:"Noto Serif Display";font-style:italic;font-weight:600;font-size:56px;margin:0 0 28px;color:#e9c977}}
.row{{display:flex;justify-content:space-between;align-items:flex-end;gap:30px}}.cta{{font-size:34px;font-weight:700}}.rv{{font-size:28px;margin-top:10px;color:#f7e6d6}}
.qr{{background:#fff;border-radius:22px;padding:14px;width:230px}}.qr svg{{width:100%;height:auto;display:block}}.ft{{position:absolute;top:40px;left:80px;font-size:20px;opacity:.85}}
</style><div class=bg></div><div class=sh></div><div class=ft>Ảnh minh hoạ · bản tặng của Nailmark</div>
<div class=in><div class=k>BỘ SƯU TẬP TẾT 2027</div><h1>{e(t['ten'])}</h1><h2>Móng đỏ son đón năm mới</h2>
<div class=row><div><div class=cta>Đặt lịch sớm, không phải chờ</div>{sao}<div class=rv>Quét mã để nhắn Zalo đặt lịch</div></div><div class=qr>{qr_svg(so)}</div></div></div>"""


def the_qr(t, so):
    dc = e((t.get("dia_chi") or [""])[0])
    return f"""<!doctype html><meta charset=utf-8>{FONT}<style>
*{{box-sizing:border-box}}body{{margin:0;width:1240px;height:1748px;background:#f5eee3;font-family:"Be Vietnam Pro";color:#17100e;display:flex;align-items:center;justify-content:center}}
.c{{width:1100px;height:1608px;border:6px solid #c9a14a;border-radius:60px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:80px;background:#fff}}
h1{{font-family:"Noto Serif Display";font-size:96px;line-height:1.05;margin:0 0 20px;color:#a3161a}}p{{font-size:44px;margin:10px 0}}.qr{{width:720px;margin:40px auto}}.qr svg{{width:100%;height:auto;display:block}}
.s{{font-size:30px;color:#6f6259}}</style><div class=c><p style="font-weight:700;letter-spacing:.15em;color:#c9a14a">QUÉT ĐỂ ĐẶT LỊCH</p><h1>{e(t['ten'])}</h1>
<div class=qr>{qr_svg(so)}</div><p><b>Zalo {so[:4]} {so[4:7]} {so[7:]}</b></p><p class=s>{dc}</p></div>"""


def trang_qua(t, co_video):
    vid = ('<figure><video src="video-web.mp4" controls playsinline muted loop></video><figcaption>Video 12 giây lướt web '
           '(đăng TikTok, Reels) · <a href="video-web.mp4" target=_blank rel=noopener>Mở file gốc</a></figcaption></figure>') if co_video else ""
    return f"""<!doctype html><html lang=vi><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Quà tặng cho {e(t['ten'])}</title>{FONT}
<style>:root{{color-scheme:light dark;--bg:light-dark(#fbf7f1,#120c0b);--ink:light-dark(#1c1210,#f3eadf);--card:light-dark(#fff,#1d1513);--line:light-dark(#e8dccd,#3a2c26);--acc:light-dark(#a3161a,#ff6b5e)}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 "Be Vietnam Pro",system-ui}}.w{{max-width:880px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-family:"Noto Serif Display";font-size:clamp(30px,6vw,46px);line-height:1.1;margin:8px 0}}h2{{font-family:"Noto Serif Display";margin:34px 0 12px}}.k{{color:#c9a14a;font-weight:700;letter-spacing:.12em;font-size:13px}}
.g{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:12px}}
figure img,figure video{{width:100%;height:auto;border-radius:12px;display:block}}figcaption{{font-size:14px;margin-top:8px}}a{{color:var(--acc)}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px}}ol li{{margin:6px 0}}@media(max-width:640px){{.g{{grid-template-columns:1fr}}}}</style>
<div class=w><div class=k>QUÀ TẶNG TỪ NAILMARK · MIỄN PHÍ, KHÔNG CẦN ĐĂNG KÝ</div><h1>Bộ quà cho {e(t['ten'])}</h1>
<p>Nailmark làm sẵn 4 món này cho tiệm. Chị dùng ngay, không mất phí, không cần trả lời lại. Ảnh móng trong quà là <b>ảnh minh hoạ</b>; khi chị dùng ảnh thật của tiệm, web và poster sẽ đẹp và đúng tay nghề hơn.</p>
<h2>1. Web đặt lịch mẫu mang tên tiệm</h2><div class=box><a href="web-mau/index.html" target=_blank rel=noopener><b>Mở web mẫu →</b></a> Thông tin lấy từ Google Maps công khai. Bản này chỉ gửi riêng cho chị, chưa đăng công khai.</div>
<h2>2. Đăng được ngay</h2><div class=g>
<figure><img src="poster-tet.png" alt="Poster Tết mang tên tiệm"><figcaption>Poster Tết 2027 (đăng Facebook, Zalo) · <a href="poster-tet.png" target=_blank rel=noopener>Mở file gốc</a></figcaption></figure>
<figure><img src="qr-quay.png" alt="Thẻ QR đặt lịch để ở quầy"><figcaption>Thẻ QR in để ở quầy (khổ A6), quét là mở Zalo của tiệm · <a href="qr-quay.png" target=_blank rel=noopener>Mở file gốc</a></figcaption></figure>
{vid}</div>
<h2>3. Bước tiếp theo (nếu chị muốn)</h2><div class=box><ol>
<li><b>Tự chấm điểm tiệm</b> theo 8 tiêu chuẩn của 17 chuỗi nail hàng đầu ở 9 quốc gia (miễn phí, 2 phút).</li>
<li><b>Muốn web thật với ảnh thật:</b> gói Khởi đầu 999.000đ, tự làm theo video 1–2 buổi. Bảng so sánh gói, phạm vi và 14 câu hỏi thường gặp có sẵn trên trang Nailmark.</li>
<li><b>Muốn có người làm toàn bộ:</b> gói Làm hộ trọn gói 9.990.000đ. Đơn từ 3 triệu, Nailmark gọi xác minh trước khi làm.</li></ol>
<p style="font-size:14px">Không dùng tiếp cũng không sao: quà vẫn là của chị. Muốn gỡ web mẫu, chị nhắn một chữ "gỡ".</p></div></div></html>"""


def chup(viec):
    """viec: list (html_path, png_path, w, h) + video spec, chạy bằng Playwright (Node)."""
    js = r"""
const {chromium}=require('playwright');const v=JSON.parse(process.argv[2]);(async()=>{const b=await chromium.launch();
for(const [h,p,w,ht] of v.anh){const pg=await b.newPage({viewport:{width:w,height:ht}});await pg.goto('file://'+h);await pg.waitForTimeout(900);await pg.screenshot({path:p});await pg.close();}
if(v.video){const ctx=await b.newContext({viewport:{width:390,height:844},recordVideo:{dir:v.video.dir,size:{width:390,height:844}}});const pg=await ctx.newPage();
await pg.goto('file://'+v.video.web);await pg.waitForTimeout(1200);const H=await pg.evaluate(()=>document.body.scrollHeight);
for(let i=0;i<110;i++){await pg.evaluate(y=>scrollTo(0,y),Math.min(H-844,i*(H-844)/100));await pg.waitForTimeout(90);}
await pg.waitForTimeout(500);await ctx.close();}
await b.close();})();"""
    f = Path(viec["tmp"]) / "chup.js"
    f.write_text(js)
    subprocess.run(["node", str(f), json.dumps(viec)], check=True, timeout=180)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--maps"); ap.add_argument("--ten"); ap.add_argument("--zalo"); ap.add_argument("--dia-chi", default="")
    ap.add_argument("--sao", default=""); ap.add_argument("--danh-gia", default="")
    g = ap.parse_args()
    if g.maps:
        from tu_dong_demo import cau_hinh, tim, truy_van
        t = cau_hinh(tim(truy_van(g.maps)))
    elif g.ten:
        t = dict(ten=g.ten, khau_hieu="Móng đẹp chuẩn Nailmark", dia_chi=[g.dia_chi], gio="Giờ mở cửa: tiệm bổ sung",
                 zalo=g.zalo or "", sao=g.sao, danh_gia=g.danh_gia, maps="", dich_vu=[],
                 ghi_chu="Bản demo Nailmark dựng riêng cho tiệm, chưa phải trang chính thức.")
    else:
        raise SystemExit("Cần --maps hoặc --ten.")
    so = re.sub(r"\D", "", g.zalo or t.get("zalo", ""))
    if len(so) != 10:
        raise SystemExit("Chưa có số Zalo 10 chữ số của tiệm (Google không có thì thêm --zalo).")
    slug = re.sub(r"[^a-z0-9]+", "-", khong_dau(t["ten"])).strip("-")[:40] or "tiem"
    out = ROOT / "nailmark" / "qua" / slug
    (out / "web-mau" / "img").mkdir(parents=True, exist_ok=True)
    # 1. web mẫu (ảnh minh hoạ)
    for f in list((ROOT / "nailmark" / "img").glob("*.jpg")):
        shutil.copy(f, out / "web-mau" / "img" / f.name)
    (out / "web-mau" / "index.html").write_text('<!doctype html><html lang=vi><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">\n' + tao(t), encoding="utf-8")
    # 2–4. poster, thẻ QR, video
    shutil.copy(ANH_TET, out / "anh-tet.jpg")
    (out / "_poster.html").write_text(poster(t, so), encoding="utf-8")
    (out / "_qr.html").write_text(the_qr(t, so), encoding="utf-8")
    tmp = out / "_tmp"; tmp.mkdir(exist_ok=True)
    chup(dict(tmp=str(tmp), anh=[[str(out / "_poster.html"), str(out / "poster-tet.png"), 1080, 1350],
                                 [str(out / "_qr.html"), str(out / "qr-quay.png"), 1240, 1748]],
              video=dict(dir=str(tmp), web=str(out / "web-mau" / "index.html"))))
    webm = next(tmp.glob("*.webm"), None)
    co_video = False
    if webm:
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(webm), "-t", "12", "-vf", "fps=30,format=yuv420p",
                            "-c:v", "libx264", "-movflags", "+faststart", str(out / "video-web.mp4")])
        co_video = r.returncode == 0
    for f in ["_poster.html", "_qr.html", "anh-tet.jpg"]:
        (out / f).unlink(missing_ok=True)
    shutil.rmtree(tmp, ignore_errors=True)
    (out / "index.html").write_text(trang_qua(t, co_video), encoding="utf-8")
    print(f"Đã tạo gói quà: {out.relative_to(ROOT)}/index.html · web mẫu · poster Tết · thẻ QR · video={'có' if co_video else 'không'}")


if __name__ == "__main__":
    main()
