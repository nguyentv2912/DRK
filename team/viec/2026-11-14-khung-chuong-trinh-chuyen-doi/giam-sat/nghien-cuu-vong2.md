# Giám sát — Lan (nghien-cuu) · Vòng 2

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Ngày chấm: 14/11/2026 · Người chấm: Bảo – Giám sát · Phiên bản prompt: 1.0
File nộp: `nghien-cuu.md` (6.024 chữ, đầu file có ghi chú vòng 2). Đối chiếu với phiếu vòng 1: `giam-sat/nghien-cuu-vong1.md`.

## Bảo đã tự kiểm chứng những gì
- **Mục Nguồn:** chạy script so link giữa phần thân (mục 1–3) và mục 4. Kết quả `127 127 missing: [] extra: []`, tức khớp đủ 127/127, không thiếu và không thừa link nào.
- **Cấu trúc bảng:** script đếm số cột ở mọi dòng bảng. Dòng nào cũng đủ 5 cột.
- **Dữ kiện không link:** grep "qua tìm kiếm"/"kết quả tìm kiếm" chỉ còn ở dòng 37 (78%, đã hạ xuống Thấp và đưa ra khỏi Kết luận) và dòng 125 (Trưởng phòng KD, Thấp, không nằm trong Kết luận). Cả hai đều theo đúng phương án thay thế mà phản hồi 2 vòng 1 cho phép. Không còn "LawSoft". Số TopCV 47,5% (dòng 110) đã có link.
- **Mốc thời gian:** grep 18/10, 22/10, 28/10. Mốc chung "tính đến 28/10/2026" xuất hiện thống nhất ở dòng 15, 75 và câu mở 2 (dòng 151).
- **Mạng:** curl tới vbpl.vn và tuoitre.vn vẫn trả `CONNECT tunnel failed, response 403`. Môi trường vẫn chặn, không phải lỗi của Lan.

## Đối chiếu phản hồi vòng 1
| # | Phản hồi vòng 1 | Tình trạng | Bằng chứng |
|---|---|---|---|
| 1 | Mở trang gốc các dữ kiện trong Kết luận (khi có quyền mạng) | **Chưa làm được, do môi trường** | Dòng 6, 8, 163 ghi rõ; curl 403 |
| 2 | Bổ sung URL cho 4 dòng "qua tìm kiếm" và TopCV, hoặc rút số khỏi Kết luận | **Đã xử lý** | IBT có Saigon Times (dòng 40); Điều 6 có link (dòng 70, 72); TopCV có link (dòng 110); 78% hạ Thấp và rút khỏi KL1 (dòng 14, 37); Trưởng phòng KD giữ Thấp (dòng 125) |
| 3 | Link toàn văn luật và số điều khoản về quảng cáo | **Xử lý một phần** | Có toàn văn: Luật 71 (TVPL, LuatVietnam), NQ 05 (LuatVietnam, bản EN TVPL), Luật 75 (PDF cổng Hà Nội, có khoản/điều cụ thể), NĐ 125 (PDF Apolat). Còn thiếu: **NĐ 284/2026** thì nhãn "Toàn văn" (dòng 76) trỏ tới bài tin của Tạp chí Toà án, không phải văn bản. **TT 67/2023** ghi "chưa tìm được". Không có link nào trên vbpl.vn hoặc congbao. Với NQ 05 và NĐ 284, số điều về quảng cáo được ghi trung thực là "chưa xác định được" |
| 4 | Thống nhất mốc thời gian; sửa Bộ TT&TT | **Đã xử lý** | Dùng chung "tính đến 28/10/2026" (dòng 15, 75, 151). Dòng 143 đã ghi rõ Bộ TT&TT hợp nhất vào Bộ KH&CN, có link VOV, đánh dấu "Cần xác minh". Còn sót nhỏ: dòng 15 viết "trả lời ngày 28/10 … *sau đó* CAEX công bố ngày 22/10", sai thứ tự thời gian; và chưa chỉ ra nguồn nào cho "Bộ Tài chính trả lời ngày 28/10" |
| 5 | Lương Quản lý vận hành và Coach (mỗi vị trí ≥2 nguồn); giá đối thủ ≥3 đơn vị | **Đã xử lý phần lớn** | Coach có 3 nguồn (dòng 121–123), QL vận hành có 3 nguồn (dòng 126–128), đều ghi rõ là tham chiếu gần. Giá: thêm Inflearn, DSC, Digistore, Plisio (dòng 55–59). Tuy vậy chưa có đơn vị coaching/cộng đồng crypto **nội địa** nào thu phí có giá công khai; Lan ghi "chưa tìm được" đúng cách |
| 6 | Mục Nguồn thiếu 18 link | **Đã xử lý** | Script cho kết quả 127/127 |

## Bảng chấm

