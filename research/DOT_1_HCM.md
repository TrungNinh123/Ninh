# Nailmark – Đợt 1 TP.HCM: 5 tiệm thử nghiệm (25/11/2026)

**Trạng thái:** đã chuẩn bị xong, **chưa liên hệ tiệm nào và chưa gửi tin nào**. Chỉ gửi khi anh duyệt.

## 1. Cách chọn
Nguồn là `crm/tiem_nen_tiep_can.csv`: 110 tiệm có từ 4,5 sao và 150 đánh giá trở lên, chưa có website riêng, không thuộc chuỗi lớn. Dữ liệu lấy từ Google Places ngày 25/11/2026.

Từ 58 tiệm ở TP.HCM, em chọn 5 tiệm theo bốn tiêu chí:
1. Có nhiều đánh giá Google nhất, tức là đã đông khách sẵn.
2. Chưa có website riêng, chỉ có Facebook hoặc không có gì.
3. Ưu tiên tiệm có 2 cơ sở, vì chủ tiệm thấy rõ giá trị của một trang web chung.
4. Tập trung ở Bình Thạnh, Phú Nhuận, Gò Vấp, Quận 1. Đây là các khu dân văn phòng 25–40 tuổi.

| # | Tiệm | Khu vực | Sao | Đánh giá | Web hiện tại | Lý do chọn |
|---|---|---|---|---|---|---|
| 1 | ELIZ Nail Beauty | Bình Thạnh | 4,9 | 2.374 | Chỉ có Facebook | Nhiều đánh giá nhất trong 110 tiệm |
| 2 | Salin Beauty (2 cơ sở) | Bình Thạnh, Phú Nhuận | 5,0 | 1.653 + 1.525 | Không có | Hai cơ sở đều 5,0 sao, có thêm học viện |
| 3 | Quýt Nail (2 cơ sở) | Gò Vấp, Phú Nhuận | 4,9 | 1.220 + 885 | Chỉ có Facebook | Nổi tiếng vẽ nail art, hợp với bộ sưu tập theo dịp |
| 4 | Nail Districts & Spa | Quận 1 | 5,0 | 1.113 | Không có | Đã có sẵn bản khám và demo từ trước |
| 5 | Charming Nail Studio | Bình Thạnh | 5,0 | 1.025 | Chỉ có Facebook | 5,0 sao với hơn 1.000 đánh giá |

**Loại khỏi đợt 1:**
- Celia Beauty Lab: theo [mytour](https://mytour.vn/en/blog/bai-viet/top-8-trusted-nail-training-centers-in-district-3-ho-chi-minh-city-mytour.html), đây chủ yếu là trường dạy nail, không phải tiệm đón khách.
- OnOn Nails Bar: để dành cho đợt 2.

**Cần kiểm lại:** nguồn [toplist](https://www.toplist.vn/top-list/tiem-lam-nail-dep-nhat-quan-go-vap-tp-hcm-44174.htm) ghi Quýt Nail Gò Vấp ở 28 Nguyễn Duy Cung, còn Google Maps ghi 255 Quang Trung. Có thể tiệm đã chuyển địa chỉ, em sẽ hỏi lại khi liên hệ.

## 2. Gói chuẩn bị cho mỗi tiệm (đã làm xong)
| Hạng mục | File | Ghi chú |
|---|---|---|
| Website demo riêng | `nailmark/tiem-eliz.html`, `tiem-salin.html`, `tiem-quyt.html`, `tiem-nail-districts.html`, `tiem-charming.html` | Có hero, bộ sưu tập 8 dịp, lookbook đánh số, cam kết, đặt lịch qua Zalo. Đầu trang ghi rõ đây là bản demo. **Không đăng công khai.** |
| Bộ Tết 2027 | Artifact bộ Tết (dùng chung) | Gồm lì xì móng, thẻ 10 lần, ảnh quà tặng, 3 tin Zalo và lịch 10 tuần |
| Bản khám và chuẩn quốc tế | `scripts/ban_kham.py`, `scripts/chuan_quoc_te.py` | Nail Districts đã có; 4 tiệm còn lại cần thêm vào `DEMO` khi anh duyệt |

## 3. Tin nhắn mẫu (chưa gửi)
**Zalo, tin đầu tiên** (thay [tên tiệm] và [số]):
> Chào chị chủ [tên tiệm], em là Nailmark, đội chuẩn hoá tiệm nail theo tiêu chuẩn quốc tế ở TP.HCM. Tiệm mình có [số] đánh giá Google, thuộc nhóm đông khách nhất thành phố nhưng chưa có website riêng. Em đã dựng thử miễn phí một trang cho tiệm (bộ sưu tập Tết, lookbook, đặt lịch qua Zalo) để chị xem trước, không ràng buộc gì. Chị cho em gửi link xem 1 phút nhé?

**Tin thứ hai, nếu chị chủ đồng ý:**
> Đây là bản demo riêng cho tiệm, chưa đăng công khai: [link]. Nếu chị thấy hợp, tháng đầu Nailmark làm miễn phí: chỉnh trang theo ảnh thật của tiệm, chuẩn bị chiến dịch Tết 2027 và bộ ảnh quà tặng cho khách. Chị chỉ cần gửi ảnh móng thật và bảng giá.

**Nguyên tắc:**
- Không dùng nội dung của tiệm này để chào tiệm khác.
- Chỉ dùng ảnh khách khi khách đã đồng ý bằng văn bản.
- Không chỉnh khuôn mặt hay màu móng trong ảnh.

## 4. Cần anh quyết
1. **Kênh liên hệ của Nailmark:** số Zalo hoặc email nào sẽ đứng tên gửi?
2. **Điều kiện ưu đãi:** chọn một trong ba:
   - (a) miễn phí tháng đầu;
   - (b) 500.000đ/tháng;
   - (c) tính tiền theo mỗi lượt đặt lịch mới.
3. **Duyệt danh sách 5 tiệm** ở trên và hai tin nhắn mẫu.
4. **Cách gửi demo:** link artifact riêng tư (cần chia sẻ từng link) hay gửi file HTML?

## 5. Lịch đề xuất (chỉ chạy sau khi anh duyệt)
- **Tuần 1 (từ 1/12):** nhắn 5 tiệm, mục tiêu 2 tiệm đồng ý xem demo.
- **Tuần 2–3:** thay ảnh Pexels bằng ảnh thật của tiệm và cài bộ Tết. Thời điểm này cách Tết khoảng 9 tuần (Tết rơi vào 6/2/2027).
- **Tuần 4–10:** chạy chiến dịch Tết, đo số lượt đặt lịch qua Zalo và đánh giá mới trên Google.
