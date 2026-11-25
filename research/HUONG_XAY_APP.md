# Nailmark – Hướng xây dựng app (25/11/2026)

**Yêu cầu của anh Ninh:** cần có hướng xây app. Anh gợi ý dùng Kyma API (kymaapi.com/models).

**Nguyên tắc sản phẩm đã chốt:**
- Đơn giản hết mức: 4 bước, 4 video, chỉ cần làm theo là xong.
- Không có người làm hộ ở các gói 999k, 1,99 triệu, 2,99 triệu.
- Có 1 buổi hỏi đáp trực tuyến mỗi tuần.
- Toàn bộ nội dung do AI làm.

## 1. Kyma API là gì (đọc trực tiếp từ kymaapi.com ngày 25/11/2026)
- **Cổng gọi AI (gateway):** một key gọi được **118 model**, gồm 83 model ngôn ngữ, 10 model ảnh, 2 model video, 10 model âm thanh, 12 model truy xuất.
- **Tương thích OpenAI và Anthropic SDK.** Base URL `https://kymaapi.com/v1`, xác thực bằng `Authorization: Bearer ky-...`. Nguồn: [llms.txt](https://kymaapi.com/llms.txt), [models](https://kymaapi.com/models.md).
- **Trả theo dùng:** không thuê bao, không phí tối thiểu. Job lỗi được hoàn tiền. Có **$0,50 tín dụng miễn phí**, không cần thẻ, chỉ dùng được cho 48 model rẻ ([pricing](https://kymaapi.com/pricing.md)).
- **Dữ liệu:** Kyma **lưu log yêu cầu, gồm cả nội dung, trong 90 ngày**. Ảnh, video, âm thanh đầu ra lưu 24 giờ ([terms](https://kymaapi.com/terms.md)). Hệ quả: **không gửi ảnh mặt khách lên Kyma** (xem mục 4).
- **Chưa thấy:** cách thanh toán bằng VND. Cần kiểm tra khi mở tài khoản.

## 2. Mỗi việc trong app dùng model nào, tốn bao nhiêu
Giá theo kymaapi.com ngày 25/11/2026, quy đổi theo giá bán ra Vietcombank: 1 USD = 26.020 đ.

| Việc trong app | Cách làm | Model / công cụ | Giá niêm yết | Ước tính mỗi tiệm |
|---|---|---|---|---|
| Bước 1: điền thông tin từ Google Maps | Đã chạy được (`scripts/tu_dong_demo.py`) | Google Places API | đã có key | 1 lượt gọi |
| Bước 2: chỉnh sáng 12 ảnh móng | **Xử lý ảnh thường (PIL), không dùng AI tạo ảnh**, để màu móng giữ đúng thật | không cần model | 0 | 0 đ |
| Bước 3: đọc bảng giá từ ảnh | Model đọc ảnh, giá rẻ | `qwen3.7-flash` (vision) | $0,0435 vào / $0,1886 ra mỗi 1 triệu token | < 100 đ |
| Viết mô tả Google Maps, 10 mẫu trả lời đánh giá | Model chữ | `claude-haiku-5.5` | $0,135 / $0,675 mỗi 1 triệu token | < 300 đ |
| Trợ lý AI trên Zalo (mỗi cuộc hỏi) | Model chữ + thư viện video | `claude-haiku-5.5` | như trên | ~50 đ/cuộc |
| Nền sang trọng cho ảnh quà tặng (theo mùa) | Tạo **một lần mỗi mùa**, dùng chung cho mọi tiệm | `flux-2-pro` | $0,0405/ảnh | ~0 đ (chia đều) |
| Ghép ảnh quà tặng cho khách | **Ghép trên máy chủ của Nailmark** (MediaPipe, đã làm được), không gửi mặt khách đi | không cần model | 0 | 0 đ |
| Giọng đọc 4 video (làm một lần) | Đọc văn bản thành giọng | `minimax-speech-hd` | $0,07/1.000 ký tự | khoảng $0,35 cho cả bộ |

**Kết luận chi phí:** tiền AI cho mỗi web chỉ **khoảng dưới 1.000 đ** (ước tính, cần đo khi chạy thật), trong khi giá bán thấp nhất là 999.000 đ. Như vậy **chi phí AI không phải vấn đề**. Chi phí thật nằm ở hosting, thanh toán, buổi hỏi đáp hằng tuần và kênh tiếp cận khách.

**Cần kiểm thử trước khi chốt model** (dùng $0,50 tín dụng miễn phí):
1. Model có đọc đúng bảng giá viết tay hoặc in bằng tiếng Việt không.
2. Giọng MiniMax đọc tiếng Việt có tự nhiên không. Trang Kyma chỉ ghi "nhiều ngôn ngữ", không ghi rõ có tiếng Việt.
3. Model chữ viết mô tả Google Maps bằng tiếng Việt có đúng giọng tiệm không.

## 3. Lộ trình app 3 giai đoạn
| Giai đoạn | Khi nào | App dạng gì | Vì sao |
|---|---|---|---|
| **1. Web app (PWA)** | 12/2026, chạy thử với 5 tiệm đợt 1 | Biến bản chạy thử `nailmark/tu-lam.html` thành app thật: mở bằng link, thêm được ra màn hình điện thoại, không cần kho ứng dụng | Nhanh nhất, rẻ nhất, sửa được hằng ngày. Kịp cho mùa Tết (Tết rơi vào 6/2/2027) |
| **2. Zalo Mini App + Zalo OA** | Q1/2027 | Mở thẳng trong Zalo. Nhắc việc, trợ lý AI và báo đơn đều qua Zalo | Zalo có **82,6 triệu người dùng mỗi tháng** (quý 3/2026, [CafeF](https://cafef.vn/vng-lai-gap-32-lan-trong-q226-813-trieu-nguoi-dung-zalo-gan-62-trieu-nguoi-choi-game-va-24-trieu-nguoi-su-dung-ai-188260803114510411.chn)). Chủ tiệm dùng Zalo cả ngày |
| **3. App iOS và Android** | Khi có trên 1.000 tiệm | App riêng của Nailmark, và về sau có thể làm app cho khách đặt lịch | Chỉ đáng làm khi đã có quy mô. App trên kho ứng dụng tốn công duyệt và bảo trì |

**Khung kỹ thuật giai đoạn 1 (đề xuất):**
- **Giao diện:** PWA. Đã có bản chạy thử 4 bước.
- **Máy chủ:** Python. Dùng lại các script đã viết: `tu_dong_demo.py`, `web_tiem.py`, `anh_tang_khach.py`, `ty_gia_vcb.py`.
- **AI:** gọi qua Kyma bằng chuẩn OpenAI. Nhờ đó nếu Kyma có sự cố hoặc tăng giá thì đổi sang nhà cung cấp khác chỉ cần đổi base URL.
- **Web của tiệm:** trang tĩnh, mỗi tiệm một đường dẫn Nailmark; tên miền riêng chỉ ở gói Làm hộ.
- **Thanh toán:** cổng QR tự xác nhận như payOS. Cần anh mở tài khoản doanh nghiệp.
- **Lưu ảnh:** trên máy chủ của Nailmark. Ảnh mặt khách không gửi ra ngoài.

## 4. Rủi ro và cách xử lý
| Rủi ro | Cách xử lý |
|---|---|
| Kyma lưu nội dung 90 ngày | Không gửi ảnh mặt khách hay số điện thoại khách. Chỉ gửi ảnh bảng giá và văn bản của tiệm. Ảnh quà tặng ghép tại máy chủ Nailmark |
| AI tạo ảnh làm đổi màu móng hoặc khuôn mặt | Không dùng AI tạo ảnh để chỉnh ảnh móng hay ảnh khách. AI tạo ảnh chỉ dùng cho nền và hoạ tiết |
| Phụ thuộc một nhà cung cấp AI | Gọi qua chuẩn OpenAI để đổi được nhà cung cấp |
| AI đọc sai giá | Bước 3 luôn bắt chủ tiệm kiểm lại từng dòng trước khi bấm "Tiếp" |

## 5. Cần anh
1. **Kyma API key.** Em xin qua biểu mẫu bảo mật, không dán vào chat, để kiểm thử 3 việc ở mục 2 bằng $0,50 miễn phí.
2. **Duyệt lộ trình 3 giai đoạn:** PWA → Zalo Mini App → app iOS và Android.
3. **Zalo OA và cổng thanh toán**, như đã nêu trước.
