# 10.000DN-1M-2027-TEAM SƯ TỬ – Bàn giao sang hội thoại mới (cập nhật 25/11/2026, chiều)

Tên dự án và tên hội thoại: **10.000DN-1M-2027-TEAM SƯ TỬ**

Thư mục Google Drive: **10.000DN-1M-2027-TEAM SƯ TỬ** – https://drive.google.com/drive/folders/1NzC_JwBeTQpwoGHzzZYWfgptvlsMAqXG

## 0. Lời nhắn mở đầu dán vào phiên mới

> Đọc file BAN_GIAO_PHIEN_MOI.md và làm tiếp từ mục 3 "SẮP LÀM". Em là team sư tử, tự điều phối; chỉ hỏi anh khi cần duyệt. Lưu mọi tài liệu mới vào thư mục Drive "10.000DN-1M-2027-TEAM SƯ TỬ".

## 1. ĐÃ LÀM

**Mô hình đã chốt**
- MREAL giúp tiệm nhỏ làm marketing đa kênh, dùng AI để làm rẻ. Người ký tin: **Phương Thư – MREAL**.
- Nâng tiệm từ **2–5 điểm lên 6–8 điểm**, chi phí ở mức tiệm 3–4 điểm. Bỏ 1 đồng thu về khoảng 2 đồng. **Thước đo cuối cùng là số đơn đặt lịch.**
- **Không nhắm tiệm đã đạt 7–8 điểm.** Chỉ chọn tiệm **còn hoạt động** và **có dấu hiệu chi tiền**.
- Phễu **100 → 30 → 10 → 3**, cộng 5 tiệm đối chứng. Dự đoán được chốt trước khi gửi, sau đó so với kết quả thật để chỉnh thang điểm.
- Bản khám kiểu bác sĩ, theo thứ tự:
  1. Hiện trạng có bằng chứng theo từng kênh.
  2. Tiệm dẫn đầu ở Việt Nam và thế giới đang làm gì.
  3. Bản demo dựng sẵn mang tên tiệm.
  4. Lộ trình 3 ngày → 6 tháng.
  5. Chi phí.
- Bảng giá:

  | Gói | Giá |
  |---|---|
  | Khởi động 3 ngày | 500.000đ |
  | Tăng tốc | 2–3 triệu/tháng |
  | Đại sứ AI (ghi rõ là AI) | +2 triệu/tháng |
  | Chuyển giao tự làm | 5–10 triệu |
  | Hệ thống | 15–30 triệu |
  | App | 30–100 triệu |

- Hướng dài hạn: hiểu thật sâu ngành nail, rồi **MREAL tự mở tiệm nail**.

**Dữ liệu và phân tích**
- Quét Google Maps 100 tiệm spa, nail, thẩm mỹ ở Quận 1. Trong đó có **29 tiệm nail** (đã gộp chi nhánh trùng).
- Nghiên cứu top ngành nail Việt Nam (`research/NGHIEN_CUU_NGANH_NAIL.md`).
- Nghiên cứu **hình mẫu thế giới** (`research/hinh_mau_the_gioi.json`): Paintbox, Sundays, Chillhouse, Vanity Projects, kèm 10 quy luật áp dụng được.
- **Khám 11 kênh cho 15 tiệm** (`crm/kham_nail_v1.json`). Mỗi kênh có link, số theo dõi, từ khoá đã tìm và nguồn.
- **Chấm website** theo 10 tiêu chí, có xem bằng mắt trên điện thoại (`crm/audit_web_v1.json`):

  | Tiệm | Điểm website |
  |---|---|
  | DANY | 8 |
  | Fleur | 8 |
  | Zeni | 8 |
  | A+ | 4 |
  | **My Doris** | **0 (web không mở được)** |
  | **Ther Nail** | **0 (web không mở được)** |

- **Xếp hạng v2** (`crm/du_doan_nail_v2.json`):
  - Ứng viên trong vùng 2–5 điểm: DANY, Ther Nail, My Doris, A+, February, Zeni, Dami, Nail Districts, Fleur.
  - Loại: Lisa, Cosie, Mina (đã dẫn đầu); Uni Beauty, Sobek, Atelier (chưa chắc đúng tiệm).

**Sản phẩm đã đăng (riêng tư; anh bật Share mới gửi được cho tiệm)**
- **Bộ demo My Doris** (landing page, lưới Instagram, Pinterest, học từ thế giới): https://claude.ai/artifact/3dF4dvsVfCnHYRUcuAsGY4
- Bản khám My Doris: https://claude.ai/artifact/KkjLZgk3rXwmq2kKMJNfbj
- Bản khám DANY: https://claude.ai/artifact/1joYNbLGsSksQiAJ9Nbqt2
- Bản khám Uni Beauty: https://claude.ai/artifact/EPQ5KNqpAXpNBm45fahTyL
- Trang đặt lịch mẫu: https://claude.ai/artifact/M5w8i2EpnrFqABKht2mLNw

**Chưa gửi tin cho tiệm nào.**

## 2. ĐANG LÀM (dừng ở đây)

