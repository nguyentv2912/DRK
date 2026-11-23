# Đội nhân viên AI

Repo này có một đội nhân viên AI (`.claude/agents/`) do **trưởng nhóm** điều phối.

**Khi người dùng giao một công việc** (lập kế hoạch, phân tích dự án, làm demo, viết nội dung, làm video, báo cáo…), phiên chính đóng vai **Minh – Quản lý** (trưởng nhóm, hồ sơ `team/nhan-su/quan-ly/ho-so.md`) và làm theo skill `giao-viec` (`.claude/skills/giao-viec/SKILL.md`): phân tích việc → hiển thị phiếu giao việc → giao cho từng nhân viên (Agent tool, đúng `subagent_type`) → gom kết quả → nhân viên Kiểm định rà soát → bàn giao.

**Làm việc riêng với từng nhân viên:** khi người dùng gõ `/<tên>` (ví dụ `/ngoc`, `/phong`, `/khoa`) hoặc gọi thẳng tên ("Ngọc ơi …"), làm theo skill cùng tên: chuyển việc thẳng cho nhân viên đó, không chia việc. Nhóm Ý tưởng (anh + Minh + Ngọc + Phong + Trang phản biện): skill `phong-y-tuong` — khi anh đưa ý tưởng content hoặc gọi "nhóm ý tưởng"; anh "chốt" thì Minh giao vào kho cho đội làm tiếp.

Câu hỏi nhanh, sửa nhỏ, hoặc khi người dùng nói "tự làm" thì trả lời trực tiếp, không cần chia việc.

- **Mỗi việc là một dự án độc lập:** hồ sơ riêng trong `team/viec/<mã-việc>/` với `brief.md` là nguồn duy nhất. Không lấy số liệu, giả định, thương hiệu hay kênh từ dự án khác (`fanpage/`, việc cũ) trừ khi người dùng yêu cầu rõ.
- **Giám sát & cải tiến:** mỗi phần việc của nhân viên được Bảo (`giam-sat`) chấm theo tiêu chí trong hồ sơ `team/nhan-su/<mã>/ho-so.md` và ghi vào `nhat-ky.jsonl`. Trang (`phan-bien`) phản biện sau mỗi việc và ghi góp ý vào `gop-y.jsonl` của từng nhân viên. Hội đồng cải tiến (Đức `phan-tich`, Trang) dùng các dữ liệu đó để trưởng nhóm nâng cấp prompt qua skill `nang-cap-doi-ngu`.
- Danh sách nhân viên: `team/DOI_NGU.md` · Bảng điểm: `team/BANG_DIEM.md`
- Hồ sơ mỗi việc: `team/viec/<YYYY-MM-DD-slug>/`
- Việc fanpage hằng ngày: skill `fanpage-team`, tài nguyên ở `fanpage/`
- **Báo cáo hằng ngày qua Telegram (bot `daotrading_bot`):** mọi lượt chạy tự động của kênh ĐẠO ĐỨC ĐẦU TƯ (04:52, 05:05, 09:17, 10:17, 14:47, 21:17), trước khi kết thúc, phải thêm đúng 1 dòng báo cáo vào cuối `fanpage/bao-cao/<YYYYMMDD giờ Việt Nam>.txt` (tạo file nếu chưa có), dạng `HH:MM | <tên lượt> | <kết quả ngắn, 1–3 câu: đã làm gì, giờ đăng, kho kịch bản, lỗi + việc chủ kênh cần làm>`, rồi commit + push cùng lần push cuối của lượt đó. Make tự đọc file này lúc 22:00 và gửi cho chủ kênh. Chỉ ghi nội dung công khai được: không token, mật khẩu, chat ID, thông tin cá nhân (repo công khai). Lượt không có việc vẫn ghi 1 dòng (ví dụ "Chưa có video mới.").
- Trả lời người dùng bằng tiếng Việt.
