# Nailmark – Chính sách giới thiệu và chi hoa hồng tự động (26/11/2026)

**Mục tiêu (anh Ninh):**
- Người gửi link chỉ việc chia sẻ link, quyền lợi của họ được giữ chắc.
- Nailmark chỉ chuyển tiền. Nailmark không khai thuế thay ai, và không kiểm tra thủ công từng đơn.

## 1. Quyền lợi đã chốt

| Đối tượng | Quyền lợi |
|---|---|
| Người gửi link, với đơn từ 5.000.000đ trở xuống | **15%** số tiền tiệm bạn thực trả |
| Người gửi link, với đơn trên 5.000.000đ | **20%** |
| Tiệm mua lần đầu qua link | Giảm **5%** |
| Khách quen (đã có đơn thanh toán), mua đơn tiếp theo | Giảm **10%** |

- Mức 10% khách quen không cộng dồn với 5% giới thiệu; hệ thống lấy mức cao hơn.
- Mã KHAUTRU99 là tiền khách đã trả cho bộ 99k, nên vẫn được trừ trước, rồi mới giảm 10%.

## 2. Cách giữ quyền lợi cho người gửi link (đã chạy và đã kiểm thử)

1. **Gắn khách 12 tháng.**
   - Tiệm mua qua link của ai thì thuộc về người đó trong 12 tháng.
   - Gia hạn, lên gói hay mua thêm trong 12 tháng vẫn tính hoa hồng cho người gửi đầu tiên, kể cả khi khách không mở lại link.
   - Người khác gửi link sau cũng không lấy được khách này.
2. **Link được nhớ 60 ngày** trên máy của khách. Khách cũng có ô tự gõ mã giới thiệu khi thanh toán.
3. **Chi từng đơn**, ngay khi qua 7 ngày giữ. Không chờ cuối tháng, không có mức tối thiểu.
4. **Minh bạch.**
   - Link quản lý riêng (có khoá bí mật) hiện từng đơn: trạng thái, lý do, ngày dự kiến nhận và mã giao dịch đã chuyển.
   - Ai chỉ biết mã giới thiệu thì chỉ thấy số tổng. Họ không xem được chi tiết và không đổi được tài khoản nhận.

## 3. Kiểm tra tự động: không ai phải duyệt

Mỗi giờ, máy tự kiểm từng đơn có mã giới thiệu:

| Kiểm tra | Không đạt thì |
|---|---|
| Đơn đã nhận đủ tiền | Chờ tiệm bạn chuyển đủ |
| Đơn chưa hoàn tiền | Hoa hồng tự huỷ |
| Đã qua 7 ngày giữ (bằng thời hạn hoàn tiền) | Tự chờ, hiện ngày dự kiến |
| Không tự giới thiệu: khác số Zalo **và** khác tên tiệm (so sau khi bỏ dấu) | Không giảm 5%, không tính hoa hồng |
| Người gửi link đã nhập tài khoản và bấm đồng ý điều khoản cộng tác viên | Chi ngay khi họ nhập |
| Tài khoản nhận không vừa bị đổi trong 3 ngày (chống chiếm tài khoản) | Chờ 3 ngày rồi tự chi |
| Mỗi đơn chi một lần (khoá chống trùng là mã đơn, gửi kèm lệnh chi) | Không chi trùng, kể cả khi lệnh được gửi lại |

- Nếu cổng chi báo lỗi, máy tự thử lại ở lần chạy sau với cùng khoá chống trùng.
- Không đơn nào phải chờ người xem.

**Kết quả chạy thử:** đạt 21/21 tình huống (`scripts/hoa_hong.py`, `scripts/thanh_toan.py`), gồm:
- giảm 5% cho khách mới và 10% cho khách quen;
- khách mua lại không mở link vẫn tính hoa hồng cho người gửi;
- người khác không lấy được khách đã gắn;
- chặn tự giới thiệu (cùng tên tiệm, khác số Zalo);
- không tính đơn chuyển thiếu tiền và đơn đã hoàn tiền;
- chưa chi khi chưa qua 7 ngày;
- người lạ không đổi được tài khoản nhận;
- chờ 3 ngày khi đổi tài khoản;
- không chi trùng;
- tổng tiền đã chuyển khớp với cách tính 15% / 20%.

**Rủi ro còn lại, nói thật:**
- Một người có thể dùng một số Zalo khác và một tên tiệm khác để mua qua link của chính mình.
- Mức thiệt tối đa cho Nailmark khi đó là 5% + 15–20% của một đơn hàng số (gần như không có giá vốn). Doanh thu vẫn dương.
- Chặn triệt để thì phải kiểm thủ công, điều anh không muốn. Nên em chọn chấp nhận rủi ro này.

