# Nailmark – Chào tiệm thế nào, tiệm quan tâm gì, sản phẩm đã sẵn chưa, làm sao để tiệm tin (25/11/2026)

Tài liệu này trả lời 5 câu hỏi của anh Ninh. **Nguyên tắc:** nói đúng sự thật, không hứa điều chưa làm được.

## 1. Sản phẩm đã hoàn thiện chưa?
**Chưa hoàn thiện để bán.** Hiện mới **đủ để chạy thử miễn phí, với người của Nailmark làm cùng tiệm**.

| Đã chạy thật | Chưa có |
|---|---|
| App 4 bước tạo web với ảnh thật và bảng giá thật, khoảng 4 giây là xong | Hosting công khai (web mới chạy trên máy thử) |
| QR tự tạo, mở thẳng Zalo của tiệm | Đăng nhập. Hiện ai biết tên tiệm và số Zalo là sửa được web, **phải có trước khi mở công khai** |
| Chỉnh sáng ảnh, giữ màu móng (đo: sắc độ 16,8° → 16,6°) | AI đọc bảng giá từ ảnh (chờ Kyma key) |
| Nhận ảnh iPhone (HEIC) | Video hướng dẫn (mới có kịch bản) |
| Web đẹp trên điện thoại, đã kiểm ở 390px và 1280px | Thanh toán, Zalo OA, trợ lý AI |

## 2. Đã test lỗi chưa? Kết quả 25/11
**Đã chạy 10 tình huống. Tìm ra 4 lỗi thật, đã sửa và chạy lại, cả 10 đều đạt.**

| # | Tình huống | Lần đầu | Sau khi sửa |
|---|---|---|---|
| 1 | Số Zalo sai | Báo lỗi rõ | Đạt |
| 2 | Ít hơn 4 ảnh | Báo lỗi rõ | Đạt |
| 3 | Ảnh rất lớn (6000×8000), ảnh ngang dài, PNG trong suốt, ảnh tí hon | Chạy được | Đạt |
| 4 | **File hỏng mang đuôi .jpg** | **Sập máy chủ (lỗi 500)** | Báo "Ảnh số 1 bị hỏng…", không để lại thư mục dở |
| 5 | **Ảnh iPhone (HEIC)** | **Âm thầm bỏ ảnh**, báo thiếu ảnh khó hiểu | Nhận và xử lý được |
| 6 | File .pdf | (chưa thử) | Báo "định dạng .pdf, chưa nhận" |
| 7 | **Bảng giá viết tự nhiên** ("Sơn gel: 150k", "Tháo gel miễn phí") | **Báo "bảng giá trống"** | Đọc được. Dòng nào không đọc được thì chỉ rõ dòng đó |
| 8 | Chèn mã độc vào tên và giá | Đã chặn | Đạt: 0 đoạn mã chạy được |
| 9 | **Hai tiệm trùng tên** | **Web tiệm sau ghi đè web tiệm trước** | Mỗi tiệm một đường dẫn riêng. Tiệm cũ cập nhật thì đúng web của mình |
| 10 | Chạy trọn 4 bước trên trình duyệt điện thoại | Đạt | Đạt, khoảng 4 giây |

**Chưa test, phải test trước khi đưa cho tiệm tự làm:**
- Điện thoại thật: iPhone và Android, mạng 4G yếu.
- Quét QR bằng camera điện thoại thật.
- Nhiều tiệm dùng cùng lúc.
- Hết hạn mức Google 100 lượt/ngày.
- **Chủ tiệm thật tự làm, không ai chỉ.** Đây là bài test quan trọng nhất.

## 3. Chủ tiệm quan tâm điều gì? (họ không quan tâm "website")
Căn cứ: `research/NOI_DAU_CHU_TIEM_NAIL.md` và dữ liệu khám 15 tiệm Quận 1.

| Họ lo | Số liệu | Nailmark nói gì (đúng với cái đã làm được) |
|---|---|---|
| **Có khách mới, giữ khách cũ** | 32% chủ salon chọn đây là việc khó nhất. Chỉ 29% khách mới quay lại (Phorest). 14/15 tiệm Quận 1 không có kênh chăm khách cũ | Khách thấy tiệm trên Google Maps thì bấm là nhắn Zalo đặt lịch được ngay |
| **Mùa Tết quá tải** | Cận Tết tiệm mở xuyên đêm, khách chờ 3 tiếng; khách tăng 4–5 lần (Lao Động) | Khách đặt lịch trước qua Zalo, tiệm xếp lịch, bớt cảnh chờ |
| **Khách bùng hẹn** | 92% doanh nghiệp làm đẹp ở Anh từng gặp (Fresha) | Chưa có tính năng nhắc lịch. **Không hứa** |
| **Cạnh tranh, khách sợ giá phát sinh** | Khách phàn nàn giá vẽ "cảm tính" (Vietcetera). 6/15 tiệm không có bảng giá công khai | Bảng giá rõ ràng trên web là lợi thế để khách chọn tiệm mình |
| **Đã đông khách nhưng không đặt được online** | 10/15 tiệm Quận 1 không đặt lịch online được. ELIZ có 2.374 đánh giá mà chưa có web | Dùng chính số liệu Google của tiệm để mở lời |

