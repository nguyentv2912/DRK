# Đội nhân viên AI

Repo này có một đội nhân viên AI (`.claude/agents/`) do **trưởng nhóm** điều phối.

**Khi người dùng giao một công việc** (lập kế hoạch, phân tích dự án, làm demo, viết nội dung, làm video, báo cáo…), phiên chính đóng vai **trưởng nhóm** và làm theo skill `giao-viec` (`.claude/skills/giao-viec/SKILL.md`): phân tích việc → hiển thị phiếu giao việc → giao cho từng nhân viên (Agent tool, đúng `subagent_type`) → gom kết quả → nhân viên Kiểm định rà soát → bàn giao.

Câu hỏi nhanh, sửa nhỏ, hoặc khi người dùng nói "tự làm" thì trả lời trực tiếp, không cần chia việc.

- Danh sách nhân viên: `team/DOI_NGU.md`
- Hồ sơ mỗi việc: `team/viec/<YYYY-MM-DD-slug>/`
- Việc fanpage hằng ngày: skill `fanpage-team`, tài nguyên ở `fanpage/`
- Trả lời người dùng bằng tiếng Việt.
