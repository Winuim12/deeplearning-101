# Deep Learning · Phòng tự học

Web ôn Deep Learning chạy local hoặc GitHub Pages, tổ chức theo **36 file PDF = 36 module**. Hiện có **356 câu khác nhau**, 382 liên kết module–câu hỏi (notes dùng chung câu), 27 câu có hình và 1.606 ảnh trang nguồn.

## Đưa lên GitHub Pages

Xem [hướng dẫn push và deploy](docs/deploy-github-pages.md). Workflow đã có trong `.github/workflows/deploy-pages.yml`: push vào `main` sẽ kiểm tra, build và deploy sau khi bật GitHub Pages. Không cần chạy API hay thuê server.

Git bỏ qua dữ liệu cá nhân/cache/build, ảnh chụp kiểm tra trong `reports/screenshots/`, hình rà soát trong `reports/figures/`, báo cáo JSON tự sinh và bản chia module `content/questions/` (tạo lại bằng `npm run prepare:bank`). Giữ `tests/` vì workflow chạy kiểm thử trước deploy; giữ PDF và `public/assets/` vì website cần để xem nguồn. Git chỉ gửi thay đổi ở những lần push tiếp theo.

Tiến độ và lịch sử lưu bằng IndexedDB trên từng trình duyệt, không tự đồng bộ giữa máy hoặc giữa bản local và website. Xóa dữ liệu website sẽ mất tiến độ. Dữ liệu cũ trong `.local/state.json` của bản Node được giữ nguyên nhưng chưa tự chuyển vào trình duyệt. Ngân hàng có đáp án trong dữ liệu tĩnh; giao diện thi chỉ hiện lời giải sau nộp. Đây là công cụ tự ôn.

## Chạy trên máy này

Dependency đã được cài trong workspace. Mở PowerShell tại `C:\DeepLearning-101`:

```powershell
npm run dev
```

Mở **http://127.0.0.1:5173/**. Giữ cửa sổ lệnh mở; Ctrl+C để dừng. Nếu port đã được sử dụng, kiểm tra bản đang chạy trước khi khởi động thêm.

Bản production để xem trước:

```powershell
npm run build
npm start
```

Mở **http://127.0.0.1:4174/**. Build tạo thư mục `dist/` để xuất bản; `npm start` chỉ phục vụ bản xem trước này.

Trên máy mới cần Node.js 24 (đã kiểm tra bằng Node 24.14.0), rồi `npm ci`. Chỉ bước cài dependency cần mạng; sử dụng app, font, công thức, hình và PDF không cần dịch vụ ngoài. Python 3/PyMuPDF/Pillow chỉ cần khi xây lại dữ liệu/hình, không cần khi chạy bản đã chuẩn bị.

## Sử dụng

1. **Thư viện slide:** tìm tên file/chủ đề, chọn module. Nút đầu trang mở module Efficient Convolutions hoặc tiếp tục module đang học.
2. **Ôn module:** câu hỏi bên trái, trang nguồn bên phải. Chọn một trong bốn đáp án rồi bấm **Kiểm tra đáp án**. Lời giải có cách suy luận, lý do từng phương án và nguồn. Dùng bảng câu để chuyển, ô số trang để xem tiếp slide, nút phóng to để đọc hình. Có bộ lọc **Chỉ câu sai**.
3. **Ôn tập tổng hợp:** mặc định 50 câu/60 phút, có thể chỉnh số câu/thời gian. Chọn toàn bộ ngân hàng, module đã ôn xong hoặc module tự chọn. Nếu bộ lọc không đủ câu, app báo rõ để bạn sửa; không lặp câu để lấp đầy.
4. **Trong đề thi:** có timer, đánh dấu, đổi lựa chọn, quay lại. Lựa chọn lưu sau từng thao tác thành công. Nộp bài báo số câu bỏ trống; hết giờ tự nộp. Chỉ sau nộp mới hiện đáp án/lời giải/nguồn.
5. **Kết quả:** điểm thang 10, số đúng/sai/bỏ trống, bộ lọc và làm lại câu sai (tùy chọn gồm câu bỏ trống). Mở lại bài ở **Lịch sử làm bài**.

Mỗi câu đúng 1 điểm, sai/bỏ trống 0. Điểm thang 10 được làm tròn hai chữ số thập phân. Deadline tuyệt đối lưu trong trình duyệt nên tải lại không cộng thêm thời gian. Nếu đóng tab khi làm bài, mở lịch sử để tiếp tục hoặc nhận kết quả đã hết giờ. Lượt thi giữ bản chụp câu hỏi để lần cập nhật ngân hàng sau không thay đổi điểm cũ.

## Dữ liệu và nguồn

