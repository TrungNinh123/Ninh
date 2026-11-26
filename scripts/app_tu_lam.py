"""Nailmark App v1 – chủ tiệm tự tạo web trong 4 bước (chạy thật, không có người làm hộ).

Chạy: python scripts/app_tu_lam.py   rồi mở http://localhost:8080
- Bước 1: tên tiệm + quận (hoặc link Google Maps) -> AI/Places điền sẵn. Có thể bỏ qua Google, tự gõ tên và địa chỉ.
- Bước 2: tải 4–12 ảnh móng thật -> cắt 3:4, chỉnh sáng giữ màu.
- Bước 3: bảng giá, mỗi dòng "Tên | Giá". (AI đọc bảng giá từ ảnh: CHƯA CÓ, chờ kiểm thử Kyma.)
- Bước 4: số Zalo -> xuất bản: web + QR in quầy.
Web tạo ra nằm ở nailmark/tiem/<slug>/ và được phục vụ tại /tiem/<slug>/.
Chưa có: đăng nhập, thanh toán, hosting công khai, tên miền. Chỉ dùng để chạy thử.
"""
import re
import sys
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tao_web import DUOI, doc_gia_chu, tao_tu_dau  # noqa: E402
from web_tiem import ROOT  # noqa: E402

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 120 * 1024 * 1024  # 12 ảnh điện thoại


@app.get("/")
def trang_chu():
    return send_from_directory(ROOT / "nailmark", "app.html")


@app.get("/huong-dan.html")
def huong_dan():
    return send_from_directory(ROOT / "nailmark", "huong-dan.html")


@app.get("/huong-dan-4-buoc.mp4")
@app.get("/huong-dan-bia.jpg")
def huong_dan_tep():
    return send_from_directory(ROOT / "nailmark", request.path.lstrip("/"))


@app.get("/img/<path:p>")
def anh_chung(p):
    return send_from_directory(ROOT / "nailmark" / "img", p)


@app.get("/tiem/<slug>/")
@app.get("/tiem/<slug>/<path:p>")
def web_tiem(slug, p="index.html"):
    return send_from_directory(ROOT / "nailmark" / "tiem" / slug, p)


@app.post("/api/tra-cuu")
def tra_cuu():
    """Bước 1: điền sẵn từ Google Places (tốn 1 lượt, hạn mức 100/ngày)."""
    from tu_dong_demo import cau_hinh, tim, truy_van
    q = (request.json or {}).get("q", "").strip()
    if len(q) < 3:
        return jsonify(loi="Nhập tên tiệm kèm quận, hoặc dán link Google Maps."), 400
    try:
        t = cau_hinh(tim(truy_van(q)))
    except SystemExit as e:
        return jsonify(loi=str(e)), 404
    except Exception:
        return jsonify(loi="Chưa tra được Google lúc này. Chị có thể tự gõ tên và địa chỉ."), 502
    return jsonify(t)


@app.post("/api/doc-tep")
def doc_tep_api():
    """Nhận mọi file (ảnh, Word, Excel, PDF, CSV, TXT), trả về loại và nội dung đã đọc, theo đúng thứ tự gửi lên."""
    from doc_tep import phan_loai
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, fs in enumerate(request.files.getlist("tep")[:30]):
            p = Path(tmp) / f"{i:02d}{Path(fs.filename or '').suffix.lower()}"
            fs.save(p)
            kq = phan_loai(p)
            kq["ten_tep"] = fs.filename
            out.append(kq)
    return jsonify(out)


@app.post("/api/xuat-ban")
def xuat_ban():
    f = request.form
    ten = f.get("ten", "").strip()
    if not ten:
        return jsonify(loi="Thiếu tên tiệm."), 400
    gia, hong = doc_gia_chu(f.get("gia", ""))
    if hong:
        return jsonify(loi="Chưa đọc được giá ở dòng: " + "; ".join(hong[:3]) + ". Mỗi dòng ghi tên rồi giá, ví dụ: Sơn gel | 150.000đ"), 400
    so = re.sub(r"\D", "", f.get("zalo", ""))
    t = dict(ten=ten, khau_hieu=f.get("khau_hieu") or "Móng đẹp chuẩn Nailmark", dia_chi=[f.get("dia_chi", "")],
             gio=f.get("gio") or "Giờ mở cửa: tiệm bổ sung", sao=f.get("sao", ""), danh_gia=f.get("danh_gia", ""),
             maps=f.get("maps", ""), dich_vu=[], ghi_chu="")
    with tempfile.TemporaryDirectory() as tmp:
        anh = []
        for i, fs in enumerate(request.files.getlist("anh")[:12]):
            duoi = Path(fs.filename or "").suffix.lower()
            if duoi not in DUOI:
                return jsonify(loi=f"Ảnh số {i + 1} có định dạng {duoi or 'lạ'}, chưa nhận. Chị chọn ảnh JPG, PNG hoặc ảnh iPhone."), 400
            p = Path(tmp) / f"{i:02d}{duoi}"
            fs.save(p)
            anh.append(p)
        try:
            kq = tao_tu_dau(t, anh, gia, so, demo=True)
        except ValueError as e:
            return jsonify(loi=str(e)), 400
        except Exception:
            app.logger.exception("xuat-ban")
            return jsonify(loi="Có lỗi khi tạo web. Chị thử lại; nếu vẫn lỗi, gửi câu hỏi vào buổi hỏi đáp tuần này."), 500
    kq["link"] = f"/tiem/{kq['slug']}/"
    kq["qr_svg"] = f"/tiem/{kq['slug']}/qr-dat-lich.svg"
    return jsonify(kq)



