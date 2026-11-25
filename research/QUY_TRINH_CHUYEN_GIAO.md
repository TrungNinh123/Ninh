# Nailmark – Quy trình chuyển giao tự động, không cần người (25/11/2026)

**Nguyên tắc:** AI làm mọi khâu. Người chỉ xử lý **3 ngoại lệ**:
1. Lỗi thanh toán.
2. Khiếu nại.
3. Xác minh đơn từ 3 triệu.

**Cách đọc bảng:** mỗi khâu ghi rõ khi nào bắt đầu, AI làm gì, gửi gì cho khách, công cụ nào, tình trạng hiện nay.

## 1. Mười khâu từ người lạ đến khách quay lại

| # | Khâu | Bắt đầu khi | AI làm gì | Khách nhận gì | Công cụ | Tình trạng 25/11 |
|---|---|---|---|---|---|---|
| 1 | **Thấy Nailmark** | Lịch đăng bài | Đăng chuỗi 30 bài, 10 video ngắn cho chủ tiệm | Bài viết dẫn về "nhận quà miễn phí" | `research/noi_dung/CHUOI_30_BAI.md` | Có nội dung. **Chưa có tài khoản Facebook/TikTok của Nailmark** |
| 2 | **Nhận quà** | Chủ tiệm mở trang quà | Công cụ chạy ngay trên trình duyệt | Thẻ QR, poster Tết, bảng giá, ảnh đã chỉnh | `nailmark/cong-cu.html` | **Chạy được** |
| 3 | **Nhận web mẫu mang tên tiệm** | Chủ tiệm dán link Google Maps | Tra Google Places, tạo web mẫu, poster, QR, video 12 giây | Trang mở quà riêng | `scripts/qua_tang.py` | **Chạy được trên máy.** Cần hosting để chạy công khai |
| 4 | **Tự tìm hiểu, không cần hỏi** | Chủ tiệm xem bảng giá | (Trang có sẵn) | Bảng so sánh 4 gói, phạm vi, 14 câu hỏi thường gặp, trang hướng dẫn và video | `index.html`, `huong-dan.html` | **Chạy được** |
| 5 | **Còn băn khoăn** | Chủ tiệm nhắn | Trợ lý AI trả lời theo ngân hàng 168 câu và bộ xử lý từ chối | Câu trả lời kèm link đúng video hoặc bước | `research/hoi_dap/`, `research/XU_LY_TU_CHOI.md` | Có nội dung. **Chưa có Zalo OA** |
| 6 | **Thanh toán** | Bấm mua | Tạo mã VietQR theo đơn, tự xác nhận khi tiền về. Đơn dưới 3 triệu: hệ thống tự chạy. Đơn từ 3 triệu: chuyển sang xác minh | Tin xác nhận đơn: gồm gì, không gồm gì | Cổng thanh toán (payOS hoặc tương đương) | **Chưa có cổng** |
| 7 | **Bàn giao** | Tiền về | Gửi link app tự làm, video, trang hướng dẫn | 1 tin Zalo, 3 link | `scripts/app_tu_lam.py`, `huong-dan.html` | App chạy được trên máy thử |
| 8 | **Tự làm web** | Mở app | Kiểm tra lỗi từng bước, báo cách sửa | Web và QR sau 4 bước | `app_tu_lam.py`, `tao_web.py` | **Chạy được** (đã test 10 tình huống lỗi) |
| 9 | **Nhắc nếu bỏ dở** | Ngày 1, 3, 7 chưa xuất bản | Nhắc đúng bước còn thiếu, kèm video của bước đó | Tin Zalo ngắn | Zalo OA | **Chưa có Zalo OA** |
| 10 | **Kiểm chất lượng sau khi xuất bản** | Ngay khi xuất bản | Kiểm tự động: đủ ảnh, bảng giá không trống, QR quét được, web xem tốt trên điện thoại | Tin "Web đạt chuẩn" kèm việc làm tiếp | `scripts/kiem_tra_web.py` | **Chạy được** (25/11): 8 mục, web mẫu đạt 8/8 |
| 11 | **Giữ khách và bán thêm** | Trước mùa lễ 6 tuần, hoặc trước hạn gia hạn 30 ngày | Chào Gói Mùa; nhắc gia hạn với giá cũ giữ nguyên | Tin Zalo | Zalo OA + lịch | **Chưa có** |

