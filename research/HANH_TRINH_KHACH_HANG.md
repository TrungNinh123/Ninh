# Nailmark – Hành trình khách hàng, từ lúc thấy đến lúc giới thiệu (26/11/2026)

**Mục tiêu:** hành trình tự nhiên, AI vận hành, không cần người. Ở bậc nào, giá trị khách nhận cũng **vượt xa** số tiền bỏ ra, để khách dùng tiếp và giới thiệu cho tiệm khác. Đây là bản nền, sau này mở rộng ra ngành khác và nước khác.

## 1. Bậc thang giá trị (mỗi bậc nhỏ, dễ bước)

| Bậc | Giá | Khách nhận | Giao trong | Vì sao "hời" | Câu mời lên bậc sau |
|---|---|---|---|---|---|
| **0. Quà miễn phí** | 0đ | Thẻ QR đặt lịch, 1 poster Tết, bảng giá đẹp, chỉnh ảnh giữ màu (4 công cụ). Dán link Google Maps thì nhận thêm web mẫu mang tên tiệm và video 12 giây | Ngay | Dùng ngay, không đăng ký | "Muốn trọn bộ Tết mang tên tiệm? 99k" |
| **1. Bộ Tết** | **99.000đ** (đề xuất mới) | 3 poster + 3 story Tết, 2 thẻ quà tặng (300k, 500k) để tiệm bán, bảng giá in quầy, thẻ QR, 10 câu đăng bài, lịch đăng 4 tuần | **~13 giây** sau khi tiền vào | Thuê thiết kế 10 ấn phẩm thường tốn hơn nhiều. Riêng 1 thẻ quà tặng bán được đã gấp 3–5 lần giá bộ | "Trừ 99k khi lên web: mã KHAUTRU99" |
| **2. Web Khởi đầu** | 999.000đ (còn 900.000đ với mã) | Web đặt lịch chạy ngay, 12 ảnh, bảng giá, Zalo, QR, thả file là tự điền | Ngay (mở app) | Năm đầu khoảng 83.000đ/tháng, chưa bằng 1 bộ sơn gel | "Thêm bộ sưu tập 8 dịp: Chuẩn, trả chênh lệch" |
| **3. Chuẩn / Đẳng cấp** | 1,99 / 2,99 triệu | Bộ sưu tập 8 dịp, Google Maps viết sẵn; Đẳng cấp thêm 2 cơ sở, ảnh quà tặng AI | Ngay | Khoảng 166.000–250.000đ/tháng | "Trước mỗi mùa lễ: Gói Mùa" |
| **4. Gói Mùa** (lặp lại) | 1,49 triệu/mùa | Bộ nội dung mùa 8/3, 20/10, Noel… | Ngay | Nguồn lãi chính, mua lại hằng mùa | – |
| **5. Chuyển giao / Làm hộ** | 4,99 / 9,99 triệu | Đào tạo nhân viên, hoặc Nailmark làm toàn bộ rồi chuyển giao 1–2 tháng | Sau gọi xác minh | Thay cả một người làm marketing | – |

## 2. Hành trình 7 chặng (AI lo từng chặng)

| Chặng | Khách nghĩ gì | Nailmark làm gì | Tạo niềm tin bằng | Công cụ | Tình trạng |
|---|---|---|---|---|---|
| **1. Thấy** | "Tiệm mình có đang mất khách không?" | Bài viết, video ngắn nói đúng nỗi đau, có số liệu | Số liệu có nguồn, không hứa suông | Chuỗi 30 bài | Có nội dung, chưa có tài khoản đăng |
| **2. Thấy giá trị** | "Cái này dùng được ngay không?" | Tự chấm 8 tiêu chuẩn; xem web mẫu **mang tên tiệm mình** | Thấy chính tiệm mình trên web mẫu | Trang chính, `qua_tang.py` | Chạy được |
| **3. Dùng miễn phí** | "Thử xem có thật không" | 4 công cụ quà chạy ngay trên trình duyệt | Không đăng ký, ảnh không rời khỏi máy | `cong-cu.html` | Chạy được |
| **4. Tin hơn** | "Có lừa không?" | Ghi rõ cái gì chạy được, cái gì chưa; bảng phạm vi; 17 câu hỏi đáp; AI nhận mình là AI | Minh bạch, cho trước, không hứa số khách | Trang chính, ngân hàng 168 câu | Chạy được |
| **5. Trả 99k** | "Ít tiền, thử luôn" | QR VietQR → tiền vào → giao bộ Tết sau ~13 giây → trang cảm ơn kèm 3 bước tiếp | Giao ngay, đúng như mô tả | `mua.html`, `thanh_toan.py`, `bo_99k.py` | **Chạy được trên máy thử** (giả lập cổng) |
| **6. Lên 999k trở lên** | "Đáng tiền, làm web luôn" | Mã KHAUTRU99 trừ 99k → mở app tạo web điền sẵn → thả file là tự điền → xuất bản → kiểm 8 mục | Không phải làm kỹ thuật; trừ tiền đã trả | `app_tu_lam.py`, `doc_tep.py`, `kiem_tra_web.py` | **Chạy được trên máy thử** |
| **7. Ở lại và giới thiệu** | "Giới thiệu cho tiệm bạn" | Nhắc mùa lễ, Gói Mùa; tiệm bạn nhận quà miễn phí, người giới thiệu được tặng bộ ảnh mùa kế tiếp | Phí năm sau giữ nguyên | Zalo OA | Chưa có Zalo OA. Thưởng giới thiệu **[CHỜ DUYỆT]** |

