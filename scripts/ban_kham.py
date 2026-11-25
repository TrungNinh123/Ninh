"""Bản khám sức khoẻ marketing (HTML) cho tiệm nail – chấm điểm dựa trên bằng chứng từng kênh.

Đầu vào: crm/leads_q1_nail.json (Google Maps) + crm/kham_nail_v1.json (khám kênh: link, người theo dõi, truy vấn đã dùng).
Chạy:   python scripts/ban_kham.py Q1S098   ->  reports/ban_kham_Q1S098.html
Thang chấm từng kênh được in ngay trong bản khám để chủ tiệm thấy vì sao có điểm đó.
"""
import html
import json
import re
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEADS = {x["id"]: x for x in json.loads((ROOT / "crm/leads_q1_nail.json").read_text(encoding="utf-8"))}
KHAM = {x["id"]: x for x in json.loads((ROOT / "crm/kham_nail_v1.json").read_text(encoding="utf-8"))}
HOA_DON_TB = 250_000
_AW = ROOT / "crm/audit_web_v1.json"
AUDIT_WEB = {x["id"]: x for x in json.loads(_AW.read_text(encoding="utf-8"))} if _AW.exists() else {}
TEN_KENH = {"website": "Website", "facebook": "Facebook", "instagram": "Instagram", "tiktok": "TikTok",
            "pinterest": "Pinterest", "youtube": "YouTube", "threads_lemon8": "Threads / Lemon8", "zalo_oa": "Zalo OA",
            "nen_tang_dat_lich": "Nền tảng đặt lịch / Tripadvisor / Foody", "bao_chi_bai_review": "Báo chí, bài review, toplist",
            "kenh_ca_nhan_chu_tiem": "Kênh cá nhân chủ tiệm / thợ"}


def so_theo_doi(t):
    """'9.649', '~16k', '11K', '2,2k' -> số; không rõ -> None."""
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*([kKmM]?)", str(t or ""))
    if not m or "không rõ" in str(t).lower():
        return None
    num, unit = m.group(1), m.group(2).lower()
    if unit:
        return float(num.replace(",", ".")) * (1000 if unit == "k" else 1_000_000)
    return float(num.replace(".", "").replace(",", ""))


def cham_kenh(k, v, maps_web, pid=None):
    """Trả về (điểm 0–10, lý do) theo thang công khai."""
    if k == "website" and pid in AUDIT_WEB:
        w = AUDIT_WEB[pid]
        if not w["truy_cap"]:
            return 0, "Website có địa chỉ nhưng không truy cập được ngày 25/11/2026 – khách bấm vào không xem được"
        dat = [c["ten"] for c in w["tieu_chi"] if c["dat"]]
        thieu = [c["ten"] for c in w["tieu_chi"] if not c["dat"]]
        return w["diem_cuoi"], (f"Đạt {len(dat)}/10 tiêu chí kỹ thuật" + (f"; thiếu: {', '.join(thieu)}" if thieu else "")
                                + (f". Xem bằng mắt trên điện thoại: {w['nhin_bang_mat']}" if w.get("nhin_bang_mat") else ""))
    if not v or not v.get("tim_thay"):
        n = len(v.get("truy_van_da_dung", [])) if v else 0
        return 0, f"Không tìm thấy sau {n} lượt tìm" if n else "Không tìm thấy"
    if k == "website":
        if maps_web and "facebook" not in maps_web:
            return 6, "Có website và đã gắn lên Google Maps"
        return 4, "Có website nhưng chưa gắn lên Google Maps nên khách tìm trên Maps không thấy"
    if k == "bao_chi_bai_review":
        n = len(v.get("nguon", []))
        return (8 if n >= 3 else 5), f"Được nhắc trong {n} nguồn"
    f = so_theo_doi(v.get("nguoi_theo_doi"))
    if f is None:
        return 3, "Có tài khoản, chưa xác minh được quy mô và mức hoạt động"
    d = 4 if f < 1000 else 5 if f < 5000 else 7 if f < 20000 else 8 if f < 100000 else 9
    ly = "thuộc nhóm dẫn đầu ngành" if d == 9 else "tần suất đăng chưa xác minh"
    return d, f"Khoảng {int(f):,} người theo dõi; {ly}".replace(",", ".")


