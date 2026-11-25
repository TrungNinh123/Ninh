# Nailmark – Kiểm kê: dịch vụ nào làm được thật, đến đâu (25/11/2026)

**Nguyên tắc (anh Ninh):** không hứa điều chưa làm được. Mỗi dịch vụ chỉ được **bán** khi đã ở mức "Chạy được".

**Ba mức:**
- **Chạy được:** đã chạy thật, có bằng chứng.
- **Làm tay được:** có công cụ, nhưng phải có người của Nailmark chạy, khách chưa tự làm được.
- **Chưa có:** mới là kế hoạch hoặc bản chạy thử giao diện.

## 1. Bảng kiểm kê

| Dịch vụ / tính năng đã ghi trên trang bán hàng | Mức hiện tại | Bằng chứng / còn thiếu gì |
|---|---|---|
| Lấy thông tin tiệm từ Google Maps (tên, địa chỉ, giờ, sao, SĐT) | **Chạy được** | `scripts/tu_dong_demo.py`, đã thử với ELIZ và Charming. Hạn mức Places 100 lượt/ngày |
| Web của tiệm theo chuẩn Nailmark, xem tốt trên điện thoại | **Chạy được** (web phiên bản 1, ảnh mẫu) | `scripts/web_tiem.py`. Đã kiểm 390px và 1280px, không tràn |
| Web với **ảnh thật và bảng giá thật** của tiệm (web phiên bản 2) | **Làm tay được** | `scripts/tao_web.py` (mới, 25/11). Đã thử với tiệm mẫu: 12 ảnh, 5 dòng giá. Người của Nailmark phải chạy lệnh |
| Chỉnh sáng ảnh, **không đổi màu móng** | **Chạy được** | Trong `tao_web.py`: nhân một hệ số chung cho cả 3 kênh màu. Đo được: sắc độ trước 16,8°, sau 16,6° |
| AI đọc bảng giá từ ảnh chụp | **Chưa có** | Chưa kiểm thử. Cần Kyma API key. Hiện bảng giá phải gõ vào file |
| App tự làm 4 bước (khách tự tải ảnh, tự xuất bản) | **Chưa có** | `nailmark/tu-lam.html` mới là giao diện chạy thử, chưa lưu, chưa xuất bản. Cần máy chủ và hosting |
| Đường dẫn web cho tiệm (hosting) | **Chưa có** | Chưa chọn nơi đăng. Web phiên bản 2 đã là thư mục tĩnh, đăng là chạy |
| Tên miền riêng tự gắn | **Chưa có** | Cần tài khoản nhà đăng ký tên miền. Trước mắt có thể làm tay |
| Đặt lịch qua Zalo trên web | **Chạy được (một phần)** | Nút tạo sẵn tin nhắn để khách tự gửi Zalo. Chưa tự động gửi vào Zalo của tiệm |
| Mã QR in để ở quầy | **Làm tay được** | Tạo QR khi có link web. Chưa tự động |
| Bộ sưu tập 8 dịp | **Chạy được** (ảnh mẫu Nailmark) | Ảnh ghép bằng `anh_tang_khach.py` từ ảnh Pexels. Chưa dùng ảnh thật của tiệm |
| Bộ Tết 2027 (nội dung, lịch 10 tuần, tin Zalo) | **Chạy được** (nội dung) | Artifact bộ Tết. Tiệm phải tự đăng |
| Ảnh quà tặng AI cho khách | **Làm tay được** | `anh_tang_khach.py` chạy bằng lệnh. Chất lượng chưa đều (từng bị mờ viền tay; có cơ chế dự phòng). Cần khách đồng ý |
| 4 video hướng dẫn tạo web, 8 video vận hành | **Chưa có** | Mới có kịch bản. Chưa quay, chưa thử giọng đọc tiếng Việt |
| Trợ lý AI 24/7 trên Zalo | **Chưa có** | Có bộ câu trả lời mẫu. Cần Zalo OA và Kyma key |
| Zalo tự nhắc ngày 1, 3, 7 | **Chưa có** | Cần Zalo OA |
| Hỏi đáp trực tuyến 1 buổi/tuần | **Chưa có** | Cần người chủ trì và chốt giờ (đề xuất Thứ Hai 21:15) |
| Thanh toán QR tự xác nhận | **Chưa có** | Cần tài khoản payOS hoặc tương đương (anh mở) |
| Tự sửa web qua form | **Chưa có** | Cần app và máy chủ |
| Đồng hành AI: báo cáo lịch hẹn theo kênh | **Chưa có** | Chưa có cách đo lượt đặt lịch. Cần gắn mã theo dõi vào nút Zalo |
| Chuyển giao: khoá video và bài kiểm tra AI chấm | **Chưa có** | Mới là đề xuất |
| Làm hộ trọn gói 9,9 triệu | **Làm tay được** | Có đủ công cụ cho người làm. Cần người thật và thời gian |
| Mục "Cam kết của tiệm" trên web | **Đã sửa 25/11** | Trước đây hiện sẵn trên mọi web, tức là **hứa thay tiệm**. Nay chỉ hiện khi tiệm xác nhận. Đã tắt ở 5 web demo đợt 1 |

**Kết luận thật:** hôm nay Nailmark **chưa bán tự phục vụ được**. Thứ làm được ngay là **người của Nailmark dùng công cụ để tạo web cho tiệm** (mức "Làm tay được"). Cách này phù hợp để **chạy thử miễn phí với 5 tiệm đợt 1**, chưa phù hợp để thu 999k từ số đông.

## 2. Các phiên bản web và app cần làm để nâng cấp
| Phiên bản | Nội dung | Mở bán gói nào | Cần làm |
|---|---|---|---|
| **Web v1** (đã có) | Web demo tạo từ Google Maps, ảnh mẫu | Không bán, chỉ để chào | Xong |
| **Web v2** (đã có lõi, 25/11) | Ảnh thật, bảng giá thật, chỉnh sáng giữ màu, cam kết chỉ khi tiệm xác nhận | Chạy thử miễn phí với 5 tiệm đợt 1 | Thêm hosting và tạo QR tự động |
| **App v1, tự làm 4 bước** | Khách tự tải ảnh, gõ hoặc chụp giá, nhập Zalo, xuất bản | **Khởi đầu, Chuẩn** (chỉ khi đã chạy thật với ≥ 3 tiệm) | Máy chủ, lưu ảnh, hosting, thanh toán QR, quay 4 video, AI đọc giá (Kyma) |
| **App v2, Zalo** | Zalo OA: trợ lý AI, nhắc việc, báo đơn. Tự sửa web | **Đẳng cấp** (tên miền), **Gói Mùa** | Zalo OA, Zalo Mini App, gắn tên miền tự động |
| **App v3, đo lường** | Đếm lượt đặt lịch theo kênh, báo cáo tháng | **Đồng hành AI** | Mã theo dõi, bảng báo cáo |

**Quy tắc:** trang bán hàng chỉ ghi giá cho gói mà phiên bản tương ứng đã chạy thật. Các gói khác ghi rõ **"Sắp mở"**.

## 3. Việc em làm tiếp (không cần anh)
1. Tạo QR tự động trong `tao_web.py`.
2. Viết khung máy chủ cho App v1, dùng lại `tao_web.py`.
3. Chạy thử Web v2 cho 5 tiệm đợt 1 khi tiệm gửi ảnh thật (chỉ sau khi anh duyệt nhắn tin).

## 4. Cần anh
- Kyma API key: anh tự thêm trong cài đặt môi trường, mục Network secrets.
- Zalo OA, payOS, nơi đặt hosting và tên miền.
