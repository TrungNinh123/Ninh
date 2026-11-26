"""Nailmark – nhận diện mọi loại file tiệm gửi lên và tự đưa vào đúng mục, không bắt tiệm gõ lại.

Nhận: ảnh (JPG, PNG, WEBP, HEIC), Word (.docx), Excel (.xlsx), CSV, PDF, văn bản (.txt).
Trả về cho mỗi file một trong các loại:
  - "anh_mong"  : ảnh móng -> đưa vào lookbook
  - "bang_gia"  : bảng giá (ảnh chụp menu, Word, Excel, PDF...) -> danh sách (tên dịch vụ, giá)
  - "thong_tin" : thông tin tiệm (số Zalo/điện thoại, giờ mở cửa, địa chỉ)
  - "khong_ro"  : không đọc được -> báo rõ lý do, gợi ý cách gửi lại
Ảnh được đọc chữ (OCR tiếng Việt) NGAY TRÊN MÁY CHỦ NAILMARK, không gửi ra dịch vụ bên ngoài.
Chạy thử: python scripts/doc_tep.py <file> [<file> ...]
"""
import csv
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tao_web import tach_gia  # noqa: E402

ANH = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}
SO_DT = re.compile(r"(?<!\d)(0\d{2,3}[\s.\-]?\d{3}[\s.\-]?\d{3,4})(?!\d)")
GIO = re.compile(r"(\d{1,2}\s*[:hH]\s*\d{0,2})\s*(?:-|–|đến|tới|~)\s*(\d{1,2}\s*[:hH]\s*\d{0,2})")
DIA_CHI = re.compile(r"(?i)\b(đường|phường|quận|p\.|q\.|tp\.?|thành phố|hẻm|lầu|tầng)\b")
GIA_SO = re.compile(r"\d[\d.,]*\s*(k|K|đ|vnđ|VNĐ|vnd|nghìn|ngàn|tr)\b|\d{2,3}[.,]000")


def lam_sach_dong(d):
    d = d.replace("…", "...").strip(" \t|•*-–_")
    d = re.sub(r"\s*[.·_]{3,}\s*", " | ", d)  # "Sơn gel ........ 150k" -> "Sơn gel | 150k"
    return re.sub(r"\s{2,}", " ", d).strip()


def doc_gia_tu_dong(dongs):
    gia = []
    for d in dongs:
        d = lam_sach_dong(d)
        if len(re.sub(r"[^A-Za-zÀ-ỹ]", "", d)) < 2 or not GIA_SO.search(d) and "miễn phí" not in d.lower():
            continue
        x = tach_gia(d)
        if x and 2 <= len(x[0]) <= 60:
            ten = re.sub(r"[\s.,:;|\-–‹›<>'\"`~_]+$", "", x[0]).strip()
            gia_ = re.sub(r"^[^\w+]+", "", x[1]).strip()  # bỏ ký tự rác OCR trước giá: '---‹ 190.000đ' -> '190.000đ'
            if ten and gia_:
                gia.append((ten, gia_))
    return gia


def chuan_gio(g):
    """'9h' -> '09:00', '21h30' -> '21:30', '9:00' -> '09:00'."""
    so = re.findall(r"\d+", g)
    h = int(so[0]); mi = int(so[1]) if len(so) > 1 and so[1] else 0
    return f"{h:02d}:{mi:02d}"


def thong_tin_tu_chu(text):
    tt = {}
    m = SO_DT.search(text)
    if m:
        tt["zalo"] = re.sub(r"\D", "", m.group(1))
    m = GIO.search(text)
    if m:
        tt["gio"] = f"{chuan_gio(m.group(1))}–{chuan_gio(m.group(2))} mỗi ngày"
    for d in text.splitlines():
        if DIA_CHI.search(d) and re.search(r"\d", d) and len(d) < 120 and not GIA_SO.search(d):
            tt["dia_chi"] = re.sub(r"(?i)^\s*(địa chỉ|đ/c|dc|address)\s*[:\-]?\s*", "", d).strip(" :-|")
            break
    return tt