## 4. Cổng chi tiền: payOS Payouts

**Thông tin đã xác minh** từ SDK chính thức `payos` 1.1.1 trên PyPI, em đã tải về và đọc mã nguồn:
- Lệnh chi: `POST https://api-merchant.payos.vn/v1/payouts`.
- Các trường: `reference_id`, `amount`, `description`, `to_bin`, `to_account_number`.
- Có header `x-idempotency-key` để chống trùng, và có chi theo lô.
- Trạng thái lệnh chi gồm cả `DRAFTING / SUBMITTED / APPROVED`. Vì vậy **cần hỏi payOS cách bật tự duyệt**: nếu tài khoản để chế độ duyệt tay, anh vẫn phải bấm duyệt từng lô.

**Đề xuất:** dùng **payOS cho cả thu tiền lẫn chi hoa hồng**. Như vậy chỉ có một tài khoản, một đối soát. Webhook thu tiền hiện viết theo SePay; khi anh chọn payOS, em đổi sang webhook payOS.

**Việc anh cần làm:**
1. Mở payOS bằng tài khoản doanh nghiệp hoặc hộ kinh doanh.
2. Bật chi hộ và tự duyệt.
3. Nạp số dư chi.
4. Đặt 3 khoá `PAYOS_PAYOUT_*` bằng Network secrets. Anh không dán khoá vào chat.

## 5. Thuế: phương án tối ưu để Nailmark chỉ chuyển tiền

**Nguyên tắc:**
- Người giới thiệu là **cộng tác viên độc lập**, không phải nhân viên. Họ bấm đồng ý điều khoản trước khi nhận tiền.
- Điều khoản ghi rõ: họ tự kê khai và nộp thuế thu nhập của mình; Nailmark chỉ chuyển hoa hồng.

**Điều cần biết:**
- Luật đặt nghĩa vụ khấu trừ lên **bên trả tiền** khi một lần trả từ ngưỡng trở lên. Ngưỡng cũ là 2 triệu đồng, theo TT 111/2013.
- Theo các nguồn thứ cấp, **Nghị định 253/2026/NĐ-CP nâng ngưỡng lên 5 triệu đồng mỗi lần chi**, hiệu lực từ 1/7/2026. Các nguồn này là Forvis Mazars và VCCI.
  - Em **chưa đọc được văn bản gốc**, vì trang thuvienphapluat chặn truy cập tự động.
- Với bảng giá hiện tại, hoa hồng **mỗi đơn cao nhất khoảng 1.898.000đ** (20% × 9.490.000đ).
- Vì chi từng đơn, mỗi lần chi đều dưới 5 triệu, nên **không phát sinh khấu trừ**. Nailmark chỉ chuyển tiền đúng như anh muốn.
  - Đây là cách chi tự nhiên theo đơn, không phải chia nhỏ để né thuế.

**Phòng khi luật thay đổi hoặc giá tăng:**
- Hệ thống có sẵn tham số `HH_THUE_NGUONG` (mặc định 5.000.000) và `HH_THUE_TY_LE` (10%).
- Lần chi nào chạm ngưỡng thì máy tự trừ và ghi rõ trên trang của cộng tác viên. Không ai phải làm tay.

**Cần một lần xác nhận của kế toán** khi anh chọn pháp nhân:
- Nghĩa vụ khấu trừ khi chi hoa hồng cho cá nhân hoặc hộ kinh doanh theo NĐ 253/2026 và TT 87/2026.
- Chứng từ cần lưu. Dữ liệu từng lệnh chi đã được lưu sẵn: mã đơn, số tiền, mã giao dịch, ngày chi.

## 6. Nguồn
- SDK payOS (PyPI `payos` 1.1.1): https://pypi.org/project/payos/ · tài liệu: https://payos.vn/docs/sdks/back-end/python
- Ngưỡng khấu trừ 5 triệu theo NĐ 253/2026:
  - VCCI: https://vcci.com.vn/en/news/thu-nhap-vang-lai-tren-5-trieu-dong-moi-phai-khau-tru-thue-tncn
  - Bản tin Forvis Mazars về NĐ 253/2026
- Thuế hoạt động affiliate/KOC (tham khảo): https://cafeland.vn/tin-tuc/thue-tncn-luu-y-quan-trong-cho-ca-nhan-lam-dich-vu-freelancer-affliate-kolkoc-153539.html
