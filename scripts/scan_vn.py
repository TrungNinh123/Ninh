"""Quét tiệm nail Việt Nam từ Google Places (TP.HCM, Hà Nội, Đà Nẵng) và nhận diện chuỗi.

Mỗi truy vấn 1 trang (tối đa 20 tiệm). Giới hạn: 100 lượt/ngày, ~5 lượt/phút (gọi chậm 13 giây/lượt).
Ra: crm/leads_vn_nail.json (toàn bộ, đã gộp trùng) và in tóm tắt.
Chạy: python scripts/scan_vn.py [--them "truy vấn 1" "truy vấn 2" ...]
"""
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "crm" / "leads_vn_nail.json"
FIELDS = ",".join("places." + f for f in ["id", "displayName", "formattedAddress", "nationalPhoneNumber", "websiteUri",
                                           "googleMapsUri", "rating", "userRatingCount", "businessStatus", "primaryType"])
HCM = ["Quận 1", "Quận 3", "Quận 5", "Quận 7", "Quận 10", "Phú Nhuận", "Bình Thạnh", "Gò Vấp", "Tân Bình", "Thủ Đức"]
HN = ["Hoàn Kiếm", "Ba Đình", "Đống Đa", "Cầu Giấy", "Tây Hồ", "Hai Bà Trưng", "Thanh Xuân"]
TRUY_VAN = [f"tiệm nail {q} Hồ Chí Minh" for q in HCM] + [f"tiệm nail {q} Hà Nội" for q in HN] + ["tiệm nail Hải Châu Đà Nẵng"]


def goi(text):
    body = {"textQuery": text, "languageCode": "vi", "regionCode": "VN", "pageSize": 20}
    req = urllib.request.Request("https://places.googleapis.com/v1/places:searchText", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "X-Goog-FieldMask": FIELDS,
                                          "X-Goog-Api-Key": "proxy-injects-key"})
    for lan in range(4):
        try:
            time.sleep(13)
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r).get("places", [])
        except urllib.error.HTTPError as e:
            if e.code == 429 and lan < 3:
                print("  429, chờ 60 giây", flush=True)
                time.sleep(60)
                continue
            raise
    return []


def thanh_pho(dc):
    d = dc.lower()
    if "hà nội" in d or "hanoi" in d:
        return "Hà Nội"
    if "đà nẵng" in d or "da nang" in d:
        return "Đà Nẵng"
    if "hồ chí minh" in d or "ho chi minh" in d or "thủ đức" in d:
        return "TP.HCM"
    return "Khác"


def khong_dau(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").replace("đ", "d")


BO = r"\b(nail[s]?|salon|spa|studio|beauty|and|&|tiem|lam|mong|chi nhanh|cn\d*|co so|cs\d*|quan \d+|q\.? ?\d+|ha noi|hcm|sai gon|saigon|tp|thu duc|the|by|house|room|lounge|bar|art|academy|eyelash|mi|massage|head|hair|cafe)\b"


def ten_goc(ten):
    s = khong_dau(ten.split("|")[0].split(" - ")[0].split("–")[0])
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(BO, " ", s)
    return " ".join(s.split())


if __name__ == "__main__":
    tv = TRUY_VAN
    if "--them" in sys.argv:
        tv = sys.argv[sys.argv.index("--them") + 1:]
    cu = {x["id"]: x for x in json.loads(OUT.read_text(encoding="utf-8"))} if OUT.exists() else {}
    for i, q in enumerate(tv, 1):
        ps = goi(q)
        moi = 0
        for p in ps:
            if p["id"] in cu:
                continue
            moi += 1
            cu[p["id"]] = dict(id=p["id"], ten=p.get("displayName", {}).get("text", ""), dia_chi=p.get("formattedAddress", ""),
                               thanh_pho=thanh_pho(p.get("formattedAddress", "")), sdt=p.get("nationalPhoneNumber", ""),
                               website=p.get("websiteUri", ""), maps=p.get("googleMapsUri", ""), sao=p.get("rating"),
                               so_danh_gia=p.get("userRatingCount", 0), trang_thai=p.get("businessStatus", ""),
                               loai=p.get("primaryType", ""), truy_van=q)
        print(f"[{i}/{len(tv)}] {q}: {len(ps)} kết quả, {moi} mới; tổng {len(cu)}", flush=True)
        OUT.write_text(json.dumps(list(cu.values()), ensure_ascii=False, indent=1), encoding="utf-8")
    print("Xong:", len(cu), "tiệm ->", OUT)
