# Review và kiểm chứng bản local

Ngày thực hiện: 2026-11-22 (Asia/Saigon).

## Phát hiện từ reviewer độc lập

Reviewer `/root/final_review` đọc riêng yêu cầu và mã, không sửa file. Bốn phát hiện Important đã xử lý:

1. **ID o0 luôn là đáp án:** chuyển sang a/b/c/d theo vị trí sau shuffle; correct phân bố theo vị trí, không có marker công khai chung. Thêm migration cho progress/lượt thi cũ; migration idempotent. Kiểm tra bank đã fail trước sửa, sau sửa pass.
2. **Race khi kiểm tra câu:** khóa bảng chọn câu và bộ lọc Chỉ câu sai trong lúc POST /practice đang chờ. Browser test có response trễ đã fail trước sửa, sau sửa pass.
3. **Hình DINO lộ đáp án:** bỏ crop ghi thẳng tên family khỏi câu hỏi family; vẫn mở nguyên trang sau khi nộp ở phần nguồn. Regression bank test fail trước, pass sau.
4. **Notes trích sai trang:** self/cross chuyển notes Transformer PDF11→9; EMA chuyển SSL notes PDF8→7. Đồng thời đối chiếu lại links cosine/NT-Xent/FFN với phần công thức thực, chuyển về trang có nội dung. Regression test fail trước, pass sau.

Minor deferred: khi mở lại một câu đã ôn, form chưa tự điền đáp án cũ. Tiến độ và record vẫn lưu. Người học chọn lại để ôn; đã ghi trong README. Không ảnh hưởng phục hồi lựa chọn của đề thi.

## Kiểm tra đã chạy

- `npm test`: 9/9 pass (domain, sources, answer marker, migration).
- `npm run test:e2e`: 7/7 pass bằng Chrome headless, dữ liệu riêng `.local/e2e`, port 4187. Bao gồm ôn module, lưu/khôi phục tiến độ, đề 50 câu, đáp án ẩn trước nộp, đổi lựa chọn, đánh dấu, reload giữ deadline, điểm/bỏ trống, mở nguồn, retry, pool thiếu câu, mobile, source nhiều module, tự nộp bằng đồng hồ mô phỏng, race response chậm và mở đủ 36 module.
- `npm run validate`: 356 câu unique, 382 module links, 1.606 ảnh nguồn, 27 câu có hình, 534 trang nguồn trực tiếp, 0 lỗi; SHA256 toàn bộ PDF gốc không đổi.
- `npm run build`: TypeScript và Vite production build pass. KaTeX tách chunk riêng; font đóng gói local.
- Premium static audit strict: 0 findings. DESIGN lint: không có errors, còn warning tokens chưa tham chiếu từ component config.
- Ảnh desktop/mobile và module: `reports/screenshots/`; browser không ghi nhận page errors trong lượt capture.
- Crop được xem trực quan ở `reports/figures/`; LSTM/GRU chuyển sang bounding box ảnh gốc để giữ đủ nhãn, các sơ đồ khác bỏ phần lời giải làm lộ đáp án khi phù hợp.

## Phạm vi chưa được chứng nhận

Đã ingest và render toàn bộ tài liệu, không đồng nghĩa đã hoàn tất kiểm chứng trực quan mọi trang hoặc đã ra câu cho từng ý trong 1.606 trang. Số câu 654 ban đầu là dự kiến, ngân hàng hiện có 356 câu. Giữ T01/T06 phần rà sâu chưa xong trong TASKS.md; xem coverage.json theo trang. Không xem validator hay test API như bằng chứng học thuật tự động cho mọi lời giải.

## Quyết định thực thi

- Workspace không phải Git repository: làm tại thư mục được giao, không tạo worktree/commit giả; tiến độ lưu trong TASKS.md. Không có merge/push/deploy bên ngoài.
- Node test runner thay Vitest cho domain, `--test-isolation=none` để không spawn worker trong sandbox. Browser dùng Playwright/Chrome riêng, không truy cập profile cá nhân; CUA/native host của phiên không khả dụng.
- Hạ tầng ingest/render được làm toàn bộ trước, sau đó app và ngân hàng phát triển trong cùng phiên. 356 câu là số thực, không nhân bản câu để đạt 654.