def ocr(path):
    from PIL import Image, ImageOps
    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
    except ImportError:
        pass
    im = ImageOps.exif_transpose(Image.open(path)).convert("L")
    if max(im.size) > 1800:
        im.thumbnail((1800, 1800))
    import numpy as np
    if float(np.asarray(im.resize((64, 64))).mean()) < 110:  # nền tối (bảng giá chữ sáng trên nền đen)
        im = ImageOps.invert(im)
    import pytesseract
    return pytesseract.image_to_string(im, lang="vie", config="--psm 6")


def chu_tu_tep(p):
    duoi = p.suffix.lower()
    if duoi in (".txt", ".md"):
        return p.read_text(encoding="utf-8", errors="ignore").splitlines()
    if duoi == ".csv":
        return [" | ".join(c for c in r if c.strip()) for r in csv.reader(io.StringIO(p.read_text(encoding="utf-8-sig", errors="ignore")))]
    if duoi in (".xlsx", ".xlsm"):
        import openpyxl
        wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
        out = []
        for ws in wb.worksheets:
            for r in ws.iter_rows(values_only=True):
                o = [str(c).strip() for c in r if c is not None and str(c).strip()]
                o = [f"{int(float(c)):,}đ".replace(",", ".") if re.fullmatch(r"\d{4,7}(\.0)?", c) else c for c in o]
                if o:
                    out.append(" | ".join(o) if len(o) <= 2 else f"{o[0]} | {o[-1]}")
        return out
    if duoi == ".docx":
        import docx
        d = docx.Document(str(p))
        out = [x.text for x in d.paragraphs if x.text.strip()]
        for t in d.tables:
            for r in t.rows:
                o = [c.text.strip() for c in r.cells if c.text.strip()]
                if o:
                    out.append(" | ".join(dict.fromkeys(o)) if len(o) <= 2 else f"{o[0]} | {o[-1]}")
        return out
    if duoi == ".pdf":
        t = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
        if len(t.strip()) < 20:  # PDF scan: đọc chữ từ ảnh trang đầu
            pre = Path(str(p) + "-trang")
            subprocess.run(["pdftoppm", "-png", "-r", "150", "-f", "1", "-l", "2", str(p), str(pre)], capture_output=True)
            t = "\n".join(ocr(x) for x in sorted(pre.parent.glob(pre.name + "*.png")))
        return [re.sub(r"\s{3,}", " | ", d) for d in t.splitlines()]
    if duoi == ".doc" or duoi == ".xls":
        raise ValueError(f"File {duoi} đời cũ: chị mở lên rồi lưu lại thành .docx/.xlsx, hoặc chụp ảnh màn hình gửi lên.")
    raise ValueError(f"Chưa đọc được định dạng {duoi or 'không đuôi'}.")


def phan_loai(path):
    p = Path(path)
    duoi = p.suffix.lower()
    kq = dict(ten_tep=p.name, loai="khong_ro", gia=[], thong_tin={}, ly_do="")
    try:
        if duoi in ANH:
            text = ocr(p)
            dongs = text.splitlines()
            gia = doc_gia_tu_dong(dongs)
            so_chu = len(re.sub(r"\s", "", text))
            if len(gia) >= 2:
                kq.update(loai="bang_gia", gia=gia, thong_tin=thong_tin_tu_chu(text))
            elif so_chu > 120 and thong_tin_tu_chu(text):
                kq.update(loai="thong_tin", thong_tin=thong_tin_tu_chu(text))
            else:
                kq.update(loai="anh_mong")
            return kq
        dongs = chu_tu_tep(p)
        text = "\n".join(dongs)
        gia = doc_gia_tu_dong(dongs)
        tt = thong_tin_tu_chu(text)
        if gia:
            kq.update(loai="bang_gia", gia=gia, thong_tin=tt)
        elif tt:
            kq.update(loai="thong_tin", thong_tin=tt)
        else:
            kq["ly_do"] = "Không thấy giá hay thông tin tiệm trong file."
    except Exception as e:  # noqa: BLE001
        kq["ly_do"] = str(e) if isinstance(e, ValueError) else "File bị hỏng hoặc không mở được."
    return kq


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(json.dumps(phan_loai(f), ensure_ascii=False))
