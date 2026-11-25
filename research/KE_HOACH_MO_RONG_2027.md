# Nailmark – Kế hoạch mở rộng 2027: TP.HCM → các thành phố lớn → toàn quốc → nước ngoài (bản đề xuất, 25/11/2026)

**Mục đích:** để anh Ninh quyết **khi nào** mở thành phố hoặc nước mới và **dựa vào số liệu nào**. Mỗi bước mở rộng có một **cổng**. Chưa đạt cổng thì chưa mở.

**Phương pháp và giới hạn:**
- Số liệu lấy từ WebSearch ngày 25/11/2026. WebFetch bị chặn (wix.com, fresha.com không truy cập được), nên phần lớn số liệu là **đoạn trích kết quả tìm kiếm**. Cần mở bản gốc trước khi đưa cho khách hoặc nhà đầu tư.
- Số nào không chắc được ghi **"chưa xác minh"**. Mọi chỉ tiêu ở cổng là **giả định**, đo ở TP.HCM rồi chỉnh lại.
- Quy đổi theo giá bán ra Vietcombank 25/11/2026 (`research/ty_gia_vcb.json`): 1 USD = 26.020 đ; 1 EUR = 28.989,55 đ; 1 GBP = 34.311,11 đ; 1 CAD = 18.376,62 đ; 1 AUD = 17.246,07 đ; 1 JPY = 166,70 đ; 1 SGD = 20.336,22 đ. Bảng Vietcombank không có CZK, nên giá cho Séc niêm yết bằng EUR.
- Bối cảnh: `MUC_TIEU_2027.md` (10.000 doanh nghiệp, lợi nhuận 1 triệu USD), `research/PHEU_BAN_HANG.md` (giá ra mắt 999k / 1,99tr / 2,99tr / 9,9tr), `research/KE_HOACH_TONG.md` (Cổng 1 ngày 22/12, Cổng 2 tháng 2/2027), `research/NGUYEN_TAC_AI_TU_PHUC_VU.md` (chỉ số "mua không cần hỏi" ≥ 80%).

---

## 0. Tóm tắt để quyết (1 trang)

| # | Đề xuất | Lý do chính |
|---|---|---|
| 1 | **Q1/2027: chỉ TP.HCM**, gồm cả vùng Bình Dương và Vũng Tàu cũ (đã thuộc TP.HCM từ 1/7/2025) | Thị trường nail lớn nhất nước. Riêng 5 đơn vị đứng đầu của TP.HCM đã có ít nhất 1.673 tiệm (Poidata). Chưa có số liệu chuyển đổi thật |
| 2 | **Q2/2027: Hà Nội, cùng một phép thử nhỏ ở Đà Nẵng.** Mở khi TP.HCM qua Cổng A | Hà Nội là thị trường lớn thứ hai. Trong mẫu của Nailmark, 50% tiệm Đà Nẵng chưa gắn web, nên nhu cầu rõ nhất |
| 3 | **Q3/2027: mở tự phục vụ toàn quốc**, ưu tiên Đồng Nai (Biên Hòa), Cần Thơ, Hải Phòng, Khánh Hòa (Nha Trang), Huế | Phễu không cần người, nên mở cả nước chỉ tốn công làm nội dung. Không cần mở từng tỉnh |
| 4 | **Nước ngoài số 1 (thử từ Q3/2027): tiệm nail của người Việt ở Mỹ**, tập trung California và Texas | Thị trường lớn nhất. Người Việt chiếm phần lớn thợ nail. Phần mềm ở Mỹ có giá 20–150 USD/tháng, nên giá Nailmark có thể cao gấp khoảng 5 lần ở Việt Nam |
| 5 | **Nước ngoài số 2 (thử Q4/2027): Úc** (Sydney, Melbourne) | Nói tiếng Anh. 320.760 người nói tiếng Việt ở nhà. Luật dễ hơn EU và Anh |
| 6 | **Để sang 2028:** Séc, Đức, Anh, Canada | Lợi thế tiếng Việt có, nhưng vướng GDPR, tiếng Đức hoặc tiếng Séc, và rủi ro danh tiếng (điều tra buôn người ở tiệm nail) |
| 7 | **Không làm 2027:** Nhật, Hàn, Singapore, Philippines, Thái | Không có lợi thế tiếng Việt ở phía chủ tiệm. Hệ sinh thái đặt lịch riêng (Hot Pepper, Naver/Kakao, LINE) |
| 8 | **Giả thuyết cần kiểm chứng trước:** chủ tiệm người Việt ở nước ngoài trả lời và mua nhiều hơn khi được chào bằng tiếng Việt | Đo bằng phép thử A/B ở mục 4.3. Nếu sai thì dừng hướng "kiều bào" và xét lại |

**Ba việc cần anh quyết ngay (trước Cổng 2, 28/2/2027):**
1. Chốt các chỉ tiêu của Cổng A (mục 2.3), hoặc sửa lại.
2. Có cho phép bắt đầu thủ tục thanh toán quốc tế từ Q2/2027 không (mục 5.5). Thủ tục này cần thời gian xét duyệt.
3. Mức giá nước ngoài ở mục 5.3: dùng làm giá thử, hay chờ số liệu từ Việt Nam.

---

## 1. Việt Nam: quy mô từng thành phố

