# Nailmark – Nguyên tắc vận hành: AI xử lý toàn bộ, cho giá trị trước, khách không cần hỏi (anh Ninh chốt 25/11/2026)

## 1. Ba nguyên tắc
1. **AI xử lý toàn bộ.** Từ nội dung quảng cáo, tư vấn, tạo web, bàn giao đến hỗ trợ đều do AI làm. Người chỉ xử lý ngoại lệ: lỗi thanh toán, khiếu nại, và bước xác minh với đơn lớn.
2. **Cho giá trị trước.** Chủ tiệm nhận quà thật, miễn phí, trước khi trả bất kỳ đồng nào. Quà vẫn là của họ kể cả khi không mua.
3. **Khách không cần hỏi gì vẫn mua được.** Mọi câu trả lời phải có sẵn **ngay tại chỗ khách đang xem**. Mỗi lần khách phải hỏi nghĩa là team AI còn thiếu nội dung.

## 2. Giá trị cho trước: đã làm được đến đâu
| Quà miễn phí | Tình trạng | Công cụ |
|---|---|---|
| Bài tự chấm điểm 8 tiêu chuẩn (17 chuỗi, 9 quốc gia) | Có trên trang Nailmark | `nailmark/index.html` |
| Web đặt lịch mẫu mang tên tiệm (dữ liệu Google Maps) | **Chạy được** | `scripts/tu_dong_demo.py` |
| Poster Tết 2027 mang tên tiệm, có QR Zalo | **Chạy được** (25/11) | `scripts/qua_tang.py` |
| Thẻ QR in để ở quầy (A6) | **Chạy được**. Đã quét thử bằng máy: mở đúng `zalo.me/<số>` | `scripts/qua_tang.py` |
| Video 12 giây lướt web (đăng TikTok, Reels) | **Chạy được** | `scripts/qua_tang.py` |
| Trang mở quà: xem, mở file gốc, bước tiếp theo | **Chạy được** | `scripts/qua_tang.py` |
| Bản khám 11 kênh có bằng chứng | Có (đợt Quận 1) | `scripts/ban_kham.py` |
| Bộ ảnh quà tặng AI ghép từ ảnh thật của tiệm | Làm tay được, cần ảnh của tiệm | `scripts/anh_tang_khach.py` |

- **Một lệnh tạo đủ gói quà, khoảng 17 giây mỗi tiệm:** `python scripts/qua_tang.py --maps "Tên tiệm + quận"`
- **Lưu ý trung thực:** ảnh móng trong quà là ảnh minh hoạ, trên quà có ghi rõ. Khi tiệm gửi ảnh thật, web và poster dùng ảnh thật.

## 3. Ngưỡng xác minh theo giá trị đơn
| Giá trị đơn | Cách mua | Người có tham gia không |
|---|---|---|
| **Dưới 3 triệu**: Khởi đầu 999k, Chuẩn 1,99 tr, Đẳng cấp 2,99 tr, Gói Mùa 1,49 tr | Tự xem, tự quét QR thanh toán, hệ thống tự xác nhận và bàn giao | **Không**, trừ khi có lỗi |
| **Từ 3 triệu**: Chuyển giao 4,99 tr, Làm hộ 9,9 tr, Đồng hành AI theo quý 7,47 tr, Chuỗi | Thanh toán xong (hoặc trước khi làm), Nailmark **gọi xác minh**; tiệm có **số điện thoại và email liên hệ** để gọi lại khi cần | Có, một lần xác minh |

**[CHỜ DUYỆT]** Số điện thoại, email liên hệ và pháp nhân của Nailmark cho bước xác minh. Chưa có thì chưa mở bán các gói từ 3 triệu.

## 4. Cách đo "khách không cần hỏi"
| Chỉ số | Cách đo | Mục tiêu |
|---|---|---|
| **Tỷ lệ mua không cần hỏi** (đơn dưới 3 triệu) | Đếm số đơn đã thanh toán mà trước đó tiệm không gửi câu hỏi nào | ≥ 80% (giả định, đo để kiểm chứng) |
| Câu hỏi mới mỗi tuần | Câu hỏi chưa có trong ngân hàng 167 câu | Giảm dần theo từng tuần |
| Thời gian từ lúc nhận quà đến lúc mua | Từ lúc mở trang quà đến lúc thanh toán | Đo để tìm chỗ khách chần chừ |

**Vòng lặp:**
1. Mỗi câu hỏi mới được AI thêm vào ngân hàng hỏi đáp trong ngày.
2. Câu hỏi nào lặp lại nhiều thì đưa lên mục Hỏi đáp trên trang (`scripts/hoi_dap_web.py`) hoặc vào đúng bước trong app.
3. Mục tiêu: câu hỏi đó không bao giờ phải hỏi lại.

## 5. Kênh để tiệm biết đến Nailmark trước
Nội dung quảng cáo cũng do AI làm. Chủ tiệm thấy Nailmark trên các kênh truyền thông rồi mới nhận quà, nên không bất ngờ.
- **Nội dung cho chủ tiệm:** "Tiệm bạn đang mất khách ở đâu", "Chuẩn của 17 chuỗi ở 9 quốc gia", video trước và sau khi có web.
- **Kênh:** Facebook, TikTok, nhóm chủ tiệm nail. Theo DataReportal, Việt Nam có khoảng 76,2 triệu người dùng Facebook và 40,9 triệu người dùng TikTok từ 18 tuổi.
- Mỗi bài đều dẫn về **"Nhận quà miễn phí cho tiệm của bạn"**: dán link Google Maps của tiệm là nhận đủ gói quà.

## 6. Việc tiếp theo để đi hết đường "không cần hỏi"
1. Đưa ô "Dán link Google Maps → nhận quà" lên trang Nailmark (cần hosting để chạy `qua_tang.py` trên máy chủ).
2. Trang mở quà dẫn thẳng sang bảng giá, rồi thanh toán QR (cần cổng thanh toán).
3. Bàn giao tự động sau thanh toán: tin xác nhận gồm phạm vi, link app, video (cần Zalo OA).
4. Đo tỷ lệ mua không cần hỏi từ những đơn đầu tiên.
