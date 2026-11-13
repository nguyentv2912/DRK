---
description: Báo cáo hiệu quả tuần hoặc tháng và đề xuất việc cần làm tiếp
argument-hint: [tuan | thang]
---

Giao cho subagent `data-analyst` làm báo cáo kỳ: $ARGUMENTS (mặc định là tuần vừa qua).

Lấy số liệu từ kết nối Metricool/Buffer nếu có, các file chủ cung cấp, `customers/leads.md` và `customers/ho-tro.md`. Không có số liệu thì nói rõ và hướng dẫn chủ cách xuất file từ nền tảng.

Sau khi có báo cáo, tóm tắt cho chủ trong 5 dòng và hỏi có muốn chạy `/solo-agency:giao-viec` với 3 đề xuất trong báo cáo không.