def diem_maps(l):
    n, s, h = l["so_danh_gia"] or 0, l["sao"] or 0, l["hang"]
    d = (4 if n >= 500 else 3 if n >= 200 else 2 if n >= 50 else 1 if n >= 10 else 0)
    d += (3 if s >= 4.8 else 2 if s >= 4.5 else 1 if s >= 4.0 else 0)
    d += (3 if h and h <= 5 else 2 if h and h <= 10 else 1 if h and h <= 20 else 0)
    return d


def main(pid):
    e = html.escape
    l, k = LEADS[pid], KHAM[pid]
    ten = l["ten"].split("|")[0].split(" - ")[0].replace("(chuỗi)", "").strip()
    kenh = {c: cham_kenh(c, k["kenh"].get(c), l["website"], pid) for c in TEN_KENH}
    dm = diem_maps(l)
    dat_lich_online = bool(re.search(r"nút đặt lịch trên website|trang online booking|form đặt lịch|form 'đặt lịch|fresha \(chi nhánh|fresha \(đặt",
                                     str(k.get("dat_lich_hien_tai")), re.I))
    hang_muc = [  # (tên, điểm anh chị, dẫn đầu, sau MREAL, trọng số nail)
        ("Ảnh & cộng đồng (Instagram, Facebook, Pinterest)",
         round(sorted([kenh["instagram"][0], kenh["facebook"][0], kenh["pinterest"][0]])[-1] * .7 +
               sorted([kenh["instagram"][0], kenh["facebook"][0], kenh["pinterest"][0]])[-2] * .3), 9, 8, 25),
        ("Video ngắn (TikTok, Reels)", kenh["tiktok"][0], 9, 8, 20),
        ("Google Maps & đánh giá", dm, 9, 8, 15),
        ("Đặt lịch online", 7 if dat_lich_online else 2, 9, 8, 15),
        ("Chăm khách cũ (Zalo OA, thành viên)", 5 if kenh["zalo_oa"][0] else 1, 8, 7, 10),
        ("Gương mặt đại diện, kênh cá nhân, báo chí", max(kenh["kenh_ca_nhan_chu_tiem"][0], kenh["bao_chi_bai_review"][0]), 9, 7, 10),
        ("Website / blog", kenh["website"][0], 9, 7, 5),
    ]
    tong = round(sum(a * w for _, a, _, _, w in hang_muc) / 100, 1)
    hang_muc = [(a, b, c, max(b, m), w) for a, b, c, m, w in hang_muc]
    sau = round(sum(m * w for _, _, _, m, w in hang_muc) / 100, 1)

    rows_k = ""
    for c, label in TEN_KENH.items():
        v = k["kenh"].get(c) or {}
        d, ly = kenh[c]
        link = v.get("link") or ""
        lk = f'<a href="{e(link)}" target="_blank" rel="noopener">{e(v.get("ten_tai_khoan") or link)}</a>' if link.startswith("http") else e(v.get("ten_tai_khoan") or "—")
        rows_k += (f"<tr><td>{e(label)}</td><td>{'Có' if v.get('tim_thay') else 'Không thấy'}</td><td>{lk}</td>"
                   f"<td class=n>{e(str(v.get('nguoi_theo_doi') or '—'))}</td><td class=n><b>{d}/10</b></td><td class=s>{e(ly)}</td></tr>")
    rows_h = "".join(f"<tr><td>{e(a)}</td><td class=n><b>{b}/10</b></td><td class=n>{c}</td><td class='n go'>{m}</td><td class=n>{w}%</td></tr>"
                     for a, b, c, m, w in hang_muc)
    manh = "".join(f"<li>{e(x)}</li>" for x in (k.get("diem_manh") or [])[:3])
    van_de = "".join(f"<li>{e(x)}</li>" for x in (k.get("van_de") or [])[:4])
    so_truy_van = sum(len((k["kenh"].get(c) or {}).get("truy_van_da_dung", [])) for c in TEN_KENH)
    kenh_manh = max(("instagram", "facebook", "tiktok"), key=lambda c: kenh[c][0])
    dan_ve = (f"Anh chị đã có lượng người theo dõi trên {TEN_KENH[kenh_manh]}. Việc đầu tiên không phải làm thêm kênh mới, "
              f"mà là <b>gắn nút đặt lịch vào {TEN_KENH[kenh_manh]}</b> để biến người xem thành lịch hẹn.") if kenh[kenh_manh][0] >= 5 else \
             "Việc đầu tiên là làm cho khách tìm thấy tiệm ở đúng nơi khách nail tìm mẫu: Instagram, TikTok, Pinterest, Google Maps — tất cả dẫn về một trang đặt lịch."
    hv = 3_000_000 // HOA_DON_TB
    page = f"""<title>Bản khám {e(ten)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600&family=Lexend:wght@500;600&display=swap">
<style>
/* Phiếu khám một cột: kết luận → hồ sơ từng kênh có bằng chứng → bảng điểm → lộ trình → chi phí */
:root{{--bg:#f7f4f6;--card:#fff;--fg:#221b20;--muted:#6f6570;--line:#e6dfe4;--accent:#b0306b;--soft:#f8e6ef;--ok:#1d7a4f;
--d:"Lexend",system-ui,sans-serif;--b:"Be Vietnam Pro",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#171215;--card:#211a1e;--fg:#f1e9ee;--muted:#b3a6af;--line:#3a3036;--accent:#f07aae;--soft:#3a1f2c;--ok:#6fd3a0;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#171215;--card:#211a1e;--fg:#f1e9ee;--muted:#b3a6af;--line:#3a3036;--accent:#f07aae;--soft:#3a1f2c;--ok:#6fd3a0;color-scheme:dark}}
*{{box-sizing:border-box}}body{{background:var(--bg);color:var(--fg);font:15px/1.6 var(--b);padding-block:24px 48px;
padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
main{{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:18px}}
h1{{font:600 26px/1.25 var(--d);margin:0;text-wrap:balance}}h2{{font:600 18px var(--d);margin:0 0 8px}}
.k{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}}
section{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;min-width:0}}
.m{{color:var(--muted);font-size:14px}}.wrap{{overflow-x:auto}}a{{color:var(--accent)}}
table{{border-collapse:collapse;width:100%;min-width:600px;font-size:14px}}th,td{{border-bottom:1px solid var(--line);padding:8px 6px;text-align:left;vertical-align:top}}
th{{font-size:12px;color:var(--muted);font-weight:600}}.n{{font-variant-numeric:tabular-nums;white-space:nowrap}}.go{{color:var(--ok);font-weight:600}}.s{{color:var(--muted);font-size:13px}}
.big{{display:flex;gap:24px;flex-wrap:wrap}}.big div{{font:600 30px var(--d)}}.big span{{display:block;font:400 13px var(--b);color:var(--muted)}}
ul,ol{{margin:0;padding-left:20px}}li{{margin:4px 0}}
.road{{display:grid;gap:10px}}.road div{{border-left:3px solid var(--accent);padding:4px 0 4px 12px}}.road b{{font-family:var(--d)}}
.pk{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}}.pk div{{border:1px solid var(--line);border-radius:12px;padding:12px}}
.pk .p{{font:600 18px var(--d);color:var(--accent)}}.cta{{background:var(--soft);border-color:transparent}}
</style>
<main>
<header><div class=k>Bản khám sức khoẻ marketing · MREAL</div><h1>{e(ten)}</h1>
<p class=m>{e(l['dia_chi'])} · Khám ngày 25/11/2026 · {so_truy_van} lượt tìm kiếm trên {len(TEN_KENH)} kênh + dữ liệu Google Maps</p></header>

<section><h2>Kết luận</h2><div class=big><div>{tong}/10<span>Hiện tại (theo trọng số ngành nail)</span></div>
<div style="color:var(--ok)">{sau}/10<span>Mục tiêu sau 1–3 tháng cùng MREAL</span></div><div>9–10<span>Tiệm dẫn đầu</span></div></div>
<p><b>Điểm mạnh đã thấy:</b></p><ul>{manh or '<li>Google Maps: ' + e(str(l['sao'])) + ' sao, ' + str(l['so_danh_gia']) + ' đánh giá</li>'}</ul>
<p><b>Vấn đề cần xử lý:</b></p><ol>{van_de}</ol>
<p>{dan_ve}</p></section>

<section><h2>Hồ sơ khám từng kênh</h2>
<p class=m>Thang chấm: không tìm thấy = 0 · có tài khoản nhưng chưa xác minh hoạt động = 3 · dưới 1.000 người theo dõi = 4 · 1.000–5.000 = 5 · 5.000–20.000 = 7 · 20.000–100.000 = 8 · trên 100.000 = 9 (nhóm dẫn đầu). Website: có nhưng chưa gắn Maps = 4, đã gắn Maps = 6.</p>
<div class=wrap><table><tr><th>Kênh</th><th>Kết quả</th><th>Tài khoản / link</th><th>Theo dõi</th><th>Điểm</th><th>Vì sao</th></tr>{rows_k}
<tr><td>Google Maps</td><td>Có</td><td><a href="{e(l['maps'])}" target="_blank" rel="noopener">Hồ sơ Maps</a></td><td class=n>{l['so_danh_gia']} đánh giá</td><td class=n><b>{dm}/10</b></td><td class=s>{e(str(l['sao']))} sao · {'hạng ' + str(l['hang']) if l['hang'] else 'ngoài top 60'} khi khách tìm spa, nail quận 1</td></tr></table></div>
<p class=m>Cách đặt lịch hiện tại: {e(str(k.get('dat_lich_hien_tai') or 'không rõ'))}</p>
<p class=m>Độ tin cậy của lần khám: {e(str(k.get('do_tin_cay')))}. Số theo dõi lấy từ kết quả tìm kiếm, chưa ghi ngày; MREAL sẽ xác nhận lại cùng anh chị.</p></section>

<section><h2>Bảng điểm theo hạng mục ngành nail</h2>
<div class=wrap><table><tr><th>Hạng mục</th><th>Anh chị</th><th>Dẫn đầu</th><th>Sau MREAL</th><th>Trọng số</th></tr>{rows_h}</table></div></section>

<section><h2>Tiệm lớn đang làm gì — và chỗ họ vẫn để hở</h2><ul>
<li>Tiệm dẫn đầu nhận đặt lịch qua mọi kênh và có website viết bài cho khách du lịch — nhưng thông tin giữa các kênh hay lệch nhau, khách vẫn phải nhắn từng chi nhánh.</li>
<li>Video "quá trình làm một bộ móng" là dạng được xem và lưu nhiều nhất, nhưng phần lớn tiệm top Quận 1 MREAL khảo sát chưa có TikTok thương hiệu đều đặn.</li>
<li>Chỉ 1/100 tiệm làm đẹp Quận 1 có bài mô tả trên Google Maps.</li></ul></section>

<section><h2>Lộ trình</h2><div class=road>
<div><b>3 ngày đầu</b><br>Thống nhất thông tin mọi kênh, gắn website/trang đặt lịch lên Google Maps, Instagram, Facebook, TikTok; bài mô tả Maps; mã QR xin đánh giá.</div>
<div><b>Tuần 1–2</b><br>Bộ ảnh mẫu Noel – Tết từ ảnh thật của tiệm (chỉnh màu đồng bộ), 6 video "quá trình làm móng", trả lời toàn bộ đánh giá, gom khách cũ vào Zalo.</div>
<div><b>Tháng 1</b><br>12 video, lưới Instagram và bảng Pinterest theo mùa, chương trình đặt trước Tết, báo cáo lượt đặt lịch theo từng kênh.</div>
<div><b>Tháng 2–3</b><br>Thành viên – nhắc làm lại sau 3 tuần, gói cô dâu & tiệc cưới, đại sứ AI của tiệm (ghi rõ là AI).</div>
<div><b>Tháng 4–6</b><br>KOC địa phương, quảng cáo theo dịp, vào nhóm dẫn đầu khu vực.</div></div></section>

<section><h2>Chi phí</h2><div class=pk>
<div><div class=p>500.000đ</div>Khởi động 3 ngày<br><span class=m>Làm xong rồi mới thanh toán</span></div>
<div><div class=p>2–3 triệu/tháng</div>Tăng tốc<br><span class=m>Dừng theo tháng</span></div>
<div><div class=p>+2 triệu/tháng</div>Đại sứ AI<br><span class=m>Tuỳ chọn</span></div></div>
<p class=m>So sánh: nhân viên marketing TP.HCM 10–15 triệu/tháng; KOC micro 1,5–5 triệu/video.</p>
<p>Với hoá đơn trung bình khoảng 250.000đ, gói 3 triệu hoà vốn ở <b>{hv} khách mới/tháng</b>; thu về gấp đôi ở {2*hv} khách. Mỗi lượt đặt lịch được đếm theo từng kênh để anh chị tự kiểm tra.</p></section>

<section class=cta><h2>Bước tiếp theo</h2><p>Anh chị trả lời "Bắt đầu" qua Zalo — MREAL làm xong 3 ngày đầu rồi anh chị mới thanh toán.</p><p class=m>Phương Thư · MREAL</p></section>
</main>"""
    out = ROOT / "reports" / f"ban_kham_{pid}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(out, tong, sau)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
