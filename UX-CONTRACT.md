# Hành vi phòng học

Nguồn yêu cầu: TASKS.md. Visual: DESIGN.md. Locale vi-VN, múi giờ Asia/Saigon; không có tài khoản, thanh toán hoặc dữ liệu ngoài máy.

| Capability | Canonical owner | Source of truth | Allowed variants | Verification |
|---|---|---|---|---|
| Select/Listbox | Native select có label | App.tsx | module/group | Browser keyboard + popup |
| Form | Cấu hình đề | TASKS.md | đề mới/làm lại | API validation + browser |
| Scrollbar | src/style.css | DESIGN.md | document/panel | responsive check |
| Toast | inline live status App | App.tsx | error/success | browser |
| Dialog | Modal | components.tsx | nộp bài/phóng to | Escape, trap, restore |

Ôn module cho kiểm tra từng câu sau lựa chọn và xem nguồn song song. Browser service không trả khóa đáp án/nguồn/lý do trong view thi trước nộp; dữ liệu tĩnh vẫn chứa đáp án cho mục đích tự ôn. Nộp bài là chuyển trạng thái bền vững, idempotent, deadline tuyệt đối theo đồng hồ máy. IndexedDB lưu atomically theo trình duyệt/đường dẫn; snapshot câu hỏi giữ điểm cũ khi bank cập nhật. Lượt ôn và lịch sử thi riêng. Đề dưới số câu yêu cầu báo thiếu rõ ràng; không mở rộng phạm vi tự động.

Search/filter library lưu query/group trên URL; clear query bằng nút có label. Không remote search, không debounce. Error giữ lựa chọn và có thử lại; lưu lỗi phải báo chưa lưu. Ảnh nguồn giữ tỉ lệ trang, có loading và lỗi inline, không đổi trang khi response cũ về muộn. Điều hướng câu hỏi giữ context và đưa focus về tiêu đề câu.
