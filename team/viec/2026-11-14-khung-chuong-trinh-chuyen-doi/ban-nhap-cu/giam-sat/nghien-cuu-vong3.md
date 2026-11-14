# Giám sát — Lan (nghien-cuu) · Vòng 3 (vòng cuối)

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày chấm: 14/11/2026 · Người chấm: Bảo – Giám sát · Phiên bản prompt: 1.0
Phạm vi: chỉ kiểm 3 lỗi nhỏ nêu trong `giam-sat/nghien-cuu-vong2.md` (phản hồi 2, 3, 4). Các phần khác giữ nguyên điểm vòng 2.

## Bảo đã tự kiểm chứng những gì
- Script so link giữa phần thân và mục 4: `130 130 set() set()`, tức khớp 130/130. Mọi dòng bảng đủ 5 cột, kể cả dòng 76.
- Mạng: curl tới portal.mof.gov.vn vẫn bị chặn (CONNECT tunnel 403). Chưa mở được trang gốc nào.

## Đối chiếu 3 lỗi vòng 2
| # | Lỗi vòng 2 | Tình trạng | Bằng chứng |
|---|---|---|---|
| 1 | Dòng 76 NĐ 284/2026: nhãn "Toàn văn" trỏ tới bài tin, ô Giá trị ghép lộn | **Đã sửa** | Cột Nguồn tách ra "Văn bản: LuatVietnam – trang văn bản" và "Bản tin: Tạp chí Toà án; …". Ô Giá trị là câu hoàn chỉnh, link không còn nằm trong ô. Có ghi "**Link toàn văn trên vbpl.vn, congbao.chinhphu.vn, thuvienphapluat.vn: chưa tìm được.**" |
| 2 | Câu mở 6 mâu thuẫn với bảng 2.6 | **Đã sửa** | Dòng 155: "đã có số tham chiếu gần (giảng viên, huấn luyện viên, trưởng phòng vận hành; xem 2.6). Chưa có số cho đúng chức danh…", vẫn giữ cách xác minh |
| 3 | Thứ tự mốc 18/10 → 22/10 → 28/10 và nguồn của mốc 28/10 | **Đã sửa** | Dòng 15 và 75: "Theo thứ tự: số liệu đến 18/10… ngày 22/10 CAEX… ngày 28/10 Bộ Tài chính trả lời…", gắn link portal.mof.gov.vn/hoidapcstc/…/166886. Dòng 75 còn ghi trung thực "trang ghi ngày đăng 25/7/2025, lệch với nội dung, cần kiểm tra lại" |

## Bảng chấm
| # | Tiêu chí (trọng số, Chặn) | % | Bằng chứng |
|---|---|---|---|
| 1 | Trả lời đủ các câu hỏi nghiên cứu (25, Chặn) | 90 | Không đổi so với vòng 2. Giá đối thủ nội địa có thu phí vẫn chỉ có 1 mức, đã ghi "chưa tìm được" |
| 2 | Số liệu quan trọng có nguồn gốc đã mở (link) (25, Chặn) | 58 | Phần trong tầm của Lan đã làm hết: NĐ 284 có trang văn bản và ghi rõ chưa tìm được link toàn văn, mốc 28/10 có link. Vẫn **chưa mở được trang nào** (curl 403), nên tiêu chí ở trần môi trường 55–60% |
| 3 | Không bịa; ghi rõ điều chưa tìm được và cách xác minh (20, Chặn) | 93 | Ba lỗi (a), (b), (c) của vòng 2 đã sửa. Chỉ còn (d): các dữ kiện sau 6/2026 chưa kiểm chứng được (do môi trường). Ngày đăng của trang MOF bị lệch đã được ghi rõ |
| 4 | Ghi thời điểm và độ tin cậy từng dữ kiện (15) | 90 | Không đổi (vẫn còn "—"/"chưa rõ năm" ở vài dòng) |
| 5 | Đúng mẫu: kết luận, bảng dữ kiện, câu hỏi mở, nguồn (15) | 97 | Dòng 76 đã sạch, mục 3 khớp bảng, Nguồn 130/130. Trừ nhẹ vì ghi chú đầu file chưa có dòng "Vòng 3" |

**Điểm:** 25×0,90 + 25×0,58 + 20×0,93 + 15×0,90 + 15×0,97 = 22,5 + 14,5 + 18,6 + 13,5 + 14,55 = **83,65 → 84/100**

**Kết luận: CHƯA ĐẠT, chỉ do môi trường.** Điểm tổng ≥ 80, cả 3 lỗi nhỏ đã sửa hết. Tiêu chí Chặn 2 vẫn 58% < 60% vì môi trường chặn mạng, không mở được trang gốc nào. Lan không còn lỗi nào tự sửa được.

## Phản hồi
1. Tiêu chí 2 (do môi trường) → khi được mở mạng cho các tên miền nguồn: mở và đối chiếu các dữ kiện trong 5 Kết luận, ưu tiên toàn văn NQ 05/2025, NĐ 284/2026 và trang hỏi đáp MOF 166886 (ngày đăng đang lệch); ghi "đã mở ngày …" và nâng lên Cao những dòng khớp.
2. Nhỏ → thêm dòng ghi chú "Vòng 3" ở đầu file, liệt kê 3 sửa đổi.

Đề xuất cho trưởng nhóm: bàn giao ở trạng thái "CHƯA ĐẠT, chặn bởi môi trường". Mọi số liệu giữ mức tin cậy TB, và số pháp lý phải được đối chiếu toàn văn trước khi đưa cho khách.