## 4. Gửi thế nào?
**Đề xuất cho 5 tiệm đợt 1: gặp trực tiếp trước, Zalo sau.** Lý do: tin nhắn Zalo từ người lạ nói về "web miễn phí" rất dễ bị coi là lừa đảo. Chỉ có 5 tiệm, đều ở TP.HCM, nên một người đến tận tiệm là được.

**Cách A, gặp trực tiếp (khuyên dùng):**
- Đến tiệm vào giờ vắng: sáng ngày thường, khoảng 10:00–11:30. Tránh tối và cuối tuần là giờ đông khách.
- Tốt nhất là **làm móng ở tiệm như một khách bình thường** rồi mới mở lời.
- Mở điện thoại cho chủ tiệm xem web đã làm sẵn mang tên tiệm. Đưa QR in sẵn mở Zalo của tiệm.
- Không xin gì, không thu tiền. Để lại số Zalo.

**Cách B, chỉ nhắn Zalo** (nếu không đi được): gửi **một tin ngắn** vào số Zalo trên Google Maps của tiệm, vào giờ vắng.

> Chào chị chủ [tên tiệm]. Em là [tên người thật] bên Nailmark ở TP.HCM. Em thấy tiệm mình có [2.374] đánh giá Google, rất đông khách, nhưng khách tìm thấy tiệm trên Maps thì chưa có chỗ đặt lịch trước. Mùa Tết khách hay phải chờ lâu. Em làm sẵn một trang đặt lịch mang tên tiệm để chị xem thử. **Miễn phí, không cần chuyển khoản, không cần đăng ký gì.** Chị cho em gửi link 1 phút nhé?

Gửi link **chỉ khi chị chủ trả lời đồng ý**. Không nhắn lần thứ hai nếu chị không trả lời trong 3 ngày.

## 5. Câu hỏi tiệm sẽ hỏi, và câu trả lời trung thực
| Tiệm hỏi | Trả lời |
|---|---|
| "Em là ai? Công ty gì?" | **Đang thiếu.** Cần anh chốt: tên người đứng ra, số điện thoại, pháp nhân (nếu có), một trang "Về Nailmark" có thông tin thật. Không có thì không nên đi chào |
| "Có mất tiền không? Sau này có bắt trả không?" | "Đợt thử này miễn phí hoàn toàn, không cần chuyển khoản. Sau này nếu chị muốn dùng tiếp thì có gói từ 999k/năm. Không dùng thì em gỡ web." |
| "Em lấy thông tin, ảnh tiệm chị ở đâu?" | "Tên, địa chỉ, số sao lấy từ Google Maps công khai. Ảnh trong bản demo là ảnh minh hoạ, **chưa phải ảnh của tiệm**. Web thật thì dùng ảnh chị gửi." |
| "Có đăng lên mạng khi chị chưa đồng ý không?" | "Không. Bản demo chỉ gửi riêng cho chị. Chị đồng ý mới đăng. Chị muốn gỡ thì em gỡ trong ngày." |
| "Khác gì Facebook của chị?" | "Facebook để đăng bài. Trang này để **khách đặt lịch và xem giá**: một link, một mã QR, khách bấm là nhắn Zalo cho tiệm." |
| "Chị đổi giá thì ai sửa?" | "Chị tự sửa trên điện thoại, mất khoảng 1 phút. Trong đợt thử, em làm cùng chị lần đầu." |
| "Có lấy ảnh khách của chị đi chỗ khác không?" | "Không. Ảnh của tiệm chỉ dùng cho web của tiệm. Ảnh có mặt khách thì phải có khách đồng ý." |
| "Có tăng khách thật không?" | "**Em chưa có số liệu để hứa.** Đợt thử này để đo: em đếm số lượt khách bấm đặt lịch trên trang và báo chị mỗi tuần." |

## 6. Làm sao để tiệm tin?
1. **Cho trước, không xin gì.** Web làm sẵn mang tên tiệm, QR in sẵn. Không thu tiền, không bắt đăng ký.
2. **Danh tính thật và rõ.** Có người thật, số điện thoại, pháp nhân, trang "Về Nailmark". **Cần anh chốt. Đây là điểm yếu nhất hiện nay.**
3. **Gặp trực tiếp ở đợt 1.** Làm móng ở tiệm rồi mới mở lời.
4. **Nói bằng số liệu của chính tiệm** (số đánh giá Google), không nói chung chung.
5. **Cam kết bằng văn bản, gửi kèm link:** không đăng khi chưa đồng ý; gỡ trong ngày khi tiệm yêu cầu; không dùng nội dung của tiệm để chào tiệm khác; không thu tiền trong đợt thử.
6. **Không hứa tăng khách.** Hứa đo và báo số mỗi tuần.
7. **Sau đợt thử:** tiệm đầu tiên có số liệu thật, được tiệm đồng ý, thì đó là bằng chứng để chào các tiệm sau.

## 7. Cần anh quyết trước khi chào bất kỳ tiệm nào
1. **Ai đứng ra:** tên người, số Zalo hoặc số điện thoại, pháp nhân (nếu có).
2. **Cách chào:** A (gặp trực tiếp, khuyên dùng) hay B (chỉ Zalo)?
3. Duyệt tin nhắn ở mục 4 và các câu trả lời ở mục 5.
