"""Quét 100 tiệm Spa / Nail / Thẩm mỹ ở Quận 1 từ Google Places API (bản chính thức).

- Chấm điểm hiện diện Google Maps trên thang 100, hoàn toàn tự động, cùng một thước đo cho mọi tiệm.
- Ghi điểm yếu bằng con số thật từ Google Maps (để dùng trong tin nhắn).
- Xuất crm/leads_q1_spa.json, sau đó chạy import_leads.py để đưa vào CRM.

Chạy:  python scripts/scan_places.py            (quét thật, cần khoá trong Network secrets)
       python scripts/scan_places.py --thu       (chạy thử với dữ liệu giả, không gọi Google)
Giới hạn: tối đa MAX_CALLS lượt gọi mỗi lần chạy để kiểm soát chi phí.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "crm" / "leads_q1_spa.json"
NGANH, KHU_VUC, MUC_TIEU, MAX_CALLS = "Spa / Nail / Thẩm mỹ", "Quận 1", 100, 45

# Từ khoá chính (dùng để đo thứ hạng) + từ khoá phụ theo phường để đủ 100 tiệm
TU_KHOA_CHINH = ["spa quận 1", "tiệm nail quận 1", "thẩm mỹ viện quận 1"]
# Từ 1/7/2025 Quận 1 cũ gồm 4 phường mới: Sài Gòn, Tân Định, Bến Thành, Cầu Ông Lãnh
PHUONG = ["Sài Gòn", "Tân Định", "Bến Thành", "Cầu Ông Lãnh", "Bến Nghé", "Đa Kao", "Phạm Ngũ Lão", "Nguyễn Cư Trinh"]
DAU_HIEU_Q1 = ["Quận 1", "Q1", "Q.1", ", Sài Gòn, Hồ Chí Minh", "Phường Sài Gòn", "Bến Thành", "Tân Định",
               "Cầu Ông Lãnh", "Bến Nghé", "Đa Kao", "Nguyễn Thái Bình", "Phạm Ngũ Lão", "Cô Giang",
               "Nguyễn Cư Trinh", "Cầu Kho"]
TU_KHOA_PHU = [f"{k} phường {p}" for p in PHUONG for k in ("spa", "nail", "thẩm mỹ")]
if "--nail" in sys.argv:  # chỉ ngành nail
    NGANH, OUT = "Nail", ROOT / "crm" / "leads_q1_nail.json"
    TU_KHOA_CHINH = ["tiệm nail quận 1", "nail salon quận 1", "làm móng quận 1"]
    TU_KHOA_PHU = [f"{k} phường {p}" for p in PHUONG for k in ("nail", "làm móng", "nail art")]

FIELDS = "nextPageToken," + ",".join("places." + f for f in [
    "id", "displayName", "formattedAddress", "nationalPhoneNumber", "websiteUri", "googleMapsUri",
    "rating", "userRatingCount", "regularOpeningHours", "editorialSummary",
    "businessStatus", "primaryType"])
calls = 0


def search(text, token=None):
    global calls
    if calls >= MAX_CALLS:
        return [], None
    calls += 1
    body = {"textQuery": text + " TP.HCM", "languageCode": "vi", "regionCode": "VN", "pageSize": 20}
    if token:
        body["pageToken"] = token
    req = urllib.request.Request(
        "https://places.googleapis.com/v1/places:searchText", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-Goog-FieldMask": FIELDS,
                 "X-Goog-Api-Key": os.environ.get("GOOGLE_PLACES_API_KEY", "proxy-injects-key")})
    for lan in range(5):
        try:
            time.sleep(13)  # tôn trọng giới hạn ~5 lượt/phút đã cài trên Google Cloud
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or lan == 4:
                raise
            time.sleep(60)
    return d.get("places", []), d.get("nextPageToken")


def bac(v, nac):
    """nac: [(ngưỡng, điểm), ...] giảm dần."""
    for nguong, diem in nac:
        if v >= nguong:
            return diem
    return nac[-1][1] if v else 0


def cham(p, hang):
    anh, so_dg, sao = len(p.get("photos", [])), p.get("userRatingCount", 0), p.get("rating", 0)
    web = p.get("websiteUri", "")
    la_fb = "facebook.com" in web
    d = {
        "C": bac(so_dg, [(300, 20), (100, 16), (30, 10), (10, 5), (1, 1)]),
        "D": bac(sao, [(4.8, 15), (4.5, 12), (4.0, 7), (0.1, 3)]),
        "E": 5 if la_fb else (15 if web else 0),
        "F": 5 if la_fb else 0,
        "G": 10 if p.get("regularOpeningHours") else 0,
        "H": 5 if p.get("nationalPhoneNumber") else 0,
        "I": 5 if p.get("editorialSummary") else 0,
        "J": 15 if hang and hang <= 5 else 10 if hang and hang <= 10 else 6 if hang and hang <= 20 else 0,
        "K": 0,
        "L": 0,
    }
    yeu = []
    if so_dg < 30:
        yeu.append(f"mới có {so_dg} đánh giá trên Google" if so_dg else "chưa có đánh giá nào trên Google")
    elif sao and sao < 4.5:
        yeu.append(f"điểm Google đang {sao:.1f} sao".replace(".", ","))
    if not web:
        yeu.append("chưa gắn website")
    elif la_fb:
        yeu.append("Google Maps đang dẫn về Facebook, chưa có website riêng")
    if not p.get("regularOpeningHours"):
        yeu.append("chưa có giờ mở cửa trên Maps")
    if not hang or hang > 20:
        yeu.append("chưa lọt top 20 khi khách tìm \"spa quận 1\"")
    return d, yeu


def main():
    global OUT
    thu = "--thu" in sys.argv
    if thu:
        OUT = ROOT / "crm" / "thu_nghiem" / "leads_thu.json"  # không bao giờ ghi đè dữ liệu thật
    places, hang = {}, {}
    if thu:
        import random
        random.seed(1)
        for i in range(120):
            places[f"p{i}"] = {"id": f"p{i}", "displayName": {"text": f"Spa Thử {i}"},
                               "formattedAddress": "Quận 1, TP.HCM", "nationalPhoneNumber": f"09{i:08d}",
                               "websiteUri": random.choice(["", "https://facebook.com/x", "https://x.vn"]),
                               "googleMapsUri": f"https://maps.google.com/?cid={i}", "rating": round(random.uniform(3.8, 5), 1),
                               "userRatingCount": random.randint(0, 500), "photos": [0] * random.randint(0, 10),
                               "regularOpeningHours": random.choice([None, {"x": 1}]), "businessStatus": "OPERATIONAL"}
            hang[f"p{i}"] = i + 1
    else:
        for q in TU_KHOA_CHINH + TU_KHOA_PHU:
            token, vi_tri = None, 0
            for _ in range(3 if q in TU_KHOA_CHINH else 1):
                res, token = search(q, token)
                for p in res:
                    vi_tri += 1
                    if p.get("businessStatus") not in (None, "OPERATIONAL") or not any(x in p.get("formattedAddress", "") for x in DAU_HIEU_Q1):
                        continue
                    if "--nail" in sys.argv and not ("nail" in p["displayName"]["text"].lower()
                            or "móng" in p["displayName"]["text"].lower() or p.get("primaryType") == "nail_salon"):
                        continue
                    places.setdefault(p["id"], p)
                    if q in TU_KHOA_CHINH:
                        hang[p["id"]] = min(hang.get(p["id"], 999), vi_tri)
                if not token:
                    break
            if len(places) >= MUC_TIEU * 1.1 and calls >= 12:
                break
    leads = []
    for n, p in enumerate(list(places.values())[:MUC_TIEU], start=1):
        d, yeu = cham(p, hang.get(p["id"]))
        leads.append({
            "id": (f"Q1N{n:03d}" if "--nail" in sys.argv else f"Q1S{n:03d}"), "nganh": NGANH, "ten": p["displayName"]["text"], "khu_vuc": KHU_VUC,
            "dia_chi": p.get("formattedAddress", ""), "sdt": (p.get("nationalPhoneNumber") or "").replace(" ", ""),
            "email": "", "website": p.get("websiteUri", ""), "fanpage": p.get("websiteUri", "") if "facebook.com" in p.get("websiteUri", "") else "",
            "maps": p.get("googleMapsUri", ""), "sao": p.get("rating"), "so_danh_gia": p.get("userRatingCount", 0),
            "hang": hang.get(p["id"]), "diem": d, "tong": sum(d.values()), "yeu_maps": yeu,
            "diem_khen": (f"{p.get('rating'):.1f}".replace(".", ",") + f" sao trên Google với {p.get('userRatingCount', 0)} đánh giá") if p.get("rating") else "",
            "diem_yeu": yeu, "nguon": [p.get("googleMapsUri", "")], "chuoi": False})
    OUT.write_text(json.dumps(leads, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{'(THỬ) ' if thu else ''}{len(leads)} tiệm, {calls} lượt gọi Google → {OUT}")
    tong = sorted(l["tong"] for l in leads)
    if tong:
        print(f"Điểm: thấp nhất {tong[0]}, trung vị {tong[len(tong)//2]}, cao nhất {tong[-1]}")


if __name__ == "__main__":
    main()
