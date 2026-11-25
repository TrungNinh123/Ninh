# Nailmark – Bản hoàn chỉnh (25/11/2026)

Bộ đầy đủ để AI vận hành Nailmark từ đầu đến cuối, không cần người. Anh Ninh chỉ giao nhiệm vụ, mục tiêu và kết quả mong muốn.

## 1. Sản phẩm trên web (đã đăng, riêng tư)
| Trang | Dùng để | Tình trạng |
|---|---|---|
| [Nailmark: trang chính](https://claude.ai/artifact/PKfZSjUNBkiZv5fcvnVq6H) | Chuẩn 17 chuỗi ở 9 quốc gia, tự chấm điểm, bảng giá ra mắt, bảng so sánh phạm vi, 14 câu hỏi đáp | Chạy được |
| [Quà miễn phí: 4 công cụ](https://claude.ai/artifact/2TvYceH8BLKFDRJxEwC2iV) | Thẻ QR đặt lịch, poster Tết 2027, bảng giá đẹp, chỉnh sáng ảnh giữ màu; chạy ngay trên trình duyệt | Chạy được. QR đã quét thử |
| [Gói quà mẫu cho một tiệm](https://claude.ai/artifact/34gGgDSoviLVRSQfRNdFwB) | Web mẫu, poster, thẻ QR, video 12 giây (tạo bằng `scripts/qua_tang.py`) | Chạy được |
| [Hướng dẫn 4 bước](https://claude.ai/artifact/QJDw8KGhpGcwCaL1uVn27Y) | Video 30 giây quay từ app thật, việc cần làm từng bước, cách xử lý lỗi | Chạy được |
| App tự làm (`scripts/app_tu_lam.py` + `nailmark/app.html`) | Tiệm tự tạo web với ảnh thật và giá thật, khoảng 4 giây | Chạy trên máy thử. Cần hosting |
| [Bộ Tết 2027](https://claude.ai/artifact/PAJCmjqvdW5unwYzWWmCet) | Chiến dịch Tết 10 tuần cho tiệm | Nội dung xong |

## 2. Công cụ tự động (repo)
| Lệnh | Việc |
|---|---|
| `scripts/tu_dong_demo.py` | Từ Google Maps ra web mẫu, kèm giờ mở cửa thật |
| `scripts/qua_tang.py` | Gói quà miễn phí cho một tiệm, khoảng 17 giây |
| `scripts/tao_web.py` | Web v2 với ảnh thật và giá thật, chỉnh sáng giữ màu, QR Zalo |
| `scripts/app_tu_lam.py` | App 4 bước, đã test 10 tình huống lỗi |
| `scripts/kiem_tra_web.py` | Kiểm 8 mục chất lượng web, báo ĐẠT hoặc CHƯA ĐẠT |
| `scripts/hoi_dap_web.py` | Đưa câu hỏi phổ biến từ ngân hàng hỏi đáp lên trang chính |
| `scripts/ty_gia_vcb.py` | Lấy tỷ giá bán ra Vietcombank |
| `scripts/video/quay_huong_dan.js` | Quay video hướng dẫn từ app thật |

## 3. Nội dung để không ai phải hỏi
| Tài liệu | Nội dung |
|---|---|
| `research/hoi_dap/` (A–D) | **168 câu hỏi có sẵn câu trả lời:** Nailmark, dịch vụ nail, vệ sinh và sức khoẻ, vận hành và thuế |
| `research/XU_LY_TU_CHOI.md` | **48 lời từ chối trong 11 nhóm.** Mỗi lời có: ý thật của khách, câu trả lời trung thực, bước tiếp theo, điều không được nói |
| `research/noi_dung/CHUOI_30_BAI.md` | **30 bài đăng** (7/12/2026 → 15/1/2027) và **10 kịch bản video ngắn**. Mỗi bài dẫn về quà miễn phí |
| `research/kien_thuc/` (01–03) | Kiến thức ngành có nguồn. Giá TP.HCM và thuế 2026 đã đối chiếu với trang gốc |
| `research/NOI_DUNG_HO_TRO.md` | 4 bước, 4 video, 8 quy tắc để không thể làm sai, buổi hỏi đáp hằng tuần |

## 4. Quy trình và nguyên tắc
| Tài liệu | Nội dung |
|---|---|
| `research/NGUYEN_TAC_AI_TU_PHUC_VU.md` | AI làm toàn bộ, cho giá trị trước, khách không cần hỏi. Đơn từ 3 triệu mới có xác minh |
| `research/QUY_TRINH_CHUYEN_GIAO.md` | 11 khâu từ lúc thấy Nailmark đến lúc gia hạn, 5 mẫu tin tự động, 3 ngoại lệ có người |
| `research/PHAM_VI_DICH_VU.md` | Mỗi gói gồm gì, không gồm gì |
| `research/PHEU_BAN_HANG.md` | Bậc giá ra mắt, lộ trình nâng giá theo mốc bằng chứng |
| `research/SAN_SANG_THUC_TE.md` | Kiểm kê trung thực: cái gì chạy được, cái gì chưa |

## 5. Kế hoạch thị trường 2027
- **Chi tiết:** `research/KE_HOACH_MO_RONG_2027.md`
- **Q1:** TP.HCM (gồm Bình Dương, Vũng Tàu cũ sau khi sáp nhập). **Cổng A (31/3):** ≥30 tiệm trả tiền và ≥80% "mua không cần hỏi".
- **Q2:** Hà Nội, thử nhỏ ở Đà Nẵng. **Q3:** tự phục vụ toàn quốc.
- **Nước ngoài:** thử với tiệm người Việt ở Mỹ (California, Texas) trong Q3, Úc trong Q4. Giá thử khoảng 5 lần giá Việt Nam: $199 / $399 / $699.
- **Lý do phải ra nước ngoài:** cả nước chỉ có khoảng 17.032 tiệm nail (Poidata 8/2025), không đủ cho mục tiêu 10.000 doanh nghiệp. Ở Mỹ, người Việt chiếm khoảng 48% thợ nail (số liệu cũ của NAILS), nên tiếng Việt là lợi thế.
- **Lưu ý:** mọi ngưỡng cổng và điểm chấm thị trường là **giả định**, phải chỉnh lại bằng số liệu thật ở TP.HCM.

## 6. Để chạy với khách thật: cần anh (đứng tên tài khoản và pháp lý)
1. **Hosting.** Để app, web của tiệm và trang quà chạy công khai.
2. **Cổng thanh toán QR tự xác nhận** cho Việt Nam. Thêm "merchant of record" (bên trung gian bán hàng và thu thuế hộ) cho nước ngoài, cần trong Q2.
3. **Zalo OA.** Để gửi tin bàn giao, nhắc việc, trợ lý AI.
4. **Tài khoản Facebook và TikTok của Nailmark.** Để đăng chuỗi 30 bài.
5. **Số điện thoại, email, pháp nhân.** Để xác minh đơn từ 3 triệu, làm hợp đồng, xuất hoá đơn.
6. **Kyma API key.** Để AI đọc bảng giá, làm giọng đọc video và trợ lý AI.

**Chín mục [CHỜ DUYỆT]:** pháp nhân và liên hệ, hợp đồng, hoàn tiền, hoá đơn, trả góp, thưởng giới thiệu, chụp ảnh trong gói Làm hộ, giá cho nhân viên thứ hai ở gói Chuyển giao, giờ buổi hỏi đáp.