### 1.1 Lưu ý về địa giới mới
Từ 12/6/2025, cả nước còn **34 đơn vị cấp tỉnh** (28 tỉnh, 6 thành phố trực thuộc Trung ương) theo Nghị quyết 202/2025/QH15 ([Tạp chí Tòa án](https://tapchitoaan.vn/index.php/tu-ngay-1262025-ca-nuoc-chinh-thuc-co-34-don-vi-hanh-chinh-cap-tinh-gom-28-tinh-va-6-thanh-pho13538.html), [LuatVietnam](https://luatvietnam.vn/hanh-chinh/nghi-quyet-202-2025-qh15-cua-quoc-hoi-ve-viec-sap-xep-don-vi-hanh-chinh-cap-tinh-402728-d1.html)). Vì vậy:
- **Bình Dương và Vũng Tàu nay thuộc TP.HCM.** Mở hai nơi này là mở rộng trong TP.HCM, không phải mở thành phố mới.
- **Biên Hòa thuộc tỉnh Đồng Nai mới** (gồm cả Bình Phước). **Nha Trang thuộc Khánh Hòa mới** (gồm cả Ninh Thuận).
- Dân số tỉnh mới gồm cả vùng nông thôn. Thị trường nail thật nằm ở **lõi đô thị**, nên cần xem cột "lõi đô thị".

### 1.2 Dân số và số tiệm nail

| Thành phố hoặc tỉnh (địa giới mới) | Dân số tỉnh hoặc thành phố mới | Lõi đô thị (dân số) | Số tiệm nail theo nguồn | Hiện diện số (mẫu Nailmark 25/11/2026) |
|---|---|---|---|---|
| **TP.HCM** (gồm Bình Dương và Bà Rịa - Vũng Tàu) | **Trên 14 triệu** ([Saigon Times](https://thesaigontimes.vn/tphcm-cong-bo-12-dau-an-noi-bat-nam-2025/), [Nhà Đầu Tư](https://nhadautu.vn/12-su-kien-dau-an-noi-bat-cua-tphcm-nam-2025-d102218.html)) | Thủ Dầu Một 336.705; Vũng Tàu 498.010 (năm và phạm vi khác nhau, **chưa xác minh**: [Wikipedia](https://en.wikipedia.org/wiki/Provincial_city_(Vietnam)), [Worldometers](https://www.worldometers.info/population/largest-cities-in-vietnam/)) | Ít nhất **1.673** ở 5 đơn vị đứng đầu: Thủ Đức 526, Gò Vấp 333, Quận 1 289, Bình Thạnh 264, Tân Bình 261 (Poidata 8/2025: [poidata](https://www.poidata.io/report/nail-salon/vietnam)). Chưa có tổng toàn thành phố | 63 tiệm trong top 100: 44% có web riêng, 25% không gắn web |
| **Hà Nội** | **Chưa xác minh** trong phiên này. Cần tra Điều tra dân số giữa kỳ 2024 ([NSO](https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2025/01/thong-cao-bao-chi-ket-qua-dieu-tra-dan-so-va-nha-o-giua-ky-nam-2024/)) | – | Ít nhất **554** ở 4 quận: Đống Đa 203, Cầu Giấy 177, Hoàng Mai 87, Long Biên 87 (Poidata 8/2025) | 27 tiệm: 33% có web riêng, 41% chỉ có Facebook hoặc Instagram |
| **Đà Nẵng** (gồm Quảng Nam) | 3.065.628 ([LSVN](https://lsvn.vn/34-tinh-thanh-pho-tren-ca-nuoc-tu-ngay-12-6-2025-a158994.html)) | Chưa xác minh | **224** (Smartscraper 4/2026, dữ liệu danh bạ thương mại: [rentechdigital](https://rentechdigital.com/smartscraper/business-report-details/vietnam/list-of-nail-salons-in-da-nang)) | 10 tiệm: **50% không gắn web**, chỉ 10% có web riêng |
| **Hải Phòng** (gồm Hải Dương) | 4.664.124 ([LSVN](https://lsvn.vn/34-tinh-thanh-pho-tren-ca-nuoc-tu-ngay-12-6-2025-a158994.html)) | Chưa xác minh | Chưa có | Chưa quét |
| **Cần Thơ** (gồm Sóc Trăng, Hậu Giang) | 4.199.824 ([LSVN](https://lsvn.vn/34-tinh-thanh-pho-tren-ca-nuoc-tu-ngay-12-6-2025-a158994.html)) | Chưa xác minh | Chưa có | Chưa quét |
| **Đồng Nai** (gồm Bình Phước; có Biên Hòa) | 4.491.408 (NQ 202/2025: [VBPL](https://vbpl.vn/TW/Lists/vbpq/Attachments/179501/202_2025_QH15_648951.doc)) | Biên Hòa 1.055.414 (không rõ năm, **chưa xác minh**: [mia.vn](https://mia.vn/cam-nang-du-lich/cac-thanh-pho-o-viet-nam-ban-can-biet-17452)) | Biên Hòa **khoảng 382** (Poidata, xem `research/CHUOI_NAIL_VN.md`) | Chưa quét |
| **Khánh Hòa** (gồm Ninh Thuận; có Nha Trang) | 2.243.554 ([Thư viện Pháp luật / NQ 202](https://thuvienphapluat.vn/van-ban/Bo-may-hanh-chinh/Nghi-quyet-202-2025-QH15-660927.aspx)) | Nha Trang 422.601 ([Wikipedia](https://en.wikipedia.org/wiki/Provincial_city_(Vietnam)), **chưa xác minh**) | Chưa có | Chưa quét |
| **Huế** | 1.432.986 ([Thư viện Pháp luật](https://thuvienphapluat.vn/hoi-dap-phap-luat/xep-hang-dan-so-34-tinh-thanh-viet-nam-moi-nhat-2026-the-nao-138084847.html)); VTC ghi gần 1,5 triệu ([VTC](https://vtcnews.vn/viet-nam-hien-co-bao-nhieu-thanh-pho-ar1036185.html)) | Chưa xác minh | Chưa có | Chưa quét |
| **Cả nước** | – | – | **17.032** (Poidata 8/2025) | 441 tiệm ở 18 quận đã quét |

**Đọc bảng:**
- **17.032 tiệm cả nước** (Poidata) là số theo danh bạ, có thể thiếu các tiệm nhỏ không có trên Google. Ngay cả nếu Nailmark chiếm 30% thị trường thì cũng chỉ khoảng 5.000 tiệm. Như `research/PHEU_BAN_HANG.md` đã nói, **riêng ngành nail ở Việt Nam không đủ 10.000 doanh nghiệp**. Đây là lý do thứ nhất để ra nước ngoài, bên cạnh việc thêm ngành (tóc, thú cưng).
- **Tỷ lệ dân số thành thị của từng thành phố: chưa xác minh.** Cần lấy từ bảng "Dân số theo thành thị, nông thôn… và tỉnh, thành phố" trong Điều tra giữa kỳ 2024 ([NSO PDF](https://nso.gov.vn/wp-content/uploads/2024/12/Dieu-tra-Dan-so-giua-ky-2024-31.12-2.pdf)). Lưu ý bảng này dùng địa giới cũ, trước sáp nhập.
- **Việc AI làm được ngay (tốn lượt Places API):** quét Google Maps cho Hải Phòng, Cần Thơ, Biên Hòa, Nha Trang, Huế bằng cùng công cụ đã dùng cho 441 tiệm. Mỗi thành phố khoảng 5–10 truy vấn.

### 1.3 Thứ tự mở thành phố đề xuất

| Thứ tự | Nơi | Thời điểm sớm nhất | Lý do | Điều chỉnh nội dung |
|---|---|---|---|---|
| 0 | TP.HCM lõi (Q1, Q3, Q7, Phú Nhuận, Bình Thạnh, Gò Vấp, Tân Bình, Thủ Đức) | Đang làm (12/2026 – Q1/2027) | Phòng thí nghiệm. Có 53 tiệm đủ điều kiện trong `crm/` | Không |
| 0b | TP.HCM mở rộng: Thủ Dầu Một, Dĩ An, Thuận An, Vũng Tàu | Q1/2027, ngay khi phễu tự phục vụ chạy | Cùng thành phố, cùng giọng văn, cùng mùa lễ. Thủ Đức đã là nơi có nhiều tiệm nail nhất cả nước (526) | Ảnh và lookbook theo giá bình dân hơn |
| 1 | **Hà Nội** | Đầu Q2/2027 (sau Cổng A) | Thị trường lớn thứ hai. Có chuỗi (Halei, Milagros, LAMIA), nên có khách cho gói "Chuỗi từ 50 triệu" | Giọng văn miền Bắc, phong cách Hàn (Milagros), mùa lạnh (tháng 11 – tháng 2) |
| 1b | **Đà Nẵng** (thử nhỏ) | Q2/2027, chạy cùng Hà Nội | 50% tiệm trong mẫu chưa có web. Khách du lịch nhiều, nên cần web 2 thứ tiếng | Web tiếng Việt + tiếng Anh (thêm tiếng Hàn nếu đo thấy cần); mùa du lịch hè |
| 2 | Đồng Nai (Biên Hòa) | Q3/2027 | Khoảng 382 tiệm, sát TP.HCM, cùng phong cách | Không |
| 2 | Cần Thơ | Q3/2027 | Trung tâm miền Tây, 4,2 triệu dân (tỉnh mới) | Giọng văn miền Tây, giá thấp hơn |
| 2 | Hải Phòng | Q3/2027 | 4,66 triệu dân (tỉnh mới), gần Hà Nội | Như Hà Nội |
| 3 | Khánh Hòa (Nha Trang), Huế | Q3–Q4/2027 | Thành phố du lịch | Web 2 thứ tiếng (Nha Trang: cân nhắc tiếng Nga, **chưa xác minh** nhu cầu) |
| 4 | Toàn quốc, tự phục vụ | Q4/2027 | Ai cũng tự đăng ký được, không cần mở từng tỉnh | Bộ Tết 2028 (Tết Mậu Thân rơi vào khoảng 26/1/2028, **cần đối chiếu lịch âm**) |

**Nguyên tắc:** "mở thành phố" chỉ có nghĩa là (1) quét Google Maps để có danh sách và web mẫu, (2) làm lookbook và lời chào theo vùng miền, (3) đăng nội dung nhắm vào chủ tiệm thành phố đó. **Không cần người tại chỗ. Không chạy quảng cáo trả tiền** trước Cổng 2 (theo `KE_HOACH_TONG.md` mục 5).

---

## 2. Cổng mở rộng (dựa trên số liệu thật ở TP.HCM)

### 2.1 Các chỉ số dùng ở mọi cổng
| Chỉ số | Cách đo | Nguồn trong repo |
|---|---|---|
| Tiệm trả tiền (cộng dồn) | Đếm giao dịch thành công qua payOS hoặc dịch vụ tương đương | `PHEU_BAN_HANG.md` bước 4 |
| **Tỷ lệ mua không cần hỏi** (đơn dưới 3 triệu) | Số đơn đã thanh toán mà trước đó tiệm không hỏi gì, chia cho tổng đơn | `NGUYEN_TAC_AI_TU_PHUC_VU.md` mục 4 |
| Tỷ lệ tự xuất bản trong 7 ngày | Số tiệm tự đăng web trong 7 ngày, chia cho số tiệm đã trả tiền | `KE_HOACH_TONG.md` mục 3 |
| Lần người chạm mỗi đơn | Số lần người phải xử lý, chia cho số đơn | `PHEU_BAN_HANG.md` mục 2a |
| Tỷ lệ mua tiếp Gói Mùa | Số khách web mua Gói Mùa, chia cho số khách web đủ điều kiện | `KE_HOACH_TONG.md` mốc 5 |
| Hoàn tiền hoặc khiếu nại | Số đơn hoàn tiền, chia cho tổng đơn | Mới |
| Bằng chứng hiệu quả | Số tiệm có số liệu trước và sau (lượt bấm đặt lịch, đánh giá Google mới) | `PHEU_BAN_HANG.md` mục 2d |

### 2.2 Bảng cổng (giả định, đo ở TP.HCM rồi chỉnh)

| Cổng | Thời điểm xét | Mở gì | Điều kiện (đạt **tất cả**) | Không đạt thì |
|---|---|---|---|---|
| **Cổng 1** (đã có) | 22/12/2026 | Mở bán Khởi đầu và Chuẩn | Có ≥ 3 tiệm có web thật | Sửa app, lùi 1 tuần |
| **Cổng 2** (đã có) | 8/2 – 28/2/2027 | Quyết giá, App v2, thêm ngành | Số liệu Tết | – |
| **Cổng A: Hà Nội + Đà Nẵng** | 31/3/2027 | Hà Nội, Đà Nẵng | (1) TP.HCM có **≥ 30 tiệm trả tiền**; (2) **≥ 80% mua không cần hỏi**; (3) ≥ 70% tự xuất bản trong 7 ngày; (4) ≤ 0,3 lần người chạm mỗi đơn dưới 3 triệu; (5) hoàn tiền ≤ 5%; (6) ≥ 10 tiệm có số liệu trước và sau | Ở lại TP.HCM. Sửa đúng bước bị kẹt. Xét lại sau 4 tuần |
| **Cổng B: toàn quốc** | 30/6/2027 | Tự phục vụ cả nước (mục 1.3, thứ tự 2–4) | (1) Tổng **≥ 150 tiệm trả tiền**; (2) Hà Nội đạt ≥ 70% chỉ số chuyển đổi của TP.HCM; (3) **≥ 80% mua không cần hỏi**; (4) **≥ 25% mua tiếp Gói Mùa 8/3 hoặc 30/4**; (5) chi phí có khách ≤ 30% giá gói đầu tiên | Chỉ mở thêm Biên Hòa (sát TP.HCM). Còn lại chờ |
| **Cổng C: thử nước ngoài** | 30/6/2027 (xét cùng Cổng B) | Thử ở Mỹ (mục 4.3) | (1) Việt Nam **≥ 150 tiệm trả tiền** và **≥ 80% mua không cần hỏi**; (2) **cổng thanh toán quốc tế đã được duyệt** và đã chạy thử 1 giao dịch thật; (3) đã có web mẫu tiếng Anh (cho khách) kèm hướng dẫn tiếng Việt (cho chủ tiệm); (4) đã có chính sách quyền riêng tư và điều khoản bằng tiếng Anh | Lùi thử nghiệm sang Q4. Vẫn chạy phần chuẩn bị |
| **Cổng D: mở rộng nước ngoài** | 30/9/2027 | Mở bán rộng ở Mỹ, thử Úc | Phép thử Mỹ đạt tiêu chí ở mục 4.3 | Dừng hoặc đổi giả thuyết (mục 4.4) |
| **Cổng E: kế hoạch 2028** | 15/12/2027 | Séc, Đức, Anh, Canada | Mỹ ≥ 100 tiệm trả tiền; Úc ≥ 20; doanh thu nước ngoài ≥ 20% tổng | Giữ 2 nước, đào sâu |

**Lưu ý:** "≥ 30 tiệm trả tiền trước 31/3" là con số **giả định**. Nếu Cổng 1 cho thấy tỷ lệ từ xem demo sang trả tiền thấp hơn dự kiến, anh có thể hạ xuống 20. **Không được hạ ngưỡng "mua không cần hỏi"**, vì mở rộng mà còn phải trả lời câu hỏi thì sẽ hết sức phục vụ.

---

## 3. Nước ngoài: quy mô thị trường và lợi thế tiếng Việt

### 3.1 Quy mô thị trường và số tiệm

| Nước | Số tiệm nail hoặc cơ sở | Quy mô thị trường | Ghi chú về số liệu |
|---|---|---|---|
| **Mỹ** | **113.275 tiệm nail** (Poidata 8/2025; Florida 10.519, California 9.216; **50% có website**) ([poidata](https://poidata.io/report/nail-salon/united-states)). IBISWorld: 347.821–348.000 cơ sở "waxing và nail" ([IBISWorld](https://www.ibisworld.com/united-states/market-size/personal-waxing-nail-salons/4411/)). NAILS (2015): khoảng 130.000 tiệm ([Daily Beast](https://www.thedailybeast.com/the-nail-diaspora-how-manicures-transformed-the-vietnamese-immigrant-experience-in-america)) | Waxing và nail $25,5 tỷ (2025) ≈ 663.510 tỷ đ (IBISWorld) | Các nguồn định nghĩa khác nhau. **Poidata là số gần nhất với "tiệm nail"** |
| **Canada** | Tóc và nail gộp chung: 41.035 (2025) đến 49.750 (2026) ([IBISWorld](https://www.ibisworld.com/canada/number-of-businesses/hair-nail-salons/1718/)). Chưa có số tiệm nail riêng | Tóc và nail C$5,8–6,0 tỷ (2025) ≈ 110.260 tỷ đ cho mức C$6 tỷ | **Số tiệm nail riêng: chưa xác minh** |
| **Anh** | Tóc và làm đẹp gộp chung: 50.481 (2025, IBISWorld; ONS 50.400) ([Policybee](https://policybee.co.uk/blog/uk-hair-and-beauty-industry-statistics)). Số nail bar "gần 5.000" (không rõ năm, **chưa xác minh**: [SCMP](https://www.scmp.com/magazines/post-magazine/article/1041471/nail-bar-blues)). Khoảng 1.680 tiệm nail mở mới trong 2019–2024 ([Scratch](https://www.scratchmagazine.co.uk/news/nail-salons-report-8-growth-in-5-years-but-its-not-all-good-news-for-the-sector)) | Tóc và làm đẹp £5,8 tỷ (2025–26) ([IBISWorld](https://www.ibisworld.com/united-kingdom/industry/hairdressing-beauty-treatment-in-the-uk/4900/)) | Tiệm nail là loại hình làm đẹp phổ biến nhất ở Anh ([Scratch](https://scratchmagazine.co.uk/news/revealed-nail-salons-are-the-most-common-beauty-business-in-the-uk)) |
| **Úc** | 6.515–6.619 cơ sở waxing và nail (2025), 16.290 lao động ([IBISWorld](https://www.ibisworld.com/australia/number-of-businesses/personal-waxing-nail-salons/5126/)) | A$1,9–2,0 tỷ (2025) ≈ 32.768 tỷ đ cho mức A$1,9 tỷ ([IBISWorld](https://www.ibisworld.com/australia/market-size/personal-waxing-nail-salons/5126/)) | Hơn 80% cơ sở ở NSW, Victoria, Queensland |
| **Đức** | Khoảng **60.000 người** làm trong ngành (Hiệp hội thợ nail Đức, trích lại) ([Worldcrunch](https://worldcrunch.com/in-the-news/cheap-nails-hidden-chains-human-trafficking-inside-berlin-s-nail-salons/)). Riêng Stuttgart gần 200 tiệm ([Stuttgarter Zeitung](https://www.stuttgarter-zeitung.de/lokales/stuttgart/das-geschaeft-mit-schoenen-haenden-warum-boomen-nagelstudios-in-stuttgart-78856896.html)) | Chưa xác minh | **Tổng số tiệm cả nước: chưa xác minh** |
| **Séc** | Riêng Praha: 266 tiệm nail (4/2026, danh bạ thương mại: [rentechdigital](https://rentechdigital.com/smartscraper/business-report-details/czech-republic/list-of-nail-salons-in-prague)); khoảng 200 (Radio Prague, bài cũ: [radio.cz](https://english.radio.cz/node/8587695)) | Chưa xác minh | Thị trường nhỏ |
| **Nhật** | 28.492 (Poidata; Tokyo 4.838, Osaka 2.527) ([poidata](https://poidata.io/report/nail-salon/japan)) | Dịch vụ nail khoảng ¥139 tỷ (2024) ≈ 23.171 tỷ đ ([Statista](https://statista.com/statistics/1223981/japan-market-size-nail-care-service)). Ngành nail ¥204,7 tỷ (2023, xem `research/hinh_mau_dong_a.md`) | Gitnux ghi 42.500 tiệm, không có nguồn gốc, **không dùng** |
| **Hàn Quốc** | **Chưa xác minh.** Có dữ liệu cấp phép ngành làm đẹp để tự đếm ([data.go.kr](https://www.data.go.kr/en/data/15096295/standard.do)) | Chưa xác minh | Phần lớn tiệm chỉ có 1–2 người ([Hankyung](https://www.hankyung.com/article/2025061710257)) |
| **Singapore** | 1.574 (Poidata 8/2025) ([poidata](https://poidata.io/report/nail-salon/singapore)) | Chưa xác minh | Chuỗi Nail Palace đã dùng Fresha |
| **Philippines** | 5.213 (Poidata 7/2026; Metro Manila 1.820) ([poidata](https://www.poidata.io/report/nail-salon/philippines)) | Chưa xác minh | Giá dịch vụ thấp |
| **Thái Lan** | 14.544 (Poidata 6–7/2026; Bangkok 3.132) ([poidata](https://poidata.io/report/nail-salon/thailand)) | Chưa xác minh | – |

### 3.2 Người Việt trong ngành nail ở nước ngoài (giả thuyết then chốt)

| Nước | Người Việt (cộng đồng) | Tỷ lệ người Việt trong ngành nail | Độ tin cậy |
|---|---|---|---|
| **Mỹ** | Khoảng 2,3 triệu người gốc Việt (2023); 36% ở California (770.000), Texas 310.000 ([Pew](https://www.pewresearch.org/race-and-ethnicity/fact-sheet/asian-americans-vietnamese-in-the-u-s/)) | **Thợ:** 48% thợ nail cả nước, 80% ở California (NAILS 2012–13, trích lại: [Matador](https://matadornetwork.com/life/why-vietnamese-americans-rule-the-nail-salon-scene)). Khoảng 3/4 thợ nail nhập cư đến từ Việt Nam ([UCLA Labor Center 2018](https://labor.ucla.edu/publication/nail-files/)). **Chủ tiệm:** NAILS nói tiệm của người Việt chiếm "gần một nửa ngành" ([NAILS](https://www.nailsmag.com/389759/the-vietnamese-american-salon-industry)); một bài UCLA cũ ghi 30% ([UCLA AASC](https://www.aasc.ucla.edu/resources/policyreports/Reframing_Immigration_Debate/Reframing_Vietnamese_Ownded_Manicure.pdf)) | Trung bình. Số liệu cũ, nhưng nhiều nguồn khớp nhau |
| **Canada** | Khoảng 275.530 người gốc Việt (Wikipedia, **chưa xác minh**); 233.000 người nói tiếng Việt (điều tra dân số 2021: [StatCan](https://www.statcan.gc.ca/o1/en/plus/9158-asian-history-month-lets-talk-languages)) | **Chưa xác minh.** Chỉ có bài báo định tính ([Globe and Mail](https://www.theglobeandmail.com/opinion/article-how-nail-salons-became-a-financial-refuge-for-the-vietnamese-diaspora/), [Vancouver Courier](https://www.vancouverisawesome.com/courier-archive/news/vietnamese-nail-salons-dominate-kingsway-2959122)) | Thấp |
| **Úc** | Khoảng 258.000 người sinh ở Việt Nam; 334.785 người gốc Việt ([ABS 2021](https://www.abs.gov.au/census/find-census-data/quickstats/2021/5105_AUS)); 320.760 người nói tiếng Việt ở nhà ([Wikipedia](https://en.wikipedia.org/wiki/Vietnamese_Australians)) | Thợ người Việt "chiếm lĩnh" thị trường (Đại học Macquarie, không có số: [MQ](https://researchers.mq.edu.au/en/publications/the-sociolinguistics-of-nail-care/)) | Thấp đến trung bình |
| **Anh** | Chưa xác minh | Năm 2007, tiệm nail là hơn một nửa số doanh nghiệp của người Việt ở Anh ([East London Lines](https://www.eastlondonlines.co.uk/?p=31240)). GLAA có hồ sơ ngành nail bar ([GLAA](https://gla.gov.uk/who-we-are/modern-slavery/industry-profiles-nail-bars-2020)) | Thấp. Kèm rủi ro danh tiếng (buôn người) |
| **Đức** | Khoảng 226.000–227.000 người gốc Việt (2024) ([Wikipedia](https://en.wikipedia.org/wiki/Vietnamese_people_in_Germany)) | **Khoảng 2/3 số tiệm** do người Việt làm chủ (ước tính của hiệp hội, trích lại: [Worldcrunch](https://worldcrunch.com/in-the-news/cheap-nails-hidden-chains-human-trafficking-inside-berlin-s-nail-salons/)) | Trung bình thấp |
| **Séc** | 61.000 trở lên (Radio Prague); 62.842 công dân Việt Nam (Cục Thống kê Séc 2020, qua [Wikipedia](https://www.wikipedia.org/wiki/Vietnamese_Czechs)) | Tiệm nail là "hiện tượng" trong kinh doanh của người Việt ([Radio Prague](https://english.radio.cz/node/8587695)). Không có tỷ lệ | Thấp |
| **Nhật** | 681.100 người Việt cư trú (cuối 2025) ([VOV](https://english.vov.vn/en/society/vietnamese-community-remains-japans-second-largest-foreign-group-post1341896.vov)) | Phần lớn là lao động và du học sinh. **Không có bằng chứng** người Việt làm chủ tiệm nail | – |
| **Hàn Quốc** | Khoảng 270.000 người (2025) ([Korea Times](https://www.koreatimes.co.kr/southkorea/globalcommunity/20251219/vietnamese-lead-surge-as-koreas-foreign-resident-population-hits-record-high)) | Không có bằng chứng | – |

**Kênh tiếng Việt đã có sẵn (Mỹ):**
- **VietSALON**: tạp chí tiếng Việt cho thợ nail, phát hành 2 tháng một số, khoảng 18.000 bản. Là ấn phẩm chị em của NAILS Magazine ([Exact Connections](https://us.exactconnections.com/media/viet-salon), [NAILS](https://www.nailsmag.com/350421/vietsalon-nail-artistry-competition-sponsored-by-cnd-brings-nail-industry-togeth)).
- Có các bên đã bán phần mềm cho tiệm nail người Việt: app "Viet Nails – Chủ tiệm / thợ" ([App Store](https://apps.apple.com/us/app/id6444178458)), Busy-N-Booked ở Arizona. Như vậy **thị trường có thật, nhưng đã có đối thủ nói tiếng Việt**.
- Khảo sát cũ của NAILS: giá dịch vụ ở tiệm người Việt **thấp hơn khoảng 36%** so với tiệm khác ([NAILS](https://www.nailsmag.com/390022/vietnamese-survey-answers-many-questions-begs-many-more)). Như vậy chủ tiệm người Việt **có thể nhạy cảm về giá hơn** mức trung bình ở Mỹ. Đây là lý do định giá ở mục 5.3 nằm dưới giá của agency và gần giá phần mềm.

**Kết luận về giả thuyết tiếng Việt:**
- **Mỹ: mạnh.** Có số liệu từ nhiều nguồn, cộng đồng lớn và tập trung, có kênh truyền thông tiếng Việt.
- **Đức, Úc, Anh, Séc: có, nhưng chủ yếu định tính.**
- **Nhật, Hàn, Đông Nam Á: không có.**
- **Điểm chưa biết:** chủ tiệm thế hệ 2 có thể thích tiếng Anh hơn. Phép thử A/B ở mục 4.3 sẽ đo điều này.

### 3.3 Tiệm ở nước ngoài đang trả bao nhiêu cho phần mềm và website

| Sản phẩm | Giá | ≈ VND | Nguồn |
|---|---|---|---|
| Fresha (Mỹ) | $19,95/tháng (1 người); $14,95/người/tháng (nhóm); phí khách mới qua sàn 20%, tối thiểu $6 | 519.099 đ/tháng; 388.999 đ/người | [GlossGenius blog](https://glossgenius.com/blog/fresha-pricing) (bên thứ ba, đối thủ viết) |
| Fresha (Anh) | £14,95/tháng (1 người); £9,95/người | 512.951 đ/tháng | [Booksy blog](https://biz.booksy.com/blog/best-salon-software-2026), **chưa xác minh** |
| Booksy (Mỹ) | $29,99/tháng + $20/người thêm | 780.340 đ + 520.400 đ/người | [Booksy blog](https://biz.booksy.com/blog/best-salon-software-2026) |
| Booksy (Anh) | £40/tháng + £5/người thêm, chưa VAT | 1.372.444 đ + 171.556 đ/người | [Booksy UK pricing](https://biz.booksy.com/en-gb/pricing) |
| Vagaro (Mỹ) | Từ $23,99/tháng (1 lịch) | 624.220 đ/tháng | [Pabau](https://pabau.com/blog/vagaro-vs-booksy/) (bên thứ ba) |
| GlossGenius (Mỹ) | $24 / $48 / $148 mỗi tháng (trả năm); Standard $28 nếu trả tháng | 624.480 đ – 3.850.960 đ/tháng | [CostBench](https://costbench.com/software/salon-spa/glossgenius/), [Koalendar](https://koalendar.com/blog/gloss-genius-pricing) |
| Square Appointments (Mỹ) | Plus $49, Premium $149 mỗi địa điểm/tháng (trang mới); trang cũ ghi $29 / $69 | 1.274.980 đ (Plus $49) | [Square](https://square.com/us/en/appointments/pricing), [Capterra](https://www.capterra.com/p/170263/Square-Appointments/pricing/) |
| Wix (trả năm) | Light $17, Core $29, Business $39, Business Elite $159 mỗi tháng | 442.340 đ – 4.137.180 đ/tháng | [Wix blog](https://www.wix.com/blog/how-much-is-a-wix-website), [Style Factory](https://www.stylefactoryproductions.com/wix-pricing) |
| Squarespace (trả năm) | Basic khoảng $16–19/tháng; Core khoảng $23/tháng | 416.320 – 494.380 đ/tháng | [Emergent](https://emergent.sh/learn/squarespace-pricing), [Beancount](https://beancount.io/blog/2026/09/17/squarespace-new-pricing-basic-core-plus-advanced-small-business-guide) |
| Web tiệm nail do agency hoặc freelancer làm (Mỹ) | Freelancer $1.000–3.000; agency từ vài nghìn USD; báo giá web tiệm nail $2.200 / $4.350 / $6.550 | 26–78 triệu đ (freelancer); 57–170 triệu đ (báo giá tiệm nail) | [ManyPixels](https://www.manypixels.co/blog/web-design/for-small-businesses), [ProjectCostEstimator](https://projectcostestimator.com/cost/industry/nail-salon) (trang bán hàng, độ tin cậy thấp) |
| Giá dịch vụ (để so) | Mỹ: gel manicure khoảng $40–70; Anh: gel khoảng £25–40, London cao hơn | 1,04–1,82 triệu đ; 0,86–1,37 triệu đ | [ThePricer](https://www.thepricer.org/how-much-does-a-manicure-cost/), [Glowbooks](https://glowbooks.co.uk/?p=42182) |

**Kết luận về giá:**
- Một tiệm ở Mỹ đã quen trả **khoảng $20–50/tháng ($240–600/năm) chỉ cho phần mềm đặt lịch**, cộng thêm **$17–39/tháng cho website** nếu tự làm.
- **Một lần gel ở Mỹ ($40–70) đã ngang 1–2 triệu đồng.** Trong khi đó, gói Khởi đầu 999k ở Việt Nam bằng khoảng 3–7 lần gel ở TP.HCM (giá gel bình dân khoảng 130.000–400.000 đ, xem `research/CHUOI_NAIL_VN.md`).
- Vì vậy giá nước ngoài **khoảng 5 lần giá Việt Nam** (mục 5.3) vẫn **thấp hơn 1 năm phần mềm và thấp hơn 10 lần web của agency**.
- **Định vị: không thay phần mềm đặt lịch.** Nailmark làm **web, lookbook và nội dung theo mùa**, rồi **gắn nút đặt lịch có sẵn** (Fresha, Booksy, Square, Vagaro…) của tiệm. Như vậy tránh đối đầu trực tiếp với các nền tảng lớn.

### 3.4 Luật, quyền riêng tư và thanh toán

| Vùng | Luật hoặc điểm chính | Hệ quả cho Nailmark | Nguồn |
|---|---|---|---|
| **EU (Đức, Séc)** | GDPR: phạt tối đa €20 triệu hoặc 4% doanh thu toàn cầu (mức cao); €10 triệu hoặc 2% (mức thấp) | Cần chính sách quyền riêng tư, thoả thuận xử lý dữ liệu (DPA) với tiệm, đồng ý cookie, xin đồng ý trước khi dùng ảnh khách (Nailmark đã có mẫu xin đồng ý ở Việt Nam). Đức có yêu cầu "Impressum" trên web, **chưa xác minh** trong phiên này | [Ủy ban châu Âu](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/enforcement-and-sanctions_en) |
| **Anh** | UK GDPR: phạt tối đa £17,5 triệu hoặc 4% doanh thu (mức cao); £8,7 triệu hoặc 2% (mức thấp) | Như EU. Thêm rủi ro danh tiếng: Anh và Đức có nhiều điều tra buôn người ở tiệm nail | [ICO](https://ico.org.uk/about-the-ico/our-information/policies-and-procedures/data-protection-fining-guidance/statutory-background/the-maximum-amount-of-a-fine-under-uk-gdpr-and-dpa-2018), [Anti-Slavery Commissioner](https://antislaverycommissioner.co.uk/news-insights/slavery-report-sounds-alarm-over-vietnamese-nail-bar-workers) |
| **Canada** | CASL: tin nhắn hoặc email thương mại phải có sự đồng ý; phạt tới C$10 triệu mỗi vi phạm (tổ chức). Quebec cần tiếng Pháp (**chưa xác minh** trong phiên này) | Tin nhắc lịch và chào Gói Mùa phải có đồng ý rõ ràng | [CRTC](https://www.crtc.gc.ca/eng/com500/info.htm) |
| **Mỹ** | Luật quyền riêng tư theo từng bang (ví dụ California); quy định tin nhắn SMS (**chưa xác minh** chi tiết trong phiên này) | Bắt đầu với web và lookbook (ít dữ liệu cá nhân). Chưa gửi SMS thay tiệm | Cần tra thêm |
| **Úc** | Đạo luật quyền riêng tư (**chưa xác minh** chi tiết) | Như Mỹ | Cần tra thêm |
| **Thanh toán** | **Stripe chưa hỗ trợ doanh nghiệp đặt tại Việt Nam** (theo blog của một nhà cung cấp, **chưa xác minh**). Paddle là bên bán thay (merchant of record), bán được ở hơn 200 nước, nhưng **chưa xác minh được Paddle có nhận người bán ở Việt Nam không**. Polar trả tiền về Việt Nam qua Stripe Connect Express; Creem có Việt Nam trong danh sách nước hỗ trợ | Dùng **bên bán thay**: họ thu thuế bán hàng hoặc VAT thay Nailmark, nên không phải đăng ký thuế ở Mỹ, EU, Úc. Cần anh mở tài khoản và chờ duyệt (mất vài tuần, **chưa xác minh**) | [Dodo Payments](https://dodopayments.com/blogs/stripe-supported-countries-alternatives), [Paddle](https://developer.paddle.com/concepts/sell/supported-countries-locales), [Polar](https://polar.sh/docs/merchant-of-record/supported-countries), [Creem](https://docs.creem.io/faq/supported-countries) |
| **Việt Nam (chiều tiền về)** | Quy định ngoại hối và thuế khi nhận tiền từ nước ngoài: **chưa xác minh** | Hỏi kế toán trước Cổng C | – |

---

## 4. Chọn thị trường nước ngoài

### 4.1 Bảng chấm điểm
Thang 1–5, điểm càng cao càng tốt (với "Luật": 5 là đơn giản nhất). Trọng số: Quy mô 25%, Lợi thế tiếng Việt 25%, Sẵn lòng trả tiền 20%, Dễ vào và dễ thu tiền 15%, Luật 15%. Điểm do AI chấm dựa trên mục 3. **Đây là phán đoán, không phải số đo.**

| Nước | Quy mô | Tiếng Việt | Sẵn lòng trả | Dễ vào, thu tiền | Luật | **Tổng (trên 5)** | Căn cứ chính |
|---|---|---|---|---|---|---|---|
| **Mỹ** | 5 | 5 | 5 | 3 | 3 | **4,40** | 113.275 tiệm; 48% thợ là người Việt (số cũ); có VietSALON; phần mềm $20–150/tháng |
| **Úc** | 3 | 4 | 4 | 4 | 4 | **3,75** | 6.500 cơ sở; 320.760 người nói tiếng Việt; dùng tiếng Anh |
| **Anh** | 3 | 4 | 4 | 3 | 2 | **3,30** | Tiệm nail là loại hình làm đẹp phổ biến nhất; Booksy £40/tháng; UK GDPR; rủi ro danh tiếng |
| **Đức** | 4 | 4 | 3 | 2 | 2 | **3,20** | 60.000 người làm trong ngành; khoảng 2/3 tiệm của người Việt (ước tính); khách cần web tiếng Đức |
| **Canada** | 3 | 3 | 4 | 3 | 3 | **3,20** | Chưa có số tiệm nail riêng; CASL; tiếng Pháp ở Quebec |
| **Séc** | 2 | 4 | 2 | 3 | 2 | **2,65** | Praha khoảng 200–266 tiệm; cộng đồng Việt khoảng 61.000 trở lên |
| **Nhật** | 4 | 1 | 4 | 1 | 3 | **2,65** | 28.492 tiệm; Hot Pepper Beauty chiếm lĩnh; không có lợi thế tiếng Việt |
| **Singapore** | 1 | 1 | 4 | 4 | 3 | **2,35** | 1.574 tiệm; Fresha đã có mặt |
| **Thái Lan** | 3 | 1 | 2 | 2 | 3 | **2,15** | 14.544 tiệm; khách đặt qua LINE |
| **Hàn Quốc** | 3 | 1 | 3 | 1 | 2 | **2,05** | Naver và Kakao chiếm lĩnh; tiệm 1–2 người |
| **Philippines** | 2 | 1 | 1 | 3 | 3 | **1,85** | 5.213 tiệm; khả năng chi trả thấp |

**Đọc bảng:** Mỹ đứng đầu rõ rệt. Úc thứ hai nhờ dễ vào. Anh, Đức, Canada gần bằng nhau. Nếu Mỹ chứng minh được giả thuyết tiếng Việt thì xét ba nước này cho 2028.

### 4.2 Đề xuất: 2 thị trường cho nửa cuối 2027

| Thứ tự | Thị trường | Đối tượng | Vì sao không chọn nước khác trước |
|---|---|---|---|
| **1** | **Mỹ: tiệm của người Việt ở California** (Orange County, San Jose, Sacramento) **và Texas** (Houston, Dallas) | Chủ tiệm 1–3 cơ sở, nói tiếng Việt, khách của tiệm nói tiếng Anh | Lớn nhất, bằng chứng tốt nhất, có kênh tiếng Việt sẵn |
| **2** | **Úc: Sydney** (khu Bankstown, Cabramatta) **và Melbourne** (Footscray, Richmond, Springvale) | Như trên | Nhỏ hơn nhưng dễ: tiếng Anh, múi giờ gần Việt Nam (lợi cho việc AI hỗ trợ trong giờ làm của tiệm), luật dễ hơn EU |

Tên khu dân cư người Việt ở Úc và Mỹ là gợi ý để quét Google Maps. **Mức độ tập trung tiệm nail ở các khu này chưa xác minh.**

### 4.3 Thiết kế phép thử ở Mỹ (Q3/2027, 8 tuần)

| Hạng mục | Thiết kế |
|---|---|
| **Giả thuyết** | H1: chào bằng tiếng Việt thì tỷ lệ trả lời và tỷ lệ mua cao hơn ít nhất 2 lần so với chào bằng tiếng Anh. H2: tiệm ở Mỹ chịu trả giá khoảng 5 lần giá Việt Nam mà vẫn giữ ≥ 70% mua không cần hỏi |
| **Danh sách** | Quét Google Places khoảng 400 tiệm ở 4 khu (Orange County, San Jose, Houston, Dallas). Lọc tiệm có dấu hiệu người Việt (tên chủ, tên tiệm, đánh giá có tiếng Việt). Chia ngẫu nhiên: 200 tiệm chào bằng tiếng Việt, 200 tiệm chào bằng tiếng Anh |
| **Kênh** | (1) Web mẫu tự động gửi qua email hoặc form trên web của tiệm (chỉ khi anh duyệt kênh và nội dung, như ở Việt Nam). (2) Nội dung cho chủ tiệm bằng tiếng Việt trên Facebook và YouTube (ví dụ "Tiệm nail ở Mỹ: web 1 trang có lookbook trong 24 giờ"). (3) Cân nhắc 1 quảng cáo trên VietSALON **sau khi** có ≥ 5 tiệm trả tiền (giá quảng cáo: **chưa xác minh**) |
| **Sản phẩm** | Web cho khách bằng tiếng Anh. Bảng điều khiển, video và trợ lý AI cho chủ tiệm bằng tiếng Việt. Nút đặt lịch gắn vào công cụ tiệm đang dùng (Fresha, Booksy, Square, Vagaro) hoặc số điện thoại hay SMS |
| **Giá thử** | Theo mục 5.3. Có 2 mức giá cho gói Chuẩn ($299 và $399) để đo độ nhạy giá |
| **Tiêu chí đạt (Cổng D, 30/9/2027)** | ≥ 10 tiệm trả tiền; tỷ lệ trả lời ở nhóm tiếng Việt ≥ 2 lần nhóm tiếng Anh; ≥ 70% mua không cần hỏi; doanh thu bình quân đơn đầu ≥ $250; ≤ 0,5 lần người chạm mỗi đơn |
| **Tiêu chí dừng** | Sau 8 tuần có < 3 tiệm trả tiền, **hoặc** nhóm tiếng Việt không hơn nhóm tiếng Anh, **hoặc** hoàn tiền > 15% |
| **Chi phí** | Lượt Places API (khoảng 400 lượt), tên miền và hosting, phí bên bán thay (theo % giao dịch). Không thuê người |

### 4.4 Nếu phép thử thất bại
- **Tiếng Việt không giúp gì:** bán bằng tiếng Anh cho mọi tiệm nhỏ ở Mỹ và Úc. Khi đó Nailmark phải cạnh tranh trực tiếp với Wix, GlossGenius…, nên cần xét lại định vị trước khi làm.
- **Giá quá cao:** thử mức khoảng 3 lần giá Việt Nam ($149 cho gói Chuẩn).
- **Không ai trả lời:** dừng hướng nước ngoài trong 2027. Dồn sức vào Việt Nam và thêm ngành (tóc, thú cưng) theo `PHEU_BAN_HANG.md`.

---

## 5. Bản địa hoá

### 5.1 Danh sách kiểm tra (mỗi thị trường)
| # | Hạng mục | Mỹ | Úc | Đức / Séc (2028) | Anh (2028) |
|---|---|---|---|---|---|
| 1 | Ngôn ngữ web cho khách | Tiếng Anh (Mỹ) | Tiếng Anh (Úc), ví dụ "colour", "appointment" | Tiếng Đức / tiếng Séc | Tiếng Anh (Anh) |
| 2 | Ngôn ngữ cho chủ tiệm | Tiếng Việt (giọng miền Nam hải ngoại), có thể chuyển sang tiếng Anh | Tiếng Việt và tiếng Anh | Tiếng Việt (giọng miền Bắc thường gặp hơn ở Séc và Đức, **chưa xác minh**) | Tiếng Việt và tiếng Anh |
| 3 | Tiền tệ | USD | AUD | EUR (Séc: niêm yết EUR, hiển thị thêm CZK) | GBP |
| 4 | Đơn vị và định dạng | Tháng/ngày, giờ AM/PM, số điện thoại +1 | Ngày/tháng, +61 | Ngày.tháng, +49 / +420 | Ngày/tháng, +44 |
| 5 | Nút đặt lịch | Gắn link Fresha, Booksy, Square, Vagaro, GlossGenius; hoặc gọi hay nhắn SMS | Fresha, Square, Timely (**chưa xác minh** mức phổ biến) | Treatwell, Fresha (**chưa xác minh**) | Fresha, Booksy, Treatwell |
| 6 | Lookbook (giả thuyết, cần kiểm chứng bằng dữ liệu Instagram và Pinterest của từng nước) | Móng dài acrylic hoặc dip powder (giá dip $35–55 theo [Yelp](https://www.yelp.com/article/how-much-do-nail-services-cost)), French, chrome, mẫu theo mùa | Gel và BIAB, móng tự nhiên, mẫu hè vào tháng 12 | Gel, móng ngắn và vừa, tông trầm | Gel, BIAB, mẫu Giáng sinh |
| 7 | Mùa lễ thay cho Tết | Mục 5.2 | Mục 5.2 | Mục 5.2 | Mục 5.2 |
| 8 | Quyền riêng tư và đồng ý | Chính sách quyền riêng tư, đồng ý dùng ảnh, không gửi SMS thay tiệm | Như Mỹ | GDPR: DPA, cookie, Impressum (Đức) | UK GDPR, DPA |
| 9 | Thanh toán | Bên bán thay (merchant of record), thẻ | Như Mỹ | Như Mỹ, có thêm SEPA (**chưa xác minh**) | Như Mỹ |
| 10 | Kiểm tra tiệm trước khi nhận | Xác minh tiệm có trên Google Maps | Như Mỹ | **Bắt buộc**: xác minh giấy phép kinh doanh (rủi ro danh tiếng) | **Bắt buộc**, như Đức |
| 11 | Hỗ trợ | Trợ lý AI 24/7 bằng tiếng Việt và tiếng Anh. Không gọi điện | Như Mỹ | Như Mỹ | Như Mỹ |

### 5.2 Lịch mùa lễ 2027 (thay cho Tết trong Gói Mùa)
Hệ thống tự chào Gói Mùa **trước 6 tuần** (theo `PHEU_BAN_HANG.md`). Ngày lễ dưới đây là lịch phổ thông, AI tính theo quy tắc của từng lễ.

| Mùa | Mỹ | Canada | Úc | Anh | Đức / Séc | Hạn chót tự động chào |
|---|---|---|---|---|---|---|
| Valentine | 14/2 | 14/2 | 14/2 | 14/2 | 14/2 | 3/1 |
| Ngày của Mẹ | **9/5/2027** (Chủ Nhật thứ hai của tháng 5) | 9/5 | 9/5 | **Mothering Sunday 7/3/2027** (3 tuần trước Lễ Phục sinh 28/3) | Muttertag và Den matek: 9/5 | 28/3 (Mỹ, Canada, Úc, Đức, Séc); 24/1 (Anh) |
| Mùa xuân, cưới, dạ hội | Prom (tháng 4–5), mùa cưới | Như Mỹ | Mùa cưới (tháng 9–11, mùa xuân Nam bán cầu) | Lễ Phục sinh 28/3 | Lễ Phục sinh 28/3; Séc có MDŽ 8/3 | 14/2 – 1/8 tuỳ nước |
| Hè | 4/7, mùa hè | 1/7 (Canada Day) | **Hè vào tháng 12 – tháng 2** | Mùa hè, lễ hội | Mùa hè | 20/5 |
| Thu | Halloween 31/10, **Thanksgiving 25/11** | Thanksgiving **11/10** | Melbourne Cup **2/11** | Bonfire Night 5/11 | – | 19/9 (Mỹ); 30/8 (Canada); 21/9 (Úc) |
| Cuối năm | **Black Friday 26/11** (bán thẻ quà tặng), Giáng sinh, Năm mới | Như Mỹ, có thêm Boxing Day 26/12 | Giáng sinh giữa mùa hè, Boxing Day | Mùa tiệc Giáng sinh | Mùa Vọng, Giáng sinh, Silvester 31/12 | 15/10 |
| Tết Nguyên đán (cho khách gốc Á) | Có ở California, Texas | Toronto, Vancouver | Sydney, Melbourne | London | Berlin, Praha | Tết 2028: khoảng 26/1/2028 (**cần đối chiếu**), chào từ 15/12/2027 |

### 5.3 Bảng giá theo nước (giá thử, chờ số liệu)

**Căn cứ:**
1. Ở Mỹ, phần mềm đặt lịch có giá $240–600/năm và Wix có giá $204–468/năm (mục 3.3). Một website do freelancer làm có giá $1.000–3.000.
2. Theo `PHEU_BAN_HANG.md` mục 2d, giai đoạn 4 "Chuẩn quốc tế" được định giá theo thị trường từng nước.
3. Mức đề xuất **khoảng 5 lần giá Việt Nam**. Mức này vẫn **dưới chi phí 1 năm phần mềm cộng web tự làm**, và chỉ bằng **khoảng 1/5 giá freelancer**.
4. Giữ đúng cấu trúc 3 mức để dùng chung phễu và chung nội dung.

| Gói | Việt Nam (giá ra mắt) | Mỹ (USD) | Úc (AUD) | Canada (CAD) | Anh (GBP) | EU: Đức, Séc (EUR) |
|---|---|---|---|---|---|---|
| Khởi đầu (một lần, gồm năm đầu) | 999.000 đ | **$199** ≈ 5.177.980 đ | A$299 ≈ 5.156.575 đ | C$269 ≈ 4.943.311 đ | £149 ≈ 5.112.355 đ | €179 ≈ 5.189.129 đ |
| Chuẩn | 1.990.000 đ | **$399** ≈ 10.381.980 đ (thử thêm mức $299 ≈ 7.779.980 đ) | A$599 ≈ 10.330.396 đ | C$549 ≈ 10.088.764 đ | £299 ≈ 10.259.022 đ | €349 ≈ 10.117.353 đ |
| Đẳng cấp | 2.990.000 đ | **$699** ≈ 18.187.980 đ | A$1.049 ≈ 18.091.127 đ | C$949 ≈ 17.439.412 đ | £529 ≈ 18.150.577 đ | €599 ≈ 17.364.740 đ |
| Duy trì từ năm thứ 2 | 499k – 990k đ/năm | $99/năm ≈ 2.575.980 đ | Theo tỷ lệ tương đương | – | – | – |
| Gói Mùa | 1.490.000 đ | $149 ≈ 3.876.980 đ | A$229 ≈ 3.949.350 đ | – | – | €139 ≈ 4.029.547 đ |
| Làm hộ trọn gói | 9.900.000 đ | $1.490 ≈ 38.769.800 đ | – | – | – | – |
| Đồng hành AI | 2.490.000 đ/tháng | $199/tháng ≈ 5.177.980 đ | – | – | – | – |

- **Giá đã gồm thuế hay chưa:** do bên bán thay tính theo từng nước. Trên trang bán hàng ghi "chưa gồm thuế bán hàng hoặc VAT".
- **Neo giá trị** giữ như ở Việt Nam: "web đáng giá $2.000" ([Clutch](https://clutch.co/web-designers/pricing), đã dùng trong `PHEU_BAN_HANG.md`).
- **Ô trống ("–")**: chưa đặt giá vì chưa mở thị trường đó trong 2027.

### 5.4 Tác động lên mục tiêu 2027 (tính thử)
| Kịch bản (Q3–Q4/2027) | Giả định | Doanh thu |
|---|---|---|
| Thận trọng | 100 tiệm Mỹ và Úc × (gói Chuẩn $399 + 1 Gói Mùa $149) | $54.800 ≈ 1,43 tỷ đ |
| Cơ sở | 500 tiệm × ($399 + 2 Gói Mùa × $149) = 500 × $697 | $348.500 ≈ 9,07 tỷ đ |
| So sánh | 500 tiệm Việt Nam × (1,99 triệu + 2 × 1,49 triệu) | 2,49 tỷ đ |

**Ý nghĩa:** mỗi tiệm ở nước ngoài mang lại doanh thu **khoảng 3,6 lần** một tiệm ở Việt Nam ($697 ≈ 18,14 triệu đ, so với 4,97 triệu đ), trong khi việc phục vụ đều do AI làm. **Đây là giả định, chưa đo.**

### 5.4b Ghi chú cho các nước chưa ưu tiên (để dùng khi xét lại năm 2028)
| Nước | Phong cách và lookbook | Mùa lễ chính | Kênh đặt lịch quen dùng | Vì sao chưa làm |
|---|---|---|---|---|
| Nhật | Gel chiếm khoảng 67% doanh thu dịch vụ; menu giá cố định theo mẫu; mẫu mới mỗi tháng (`research/hinh_mau_dong_a.md`) | White Day 14/3, mùa tốt nghiệp và nhập học (tháng 3–4), Giáng sinh | Hot Pepper Beauty, Rakuten Beauty, LINE | Cần tiếng Nhật; nền tảng lớn chiếm lĩnh; không có lợi thế tiếng Việt ở phía chủ tiệm |
| Hàn Quốc | "Mẫu của tháng" (이달의 아트) giá 45.000–85.000 won (`research/hinh_mau_dong_a.md`) | Valentine, White Day, Chuseok | Naver, KakaoTalk, Daangn | Hệ sinh thái riêng; luật dữ liệu chặt (**chưa xác minh** chi tiết) |
| Singapore | Mani nhanh, gói trả trước (Nail Palace từng bị cảnh cáo vì ép bán gói, `research/hinh_mau_dong_nam_a.md`) | Tết Nguyên đán, Hari Raya, Deepavali, Giáng sinh | Fresha | Thị trường nhỏ (1.574 tiệm) |
| Thái Lan, Philippines | Giá dịch vụ thấp | Songkran (Thái); Giáng sinh kéo dài (Philippines) | LINE (Thái), Facebook (Philippines), **chưa xác minh** | Khả năng chi trả thấp; không có lợi thế tiếng Việt |
| Canada | Như Mỹ; Quebec cần tiếng Pháp | Thanksgiving 11/10, Ngày của Mẹ 9/5 | Như Mỹ | CASL; số tiệm nail riêng chưa có |

### 5.5 Việc chuẩn bị trước Cổng C (Q2/2027, AI làm, anh duyệt)
1. Chọn bên bán thay (Paddle, Polar hoặc Creem). Kiểm tra Paddle có nhận người bán ở Việt Nam không. **Anh mở tài khoản.**
2. Dịch phễu sang tiếng Anh: trang bán hàng, bài tự chấm 8 tiêu chuẩn, web mẫu, 8 video (lồng tiếng AI, có phụ đề tiếng Việt).
3. Làm chính sách quyền riêng tư, điều khoản, mẫu xin đồng ý dùng ảnh (tiếng Anh). **Nên nhờ luật sư xem 1 lần**, có tính phí, chờ anh duyệt.
4. Sửa `tu_dong_demo.py` để chạy với địa chỉ và giờ mở cửa ở Mỹ và Úc (Places API đã hỗ trợ toàn cầu).
5. Hỏi kế toán về việc nhận ngoại tệ và thuế ở Việt Nam.

---

## 6. Lộ trình 2027 theo quý

| Quý | Việt Nam | Nước ngoài | Cổng và chỉ số | Anh Ninh làm |
|---|---|---|---|---|
| **Q1/2027** | TP.HCM: phễu tự phục vụ, mùa Tết, Gói 8/3, App v2 (Zalo). Mở rộng sang Thủ Dầu Một, Dĩ An, Vũng Tàu. Quét Google Maps Hà Nội (bổ sung), Đà Nẵng, Hải Phòng, Cần Thơ, Biên Hòa, Nha Trang, Huế | Không làm gì (chỉ nghiên cứu trên giấy) | Cổng 2 (2/2027); **Cổng A (31/3)**: ≥ 30 tiệm trả tiền, ≥ 80% mua không cần hỏi, ≥ 10 tiệm có số liệu trước và sau | Duyệt tin nhắn, chốt giá sau Tết |
| **Q2/2027** | Hà Nội và Đà Nẵng: lookbook theo vùng, nội dung cho chủ tiệm, web 2 thứ tiếng ở Đà Nẵng. Gói Mùa 30/4 – 1/5. Bắt đầu nâng giá giai đoạn 2 nếu đủ bằng chứng | **Chuẩn bị** (mục 5.5): bên bán thay, tiếng Anh, chính sách, quét 400 tiệm ở Mỹ | **Cổng B và Cổng C (30/6)**: ≥ 150 tiệm trả tiền, ≥ 25% mua tiếp Gói Mùa, thanh toán quốc tế chạy thật | Mở tài khoản thanh toán quốc tế; duyệt kênh chào ở Mỹ |
| **Q3/2027** | Mở tự phục vụ toàn quốc: Biên Hòa, Cần Thơ, Hải Phòng, Nha Trang, Huế. Gói Mùa 2/9 và 20/10 | **Phép thử Mỹ** 8 tuần (mục 4.3). Gói Mùa Halloween và Thanksgiving chào từ 19/9 | **Cổng D (30/9)**: Mỹ ≥ 10 tiệm trả tiền, tiếng Việt ≥ 2 lần tiếng Anh, ≥ 70% mua không cần hỏi | Quyết mở rộng hay dừng |
| **Q4/2027** | Toàn quốc. Gói Noel. **Bộ Tết 2028 chào từ giữa tháng 12** | Mỹ: mở bán rộng (nếu qua Cổng D), Black Friday 26/11, Giáng sinh. **Úc: thử** (Sydney, Melbourne; mùa hè và Giáng sinh) | **Cổng E (15/12)**: Mỹ ≥ 100 tiệm, Úc ≥ 20, nước ngoài ≥ 20% doanh thu. Chọn nước cho 2028 (Anh, Đức, Canada, Séc) | Duyệt kế hoạch 2028 |

### 6.0 Chỉ tiêu cộng dồn theo quý (giả định, chỉnh sau Cổng 2)
| Chỉ số | Hết Q1 | Hết Q2 | Hết Q3 | Hết Q4 |
|---|---|---|---|---|
| Tiệm trả tiền ở Việt Nam (cộng dồn) | 30 | 150 | 500 | 1.200 |
| Trong đó ngoài TP.HCM | 0 | 30 | 200 | 600 |
| Tiệm trả tiền ở nước ngoài | 0 | 0 | 10 | 120 (Mỹ 100, Úc 20) |
| Tỷ lệ mua không cần hỏi | ≥ 80% | ≥ 80% | ≥ 80% (Việt Nam); ≥ 70% (Mỹ) | ≥ 80% (mọi nơi) |
| Tỷ lệ mua tiếp Gói Mùa | Đo lần đầu (8/3) | ≥ 25% | ≥ 30% | ≥ 35% |
| Lần người chạm mỗi đơn dưới 3 triệu | ≤ 0,3 | ≤ 0,3 | ≤ 0,3 | ≤ 0,2 |
| Hoàn tiền | ≤ 5% | ≤ 5% | ≤ 5% (Mỹ ≤ 10%) | ≤ 5% |

**Lưu ý:** 1.200 tiệm ở Việt Nam cộng 120 tiệm ở nước ngoài vẫn còn xa mốc 10.000 doanh nghiệp trong `MUC_TIEU_2027.md`. Khoảng cách còn lại phải đến từ ngành mới (tóc, thú cưng, theo Cổng 2) và kênh số đông. **Kế hoạch này không tự đạt được mục tiêu 10.000 doanh nghiệp.** Đây là điều cần nói rõ với anh.

### 6.1 Nguồn lực (chỉ dùng AI)
| Mảng việc | AI làm | Người làm (anh Ninh hoặc thuê ngoài có tính phí) |
|---|---|---|
| Quét Google Maps, tạo web mẫu | Tự động (Places API, `tu_dong_demo.py`) | – |
| Nội dung cho chủ tiệm (tiếng Việt, tiếng Anh) | Viết, dựng video, lồng tiếng | Duyệt mẫu 1 lần mỗi thị trường |
| Lookbook theo vùng miền và theo nước | Tổng hợp xu hướng, chọn mẫu, đặt tên | – |
| Hỗ trợ khách | Trợ lý AI 24/7 | Ngoại lệ, trong vòng 24 giờ |
| Thanh toán, thuế | Theo dõi, đối soát | **Mở tài khoản; kế toán** |
| Pháp lý (chính sách quyền riêng tư, điều khoản) | Soạn bản nháp | **Luật sư xem 1 lần mỗi vùng** (có phí, chờ anh duyệt) |
| Bán hợp đồng Chuỗi (từ 50 triệu đ/năm) | Chuẩn bị hồ sơ | **Anh Ninh** |

**Nút cổ chai thật sự không phải công sức AI**, mà là: (1) thời gian xét duyệt tài khoản thanh toán, (2) thời gian anh duyệt kênh và nội dung, (3) việc tiệm trả lời và gửi ảnh.

---

## 7. Rủi ro và cách chặn

| # | Rủi ro | Khả năng | Ảnh hưởng | Chặn bằng |
|---|---|---|---|---|
| 1 | Mở thành phố mới khi TP.HCM chưa chứng minh được, khiến việc phục vụ bị loãng | Trung bình | Cao | Cổng A và B bắt buộc. Không đạt "≥ 80% mua không cần hỏi" thì không mở |
| 2 | Riêng ngành nail ở Việt Nam không đủ 10.000 doanh nghiệp (cả nước khoảng 17.032 tiệm) | Cao | Cao | Ra nước ngoài (doanh thu mỗi tiệm khoảng 3,6 lần) và thêm ngành tóc, thú cưng |
| 3 | Giả thuyết tiếng Việt sai (chủ tiệm thế hệ 2 thích tiếng Anh; đã có đối thủ nói tiếng Việt) | Trung bình | Cao | Phép thử A/B với tiêu chí dừng rõ ràng (mục 4.3) |
| 4 | Không nhận được tiền từ nước ngoài (Stripe không hỗ trợ Việt Nam) | Trung bình | Cao | Bên bán thay; mở tài khoản từ Q2. Có phương án dự phòng (Polar, Creem) |
| 5 | Vi phạm quyền riêng tư (GDPR, UK GDPR, CASL) | Thấp nếu chưa vào EU, Anh, Canada | Rất cao | 2027 chỉ làm Mỹ và Úc. Không gửi SMS thay tiệm. Xin đồng ý dùng ảnh |
| 6 | Rủi ro danh tiếng: tiệm có liên quan buôn người hoặc lao động cưỡng bức (Anh, Đức, Bỉ) | Thấp đến trung bình | Rất cao | Xác minh tiệm trước khi nhận; điều khoản cho phép từ chối; chưa vào Anh, Đức trong 2027 |
| 7 | Chủ tiệm người Việt nhạy cảm về giá (giá dịch vụ thấp hơn khoảng 36% so với tiệm khác) | Trung bình | Trung bình | Thử 2 mức giá. Có mức Khởi đầu $199. Dùng "1 năm phần mềm" làm neo so sánh |
| 8 | Đối thủ lớn (Fresha miễn phí hoặc rẻ, GlossGenius có sẵn web) | Cao | Trung bình | Không cạnh tranh về đặt lịch. Bán lookbook, nội dung mùa lễ và hướng dẫn bằng tiếng Việt, gắn với công cụ tiệm đang dùng |
| 9 | Số liệu thị trường sai (lấy từ đoạn trích, WebFetch bị chặn) | Cao | Trung bình | Trước Cổng C, mở bản gốc các nguồn Poidata, IBISWorld, Pew, UCLA. Quyết định dựa trên số đo của chính Nailmark, không dựa trên số thị trường |
| 10 | Hỗ trợ khác múi giờ (Mỹ chậm 14–15 giờ so với Việt Nam) | Cao | Thấp | Trợ lý AI 24/7. Người chỉ xử lý ngoại lệ trong 24 giờ |

---

## 8. Việc AI làm tiếp ngay (không cần anh duyệt vì không liên hệ ai)
1. Quét Google Maps Hải Phòng, Cần Thơ, Biên Hòa, Nha Trang, Huế và bổ sung Hà Nội. Ghi kết quả vào `research/` để thay các ô "chưa có" ở mục 1.2.
2. Tra bảng dân số thành thị trong Điều tra giữa kỳ 2024 (NSO) để điền cột "lõi đô thị".
3. Quét thử 50 tiệm ở Orange County để đo tỷ lệ tiệm có web và có link đặt lịch. So với số 50% có website của Poidata.

## 9. Danh sách giả định cần kiểm chứng (cập nhật sau mỗi cổng)
| # | Giả định | Dùng ở đâu | Kiểm chứng bằng | Khi nào |
|---|---|---|---|---|
| G1 | TP.HCM đạt ≥ 30 tiệm trả tiền trước 31/3/2027 | Cổng A | Đếm giao dịch payOS | 31/3/2027 |
| G2 | ≥ 80% đơn dưới 3 triệu được mua mà không cần hỏi | Mọi cổng | Đối chiếu đơn với nhật ký hỏi đáp | Hằng tuần |
| G3 | ≥ 25% khách web mua tiếp Gói Mùa | Cổng B; lợi nhuận | Tỷ lệ mua Gói 8/3 và 30/4 | 30/6/2027 |
| G4 | Hà Nội chuyển đổi được ≥ 70% so với TP.HCM | Cổng B | So tỷ lệ demo → trả tiền | 30/6/2027 |
| G5 | Chủ tiệm người Việt ở Mỹ trả lời tin tiếng Việt nhiều gấp ≥ 2 lần tin tiếng Anh | Cổng D | Phép thử A/B (mục 4.3) | 30/9/2027 |
| G6 | Tiệm ở Mỹ chịu giá khoảng 5 lần Việt Nam | Mục 5.3 | So 2 mức giá $299 và $399 | 30/9/2027 |
| G7 | Có bên bán thay nhận người bán ở Việt Nam | Cổng C | Mở tài khoản thật, chạy 1 giao dịch | 30/6/2027 |
| G8 | Số tiệm thị trường (Poidata, IBISWorld) đủ đúng để xếp hạng nước | Mục 4.1 | Mở bản gốc; quét Google Maps mẫu | Trước Cổng C |
| G9 | 50% tiệm ở Mỹ đã có website (Poidata), nên phần còn lại là khách tiềm năng, và cả tiệm có web xấu | Mục 4.3 | Quét 50 tiệm ở Orange County | Q2/2027 |
| G10 | Doanh thu mỗi tiệm nước ngoài khoảng 3,6 lần Việt Nam, chi phí phục vụ tương đương | Mục 5.4 | Đo doanh thu và số lần chạm của 10 tiệm Mỹ đầu tiên | Q4/2027 |

## 10. Nguồn chính (theo nhóm)
- **Việt Nam:** [Poidata VN](https://www.poidata.io/report/nail-salon/vietnam) · [Saigon Times](https://thesaigontimes.vn/tphcm-cong-bo-12-dau-an-noi-bat-nam-2025/) · [LSVN 34 tỉnh](https://lsvn.vn/34-tinh-thanh-pho-tren-ca-nuoc-tu-ngay-12-6-2025-a158994.html) · [NQ 202/2025](https://vbpl.vn/TW/Lists/vbpq/Attachments/179501/202_2025_QH15_648951.doc) · [Thư viện Pháp luật](https://thuvienphapluat.vn/hoi-dap-phap-luat/xep-hang-dan-so-34-tinh-thanh-viet-nam-moi-nhat-2026-the-nao-138084847.html) · [NSO DSGK 2024](https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2025/01/thong-cao-bao-chi-ket-qua-dieu-tra-dan-so-va-nha-o-giua-ky-nam-2024/) · [Smartscraper Đà Nẵng](https://rentechdigital.com/smartscraper/business-report-details/vietnam/list-of-nail-salons-in-da-nang)
- **Thị trường nước ngoài:** [Poidata US](https://poidata.io/report/nail-salon/united-states) · [Poidata JP](https://poidata.io/report/nail-salon/japan) · [Poidata SG](https://poidata.io/report/nail-salon/singapore) · [Poidata TH](https://poidata.io/report/nail-salon/thailand) · [Poidata PH](https://www.poidata.io/report/nail-salon/philippines) · [IBISWorld US](https://www.ibisworld.com/united-states/market-size/personal-waxing-nail-salons/4411/) · [IBISWorld AU](https://www.ibisworld.com/australia/market-size/personal-waxing-nail-salons/5126/) · [IBISWorld CA](https://www.ibisworld.com/canada/number-of-businesses/hair-nail-salons/1718/) · [IBISWorld UK](https://www.ibisworld.com/united-kingdom/industry/hairdressing-beauty-treatment-in-the-uk/4900/) · [Scratch UK](https://www.scratchmagazine.co.uk/news/nail-salons-report-8-growth-in-5-years-but-its-not-all-good-news-for-the-sector) · [Statista JP](https://statista.com/statistics/1223981/japan-market-size-nail-care-service)
- **Người Việt trong ngành nail:** [UCLA Labor Center](https://labor.ucla.edu/publication/nail-files/) · [UCLA CA 2024](https://labor.ucla.edu/wp-content/uploads/2024/04/Nail-Files-California-3.18.2024.pdf) · [Matador / NAILS 2012–13](https://matadornetwork.com/life/why-vietnamese-americans-rule-the-nail-salon-scene) · [NAILS](https://www.nailsmag.com/389759/the-vietnamese-american-salon-industry) · [NAILS khảo sát giá](https://www.nailsmag.com/390022/vietnamese-survey-answers-many-questions-begs-many-more) · [Pew](https://www.pewresearch.org/race-and-ethnicity/fact-sheet/asian-americans-vietnamese-in-the-u-s/) · [ABS](https://www.abs.gov.au/census/find-census-data/quickstats/2021/5105_AUS) · [Worldcrunch (Đức)](https://worldcrunch.com/in-the-news/cheap-nails-hidden-chains-human-trafficking-inside-berlin-s-nail-salons/) · [Radio Prague](https://english.radio.cz/node/8587695) · [East London Lines](https://www.eastlondonlines.co.uk/?p=31240) · [VietSALON](https://us.exactconnections.com/media/viet-salon) · [VOV (Nhật)](https://english.vov.vn/en/society/vietnamese-community-remains-japans-second-largest-foreign-group-post1341896.vov) · [Korea Times](https://www.koreatimes.co.kr/southkorea/globalcommunity/20251219/vietnamese-lead-surge-as-koreas-foreign-resident-population-hits-record-high)
- **Giá phần mềm và web:** [Fresha qua GlossGenius](https://glossgenius.com/blog/fresha-pricing) · [Booksy UK](https://biz.booksy.com/en-gb/pricing) · [Booksy blog](https://biz.booksy.com/blog/best-salon-software-2026) · [Pabau (Vagaro)](https://pabau.com/blog/vagaro-vs-booksy/) · [CostBench GlossGenius](https://costbench.com/software/salon-spa/glossgenius/) · [Square](https://square.com/us/en/appointments/pricing) · [Wix blog](https://www.wix.com/blog/how-much-is-a-wix-website) · [Squarespace (Emergent)](https://emergent.sh/learn/squarespace-pricing) · [ManyPixels](https://www.manypixels.co/blog/web-design/for-small-businesses) · [ThePricer](https://www.thepricer.org/how-much-does-a-manicure-cost/)
- **Luật và thanh toán:** [EU GDPR](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/enforcement-and-sanctions_en) · [ICO](https://ico.org.uk/about-the-ico/our-information/policies-and-procedures/data-protection-fining-guidance/statutory-background/the-maximum-amount-of-a-fine-under-uk-gdpr-and-dpa-2018) · [CRTC CASL](https://www.crtc.gc.ca/eng/com500/info.htm) · [Paddle](https://developer.paddle.com/concepts/sell/supported-countries-locales) · [Polar](https://polar.sh/docs/merchant-of-record/supported-countries) · [Creem](https://docs.creem.io/faq/supported-countries) · [Dodo Payments](https://dodopayments.com/blogs/stripe-supported-countries-alternatives)
