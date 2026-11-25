# Nailmark – Kế hoạch tổng, từ 25/11/2026 đến hết Q1/2027

**Mục tiêu giai đoạn này:** có chiến thắng đầu tiên ở TP.HCM trước Tết (Thứ Bảy 6/2/2027, còn 73 ngày), và có số liệu thật để mở bán. Chưa đặt mục tiêu doanh thu.

**Nguyên tắc:**
- Không hứa điều chưa làm được.
- Gói nào có công cụ chạy thật mới mở bán gói đó.
- Không liên hệ tiệm nào khi anh chưa duyệt.

## 0. Cập nhật 25/11 tối: rút ngắn theo câu hỏi của anh "tại sao không xong ngay ngày mai"
- **Phần kỹ thuật đã xong ngay trong tối 25/11:** QR tự động; App v1 tự làm 4 bước chạy thật (khoảng 4 giây từ lúc bấm xuất bản đến khi có web và QR).
- **Phần còn lại không nằm trong tay team:** tiệm trả lời và gửi ảnh, xét duyệt tài khoản Zalo OA và payOS, anh mở hosting và tên miền.
- **Vì vậy: anh duyệt tin nhắn trong ngày 26/11 thì nhắn 5 tiệm luôn ngày 26/11.** Tiệm gửi ảnh ngày nào thì web thật lên ngày đó. Có hosting thì đưa lên mạng trong ngày.

## 1. Bảy mốc

| # | Thời gian | Mốc | Em làm (AI) | Anh làm | Đạt khi |
|---|---|---|---|---|---|
| 0 | 26/11 – 30/11 | **Chuẩn bị** | Tạo QR tự động. Khung máy chủ App v1. Đề xuất nơi hosting. Kiểm thử Kyma (khi có key) | Chốt: Zalo OA, payOS, hosting và tên miền, Kyma key. **Duyệt nhắn 5 tiệm** | Đủ 4 thứ anh chốt |
| 1 | 1/12 – 7/12 | **Chào 5 tiệm** | Gửi tin đã duyệt (qua kênh anh chọn), gửi web demo, theo dõi trả lời | Duyệt từng tin trước khi gửi | **≥ 2/5 tiệm đồng ý thử miễn phí** |
| 2 | 8/12 – 14/12 | **Web v2 cho tiệm thử** (Nailmark làm tay, miễn phí) | Nhận ảnh thật và bảng giá, chạy `tao_web.py`, đăng web, làm QR. Quay 4 video hướng dẫn | Xem và duyệt web trước khi giao | 2 tiệm có web thật, QR đặt ở quầy |
| 3 | 15/12 – 21/12 | **App v1 chạy thật** | Hoàn thiện 4 bước: lưu, xuất bản, gắn thanh toán. Cho 1–2 tiệm mới **tự làm**, em chỉ quan sát và bấm giờ | – | Tiệm tự xuất bản được, **trong ≤ 2 buổi** |
| **Cổng 1** | **22/12** | **Quyết định mở bán** | Báo cáo số liệu: thời gian tự làm, chỗ hay kẹt, lỗi | **Anh quyết** | Có ≥ 3 tiệm có web thật → mở **Khởi đầu và Chuẩn** giá ra mắt. Chưa đủ thì sửa app, lùi 1 tuần |
| 4 | 22/12 – 6/2 | **Mùa Tết** | Cài bộ Tết cho tiệm thử. Chạy phễu: nội dung cho chủ tiệm, web mẫu tự động. Bắt đầu hỏi đáp hằng tuần khi có khách trả tiền | Chủ trì hỏi đáp (hoặc chỉ định người) | Đo được lượt bấm đặt lịch trên web của tiệm thử |
| **Cổng 2** | **8/2 – 28/2** | **Tổng kết Tết** | Báo cáo: lượt đặt lịch trước và sau, đánh giá Google mới, số khách trả tiền, chỗ khách kẹt | **Anh quyết** 3 việc | Có số liệu để: (1) nâng giá hay giữ; (2) làm App v2 Zalo; (3) thử thêm salon tóc |
| 5 | 3/2027 | **Gói Mùa 8/3 + App v2 (Zalo)** | Gói Mùa 8/3 cho khách cũ. Trợ lý AI và nhắc việc qua Zalo OA | – | Tỷ lệ khách web mua tiếp Gói Mùa (chỉ số lợi nhuận chính) |

## 2. Bốn việc anh cần chốt trước Chủ Nhật 30/11
Không có 4 việc này thì mốc 1 chưa chạy được.

1. **Kênh liên hệ của Nailmark:** số Zalo hoặc Zalo OA để nhắn tiệm và hỗ trợ.
2. **Duyệt danh sách 5 tiệm và 2 tin nhắn** (`research/DOT_1_HCM.md`).
3. **Kyma API key:** anh tự thêm trong cài đặt môi trường, mục Network secrets.
4. **Thanh toán và hosting:** tài khoản payOS hoặc tương đương. Có thể để đến mốc 3 (15/12).

## 3. Chỉ số đo
| Chỉ số | Mục tiêu đặt ra (giả định, đo để kiểm chứng) |
|---|---|
| Tiệm đồng ý thử / số tiệm được nhắn | ≥ 2/5 |
| Thời gian tiệm tự tạo xong web | ≤ 2 buổi |
| Tỷ lệ tiệm tự xuất bản trong 7 ngày | ≥ 80% |
| Lượt bấm "Đặt lịch" trên web tiệm thử mỗi tuần | Đo nền trước, so sau Tết |
| Đánh giá Google mới mỗi tiệm thử trong mùa Tết | Đo nền trước, so sau Tết |
| Số tiệm trả tiền trước Cổng 2 | Chưa đặt. Đặt sau Cổng 1 khi có tỷ lệ chuyển đổi thật |

## 4. Rủi ro lớn nhất và cách chặn
| Rủi ro | Chặn bằng |
|---|---|
| Chậm chốt 4 việc, lỡ mùa Tết | Hạn chót 30/11. Nếu trễ, bỏ bớt: Tết chỉ làm web v2 tay cho tiệm thử, chưa mở bán |
| Tiệm không đồng ý thử | Danh sách còn 53 tiệm TP.HCM khác đủ điều kiện (`crm/tiem_nen_tiep_can.csv`). Đổi lời chào, không đổi giá |
| Tiệm tự làm không nổi trong 2 buổi | Không thêm người hỗ trợ. Sửa video và công cụ ở đúng bước bị kẹt (đo ở mốc 3) |
| Hứa quá khả năng | Trang bán hàng ghi "Sắp mở". Chỉ mở gói khi công cụ của gói đó đã chạy (`research/SAN_SANG_THUC_TE.md`) |

## 5. Chưa làm trong giai đoạn này (cố ý gác lại)
- Hà Nội, các tỉnh khác.
- Salon tóc và thú cưng: xem lại ở Cổng 2.
- App iOS và Android: chỉ khi có trên 1.000 tiệm.
- Chạy quảng cáo trả tiền.
