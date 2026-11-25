# Kế hoạch triển khai: tiếp cận tiệm trên Google Maps

## 1. Địa bàn

**Đợt 1 (ưu tiên):** Quận 1, Quận 3, Quận 10, Quận 2 (Thảo Điền, An Phú). Tên quận cũ; từ 1/7/2025 TP.HCM không còn cấp quận.
- Tiệm dày, khách chi tiêu cao, nhiều tiệm và chuỗi đủ sức mua gói lớn (Hệ thống, App 15–100 triệu).
- Ở khu trung tâm, nhiều tiệm đã có agency làm. Tiệm nào điểm cao thì chào thẳng trang đặt lịch, gói Chuyển giao hoặc App, không chào gói 500.000đ.

**Đợt 2:** Phú Nhuận, Bình Thạnh, Tân Bình, Gò Vấp.

**Sau đó:** Quận 7, rồi Hà Nội.

## 2. Ngành đợt 1

Spa, nail, thẩm mỹ · Nha khoa · Rửa xe, gara ô tô · Nhà hàng. Cả bốn ngành đều cần **trang đặt lịch**.

## 3. Quy trình mỗi ngày

| Bước | Ai | Việc |
|---|---|---|
| 1 | AI | Quét tiệm mới (`scripts/scan_places.py`), chấm điểm sơ bộ, đưa vào CRM |
| 2 | AI | Xem thêm website, fanpage của tiệm, chấm nốt các hạng mục còn thiếu, ghi điểm yếu |
| 3 | AI | Làm mẫu riêng cho tiệm nhóm A/B: ảnh trước–sau, video 15 giây, trang đặt lịch mẫu |
| 4 | AI | Soạn tin nhắn riêng cho từng tiệm theo mẫu Z1/E1, ghi vào CRM |
| 5 | AI / người | Email: AI gửi. Zalo: người gửi bấm link Zalo trong CRM, dán tin đã soạn |
| 6 | Người gửi | Dán nguyên văn tin tiệm trả lời vào "Nhật ký liên hệ" |
| 7 | AI | Soạn câu trả lời (R1–R6), chốt, gửi QR thanh toán (P1), hướng dẫn cấp quyền (H1) |
| 8 | AI | Sản xuất, bàn giao (B1), báo cáo ngày 14 và chào gói tháng (U1) |
| 9 | Anh Ninh | Duyệt 2–3 đợt gửi đầu tiên. Nhận tiền |

## 4. Nhịp liên hệ

- Tối đa 3 lần: ngày 0 (Z1/E1), ngày +2 (Z2), ngày +7 (Z3). CRM tự tính ngày nhắc.
- Tiệm nói "không" thì dừng ngay, chuyển trạng thái "Dừng liên hệ".
- Ưu tiên trả lời tiệm đã phản hồi trước khi gửi tin mới.

## 5. Chỉ tiêu 5 tuần (đến 31/12/2026)

| Tuần | Tiệm được gửi | Mục tiêu chốt |
|---|---|---|
| 1 | 30 (đợt duyệt) | 3–5 |
| 2–5 | 400–500/tuần | 20–25/tuần |
| Tổng | ~1.800 | ~90 gói đầu + ~25 gói duy trì ≈ 100–110 triệu |

## 6. Cần anh Ninh cung cấp

1. Khoá Google Places API (nhập qua ô bảo mật, không dán vào chat).
2. Kết nối hộp thư Gmail dùng để gửi chào hàng.
3. Tên công ty, tên người ký tin, số Zalo công ty, tài khoản ngân hàng (để làm QR).
4. Email công ty dùng để tiệm thêm làm người quản lý hồ sơ Google Maps.
5. Tài khoản lưu trữ web và tên miền cho landing page và trang đặt lịch.
6. Người gửi Zalo (anh hoặc 1–2 người).

## 7. Tệp trong thư mục

- `crm/CRM_Tiem.xlsx`: CRM gồm danh sách tiệm, chấm điểm, nhật ký liên hệ, mẫu tin nhắn, bảng giá, báo cáo.
- `scripts/build_crm.py`: tạo lại CRM trống.
- `scripts/scan_places.py`: quét tiệm từ Google Places API vào CRM.

## 8. Hệ sinh thái: phễu từ rộng đến sâu

| Bậc | Sản phẩm | Giá | Mục đích |
|---|---|---|---|
| 0 | Phiếu chấm điểm + bản mẫu riêng; hội thảo online "Chủ tiệm tự làm Google Maps đón Tết" | Miễn phí | Mở phễu thật rộng |
| 1 | Lên hình / Lên hạng | 500.000đ – 1 triệu | Khách thấy kết quả, tin mình |
| 2 | Duy trì (làm thay) | 1–3 triệu/tháng | Khách muốn giao hết |
| 3 | Chuyển giao tự làm: đào tạo + bộ công cụ AI + kèm 1:1 | 5–10 triệu | Khách muốn tự chủ, không phụ thuộc |
| 4 | Hệ thống trọn gói: website, đặt lịch, danh sách khách, tự động chăm khách | 15–30 triệu | Tiệm có nhiều khách, muốn sở hữu hệ thống |
| 5 | App riêng cho chuỗi + gói sư tử % hiệu quả | 30–100 triệu | Chuỗi, nhiều chi nhánh, khách lớn |
| + | Bảo trì hệ thống/app | ~500.000đ/tháng | Thu đều sau khi bán gói lớn |

Khách lớn được nhận diện ngay khi quét: từ 300 đánh giá trở lên, nhiều chi nhánh cùng tên, đã có website. CRM tự gắn nhãn "KHÁCH LỚN" và chuyển cho sư tử hoặc anh Ninh đi gặp trực tiếp.