# ---------------- Thanh toán và giao hàng tự động ----------------
import os  # noqa: E402
import threading  # noqa: E402

import thanh_toan as tt  # noqa: E402


@app.get("/mua")
def trang_mua():
    return send_from_directory(ROOT / "nailmark", "mua.html")


@app.post("/api/don")
def api_tao_don():
    j = request.json or {}
    so = re.sub(r"\D", "", j.get("zalo", ""))
    if len((j.get("ten") or "").strip()) < 2 or len(so) != 10:
        return jsonify(loi="Cần tên tiệm và số Zalo 10 chữ số."), 400
    try:
        don = tt.tao_don(j.get("goi", ""), j["ten"].strip(), so, j.get("ma_giam", ""), ma_gt=j.get("gt", ""))
    except ValueError as e:
        return jsonify(loi=str(e)), 400
    return jsonify(don_cong_khai(don))


def don_cong_khai(don):
    tk = tt.tai_khoan()
    return dict(ma=don["ma"], goi=don["goi"], ten_goi=don["ten_goi"], so_tien=don["so_tien"], giam=don["giam"],
                trang_thai=don["trang_thai"], giao=don.get("giao"), xac_minh=don["xac_minh"], giam_gt=don.get("giam_gt", 0),
                ma_gt_cua_toi=tt.ma_gioi_thieu(don["zalo"]) if don["trang_thai"] in ("da_tra", "cho_xac_minh") else None, qr=f"/api/don/{don['ma']}/qr.svg",
                ngan_hang=dict(stk=tk["stk"], ten=tk["ten"], mau=tk["mau"]), dev=os.environ.get("NAILMARK_DEV") == "1")


@app.get("/api/don/<ma>")
def api_don(ma):
    don = tt.lay_don(ma)
    return (jsonify(don_cong_khai(don)) if don else (jsonify(loi="Không có đơn."), 404))


@app.get("/api/don/<ma>/qr.svg")
def api_qr(ma):
    import segno
    don = tt.lay_don(ma)
    if not don:
        return "", 404
    import io
    b = io.BytesIO(); segno.make(don["qr"], error="m").save(b, kind="svg", scale=8, border=2, dark="#17100e")
    return app.response_class(b.getvalue(), mimetype="image/svg+xml")


def giao_hang(don):
    """Giao ngay khi tiền vào. Bộ 99k: tạo bộ ảnh; gói web: mở app tạo web (điền sẵn tên tiệm)."""
    ma = don["ma"]
    if don["trang_thai"] != "da_tra":
        return
    if don["goi"] == "bo-tet-99k":
        tt.cap_nhat(ma, giao_trang_thai="dang_tao")
        from bo_99k import tao
        out = tao(dict(ten=don["ten_tiem"]), don["zalo"], [("Sơn gel trơn", "150.000đ"), ("Sơn gel + vẽ Tết", "190.000đ"),
                                                          ("Đắp gel, nối móng", "350.000đ"), ("Chăm sóc chân", "120.000đ")])
        tt.cap_nhat(ma, giao=f"/bo99/{out.name}/", giao_trang_thai="xong")
    elif don["goi"] in ("khoi-dau", "chuan", "dang-cap"):
        from urllib.parse import quote
        tt.cap_nhat(ma, giao=f"/?don={ma}&q={quote(don['ten_tiem'])}", giao_trang_thai="xong")
    else:
        tt.cap_nhat(ma, giao_trang_thai="cho_bat_dau")


@app.get("/api/gioi-thieu/<ma>")
def api_gioi_thieu(ma):
    tk = tt.thong_ke_gt(ma)
    return jsonify(tk) if tk else (jsonify(loi="Mã giới thiệu chưa có hoặc chưa kích hoạt."), 404)


@app.get("/gioi-thieu")
def trang_gioi_thieu():
    return send_from_directory(ROOT / "nailmark", "gioi-thieu.html")


@app.post("/api/webhook/sepay")
def webhook_sepay():
    """Tin báo tiền vào từ SePay. Trường dữ liệu theo tài liệu SePay (content, transferAmount, transferType, id) –
    ĐỐI CHIẾU lại tài liệu chính thức khi mở tài khoản."""
    khoa = os.environ.get("SEPAY_API_KEY")
    if not khoa or request.headers.get("Authorization", "") != f"Apikey {khoa}":
        return jsonify(success=False), 401
    j = request.json or {}
    if j.get("transferType", "in") != "in":
        return jsonify(success=True)
    don = tt.ghi_nhan_tien(j.get("content", ""), j.get("transferAmount", 0), j.get("id"))
    if don:
        threading.Thread(target=giao_hang, args=(don,), daemon=True).start()
    return jsonify(success=True)


@app.post("/api/gia-lap/<ma>")
def gia_lap(ma):
    if os.environ.get("NAILMARK_DEV") != "1":
        return "", 404
    don = tt.lay_don(ma)
    if not don:
        return jsonify(loi="Không có đơn."), 404
    d = tt.ghi_nhan_tien(ma, don["so_tien"], f"GIALAP-{ma}")
    if d:
        threading.Thread(target=giao_hang, args=(d,), daemon=True).start()
    return jsonify(ok=True)


@app.get("/bo99/<slug>/")
@app.get("/bo99/<slug>/<path:p>")
def bo99(slug, p="index.html"):
    return send_from_directory(ROOT / "nailmark" / "bo99" / slug, p)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
