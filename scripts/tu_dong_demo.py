"""Cửa vào phễu Nailmark: tên tiệm hoặc link Google Maps -> web mẫu riêng cho tiệm, tự động.

Lấy dữ liệu thật từ Google Places (tên, địa chỉ, số sao, số đánh giá, SĐT, giờ mở cửa, link Maps)
rồi dựng trang bằng scripts/web_tiem.py. Trang ghi rõ là bản demo, chỉ gửi riêng cho chủ tiệm.
Chạy: python scripts/tu_dong_demo.py "ELIZ Nail Beauty Bình Thạnh"
      python scripts/tu_dong_demo.py "https://www.google.com/maps/place/ELIZ+Nail+Beauty/..."
Mỗi lần chạy tốn 1 lượt Places API (hạn mức 100 lượt/ngày).
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_vn import khong_dau  # noqa: E402
from web_tiem import ROOT, tao  # noqa: E402

FIELDS = ("places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.nationalPhoneNumber,"
          "places.regularOpeningHours.weekdayDescriptions,places.googleMapsUri,places.websiteUri,places.types")
THU = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


def truy_van(dau_vao):
    """Lấy chuỗi tìm kiếm từ link Google Maps (/maps/place/<tên>/ hoặc ?q=) hoặc dùng nguyên văn."""
    if "google." in dau_vao or "goo.gl" in dau_vao:
        m = re.search(r"/maps/place/([^/@?]+)", dau_vao)
        if m:
            return urllib.parse.unquote_plus(m.group(1))
        q = urllib.parse.parse_qs(urllib.parse.urlparse(dau_vao).query).get("q")
        if q:
            return q[0]
        raise SystemExit("Link rút gọn chưa đọc được tên tiệm: hãy dán tên tiệm kèm quận.")
    return dau_vao


def tim(q):
    body = {"textQuery": q, "languageCode": "vi", "regionCode": "VN", "pageSize": 1}
    req = urllib.request.Request("https://places.googleapis.com/v1/places:searchText", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "X-Goog-FieldMask": FIELDS,
                                          "X-Goog-Api-Key": "proxy-injects-key"})
    with urllib.request.urlopen(req, timeout=40) as r:
        ds = json.load(r).get("places", [])
    if not ds:
        raise SystemExit(f"Không tìm thấy tiệm cho: {q}")
    return ds[0]


def so_vn(x):
    return f"{x:,}".replace(",", ".")


def gio_mo_cua(p):
    ds = p.get("regularOpeningHours", {}).get("weekdayDescriptions") or []
    if not ds:
        return "Giờ mở cửa: tiệm bổ sung"
    gio = [d.split(": ", 1)[-1] for d in ds]
    if len(set(gio)) == 1:
        return f"{gio[0]} mỗi ngày"
    return " · ".join(f"{THU[i] if i < 7 else ''}: {g}" for i, g in enumerate(gio))


def cau_hinh(p):
    ten = p["displayName"]["text"]
    sao = p.get("rating")
    dg = p.get("userRatingCount", 0)
    loai = " ".join(p.get("types", []))
    dv = ["Sơn gel", "Nail art", "Đắp gel, nối móng", "Chăm sóc tay chân"]
    if "spa" in loai or "spa" in ten.lower():
        dv.append("Spa, thư giãn")
    sao_vn = f"{sao:.1f}".replace(".", ",") if sao else ""
    kh = (f"{so_vn(dg)} khách chấm {sao_vn} sao trên Google" if sao and dg
          else "Móng đẹp chuẩn Nailmark")
    return dict(ten=ten, khau_hieu=kh, dia_chi=[p.get("formattedAddress", "")], gio=gio_mo_cua(p),
                zalo=p.get("nationalPhoneNumber", "tiệm bổ sung"), sao=sao_vn,
                danh_gia=so_vn(dg) if dg else "", maps=p.get("googleMapsUri", ""), dich_vu=dv,
                ghi_chu="Bản demo Nailmark dựng riêng cho tiệm, chưa phải trang chính thức.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    p = tim(truy_van(" ".join(sys.argv[1:])))
    t = cau_hinh(p)
    slug = re.sub(r"[^a-z0-9]+", "-", khong_dau(t["ten"])).strip("-")[:40]
    out = ROOT / "nailmark" / f"tiem-{slug}.html"
    out.write_text(tao(t), encoding="utf-8")
    print(json.dumps({k: t[k] for k in ("ten", "dia_chi", "gio", "zalo", "sao", "danh_gia")}, ensure_ascii=False, indent=1))
    print("Web có sẵn website riêng:", p.get("websiteUri", "không"))
    print("Đã tạo", out.relative_to(ROOT))