- **Chờ anh Ninh duyệt bộ demo My Doris**: hướng thiết kế, nội dung, giá.
- Bản khám v2 của 15 tiệm đã có điểm website thật. **Chưa ghép phần "hình mẫu thế giới + demo"** vào bản khám (bản khám v3).

## 3. SẮP LÀM (theo thứ tự)

1. **Ther Nail:** kiểm tra tiệm còn hoạt động không (website lỗi, có video "bóc phốt", một nguồn ghi đã đóng cửa). Nếu đã đóng thì loại.
2. **Dựng bộ demo** cho các tiệm còn lại trong vùng 2–5 điểm: Nail Districts, February, Dami, A+ (rồi Zeni, Fleur, DANY nếu cần). Ảnh phải là ảnh thật của tiệm; giá lấy theo bảng giá của tiệm.
3. **Bản khám v3** gồm hiện trạng có bằng chứng, hình mẫu thế giới, demo của tiệm, lộ trình và giá (sửa `scripts/ban_kham.py`).
4. **Kênh mạng xã hội:** chấm chất lượng bài đăng (tần suất, ảnh, tương tác). Cần người mở tay trên điện thoại (khoảng 3 phút/tiệm) hoặc Claude in Chrome.
5. Anh Ninh duyệt và bật Share. **Gửi vòng 1 cho 5–7 tiệm**: Zalo do người gửi, email do AI.
6. Theo dõi phản hồi trong CRM. Sau 7–14 ngày, chạy vòng học: so dự đoán v1/v2 với kết quả thật, chỉnh thang điểm.
7. Quét thêm tiệm nail các quận khác khi đủ hạn mức Google (100 lượt/ngày, mở lại khoảng 15h giờ VN).

## 4. Hạ tầng và giới hạn

- **Môi trường "Mặc định":**
  - Khoá Google Places nằm ở Network secrets (host `places.googleapis.com`, header `X-Goog-Api-Key`).
  - Mạng đã cho phép website các tiệm: mydorisnail.com, thernailspace.com, fleurbeauty.vn, zeninailspa.com, acongstudio.wordpress.com, haiyen2dt-hue.github.io (kèm bản www). Muốn mở thêm website tiệm khác thì thêm vào Allowed domains.
- **Google Places:** 100 lượt tìm/ngày và giới hạn theo phút. Không trả ảnh và đánh giá. Công cụ quét đã tự gọi chậm và tự thử lại khi bị giới hạn.
- **Facebook, Instagram, TikTok:** bắt đăng nhập, cần người xem tay hoặc Claude in Chrome.
- **GitHub đẩy lên bị lỗi 403:** kết nối lại tại claude.ai/connect-github. Trong lúc chờ, dùng file zip trên Drive.
- **Zalo:** AI không gửi được. Dùng link `zalo.me/<số>` trong CRM.

## 5. Tệp quan trọng

| Tệp | Nội dung |
|---|---|
| `crm/CRM_Tiem.xlsx` | CRM: danh sách tiệm, chấm điểm, phễu, duyệt tin, báo cáo |
| `crm/leads_q1_spa.json`, `crm/leads_q1_nail.json` | Dữ liệu Google Maps |
| `crm/kham_nail_v1.json`, `crm/audit_web_v1.json` | Khám 11 kênh, chấm website |
| `crm/du_doan_nail_v1.json`, `crm/du_doan_nail_v2.json` | Dự đoán đã chốt |
| `research/` | Nghiên cứu ngành, hình mẫu thế giới, kết quả khám gốc |
| `reports/ban_kham_*.html`, `reports/demo_Q1S044.html` | 15 bản khám, bộ demo |
| `scripts/scan_places.py` | Quét Google (`--nail`; `--thu` = chạy thử, không ghi đè dữ liệu thật) |
| `scripts/funnel.py` | Phễu (`--nail`) |
| `scripts/audit_web.py` | Chấm website |
| `scripts/ban_kham.py` | Tạo bản khám |
| `scripts/import_leads.py`, `scripts/build_crm.py` | Nhập tiệm, tạo CRM |
| `booking/index.html` | Trang đặt lịch mẫu |

## 6. Cách mở lại

1. Mở phiên mới với kho `TrungNinh123/Ninh`, môi trường **"Mặc định"**.
2. Tải **`MREAL_ban_giao_v3.zip`** từ thư mục Drive ở đầu trang, đính kèm vào phiên mới. Zip chứa toàn bộ tệp làm việc (không kèm lịch sử git và ảnh chụp website; ảnh chụp lại bằng Playwright khi cần).
3. Dán lời nhắn ở mục 0.

## 7. Cách anh Ninh muốn làm việc

- Chủ động làm, chỉ hỏi khi cần duyệt. Báo ngắn gọn, rõ ràng.
- Mọi kết luận phải có bằng chứng. Không nói "chưa kiểm tra" mà phải đi kiểm tra.
- Làm thành hệ thống có số đo, áp dụng được trên diện rộng.
- Tập trung: một quận, một ngành, rồi mới mở rộng.
- Cho tiệm thấy **hình mẫu và bản demo của chính họ** trước, rồi mới nói giá.