| # | Tiêu chí (trọng số, Chặn) | % | Bằng chứng |
|---|---|---|---|
| 1 | Trả lời đủ các câu hỏi nghiên cứu (25, Chặn) | 90 | Đủ 7 câu. Lương Coach và QL vận hành đã có số (dòng 121–128). Mức giá có thêm 4 đơn vị. Bị trừ vì giá đối thủ nội địa có thu phí vẫn chỉ có 1 mức (Unica): Inflearn là nền tảng Hàn Quốc, DSC và Phổ cập Tài sản số đều miễn phí, Digistore và Plisio là giá quốc tế |
| 2 | Số liệu quan trọng có nguồn gốc đã mở (link) (25, Chặn) | 55 | Vẫn **không trang nào được mở** (curl 403). Phần trong tầm của Lan đã cải thiện: gần như mọi dữ kiện đều có link cụ thể, các số không có link đã hạ xuống Thấp và rút khỏi Kết luận, phần lớn luật đã có link toàn văn. Còn thiếu: toàn văn NĐ 284/2026 (nhãn "Toàn văn" trỏ tới bài báo) và TT 67/2023. **Trần do môi trường:** khi chưa mở được trang nào thì tiêu chí này không thể vượt khoảng 55–60%, dù Lan sửa nội dung đến đâu. Khi có mạng và mở, đối chiếu xong các dữ kiện trong Kết luận, tiêu chí có thể lên 85–95% |
| 3 | Không bịa; ghi rõ điều chưa tìm được và cách xác minh (20, Chặn) | 88 | Hai lỗi vòng 1 (mốc thời gian, Bộ TT&TT) đã sửa. Các ô "chưa xác định/chưa tìm được" đều trung thực. Bị trừ vì: (a) dòng 76 gọi bài tin là "Toàn văn", gây hiểu sai loại nguồn; (b) dòng 15 có cụm "sau đó" sai thứ tự, và chưa chỉ rõ nguồn của mốc "BTC trả lời 28/10"; (c) câu mở 6 (dòng 155) vẫn ghi "Lương quản lý vận hành, coach tài chính: chưa có số", mâu thuẫn với bảng 2.6; (d) các dữ kiện sau 6/2026 vẫn chưa kiểm chứng được (giới hạn môi trường) |
| 4 | Ghi thời điểm và độ tin cậy từng dữ kiện (15) | 90 | Mọi dòng đều có cột Thời điểm và cột Độ tin cậy, các dòng mới cũng có nhãn đầy đủ. Vẫn còn "—" hoặc "chưa rõ năm" ở dòng 43, 62, 81, 129, giống vòng 1 |
| 5 | Đúng mẫu: kết luận, bảng dữ kiện, câu hỏi mở, nguồn (15) | 95 | Đủ 4 phần. Mục Nguồn khớp 127/127 và được sinh tự động. Bị trừ vì ô Giá trị ở dòng 76 bị ghép lộn: link nguồn nằm giữa ô, sau đó là một mảnh câu viết thường "phạt tối đa…". Ngoài ra mục 3 chưa cập nhật theo bảng (câu 6) |

**Điểm:** 25×0,90 + 25×0,55 + 20×0,88 + 15×0,90 + 15×0,95 = 22,5 + 13,75 + 17,6 + 13,5 + 14,25 = **81,6 → 82/100**

**Kết luận: CHƯA ĐẠT.** Điểm tổng đã đạt ngưỡng 80, nhưng tiêu chí Chặn số 2 chỉ được 55%, dưới 60%.

Ghi chú cho trưởng nhóm: điều duy nhất còn chặn là **trần do môi trường** ở tiêu chí 2. Các lỗi Lan tự sửa được ở dưới đều nhỏ, có sửa hết cũng không đưa tiêu chí 2 qua 60% nếu vẫn chưa mở được trang. Có hai hướng: (a) chủ dự án mở mạng cho các tên miền nguồn, Lan mở và đối chiếu các dữ kiện trong Kết luận rồi nộp vòng 3; (b) chủ dự án chấp nhận bàn giao ở trạng thái "CHƯA ĐẠT, chặn bởi môi trường", trong đó toàn bộ số liệu ghi mức tin cậy TB, và mọi số pháp lý phải được đối chiếu toàn văn trước khi đưa cho khách.

## Phản hồi (theo mức quan trọng)
1. Tiêu chí 2 (do môi trường): chưa mở được trang gốc nào. → Khi có mạng, mở và đối chiếu các dữ kiện trong 5 Kết luận, ghi "đã mở ngày …", nâng lên Cao những dòng khớp. Ưu tiên toàn văn NQ 05/2025 và NĐ 284/2026 để chốt số điều về quảng cáo.
2. Dòng 76 (NĐ 284/2026): nhãn "Toàn văn" trỏ tới bài tin, và ô Giá trị bị ghép lộn. → Đổi nhãn thành "Bản tin", chuyển các link sang cột Nguồn, viết lại mảnh "phạt tối đa…" thành câu hoàn chỉnh. Tìm link toàn văn trên vbpl.vn, congbao.chinhphu.vn hoặc thuvienphapluat.vn qua công cụ tìm kiếm; nếu không có thì ghi "chưa tìm được link toàn văn" như đã làm với TT 67.
3. Câu mở 6 (dòng 155) mâu thuẫn với bảng 2.6. → Sửa thành "đã có số tham chiếu gần (giảng viên, huấn luyện viên, trưởng phòng vận hành), chưa có số cho đúng chức danh coach tài chính hay QL vận hành ngành giáo dục tài chính", giữ cách xác minh.
4. Dòng 15 và 75: cụm "sau đó CAEX công bố 22/10" sai thứ tự, và mốc "BTC trả lời 28/10" chưa có nguồn cụ thể. → Viết lại theo đúng thứ tự (18/10 số liệu, 22/10 CAEX, 28/10 BTC trả lời) và gắn link của nguồn nêu mốc 28/10 ngay cạnh.
5. Tiêu chí 1 (nếu còn thời gian): giá đối thủ nội địa có thu phí mới có 1 mức. → Tìm thêm landing page có niêm yết học phí của khoá crypto hoặc coaching tài chính tại VN; nếu không có thì giữ "chưa tìm được" (đã làm đúng).