## 3. Sau khi trả tiền: cảm ơn và bước tiếp theo (tự động)
- **Trên màn hình, ngay khi tiền vào:**
  - Dấu xác nhận, câu "Cảm ơn chị đã tin Nailmark", số tiền, mã đơn.
  - Nút "Mở sản phẩm của tiệm".
  - "Bước tiếp theo" 3 dòng, viết riêng cho từng gói.
- **Bộ 99k:** trang giao hàng có cả 10 ảnh, file zip, 10 câu đăng bài, lịch đăng, mã trừ 99k và lời mời giới thiệu.
- **Gói web:** mở app với tên tiệm điền sẵn. Xuất bản xong, trang "Xong" có 3 việc kèm 3 nút.
- **Đơn từ 3 triệu:** "Nailmark gọi xác minh trong 24 giờ". Cần anh chốt số điện thoại và pháp nhân **[CHỜ DUYỆT]**.
- **Lỗi:** chuyển thiếu tiền thì trang báo và đơn được đánh dấu để xử lý. Cổng báo trùng giao dịch thì bỏ qua. Tin báo sai khoá xác thực thì bị chặn.

## 4. Tự đánh giá: đã tối ưu chưa?
| Tiêu chí | Đánh giá trung thực |
|---|---|
| Bậc nhảy giữa các mức giá | **Đã sửa:** thêm bậc 99k giữa 0đ và 999k; có mã trừ để lên bậc sau |
| Giá trị so với giá | Tốt ở bậc 0, 99k, 999k: giao ngay, nhiều thứ dùng được. **Chưa đo** cảm nhận thật của tiệm |
| Tự vận hành | Phần sản phẩm tự chạy được. **Còn thiếu** cổng thanh toán thật, Zalo OA, hosting |
| Niềm tin | Minh bạch tốt. **Điểm yếu lớn nhất: chưa có danh tính pháp nhân và tiệm mẫu có kết quả thật** |
| Hiệu ứng marketing | Ảnh đẹp, đồng bộ thương hiệu. Mỗi poster, thẻ QR, thẻ quà tặng đều in tên tiệm, không chèn logo Nailmark lên. **Đề xuất:** thêm dòng nhỏ "Thiết kế bởi Nailmark" ở chân poster để lan truyền (cần anh duyệt, vì có tiệm không thích) |
| Rủi ro | Bậc 99k có thể "ăn" mất người lẽ ra mua 999k. Cách chặn: bộ 99k chỉ là ấn phẩm, không có web đặt lịch; mã trừ 99k đẩy khách lên |

**Chỉ số cần đo ngay khi chạy thật:** % người nhận quà mua 99k · % người mua 99k lên 999k trong 30 ngày · % mua mà không hỏi · thời gian từ trả tiền đến lúc web xuất bản · số tiệm được giới thiệu trên mỗi khách.

## 5. Còn cần anh
1. **Chốt bậc 99k** (giá, nội dung, mã trừ 99k).
2. **Cổng thanh toán:** SePay hoặc payOS, kèm tài khoản ngân hàng nhận tiền. Code đã sẵn sàng, chỉ cần điền khoá xác thực.
3. **Hosting, Zalo OA, pháp nhân và số liên hệ để xác minh.**
4. **Thưởng giới thiệu và dòng chữ "Thiết kế bởi Nailmark"** trên ấn phẩm.