## 2. Mẫu tin tự động

**Tin 1 · Xác nhận đơn** (gửi ngay khi tiền về):
> Nailmark đã nhận [số tiền] cho gói [tên gói]. Gói gồm: [3 dòng]. Không gồm: [2 dòng]. Bắt đầu tại: [link app]. Video 30 giây: [link]. Hướng dẫn từng bước: [link]. Kẹt ở bước nào, mục "Gặp lỗi thì làm gì" của bước đó có sẵn cách sửa.

**Tin 2 · Nhắc ngày 1, 3, 7** (chỉ gửi khi chưa xuất bản):
> Web của [tên tiệm] còn thiếu bước [n]: [tên bước]. Video [1–3 phút]: [link]. Làm xong bước này là còn [4−n] bước.

**Tin 3 · Web đạt chuẩn:**
> Web của [tên tiệm] đã lên: [link]. Kiểm tra tự động: [12] ảnh, bảng giá [n] dòng, QR quét được. Việc tiếp theo: in QR đặt ở quầy, gắn link vào Google Maps (hướng dẫn: [link]).

**Tin 4 · Trước mùa lễ:**
> [Dịp] còn 6 tuần. Bộ [dịp] cho [tên tiệm] gồm bộ sưu tập, 10 bài đăng, ảnh quà tặng cho khách: 1.490.000đ. Hoặc tự làm miễn phí theo video 8: [link].

**Tin 5 · Gia hạn:**
> Web của [tên tiệm] còn 30 ngày nữa đến hạn. Phí duy trì vẫn [499.000đ / 990.000đ] như lúc chị mua, dù giá mới đã tăng. Gia hạn: [mã QR].

## 3. Ba ngoại lệ có người xử lý
| Ngoại lệ | Cách nhận biết | Xử lý | Hạn |
|---|---|---|---|
| Lỗi thanh toán | Tiền về nhưng không khớp mã đơn | Đối soát, xác nhận tay | 24 giờ |
| Khiếu nại | Trợ lý AI thấy từ khoá khiếu nại hoặc đòi hoàn tiền | Chuyển cho người. Chính sách hoàn tiền **[CHỜ DUYỆT]** | 24 giờ |
| Đơn từ 3 triệu | Gói Chuyển giao, Làm hộ, Đồng hành theo quý, chuỗi | Một cuộc gọi xác minh. Số điện thoại, email, pháp nhân **[CHỜ DUYỆT]** | Trước khi bắt đầu làm |

## 4. Tình trạng tổng: còn thiếu gì để chạy không người
| Thiếu | Ai làm | Ảnh hưởng |
|---|---|---|
| Hosting công khai (chạy app, web tiệm, trang quà) | Anh mở tài khoản, em triển khai | Khâu 3, 7, 8 mới chạy được với khách thật |
| Cổng thanh toán QR tự xác nhận | Anh đăng ký doanh nghiệp | Khâu 6 |
| Zalo OA | Anh đăng ký | Khâu 5, 9, 11 |
| Tài khoản Facebook/TikTok của Nailmark | Anh tạo, hoặc giao quyền | Khâu 1 |
| Số điện thoại, email, pháp nhân | Anh chốt | Ngoại lệ 3; mở bán gói từ 3 triệu |
| Kyma API key | Anh thêm trong cài đặt môi trường | AI đọc bảng giá từ ảnh, giọng đọc video, trợ lý AI |
