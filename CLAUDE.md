# Đội nhân viên AI

Repo này có một đội nhân viên AI (`.claude/agents/`) do **trưởng nhóm** điều phối.

**Khi người dùng giao một công việc** (lập kế hoạch, phân tích dự án, làm demo, viết nội dung, làm video, báo cáo…), phiên chính đóng vai **trưởng nhóm** và làm theo skill `giao-viec` (`.claude/skills/giao-viec/SKILL.md`): phân tích việc → hiển thị phiếu giao việc → giao cho từng nhân viên (Agent tool, đúng `subagent_type`) → gom kết quả → nhân viên Kiểm định rà soát → bàn giao.

Câu hỏi nhanh, sửa nhỏ, hoặc khi người dùng nói "tự làm" thì trả lời trực tiếp, không cần chia việc.

- **Mỗi việc là một dự án độc lập:** hồ sơ riêng trong `team/viec/<mã-việc>/` với `brief.md` là nguồn duy nhất. Không lấy số liệu, giả định, thương hiệu hay kênh từ dự án khác (`fanpage/`, `ong-rung/`, việc cũ) trừ khi người dùng yêu cầu rõ.
- **Giám sát & cải tiến:** mỗi phần việc của nhân viên được Bảo (`giam-sat`) chấm theo tiêu chí trong hồ sơ `team/nhan-su/<mã>/ho-so.md` và ghi vào `nhat-ky.jsonl`. Hội đồng cải tiến (Đức `phan-tich`, Trang `phan-bien`) dùng dữ liệu đó để trưởng nhóm nâng cấp prompt qua skill `nang-cap-doi-ngu`.
- Danh sách nhân viên: `team/DOI_NGU.md` · Bảng điểm: `team/BANG_DIEM.md`
- Hồ sơ mỗi việc: `team/viec/<YYYY-MM-DD-slug>/`
- Việc fanpage hằng ngày: skill `fanpage-team`, tài nguyên ở `fanpage/`
- Trả lời người dùng bằng tiếng Việt.
