"""Khâu 10: kiểm chất lượng web của tiệm sau khi xuất bản, tự động, không cần người.

Kiểm: (1) đủ ảnh lookbook và ảnh tải được, (2) bảng giá không trống, (3) mã QR quét ra đúng zalo.me/<số>,
(4) không tràn ngang ở màn hình 390px và 1280px, (5) không lỗi script, (6) không còn chữ giữ chỗ.
Chạy: python scripts/kiem_tra_web.py nailmark/tiem/<slug>
Kết quả: in bảng ĐẠT/CHƯA ĐẠT và ghi <thư mục>/kiem-tra.json. Mã thoát 0 = đạt hết.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

CHU_GIU_CHO = ["hiển thị ở đây", "tiệm bổ sung", "[tên", "lorem"]


def do_trinh_duyet(html):
    js = r"""
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const kq={};
for(const w of [390,1280]){const p=await b.newPage({viewport:{width:w,height:900}});const e=[];p.on('pageerror',x=>e.push(x.message));
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(800);
kq['w'+w]={sw:await p.evaluate(()=>document.documentElement.scrollWidth),loi:e,
 anh_hong:await p.evaluate(async()=>{const im=[...document.images];for(const i of im){i.loading='eager';}await new Promise(r=>setTimeout(r,800));return im.filter(i=>!(i.complete&&i.naturalWidth>0)).map(i=>i.getAttribute('src'));}),
 so_anh_lookbook:await p.evaluate(()=>document.querySelectorAll('.lb img').length),
 so_dong_gia:await p.evaluate(()=>document.querySelectorAll('table.gia tr').length)};await p.close();}
console.log(JSON.stringify(kq));await b.close();})();"""
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(js)
    out = subprocess.run(["node", f.name, str(html)], capture_output=True, text=True, timeout=120)
    return json.loads(out.stdout.strip().splitlines()[-1])


def main():
    d = Path(sys.argv[1]).resolve()
    html = d / "index.html"
    s = html.read_text(encoding="utf-8")
    so = (d / "chu.txt").read_text().strip() if (d / "chu.txt").exists() else ""
    tr = do_trinh_duyet(html)
    qr_text = []
    try:
        import zxingcpp
        from PIL import Image
        import cairosvg  # noqa: F401  (nếu có thì đọc SVG trực tiếp)
    except Exception:
        pass
    try:
        import io
        import zxingcpp
        from PIL import Image
        svg = d / "qr-dat-lich.svg"
        png = Path(tempfile.mkdtemp()) / "qr.png"
        js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:600,height:600}});"
              f"await p.goto('file://{svg}');await p.screenshot({{path:'{png}'}});await b.close();}})();")
        subprocess.run(["node", "-e", js], check=True, timeout=60)
        qr_text = [r.text for r in zxingcpp.read_barcodes(Image.open(png))]
    except Exception as e:  # noqa: BLE001
        qr_text = [f"lỗi đọc QR: {e}"]
    kiem = [
        ("Ảnh lookbook ≥ 4", tr["w390"]["so_anh_lookbook"] >= 4, f"{tr['w390']['so_anh_lookbook']} ảnh"),
        ("Không ảnh hỏng", not tr["w1280"]["anh_hong"], ", ".join(tr["w1280"]["anh_hong"][:3]) or "0"),
        ("Bảng giá có dòng", tr["w390"]["so_dong_gia"] >= 1, f"{tr['w390']['so_dong_gia']} dòng"),
        ("QR mở đúng Zalo", bool(so) and f"https://zalo.me/{so}" in qr_text, ", ".join(qr_text) or "không đọc được"),
        ("Không tràn ngang 390px", tr["w390"]["sw"] <= 390, str(tr["w390"]["sw"])),
        ("Không tràn ngang 1280px", tr["w1280"]["sw"] <= 1280, str(tr["w1280"]["sw"])),
        ("Không lỗi script", not (tr["w390"]["loi"] or tr["w1280"]["loi"]), "; ".join(tr["w390"]["loi"] + tr["w1280"]["loi"]) or "0"),
        ("Không còn chữ giữ chỗ", not any(k in s for k in CHU_GIU_CHO), ", ".join(k for k in CHU_GIU_CHO if k in s) or "0"),
    ]
    dat = all(k[1] for k in kiem)
    for ten, ok, ct in kiem:
        print(f"{'ĐẠT ' if ok else 'CHƯA'} · {ten} · {ct}")
    print("KẾT LUẬN:", "WEB ĐẠT CHUẨN" if dat else "CHƯA ĐẠT, xem dòng CHƯA")
    (d / "kiem-tra.json").write_text(json.dumps([dict(muc=a, dat=b, chi_tiet=c) for a, b, c in kiem], ensure_ascii=False, indent=1), encoding="utf-8")
    sys.exit(0 if dat else 1)


if __name__ == "__main__":
    main()
