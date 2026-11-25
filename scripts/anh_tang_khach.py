"""Bộ ảnh tặng khách: tách nền ảnh khách (khoe móng) và ghép vào bối cảnh sang trọng.

Nguyên tắc: không đổi mặt, không đổi màu móng; chỉ thay nền và thêm khung, con dấu tiệm.
Cần sự đồng ý của khách trước khi chụp và đăng (ảnh khuôn mặt là dữ liệu cá nhân).

Chạy:  python scripts/anh_tang_khach.py <ảnh_vào> <thư_mục_ra> [--tiem "Tên tiệm"] [--model đường_dẫn.tflite]
Ra:    <tên>_tet.jpg (đỏ son, hoa mai, vòm vàng) và <tên>_lua.jpg (lụa vỏ trứng, tối giản), khổ 1080x1350
Mô hình tách nền: MediaPipe selfie_multiclass_256x256 (Google), chạy trên máy, không gửi ảnh ra ngoài.
"""
import argparse
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
SON, SON2, DEN, VANG, VANG2, TRUNG = (163, 22, 26), (110, 12, 16), (23, 16, 14), (201, 161, 74), (233, 201, 119), (245, 238, 227)


def font(size, bold=True):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def mask_nguoi(path, model):
    import mediapipe as mp
    from mediapipe.tasks import python as mpp
    from mediapipe.tasks.python import vision
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=mpp.BaseOptions(model_asset_path=str(model)), output_confidence_masks=True))
    r = seg.segment(mp.Image.create_from_file(str(path)))
    bg = np.squeeze(r.confidence_masks[0].numpy_view())
    nguoi = np.clip(((1 - bg) - .35) / .3, 0, 1)  # làm sắc viền, tránh bàn tay bị mờ "ma"
    ro = float((nguoi > .5).mean())
    mo = float(((nguoi > .1) & (nguoi < .9)).mean())
    if ro < .12 or mo > .18:  # tách nền kém (ảnh chỉ có tay trên nền rối): giữ nguyên ảnh gốc trong khung
        return Image.new("L", (bg.shape[1], bg.shape[0]), 255)
    m = Image.fromarray((nguoi * 255).astype("uint8"))
    return m.filter(ImageFilter.GaussianBlur(1.2))


def gradient(c1, c2, w, h, cx=.7, cy=.35):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx / w - cx) * 1.2) ** 2 + (yy / h - cy) ** 2)
    t = np.clip(d / 1.0, 0, 1)[..., None]
    arr = np.array(c1) * (1 - t) + np.array(c2) * t
    return Image.fromarray(arr.astype("uint8"))


def vo_trung(im, n, seed, box, color=TRUNG, alpha=(25, 70)):
    rnd = random.Random(seed)
    lay = Image.new("RGBA", im.size)
    d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y, r = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(4, 12)
        k = rnd.randint(4, 6)
        pts = [(x + math.cos(i / k * 6.283 + rnd.random() * .6) * r * rnd.uniform(.6, 1.1),
                y + math.sin(i / k * 6.283 + rnd.random() * .6) * r * rnd.uniform(.6, 1.1)) for i in range(k)]
        d.polygon(pts, fill=color + (rnd.randint(*alpha),))
    im.alpha_composite(lay)


def canh_mai(d, x, y, dai, goc, seed, scale=1.0):
    """Cành mai vàng: thân nâu sơn, hoa 5 cánh vàng."""
    rnd = random.Random(seed)
    pts = [(x, y)]
    for i in range(6):
        goc += rnd.uniform(-.35, .35)
        x += math.cos(goc) * dai / 6
        y += math.sin(goc) * dai / 6
        pts.append((x, y))
    d.line(pts, fill=(58, 30, 20, 255), width=int(10 * scale), joint="curve")
    for (px, py) in pts[1:]:
        for _ in range(2):
            hx, hy = px + rnd.uniform(-38, 38) * scale, py + rnd.uniform(-38, 38) * scale
            r = rnd.uniform(13, 20) * scale
            for k in range(5):
                a = k / 5 * 6.283 + rnd.random()
                cx, cy = hx + math.cos(a) * r * .55, hy + math.sin(a) * r * .55
                d.ellipse([cx - r * .5, cy - r * .5, cx + r * .5, cy + r * .5], fill=(240, 190, 60, 255))
            d.ellipse([hx - r * .22, hy - r * .22, hx + r * .22, hy + r * .22], fill=(190, 90, 20, 255))


