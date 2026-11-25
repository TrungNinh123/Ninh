"""Nailmark – bộ máy tạo web phiên bản 2: web của tiệm với ẢNH THẬT và BẢNG GIÁ THẬT.

Đây là phần lõi mà app 4 bước (nailmark/tu-lam.html) sẽ gọi. Hiện chạy bằng dòng lệnh:
  python scripts/tao_web.py --maps "Tên tiệm + quận"   --anh thu_muc_anh --gia bang_gia.txt --zalo 0900000000
  python scripts/tao_web.py --ten "Sơn Mài Nail" --dia-chi "Quận 1" --anh ... --gia ... --zalo ...   (không gọi Google)
- Ảnh: lấy tối đa 12 ảnh (jpg/png/webp), cắt khung 3:4 giữa ảnh, thu về 900x1200,
  chỉnh SÁNG bằng một hệ số chung cho cả 3 kênh màu -> giữ nguyên tỉ lệ màu, không đổi màu móng.
- Bảng giá: file chữ, mỗi dòng "Tên dịch vụ | Giá". (Bước AI đọc bảng giá từ ảnh: chưa có, chờ kiểm thử Kyma.)
- Kết quả: nailmark/tiem/<slug>/index.html + img/ (gửi cả thư mục lên hosting là chạy).
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_vn import khong_dau  # noqa: E402
from web_tiem import ROOT, DIP, tao  # noqa: E402

DUOI = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}
try:  # ảnh iPhone mặc định là HEIC
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass
GIA_SO = re.compile(r"^(.*?)[\s:\-–|]+((?:từ\s*)?[\d.,]+\s*(?:k|K|đ|vnđ|VNĐ|nghìn|ngàn|tr|triệu)?\S*)\s*$")


def chinh_anh(src, dst, w=900, h=1200, sang_muc_tieu=0.52):
    """Cắt 3:4, thu nhỏ, chỉnh sáng bằng hệ số chung (không đổi tông màu). Trả về hệ số đã dùng."""
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.5))
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    tb = float(np.median(lum)) or 1e-3
    k = float(np.clip(sang_muc_tieu / tb, 0.8, 1.6))  # chỉ sáng/tối vừa phải, không biến dạng ảnh
    # nhân chung 3 kênh; điểm nào sắp cháy sáng thì giảm hệ số tại điểm đó để giữ tỉ lệ màu
    mx = a.max(axis=2, keepdims=True)
    kk = np.minimum(k, 1.0 / np.maximum(mx, 1e-3))
    out = np.clip(a * kk, 0, 1)
    Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(dst, "JPEG", quality=86, optimize=True, progressive=True)
    return k


def tach_gia(dong):
    """'Sơn gel | 150.000đ', 'Sơn gel: 150k', 'Sơn gel - 150.000đ', 'Sơn gel 150k' -> (tên, giá). Không đọc được -> None."""
    dong = dong.strip()
    if not dong:
        return None
    if "|" in dong:
        a, b = [x.strip() for x in dong.split("|", 1)]
        return (a, b) if a and b else None
    m = re.match(r"^(.*?)[\s:\-–]+(miễn phí|free|liên hệ|tặng kèm)\s*$", dong, re.I)
    if m and m.group(1).strip():
        return (m.group(1).strip(), m.group(2).strip().capitalize())
    m = GIA_SO.match(dong)
    return (m.group(1).strip(), m.group(2).strip()) if m and m.group(1).strip() else None


def doc_gia_chu(text):
    """Trả về (danh sách giá, các dòng không đọc được)."""
    ds, hong = [], []
    for d in text.splitlines():
        if d.strip():
            x = tach_gia(d)
            (ds.append(x) if x else hong.append(d.strip()))
    return ds, hong


def doc_gia(path):
    ds = []
    for dong in Path(path).read_text(encoding="utf-8").splitlines():
        if "|" in dong:
            a, b = [x.strip() for x in dong.split("|", 1)]
            if a and b:
                ds.append((a, b))
    if not ds:
        raise SystemExit("Bảng giá trống: mỗi dòng cần dạng 'Tên dịch vụ | Giá'.")
    return ds


def tao_qr(out, so, url=None):
    """QR in quầy. Chưa có link web thì QR mở thẳng Zalo của tiệm (zalo.me/<số>), dùng được ngay."""
    import segno
    dich = url or f"https://zalo.me/{so}"
    segno.make(dich, error="m").save(out / "qr-dat-lich.svg", scale=10, border=2, dark="#17100e")
    return dich


def tao_tu_dau(t, anh, gia, so, demo=False, cam_ket=False, url=None):
    """Lõi dùng chung: t = thông tin tiệm, anh = danh sách file ảnh, gia = [(tên, giá)], so = số Zalo 10 chữ số."""
    if len(so) != 10:
        raise ValueError("Số Zalo cần đúng 10 chữ số.")
    if len(anh) < 4:
        raise ValueError(f"Cần ít nhất 4 ảnh móng (khuyên dùng 12), mới có {len(anh)}.")
    if not gia:
        raise ValueError("Bảng giá trống.")
    t = dict(t)
    t["zalo"] = f"{so[:4]} {so[4:7]} {so[7:]}"
    t["gia"] = gia
    t["nguon_anh"] = "Ảnh móng: của tiệm"
    t["cam_ket"] = bool(cam_ket)
    t["ghi_chu"] = "Bản demo Nailmark, chưa phải trang chính thức." if demo else ""
    goc = re.sub(r"[^a-z0-9]+", "-", khong_dau(t["ten"])).strip("-")[:40] or "tiem"
    slug, n = goc, 1
    while (ROOT / "nailmark" / "tiem" / slug / "chu.txt").exists() and \
            (ROOT / "nailmark" / "tiem" / slug / "chu.txt").read_text().strip() != so:
        n += 1
        slug = f"{goc}-{n}"  # cùng tên nhưng khác chủ (khác số Zalo) -> đường dẫn riêng, không ghi đè
    out = ROOT / "nailmark" / "tiem" / slug
    moi = not out.exists()
    (out / "img").mkdir(parents=True, exist_ok=True)
    (out / "chu.txt").write_text(so)
    he_so, t["anh"] = [], []
    for i, p in enumerate(anh[:12], 1):
        ten = f"img/mau-{i:02d}.jpg"
        try:
            he_so.append(chinh_anh(p, out / ten))
        except Exception:
            if moi:
                shutil.rmtree(out, ignore_errors=True)  # không để lại thư mục dở dang
            raise ValueError(f"Ảnh số {i} bị hỏng hoặc không phải ảnh. Chị chụp lại hoặc chọn ảnh khác.")
        t["anh"].append(ten)
    for k, _ in DIP:  # bộ sưu tập theo dịp: hiện vẫn là ảnh mẫu Nailmark
        shutil.copy(ROOT / "nailmark" / "img" / f"bst-{k}.jpg", out / "img" / f"bst-{k}.jpg")
    html = tao(t)
    if not t["ghi_chu"]:
        html = html.replace("<div class=note></div>\n", "")
    (out / "index.html").write_text(html, encoding="utf-8")
    qr = tao_qr(out, so, url)
    return dict(slug=slug, thu_muc=str(out.relative_to(ROOT)), so_anh=len(t["anh"]), so_gia=len(gia),
                he_so=(round(min(he_so), 2), round(max(he_so), 2)), qr=qr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--maps", help="tên tiệm + quận, hoặc link Google Maps (tốn 1 lượt Places)")
    ap.add_argument("--ten"); ap.add_argument("--dia-chi", default=""); ap.add_argument("--gio", default="Giờ mở cửa: tiệm bổ sung")
    ap.add_argument("--anh", required=True, help="thư mục ảnh móng thật của tiệm")
    ap.add_argument("--gia", required=True, help="file bảng giá")
    ap.add_argument("--zalo", required=True)
    ap.add_argument("--demo", action="store_true", help="ghi dải 'bản demo' ở đầu trang")
    ap.add_argument("--url", help="link web của tiệm khi đã có hosting; chưa có thì QR mở Zalo")
    ap.add_argument("--cam-ket", action="store_true", help="chỉ bật khi tiệm XÁC NHẬN đúng: giá trọn gói, hấp tiệt trùng, bảo hành 10 ngày")
    g = ap.parse_args()

    so = re.sub(r"\D", "", g.zalo)
    anh = sorted(p for p in Path(g.anh).iterdir() if p.suffix.lower() in DUOI)[:12]

    if g.maps:
        from tu_dong_demo import cau_hinh, tim, truy_van
        t = cau_hinh(tim(truy_van(g.maps)))
    elif g.ten:
        t = dict(ten=g.ten, khau_hieu="Móng đẹp chuẩn Nailmark", dia_chi=[g.dia_chi], gio=g.gio, sao="", danh_gia="",
                 maps="", dich_vu=["Sơn gel", "Nail art", "Đắp gel, nối móng", "Chăm sóc tay chân"], ghi_chu="")
    else:
        raise SystemExit("Cần --maps hoặc --ten.")
    try:
        kq = tao_tu_dau(t, anh, doc_gia(g.gia), so, demo=g.demo, cam_ket=g.cam_ket, url=g.url)
    except ValueError as loi:
        raise SystemExit(str(loi))
    print(f"Đã tạo {kq['thu_muc']}/index.html · {kq['so_anh']} ảnh · {kq['so_gia']} dòng giá · "
          f"hệ số sáng {kq['he_so'][0]}–{kq['he_so'][1]} · QR -> {kq['qr']}")


if __name__ == "__main__":
    main()
