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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