def con_dau(size, chu="NAILMARK", duoi="ĐẠT CHUẨN"):
    s = Image.new("RGBA", (size, size))
    d = ImageDraw.Draw(s)
    d.rounded_rectangle([4, 4, size - 4, size - 4], radius=size // 9, fill=(196, 35, 31, 235))
    d.rounded_rectangle([size * .1, size * .1, size * .9, size * .9], radius=size // 14, outline=TRUNG + (255,), width=max(2, size // 40))
    f1, f2 = font(size // 9), font(size // 11)
    d.text((size / 2, size * .26), chu, font=f1, fill=TRUNG, anchor="mm")
    d.text((size / 2, size * .76), duoi, font=f2, fill=TRUNG, anchor="mm")
    w = size * .22
    d.rounded_rectangle([size / 2 - w / 2, size * .36, size / 2 + w / 2, size * .64], radius=int(w / 2), fill=TRUNG)
    return s.rotate(8, resample=Image.BICUBIC, expand=True)


def dat_nguoi(nen, anh, mask, vung):
    """Đặt người vào vùng (x0,y0,x1,y1), canh đáy, giữ tỉ lệ; bóng mềm phía sau."""
    x0, y0, x1, y1 = vung
    bw, bh = x1 - x0, y1 - y0
    ty = mask.getbbox() or (0, 0, *anh.size)
    anh, mask = anh.crop(ty), mask.crop(ty)
    k = min(bw / anh.width, bh / anh.height)
    sz = (int(anh.width * k), int(anh.height * k))
    anh, mask = anh.resize(sz, Image.LANCZOS), mask.resize(sz, Image.LANCZOS)
    px, py = x0 + (bw - sz[0]) // 2, y1 - sz[1]
    bong = Image.new("RGBA", nen.size)
    sh = Image.new("RGBA", sz, (0, 0, 0, 140))
    bong.paste(sh, (px + 18, py + 22), mask)
    nen.alpha_composite(bong.filter(ImageFilter.GaussianBlur(22)))
    nen.paste(anh, (px, py), mask)


def trong_cua_so(nen, anh, mask, hinh, nen_trong):
    """Đặt người vào cửa sổ (mặt nạ hình học `hinh`, cùng cỡ nền): người phủ kín cửa sổ, mép ảnh cụt nằm ngoài cửa sổ."""
    bb = hinh.getbbox()
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    k = max(bw / anh.width, bh / anh.height) * 1.02
    sz = (int(anh.width * k), int(anh.height * k))
    a2, m2 = anh.resize(sz, Image.LANCZOS).convert("RGBA"), mask.resize(sz, Image.LANCZOS)
    px, py = bb[0] + (bw - sz[0]) // 2, bb[3] - sz[1]
    lop = nen_trong.copy()
    bong = Image.new("RGBA", nen.size)
    bong.paste(Image.new("RGBA", sz, (0, 0, 0, 150)), (px + 16, py + 20), m2)
    lop.alpha_composite(bong.filter(ImageFilter.GaussianBlur(20)))
    lop.paste(a2, (px, py), m2)
    nen.paste(lop, (0, 0), hinh)


def kieu_tet(anh, mask, tiem):
    nen = gradient((205, 40, 34), SON2, W, H).convert("RGBA")
    vo_trung(nen, 520, 7, (0, 0, W, H))
    ax0, ay0, ax1, ay1 = 130, 150, 950, H - 150
    hinh = Image.new("L", (W, H))
    ImageDraw.Draw(hinh).rounded_rectangle([ax0, ay0, ax1, ay1 + 400], radius=(ax1 - ax0) // 2, fill=255)
    trong = gradient((150, 22, 24), (70, 8, 10), W, H, .5, .3).convert("RGBA")
    vo_trung(trong, 300, 19, (ax0, ay0, ax1, ay1), VANG2, (20, 55))
    canh_mai(ImageDraw.Draw(trong), ax0 - 40, ay0 + 160, 420, .2, 5, .9)
    trong_cua_so(nen, anh, mask, hinh, trong)
    d = ImageDraw.Draw(nen)
    d.rounded_rectangle([ax0, ay0, ax1, ay1 + 400], radius=(ax1 - ax0) // 2, outline=VANG + (255,), width=12)
    d.rounded_rectangle([ax0 - 22, ay0 - 22, ax1 + 22, ay1 + 400], radius=(ax1 - ax0) // 2 + 22, outline=VANG2 + (150,), width=3)
    canh_mai(d, -30, 250, 380, .5, 3)
    canh_mai(d, W + 30, 110, 360, math.pi - .55, 11, .85)
    d.rectangle([0, H - 150, W, H], fill=DEN + (255,))
    d.line([0, H - 150, W, H - 150], fill=VANG + (255,), width=3)
    d.text((70, H - 104), "Xuân Đinh Mùi 2027", font=font(46), fill=VANG2)
    d.text((70, H - 50), f"Bộ móng Tết tại {tiem}", font=font(28, False), fill=TRUNG)
    cd = con_dau(190)
    nen.alpha_composite(cd, (W - cd.width - 40, H - cd.height - 70))
    return nen.convert("RGB")


def kieu_lua(anh, mask, tiem):
    nen = gradient((248, 242, 233), (226, 210, 190), W, H, .3, .2).convert("RGBA")
    lay = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(lay)
    for i in range(9):
        y = -200 + i * 190
        d.polygon([(0, y), (W, y + 420), (W, y + 520), (0, y + 100)], fill=(255, 255, 255, 38 if i % 2 else 18))
    nen.alpha_composite(lay.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(nen)
    d.ellipse([W - 470, 70, W - 50, 490], fill=SON + (255,))
    cx0, cy0, cx1, cy1 = 90, 170, W - 90, H - 170
    hinh = Image.new("L", (W, H))
    ImageDraw.Draw(hinh).rounded_rectangle([cx0, cy0, cx1, cy1], radius=48, fill=255)
    trong = gradient((240, 230, 216), (205, 186, 160), W, H, .6, .3).convert("RGBA")
    ImageDraw.Draw(trong).ellipse([W - 420, 120, W - 80, 460], fill=SON + (255,))
    trong_cua_so(nen, anh, mask, hinh, trong)
    d = ImageDraw.Draw(nen)
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=48, outline=DEN + (255,), width=3)
    d.text((90, 70), tiem, font=font(48), fill=DEN)
    d.text((90, 128), "Nail lacquer · Xuân 2027", font=font(24, False), fill=(120, 95, 70))
    d.text((90, H - 120), "Chọn mẫu · đặt lịch · quay lại sau 3 tuần", font=font(26, False), fill=(90, 70, 55))
    cd = con_dau(160)
    nen.alpha_composite(cd, (W - cd.width - 50, H - cd.height - 60))
    return nen.convert("RGB")


def hoa_van(d, kieu, seed, mau):
    """Hoạ tiết theo dịp, vẽ ở hai góc trên."""
    rnd = random.Random(seed)
    if kieu == "mai":
        canh_mai(d, -30, 250, 380, .5, 3)
        canh_mai(d, W + 30, 110, 360, math.pi - .55, 11, .85)
    elif kieu == "tim":
        for _ in range(26):
            x, y, r = rnd.choice([rnd.uniform(0, 260), rnd.uniform(W - 260, W)]), rnd.uniform(20, 560), rnd.uniform(10, 30)
            c = mau + (rnd.randint(140, 230),)
            d.ellipse([x - r, y - r, x, y], fill=c); d.ellipse([x, y - r, x + r, y], fill=c)
            d.polygon([(x - r, y - r / 2), (x + r, y - r / 2), (x, y + r)], fill=c)
    elif kieu == "hong":
        for _ in range(14):
            x, y, r = rnd.choice([rnd.uniform(-20, 220), rnd.uniform(W - 220, W + 20)]), rnd.uniform(20, 520), rnd.uniform(26, 46)
            for k in range(4, 0, -1):
                rr = r * k / 4
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=tuple(max(0, c - 22 * (4 - k)) for c in mau) + (255,), outline=(255, 255, 255, 70), width=2)
            d.ellipse([x + r * .4, y + r * .6, x + r * 1.5, y + r * 1.1], fill=(70, 110, 60, 255))
    elif kieu == "tuyet":
        for _ in range(60):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, 640), rnd.uniform(4, 14)
            for k in range(3):
                a = k * math.pi / 3
                d.line([(x - math.cos(a) * r, y - math.sin(a) * r), (x + math.cos(a) * r, y + math.sin(a) * r)], fill=(255, 255, 255, 200), width=2)
    elif kieu == "phao":
        for _ in range(160):
            x, y = rnd.uniform(0, W), rnd.uniform(0, 700)
            w, h = rnd.uniform(6, 14), rnd.uniform(3, 7)
            c = rnd.choice([VANG, VANG2, (255, 255, 255), mau])
            d.rectangle([x, y, x + w, y + h], fill=c + (rnd.randint(120, 230),))
    elif kieu == "sao":
        for _ in range(46):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, 620), rnd.uniform(6, 20)
            c = rnd.choice([VANG2, (255, 255, 255), mau]) + (rnd.randint(150, 240),)
            d.polygon([(x, y - r), (x + r * .25, y - r * .25), (x + r, y), (x + r * .25, y + r * .25), (x, y + r), (x - r * .25, y + r * .25), (x - r, y), (x - r * .25, y - r * .25)], fill=c)
    elif kieu == "nhan":
        for (x, y, r) in [(170, 230, 70), (250, 270, 62)]:
            d.ellipse([x - r, y - r, x + r, y + r], outline=VANG2 + (255,), width=10)
        for _ in range(18):
            x, y, r = rnd.uniform(W - 300, W - 20), rnd.uniform(40, 520), rnd.uniform(14, 26)
            for k in range(6):
                a = k / 6 * 6.283
                cx, cy = x + math.cos(a) * r * .6, y + math.sin(a) * r * .6
                d.ellipse([cx - r * .45, cy - r * .45, cx + r * .45, cy + r * .45], fill=(255, 255, 255, 220))
            d.ellipse([x - r * .25, y - r * .25, x + r * .25, y + r * .25], fill=VANG2 + (255,))


CHU_DE = {
    "tet": dict(c1=(205, 40, 34), c2=SON2, t1=(150, 22, 24), t2=(70, 8, 10), vien=VANG, chu=VANG2, hv="mai", mau=VANG, tieu="Xuân Đinh Mùi 2027", phu="Bộ móng Tết"),
    "valentine": dict(c1=(214, 64, 104), c2=(120, 18, 52), t1=(170, 40, 80), t2=(90, 10, 40), vien=(240, 200, 210), chu=(255, 220, 230), hv="tim", mau=(255, 150, 180), tieu="Valentine 14/2", phu="Bộ móng tình nhân"),
    "8-3": dict(c1=(240, 170, 180), c2=(186, 90, 120), t1=(250, 220, 220), t2=(210, 150, 160), vien=(255, 255, 255), chu=(255, 245, 240), hv="hong", mau=(225, 95, 125), tieu="Mùng 8 tháng 3", phu="Bộ móng tôn vinh phái đẹp"),
    "20-10": dict(c1=(120, 60, 120), c2=(50, 20, 60), t1=(150, 90, 150), t2=(70, 30, 80), vien=VANG2, chu=VANG2, hv="hong", mau=(170, 60, 110), tieu="Ngày 20 tháng 10", phu="Bộ móng phụ nữ Việt Nam"),
    "cuoi": dict(c1=(250, 246, 238), c2=(222, 206, 182), t1=(255, 252, 246), t2=(230, 216, 196), vien=VANG, chu=(110, 80, 40), hv="nhan", mau=VANG, tieu="Tiệc cưới", phu="Bộ móng cô dâu và phù dâu"),
    "cong-ty": dict(c1=(40, 34, 32), c2=(12, 10, 10), t1=(50, 42, 38), t2=(20, 16, 14), vien=VANG, chu=VANG2, hv="phao", mau=VANG, tieu="Sinh nhật công ty", phu="Bộ móng tiệc doanh nghiệp"),
    "sinh-nhat": dict(c1=(236, 196, 176), c2=(176, 110, 96), t1=(248, 226, 212), t2=(214, 160, 140), vien=VANG, chu=(255, 246, 236), hv="phao", mau=(255, 160, 170), tieu="Sinh nhật của nàng", phu="Bộ móng tự thưởng"),
    "doc-than": dict(c1=(70, 30, 90), c2=(22, 10, 36), t1=(96, 50, 120), t2=(36, 16, 56), vien=VANG2, chu=VANG2, hv="sao", mau=(230, 120, 200), tieu="Ngày độc thân 11/11", phu="Bộ móng yêu bản thân"),
    "thang-chuc": dict(c1=(70, 30, 90), c2=(22, 10, 36), t1=(96, 50, 120), t2=(36, 16, 56), vien=VANG2, chu=VANG2, hv="sao", mau=(230, 190, 90), tieu="Ngày thăng chức", phu="Bộ móng thành công"),
    "cuoi-nam": dict(c1=(24, 90, 64), c2=(8, 40, 28), t1=(30, 110, 76), t2=(10, 50, 34), vien=VANG2, chu=(255, 240, 225), hv="tuyet", mau=(200, 30, 40), tieu="Tiệc cuối năm & Noel", phu="Bộ móng tất niên, Giáng sinh"),
    "noel": dict(c1=(24, 90, 64), c2=(8, 40, 28), t1=(30, 110, 76), t2=(10, 50, 34), vien=VANG2, chu=(255, 240, 225), hv="tuyet", mau=(200, 30, 40), tieu="Giáng sinh", phu="Bộ móng Noel"),
    "tot-nghiep": dict(c1=(60, 80, 140), c2=(22, 30, 70), t1=(90, 110, 170), t2=(30, 40, 90), vien=VANG2, chu=VANG2, hv="phao", mau=(160, 190, 255), tieu="Lễ tốt nghiệp", phu="Bộ móng ngày ra trường"),
}


def ve_chu_de(anh, mask, ten, tiem):
    t = CHU_DE[ten]
    nen = gradient(t["c1"], t["c2"], W, H).convert("RGBA")
    vo_trung(nen, 420, hash(ten) % 97, (0, 0, W, H), (255, 255, 255), (12, 40))
    ax0, ay0, ax1, ay1 = 130, 150, 950, H - 150
    hinh = Image.new("L", (W, H))
    ImageDraw.Draw(hinh).rounded_rectangle([ax0, ay0, ax1, ay1 + 400], radius=(ax1 - ax0) // 2, fill=255)
    trong = gradient(t["t1"], t["t2"], W, H, .5, .3).convert("RGBA")
    trong_cua_so(nen, anh, mask, hinh, trong)
    d = ImageDraw.Draw(nen)
    d.rounded_rectangle([ax0, ay0, ax1, ay1 + 400], radius=(ax1 - ax0) // 2, outline=t["vien"] + (255,), width=12)
    d.rounded_rectangle([ax0 - 22, ay0 - 22, ax1 + 22, ay1 + 400], radius=(ax1 - ax0) // 2 + 22, outline=t["vien"] + (130,), width=3)
    hoa_van(d, t["hv"], 5, t["mau"])
    sang = sum(t["c2"]) > 500
    d.rectangle([0, H - 150, W, H], fill=((250, 246, 238) if sang else DEN) + (255,))
    d.line([0, H - 150, W, H - 150], fill=t["vien"] + (255,), width=3)
    d.text((70, H - 104), t["tieu"], font=font(46), fill=t["chu"] if not sang else (110, 80, 40))
    d.text((70, H - 50), f"{t['phu']} · {tiem}", font=font(26, False), fill=TRUNG if not sang else (90, 70, 55))
    cd = con_dau(180)
    nen.alpha_composite(cd, (W - cd.width - 40, H - cd.height - 70))
    return nen.convert("RGB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("vao")
    ap.add_argument("ra")
    ap.add_argument("--tiem", default="Tiệm nail của bạn")
    ap.add_argument("--giu-nen", action="store_true", help="không tách nền, đặt nguyên ảnh vào khung")
    ap.add_argument("--chu-de", default="", help="tet, valentine, 8-3, 20-10, cuoi, cuoi-nam, sinh-nhat, thang-chuc (thêm: doc-than, noel, cong-ty, tot-nghiep)")
    ap.add_argument("--model", default=str(Path(__file__).resolve().parent.parent / "models" / "selfie_multiclass_256x256.tflite"))
    a = ap.parse_args()
    anh = Image.open(a.vao).convert("RGB")
    mask = Image.new("L", anh.size, 255) if a.giu_nen else mask_nguoi(a.vao, a.model)
    out = Path(a.ra)
    out.mkdir(parents=True, exist_ok=True)
    ten = Path(a.vao).stem
    if a.chu_de:
        ve_chu_de(anh, mask, a.chu_de, a.tiem).save(out / f"{ten}_{a.chu_de}.jpg", quality=86)
        print("Đã tạo", out / f"{ten}_{a.chu_de}.jpg")
        raise SystemExit
    kieu_tet(anh, mask, a.tiem).save(out / f"{ten}_tet.jpg", quality=88)
    kieu_lua(anh, mask, a.tiem).save(out / f"{ten}_lua.jpg", quality=88)
    print("Đã tạo", out / f"{ten}_tet.jpg", out / f"{ten}_lua.jpg")
