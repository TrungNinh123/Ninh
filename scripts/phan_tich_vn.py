"""Phân tích crm/leads_vn_nail.json: top 100 tiệm nail còn hoạt động, nhận diện chuỗi, chỉ số hiện diện số.
Ra: research/top100_nail_vn.json và research/100_TIEM_NAIL_VN.md
"""
import json
import statistics as st
from collections import defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_vn import ten_goc, khong_dau  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "crm" / "leads_vn_nail.json").read_text(encoding="utf-8"))


def la_nail(x):
    t = khong_dau(x["ten"])
    return x["loai"] == "nail_salon" or "nail" in t or "mong" in t


def web_rieng(w):
    return bool(w) and not any(k in w for k in ("facebook.com", "instagram.com", "tiktok.com", "linktr.ee", "zalo.me"))


ok = [x for x in D if x["trang_thai"] == "OPERATIONAL" and la_nail(x) and x["thanh_pho"] != "Khác"]
dong = [x for x in D if x["trang_thai"] in ("CLOSED_PERMANENTLY", "CLOSED_TEMPORARILY") and la_nail(x)]
nhom = defaultdict(list)
for x in ok:
    k = ten_goc(x["ten"])
    if len(k) >= 3:
        nhom[k].append(x)
chuoi = sorted(((k, v) for k, v in nhom.items() if len(v) >= 2), key=lambda kv: (-len(kv[1]), -sum(y["so_danh_gia"] or 0 for y in kv[1])))
top = sorted(ok, key=lambda x: -(x["so_danh_gia"] or 0))[:100]
for x in top:
    x["web_rieng"] = web_rieng(x["website"])
    x["chuoi"] = len(nhom.get(ten_goc(x["ten"]), [])) >= 2
(ROOT / "research" / "top100_nail_vn.json").write_text(json.dumps(top, ensure_ascii=False, indent=1), encoding="utf-8")


def tom(ds, ten):
    n = len(ds) or 1
    dg = [x["so_danh_gia"] or 0 for x in ds]
    return (f"| {ten} | {len(ds)} | {st.median(dg) if dg else 0:,.0f} | {sum(1 for x in ds if web_rieng(x['website'])) / n:.0%} | "
            f"{sum(1 for x in ds if x['website'] and not web_rieng(x['website'])) / n:.0%} | {sum(1 for x in ds if not x['website']) / n:.0%} | "
            f"{st.mean([x['sao'] for x in ds if x['sao']]) if ds else 0:.2f} |").replace(",", ".")


L = ["# 100 tiệm nail Việt Nam (Google Maps, quét 25/11/2026)", "",
     f"Quét {len(D)} địa điểm từ {len(set(x['truy_van'] for x in D))} truy vấn (10 quận TP.HCM, 7 quận Hà Nội, Hải Châu Đà Nẵng). "
     f"Sau khi lọc còn hoạt động và đúng ngành nail: {len(ok)} tiệm. Đã đóng cửa: {len(dong)}.", "",
     "Giới hạn: Google trả tối đa 20 tiệm mỗi truy vấn, xếp theo độ liên quan, nên đây là mẫu các tiệm nổi bật nhất mỗi quận, không phải toàn bộ thị trường.", "",
     "## Hiện diện số của 100 tiệm nhiều đánh giá nhất", "",
     "| Nhóm | Số tiệm | Đánh giá (trung vị) | Web riêng | Chỉ gắn Facebook/IG | Không gắn web | Sao TB |", "|---|---|---|---|---|---|---|",
     tom(top, "Top 100")]
for tp in ("TP.HCM", "Hà Nội", "Đà Nẵng"):
    L.append(tom([x for x in top if x["thanh_pho"] == tp], tp))
L += ["", "## Chuỗi nhận diện được (từ 2 địa điểm trở lên trong mẫu)", "", "| Thương hiệu | Số điểm trong mẫu | Thành phố | Tổng đánh giá | Sao TB |", "|---|---|---|---|---|"]
for k, v in chuoi[:25]:
    L.append(f"| {v[0]['ten'].split('|')[0][:45]} | {len(v)} | {', '.join(sorted(set(y['thanh_pho'] for y in v)))} | "
             f"{sum(y['so_danh_gia'] or 0 for y in v):,} | {st.mean([y['sao'] for y in v if y['sao']]):.2f} |".replace(",", "."))
L += ["", "## Top 100 (xếp theo số đánh giá Google)", "", "| # | Tiệm | Thành phố | Sao | Đánh giá | Web | Chuỗi |", "|---|---|---|---|---|---|---|"]
for i, x in enumerate(top, 1):
    w = "riêng" if x["web_rieng"] else ("MXH" if x["website"] else "không")
    L.append(f"| {i} | {x['ten'].split('|')[0][:50]} | {x['thanh_pho']} | {x['sao']} | {x['so_danh_gia']:,} | {w} | {'có' if x['chuoi'] else ''} |".replace(",", "."))
(ROOT / "research" / "100_TIEM_NAIL_VN.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L[:40]))
