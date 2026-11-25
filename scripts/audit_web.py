"""Chấm chất lượng website tiệm (thang 10, 10 tiêu chí × 1 điểm), có bằng chứng.

Chạy: python scripts/audit_web.py  ->  crm/audit_web_v1.json
Tiêu chí:
 1 Truy cập được, HTTPS            6 Có nút / form đặt lịch online
 2 Tải nhanh (< 3 giây)             7 Bấm gọi / Zalo / WhatsApp trực tiếp
 3 Tối ưu điện thoại (viewport)     8 Đủ ảnh mẫu (≥ 12 ảnh)
 4 Tiêu đề + mô tả SEO              9 Có địa chỉ / bản đồ / giờ mở cửa
 5 Có bảng giá dịch vụ             10 Có blog / bài viết và tiếng Việt + Anh
"""
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES = {
    "Q1S055": "https://zeninailspa.com/",
    "Q1S076": "https://fleurbeauty.vn/en/",
    "Q1S042": "https://acongstudio.wordpress.com/",
    "Q1S098": "https://haiyen2dt-hue.github.io/",
    "Q1S044": "https://mydorisnail.com/",
    "Q1S059": "https://thernailspace.com/",
}


def fetch(url):
    t = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read(3_000_000).decode("utf-8", "ignore"), time.time() - t, r.geturl()


def audit(pid, url):
    try:
        h, sec, final = fetch(url)
    except Exception as e:  # noqa: BLE001
        return {"id": pid, "url": url, "diem": 0, "truy_cap": False,
                "bang_chung": [f"Không truy cập được ({type(e).__name__}) ngày 25/11/2026 – khách bấm link sẽ không xem được trang"]}
    low = h.lower()
    title = re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I)
    desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', h, re.I)
    imgs = len(re.findall(r"<img\b", low))
    checks = [
        ("Truy cập được, HTTPS", final.startswith("https"), final),
        ("Tải nhanh < 3 giây", sec < 3, f"{sec:.1f} giây"),
        ("Tối ưu điện thoại", "name=\"viewport\"" in low or "name='viewport'" in low, "có thẻ viewport" if "viewport" in low else "không có thẻ viewport"),
        ("Tiêu đề + mô tả SEO", bool(title and desc), f"title: {(title.group(1).strip()[:70] if title else '—')} | description: {'có' if desc else 'không'}"),
        ("Có bảng giá", bool(re.search(r"\d{2,3}[.,]?0{3}\s*(đ|vnd|₫)|\d{2,3}k\b|price|bảng giá", low)), "có giá/“price”" if re.search(r"price|bảng giá|\dk\b", low) else "không thấy giá"),
        ("Nút/form đặt lịch online", bool(re.search(r"book now|booking|đặt lịch|dat-lich|appointment|fresha", low)), "có từ khoá đặt lịch" if re.search(r"book|đặt lịch|appointment", low) else "không có"),
        ("Bấm gọi / Zalo / WhatsApp", bool(re.search(r"tel:|zalo\.me|wa\.me|whatsapp", low)), ", ".join(x for x in ("tel:", "zalo.me", "wa.me", "whatsapp") if x in low) or "không có"),
        ("Đủ ảnh mẫu (≥12)", imgs >= 12, f"{imgs} ảnh"),
        ("Địa chỉ / bản đồ / giờ", bool(re.search(r"google\.com/maps|maps\.app|giờ mở cửa|opening hours|open daily|\d{1,2}:\d{2}\s*(am|pm|-)", low)), "có" if "maps" in low else "chỉ chữ / không có bản đồ"),
        ("Blog + song ngữ", bool(re.search(r"/blog|bài viết|/news|/tin-tuc", low)) and bool(re.search(r"tiếng việt|/vi/|lang=\"vi|english|/en/", low)), "có blog" if re.search(r"/blog|/news|tin-tuc", low) else "không có blog"),
    ]
    return {"id": pid, "url": url, "truy_cap": True, "diem": sum(1 for _, ok, _ in checks if ok),
            "tieu_chi": [{"ten": n, "dat": ok, "bang_chung": ev} for n, ok, ev in checks]}


if __name__ == "__main__":
    out = [audit(p, u) for p, u in SITES.items()]
    (ROOT / "crm/audit_web_v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in out:
        print(r["id"], r["diem"], "/10", "" if r["truy_cap"] else r["bang_chung"][0])
        for c in r.get("tieu_chi", []):
            print("   ", "✓" if c["dat"] else "✗", c["ten"], "–", c["bang_chung"][:90])