- File gốc `slides/` được giữ nguyên, có SHA256 đối chiếu trong `content/modules.json`.
- `content/authoring/*.txt`: các câu biên soạn, đáp án và lý do phương án nhiễu. Format được mô tả ở đầu file; dùng dấu `|` phân trường và `~` tách phương án sai/lý do.
- `scripts/build_bank.py`: biên dịch nguồn biên soạn, các bài tính/đọc hình, phân bố vị trí đáp án và liên kết notes.
- `content/bank.json`: ngân hàng tổng; `content/questions/*.json` là bản chia module sinh tự động. Không sửa các bản generated riêng lẻ; sửa authoring hoặc builder rồi biên dịch lại.
- `content/sources.json`: số trang PDF (từ 1), tiêu đề và số slide in được trích trực tiếp nếu xác nhận được. Không lấy số trang PDF trừ 1 để đoán.
- `content/pages/*.json`: văn bản trích xuất từng trang để rà nguồn.
- `public/assets/questions/`: SVG bài áp dụng và crop từ slide; crop lưu thêm `imageSource` trong câu hỏi. `public/assets/sources/` là ảnh đầy đủ của mọi trang.
- `scripts/export-static.mjs`: xuất `public/data/study.json` và sao chép PDF vào `public/slides/` khi dev/build; kiểm tra hash gốc. Các bản xuất này không cần commit.
- IndexedDB: tiến độ cá nhân theo origin và đường dẫn website, không nằm trong repository hay `dist/`. `.local/` của bản Node cũ được Git bỏ qua. `server/index.mjs` và `scripts/dev.mjs` giữ lại để tham khảo bản cũ; không dùng để chạy/deploy bản tĩnh.

Lời giải liệt kê đủ các trang được sử dụng, có vị trí cần xem lại, ảnh nguồn và liên kết PDF `#page=X`. Link PDF mở tại trang còn tùy trình đọc của browser; trình xem ảnh trong app luôn chỉ đúng trang đã chọn. Câu có nhiều module vẫn giữ cùng một ID và không xuất hiện lặp trong một đề.

## Thêm hoặc chỉnh ngân hàng

Sau khi bổ sung slide/câu hỏi, đối chiếu tài liệu thật và kiểm chứng đáp án trước khi đưa vào đề. Không ghi đè hoặc đổi file slide gốc âm thầm. Các lệnh tái tạo:

```powershell
npm run prepare:slides
npm run prepare:bank
npm run validate
```

Sau đó chạy lại `npm run dev` hoặc `npm run build` để xuất ngân hàng mới. `prepare:slides` tái tạo manifest/text; ảnh đã render được giữ nếu tồn tại. Nếu cố ý thay nội dung PDF, cần tái render đúng các ảnh bị ảnh hưởng và rà lại câu liên quan, không chỉ tin cache ảnh cũ. Giữ ID câu/lựa chọn ổn định để liên kết tiến độ ôn; lịch sử thi đã có snapshot riêng.

Số câu từng module: [reports/module-counts.md](reports/module-counts.md). Bản đồ độ phủ: `content/coverage.json`. **534 trang hiện là nguồn trực tiếp của câu hỏi; không đồng nghĩa mọi chi tiết trên 1.606 trang đã có câu kiểm tra.** Mốc 654 câu trong kế hoạch là ước lượng ban đầu, không phải số câu đã hoàn thành.

## Nguồn còn cần chú ý

Không có file không mở được. Các phần cắt/sát sidebar đã phát hiện:

| File | Trang PDF | Vấn đề |
|---|---:|---|
| 2.6-Metrics.pdf | 20 | Diễn giải cuối trang bị cắt; bảng đầu vào đọc được |
| 3.2-Conv2d-Efficient.pdf | 25 | Chú thích shape cuối khung code bị cắt |
| 3.3-Conv2d-Transposed.pdf | 10 | Công thức dài sát sidebar; đối chiếu ví dụ trang 12 |
| 8.1-Detection.ENE.pdf | 76 | Tiêu đề lấn sidebar; bảng cost đọc được |

Câu hỏi không dựa vào phần chữ bị mất. Chưa tuyên bố hoàn tất rà trực quan toàn bộ mọi hình/công thức của tài liệu. Trạng thái và phần còn lại được giữ trong `TASKS.md` và `content/coverage.json` để tiếp tục đúng chỗ. Ngân hàng hiện tại bao phủ các trọng tâm đã biên soạn, chưa phải cam kết bao phủ từng ý có thể ra thi.

## Kiểm tra

```powershell
npm test
npm run validate
npm run build
npm run test:e2e
```

Playwright dùng Chrome cài sẵn trên Windows ở đường dẫn cấu hình `playwright.config.ts`. Trên máy khác sửa `executablePath` hoặc cài browser bằng `npx playwright install chromium`. E2E chạy `dist/` trên **http://127.0.0.1:4188/pages-proof/** với browser context riêng, xác nhận mọi luồng không gọi `/api/` và hoạt động dưới đường dẫn repository.

Đã kiểm tra domain/nguồn/ID lựa chọn, giữ deadline, nộp idempotent, chuyển định dạng lựa chọn cũ; browser kiểm tra ôn module, lưu tiến độ, đề 50 câu, đổi lựa chọn/đánh dấu/tải lại, điểm/nộp/mở nguồn/làm lại, thiếu câu, mobile, tự nộp bằng đồng hồ mô phỏng và request trả chậm. Hash toàn bộ file PDF gốc được xác nhận không đổi. Kết quả hiện hành ở `reports/validation.json`, `test-results/e2e-results.json` và `premium-audit.json`.

Kết quả bản tĩnh: 18 unit tests, 8 browser tests, validator và TypeScript/Vite build đều PASS. Browser tests gồm hai tab ghi đồng thời, browser riêng, lỗi tải dữ liệu và lỗi quyền lưu trữ. Một chi tiết giao diện còn lại: mở lại câu đã ôn vẫn giữ trạng thái đúng/sai trong tiến độ, nhưng chưa tự điền lại lựa chọn cũ trên form; có thể chọn lại để ôn. Record câu trả lời cũ vẫn lưu trong IndexedDB.
