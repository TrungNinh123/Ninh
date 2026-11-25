"""Lấy tỷ giá chính thức của Vietcombank (bảng XML trên portal VCB) và lưu vào research/ty_gia_vcb.json.

Quy ước của team: mọi quy đổi tiền tệ trong tài liệu và website đều dùng **giá bán ra của VCB**,
ghi rõ ngày giờ niêm yết. Chạy lại script trước khi cập nhật số liệu.
Chạy: python scripts/ty_gia_vcb.py [USD JPY ...]
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

URL = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"
OUT = Path(__file__).resolve().parent.parent / "research" / "ty_gia_vcb.json"


def so(x):
    x = (x or "").replace(",", "").strip()
    return float(x) if x and x != "-" else None


def lay():
    with urllib.request.urlopen(URL, timeout=30) as r:
        root = ET.fromstring(r.read())
    bang = {}
    for ex in root.iter("Exrate"):
        bang[ex.get("CurrencyCode")] = dict(mua_tien_mat=so(ex.get("Buy")), mua_chuyen_khoan=so(ex.get("Transfer")),
                                            ban_ra=so(ex.get("Sell")))
    return dict(nguon=URL, thoi_diem=root.findtext("DateTime"), quy_uoc="Quy đổi theo giá bán ra", ty_gia=bang)


def doi(so_tien, tu, du_lieu=None):
    """Đổi một số tiền ngoại tệ sang VND theo giá bán ra VCB."""
    d = du_lieu or json.loads(OUT.read_text(encoding="utf-8"))
    return so_tien * d["ty_gia"][tu]["ban_ra"]


if __name__ == "__main__":
    d = lay()
    OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print("VCB", d["thoi_diem"])
    for m in sys.argv[1:] or ["USD", "JPY", "EUR", "SGD", "THB", "CNY", "GBP", "AED"]:
        if m in d["ty_gia"]:
            print(f"  {m}: bán ra {d['ty_gia'][m]['ban_ra']:,} đ")
