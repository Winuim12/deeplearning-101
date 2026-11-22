# Deep Learning Exam — Implementation Plan và theo dõi tiến độ

> Khi tiếp tục công việc, đọc file này trước. Thực hiện lần lượt theo `superpowers:executing-plans`; cập nhật trạng thái, bằng chứng kiểm tra và bước tiếp theo sau mỗi phần việc. Không tự đánh dấu hoàn thành khi chưa kiểm chứng kết quả.

**Goal:** Web chạy local để ôn theo từng file slide, vừa làm vừa xem nguồn, và thi tổng hợp ngẫu nhiên 50 câu từ ngân hàng đã kiểm chứng.

**Architecture hiện hành:** Mỗi PDF là một module. Ngân hàng, hình và nguồn tách khỏi giao diện React/Vite. Bản tĩnh dùng IndexedDB cho tiến độ/lượt thi, deadline tuyệt đối và snapshot để chấm điểm. GitHub Actions build/deploy Pages theo yêu cầu mới; Node API là bản cũ giữ tham khảo.

**Tech Stack dự kiến:** React, TypeScript, Vite, Node.js, KaTeX; Vitest và Playwright để kiểm tra logic và hành trình sử dụng. Dùng Python/PyMuPDF sẵn có cho đọc, render và crop PDF. Xác nhận dependency và lệnh thực tế khi triển khai.

**Spec:** Yêu cầu đã thống nhất trong hội thoại, được ghi lại đầy đủ trong phần ràng buộc của file này. Đây là tài liệu theo dõi chính tại `C:\DeepLearning-101`.

## Trạng thái hiện tại

- [x] Khảo sát workspace: chỉ có `slides/`, chưa có ứng dụng và chưa có Git repository.
- [x] Quét tài liệu: 36 PDF, tổng 1.606 trang, không có thư mục con tại thời điểm khảo sát.
- [x] Khảo sát văn bản theo trang và xem trực quan 36 trang trọng điểm ở lượt lập kế hoạch.
- [x] Trình bày kế hoạch và câu mẫu Dice/IoU từ trang PDF 53–54 của `7.1-Segmentation.ENE.pdf`.
- [x] Cập nhật thiết kế: mỗi file PDF là một module ôn; chế độ tổng hợp bốc 50 câu.
- [x] Người dùng cho phép bắt đầu và yêu cầu viết danh sách task trước khi triển khai.
- [x] Tạo tài liệu theo dõi này.
- [ ] Triển khai ứng dụng.

**Việc đang làm:** Đã hoàn thành chuyển sang static GitHub Pages và kiểm thử; chờ người dùng tạo repo, push và bật Pages. T01/T06 rà sâu toàn bộ nguồn còn chưa được chứng nhận.

**Bước tiếp theo:** Deploy theo `docs/deploy-github-pages.md`. Nếu tiếp tục rà học thuật, đọc `reports/reading-status.md`, `content/coverage.json` và `content/pages/`; ưu tiên trang chưa xem trực quan hoặc chưa có câu ở từng module. Sau sửa bank: `npm run prepare:bank`, `python -X utf8 scripts/reconcile_coverage.py`, `npm run validate`, build lại. Không làm lại app từ đầu.

**Lưu ý:** Chưa đọc kỹ và kiểm chứng trực quan toàn bộ 1.606 trang. Không coi kết quả khảo sát ban đầu là ngân hàng câu hỏi đã hoàn thành. Mốc 600–700 câu, phân bổ ban đầu 654 câu, chỉ là ước lượng; số cuối cùng phụ thuộc mật độ kiến thức và loại trùng.

## Ràng buộc áp dụng cho mọi task

1. Giữ nguyên file gốc trong `slides/`; chỉ tạo dữ liệu và hình dẫn xuất ngoài thư mục này.
2. Quét đệ quy; mỗi file bài giảng PDF là một module, câu hỏi sắp theo trang/nhóm trang nguồn. Không ép một câu trên mỗi trang.
3. Nội dung tiếng Việt, giữ thuật ngữ Deep Learning tiếng Anh như bài giảng. Mỗi câu có bốn lựa chọn A/B/C/D, đúng một đáp án.
4. Ưu tiên hiểu khái niệm, áp dụng công thức/thuật toán và phân tích hình/kết quả; phương án nhiễu phải có lý do cụ thể.
5. Một câu có thể dùng nhiều trang và nhiều chủ đề. Câu dùng chung giữa các module giữ cùng ID để không bốc trùng trong đề tổng hợp.
6. Khi ôn module: xem slide cạnh câu hỏi, chuyển đúng trang nguồn, bấm Kiểm tra để nhận lời giải sau khi trả lời; theo dõi tiến độ và làm lại câu sai.
7. Khi thi: chọn đề/chủ đề/module; đề tổng hợp mặc định 50 câu khác nhau. Có timer, bảng số câu, đánh dấu, quay lại và đổi lựa chọn trước khi nộp.
8. Khi nộp: hiển thị số câu chưa trả lời. Hết giờ tự nộp; chỉ hiện đáp án, lời giải và nguồn sau khi nộp trong chế độ thi.
9. Mỗi lời giải có lựa chọn của người học, đáp án đúng, bước suy luận/tính toán và giải thích riêng vì sao từng phương án nhiễu sai.
10. Nguồn theo mẫu `Tên file gốc · trang PDF X · tiêu đề slide nếu có`. PDF đếm từ 1; số slide in trên trang được lưu riêng sau khi kiểm chứng. Nếu có PowerPoint bổ sung, ghi số slide.
11. Nguồn nhiều trang phải liệt kê đủ. Chỉ rõ vùng cần xem lại; mở ảnh trang nguồn/ảnh trích và PDF tại đúng trang.
12. Hình đề nằm cạnh đề và phóng to được. Hình lộ đáp án phải vẽ lại đúng nhãn, trục, số liệu; giữ nguồn gốc và ghi rõ phần đã vẽ lại.
13. Câu chưa kiểm chứng ở trạng thái draft, không được lấy vào đề. Không đoán phần nguồn bị mờ, mất hoặc cắt.
14. Chấm mỗi câu một điểm; sai/bỏ trống bằng 0. Hiển thị số đúng/tổng, phần trăm và thang 10. Có bộ lọc sai/bỏ trống và làm lại câu sai.
15. Khôi phục tiến độ sau tải lại; thời hạn không bị đặt lại. Đề tổng hợp có thể lấy toàn bộ module hoặc chỉ module đã ôn; không bắt buộc ôn xong mới mở thi tổng hợp.
16. Dữ liệu/hình/font/công thức phục vụ local; không phụ thuộc API bên ngoài khi sử dụng. Không triển khai hosting ngoài phạm vi yêu cầu.
17. Mỗi task chỉ được đánh dấu xong khi có kết quả kiểm tra phù hợp. Mỗi module phải báo số câu thực tế và trang chưa xử lý; không bàn giao ngân hàng ít câu như thể đã phủ đủ tài liệu.

## Cấu trúc file dự kiến

| Đường dẫn | Trách nhiệm |
|---|---|
| `TASKS.md` | Yêu cầu, tiến độ, quyết định và điểm tiếp tục |
| `DESIGN.md` | Thiết kế giao diện và hành vi nhất quán giữa các màn hình |
| `content/modules.json` | Module, file gốc, thứ tự và liên kết câu hỏi |
| `content/topics.json` | Chủ đề và quan hệ với module/câu hỏi |
| `content/sources.json` | Trang, tiêu đề, số slide in, vùng ảnh và tình trạng kiểm chứng |
| `content/questions/*.json` | Câu hỏi, lựa chọn, đáp án, lời giải và nguồn |
| `content/coverage.json` | Mức phủ nội dung, trang bỏ qua, phần chưa đọc rõ |
| `public/assets/questions/` | Hình dùng trong đề |
| `public/assets/sources/` | Ảnh trang nguồn và ảnh trích |
| `scripts/` | Công cụ đọc nguồn, chuẩn bị hình và kiểm tra ngân hàng |
| `src/` | Giao diện chọn module, ôn, thi và chữa bài |
| `server/` | API module, luyện tập, lượt thi, deadline và chấm điểm |
| `.local/` | Dữ liệu tiến độ/lượt thi của người dùng, tách khỏi ngân hàng |
| `tests/` | Kiểm thử dữ liệu, logic và trình duyệt |
| `README.md` | Lệnh chạy đã thử, hướng dẫn dùng và giới hạn còn lại |

Các tên file chi tiết trong từng thư mục được chốt khi thực hiện task; nếu thay đổi cấu trúc trên thì cập nhật tài liệu này cùng thay đổi.

## Review Focus

- T03/T11: câu liên kết nhiều module chỉ xuất hiện một lần trong đề 50 câu; đáp án khớp ID lựa chọn khi đổi thứ tự.
- T07/T10: trang PDF, số slide in, crop và tiêu đề không lệch; chế độ thi chưa nộp không hiện nguồn/lời giải.
- T11: tải lại, tab nền, hết hạn khi đóng tab và nộp liên tiếp không làm tăng thời gian hoặc chấm hai lần.
- T08/T12: tiến độ ôn không bị nhầm với điểm thi; làm lại câu sai tạo lượt riêng, giữ lịch sử.
- T03/T11: ngân hàng dưới 50 câu hợp lệ trong bộ lọc phải báo rõ, không nhân bản câu hoặc âm thầm đổi phạm vi.

## Danh sách task triển khai

### T01 — Lập bản đồ tài liệu theo trang
- [x] Tạo manifest 36 file và số trang; lưu hash để đối chiếu nguồn gốc.
- [ ] Đọc kỹ nội dung theo trang; xem hình, công thức, bảng, sơ đồ và đồ thị quan trọng.
- [ ] Ghi chủ đề/concept, trang bìa/mục lục/lặp, nội dung dùng chung và vùng chưa đọc rõ vào `content/coverage.json`.
- [ ] Kiểm chứng số trang và ghi bằng chứng; báo riêng trang chỉ trích được chữ nhưng chưa xem ảnh.

### T02 — Chốt thiết kế giao diện và khởi tạo ứng dụng
- [x] Đọc skill Sites và frontend design phù hợp với triển khai local; ghi quyết định giao diện vào `DESIGN.md`.
- [x] Khởi tạo React/TypeScript/Vite và API Node.js; chỉ cài dependency cần thiết.
- [x] Tạo một lệnh chạy local cho giao diện và API; xác nhận HTTP local trả kết quả (browser QA đang chạy).
- [x] Bố trí ba luồng: thư viện module, ôn cạnh slide, thi/chữa bài; kiểm tra bàn phím và màn hình nhỏ.

### T03 — Định nghĩa dataset và bộ kiểm tra ngân hàng
- [x] Tạo schema module/topic/source/question, ID ổn định và liên kết nhiều module.
- [x] Định nghĩa `validateBank(bank)` trả lỗi/warning; `selectExamQuestions(bank, filters, count, seed)` trả các ID câu khác nhau hoặc lỗi thiếu câu rõ ràng.
- [x] Viết và chạy kiểm tra trước cho bốn lựa chọn, một đáp án, nguồn tồn tại/trang hợp lệ, câu draft, trùng ID, trùng concept và thiếu hình.
- [x] Kiểm tra câu dùng chung không bị nhân bản khi chọn nhiều module; lựa chọn giữ đúng đáp án theo ID.

### T04 — Chuẩn bị ảnh đề và trình xem nguồn
- [x] Tạo công cụ render/crop PDF, lưu crop box và nguồn; 1.606 ảnh toàn trang đã render ngoài `slides/`.
- [x] Vẽ lại hình lộ đáp án bằng SVG, kiểm tra nhãn/trục/số liệu so với nguồn.
- [x] Kiểm tra độ nét, zoom, nhãn thay thế, công thức và xử lý thiếu ảnh.
- [x] Đối chiếu hash để xác nhận các PDF gốc không bị đổi.

### T05 — Hoàn thành một module mẫu xuyên suốt
- [x] Chọn `3.2-Conv2d-Efficient.pdf` làm module đầu tiên; giữ câu Dice/IoU làm mẫu kiểm chứng bổ sung cho hình và phép tính.
- [x] Soạn câu theo toàn bộ kiến thức có giá trị trong module: shape, parameter/bias, receptive field, channel mixing, API/depth multiplier.
- [x] Cung cấp hình phù hợp, lời giải từng lựa chọn, nguồn đúng trang và báo phần bị cắt.
- [x] Chạy được luồng mở module → xem slide → trả lời → kiểm tra → mở nguồn → tiếp tục.
- [x] Kiểm tra kết quả để dùng làm chuẩn cho các module còn lại.

### T06 — Biên soạn và kiểm chứng toàn bộ ngân hàng
- [ ] Hoàn thành lần lượt checklist 36 module bên dưới; không áp chỉ tiêu cứng theo trang.
- [ ] Tính lại phép tính; xác nhận mỗi câu chỉ có một đáp án đúng, đủ giả thiết và bốn lựa chọn phân biệt.
- [ ] Rà câu trùng giữa Transformer/notes, SSL, Generative Text/LLM và các phần metric.
- [ ] Tách nội dung suy ra trong lời giải khỏi nội dung được khẳng định trực tiếp trên slide.
- [ ] Chạy validator; chỉ chuyển câu đã kiểm chứng sang ready. Báo số câu thực tế và độ phủ từng module.

### T07 — Thư viện module và xem slide
- [x] Hiển thị đủ module, số trang, số câu ready và tiến độ.
- [x] Chọn module/chủ đề; điều hướng trang, câu theo trang và câu dùng nhiều trang.
- [x] Xem slide cạnh câu, phóng to hình và mở PDF đúng trang.
- [x] Kiểm tra với trang đầu/cuối, tên file có ký tự đặc biệt và nguồn nhiều trang.

### T08 — Chế độ ôn module và lưu tiến độ
- [x] Lưu câu đã làm, lựa chọn, kết quả, lần ôn và trạng thái hoàn thành theo module.
- [x] Bấm Kiểm tra sau khi trả lời để xem lời giải; trước đó không lộ đáp án.
- [x] Tiếp tục sau tải lại; lọc câu chưa làm/sai và làm lại câu sai.
- [x] Kiểm tra tiến độ của câu dùng chung và migration ID lựa chọn; record lưu cũ được giữ. Form câu ôn cũ chưa tự điền lại lựa chọn (minor deferred).

### T09 — Tạo đề tổng hợp ngẫu nhiên 50 câu
- [x] Chọn toàn ngân hàng/module đã ôn/các module hoặc chủ đề cụ thể, số câu và thời gian.
- [x] Đề tổng hợp mặc định 50 câu ready, không lặp ID; lưu bộ câu đã chọn cho cả lượt.
- [x] Áp trọng số chủ đề hợp lý; tránh nhiều câu gần như cùng một concept.
- [x] Nếu bộ lọc không đủ 50 câu, thông báo số sẵn có và cho sửa cấu hình; không lấy câu draft hoặc lặp.

### T10 — Màn hình thi
- [x] Hiển thị timer, bảng số câu, trạng thái đã trả lời, đánh dấu và điều hướng.
- [x] Cho đổi lựa chọn trước khi nộp; lưu trạng thái khi chuyển câu/tải lại.
- [x] Hiển thị số chưa trả lời khi nộp; giữ đáp án/lời giải/nguồn ở phía server cho đến khi nộp.
- [x] Kiểm tra ảnh, công thức, bàn phím, cuộn và bố cục trên màn hình nhỏ.

### T11 — Deadline, nộp bài và chấm điểm
- [x] Định nghĩa `gradeAttempt(questionIds, answers)` trả số đúng/sai/bỏ trống, phần trăm và thang 10; thử dữ liệu biết trước trước khi triển khai.
- [x] Lưu deadline tuyệt đối ở server; tự nộp khi hết giờ, kể cả sau khi quay lại tab/tải lại.
- [x] Nộp có tính idempotent; sau nộp không thay đổi lựa chọn và không chấm lại thành kết quả khác.
- [x] Kiểm tra đúng toàn bộ, sai toàn bộ, bỏ trống, đáp án thiếu/không hợp lệ, nộp sát deadline và nộp trùng.

### T12 — Chữa bài và làm lại câu sai
- [x] Hiển thị lựa chọn của người học, đáp án, lời giải tính từng bước và lý do phương án đã chọn sai.
- [x] Lọc đúng/sai/bỏ trống/đánh dấu; mở ảnh trích, ảnh toàn trang và PDF đúng nguồn.
- [x] Làm lại câu sai tạo lượt mới; cho chọn gồm cả câu bỏ trống; lưu lịch sử lượt cũ.
- [x] Kiểm tra đề không có câu sai, đề chỉ bỏ trống và câu dựa trên nhiều trang.

### T13 — Kiểm thử toàn hệ thống và rà chất lượng
- [x] Chạy validator toàn ngân hàng, kiểm tra logic và build ứng dụng; sửa lỗi trước khi ghi hoàn thành.
- [x] Chạy trình duyệt ít nhất một lượt từ chọn đề → trả lời/đổi lựa chọn/đánh dấu → nộp → điểm → mở nguồn → làm lại câu sai.
- [x] Chạy riêng luồng ôn module, tải lại, tab nền, tự nộp và phục hồi sau khởi động server.
- [ ] Hoàn tất chứng nhận rà thủ công mọi nguồn/hình của ngân hàng; kiểm tra liên kết và asset tự động đã PASS. Giữ phần rà sâu toàn bộ mở.
- [x] Kiểm tra sử dụng local không cần truy cập mạng ngoài và PDF gốc còn nguyên.
- [x] Ghi lệnh, kết quả và giới hạn thực tế vào nhật ký dưới đây.

### T14 — Hoàn thiện và bàn giao
- [x] Viết `README.md`: cài/chạy, địa chỉ mở web, ôn module, thi 50 câu, thêm module/câu hỏi.
- [x] Liệt kê số câu ready từng module/chủ đề, số hình và các file/trang chưa xử lý.
- [x] Xác nhận lại lệnh local trên bản cuối; chỉ công bố địa chỉ sau khi mở thử thành công.
- [x] Cập nhật checklist và báo trung thực phần hoàn thành/còn thiếu; không coi module trống là hoàn tất.

## Checklist nội dung theo module

`Đọc kỹ` = đã xem đủ nội dung liên quan và kiểm tra hình/công thức; `Câu` = đã soạn và kiểm chứng bộ câu; `Nguồn` = đã đối chiếu trang/crop; `Chạy` = đã thử module trong ứng dụng. Số trang được xác nhận ở lượt khảo sát, cần kiểm tra lại nếu tài liệu thay đổi.

| Module / file gốc | Trang | Đọc kỹ | Câu | Nguồn | Chạy |
|---|---:|:---:|:---:|:---:|:---:|
| 1.1-DLA_intro.pdf | 102 | [ ] | [x] | [ ] | [x] |
| 2.1-ProblemFormulation.pdf | 16 | [ ] | [x] | [ ] | [x] |
| 2.2-Datasets.pdf | 34 | [ ] | [x] | [ ] | [x] |
| 2.3-RegressionSummary.pdf | 22 | [ ] | [x] | [ ] | [x] |
| 2.4-ClassificationSummary.pdf | 29 | [ ] | [x] | [ ] | [x] |
| 2.5-Losses.pdf | 25 | [ ] | [x] | [ ] | [x] |
| 2.6-Metrics.pdf | 22 | [ ] | [x] | [ ] | [x] |
| 2.7-ModelCapacity.pdf | 26 | [ ] | [x] | [ ] | [x] |
| 2.8-MLP.pdf | 31 | [ ] | [x] | [ ] | [x] |
| 2.9-TrainingANN.pdf | 71 | [ ] | [x] | [ ] | [x] |
| 3.1-Conv2d-Overview.pdf | 39 | [ ] | [x] | [ ] | [x] |
| 3.2-Conv2d-Efficient.pdf | 29 | [x] | [x] | [x] | [x] |
| 3.3-Conv2d-Transposed.pdf | 25 | [ ] | [x] | [ ] | [x] |
| 3.4-Conv2d-Dilated.pdf | 26 | [ ] | [x] | [ ] | [x] |
| 3.5-Normalization.pdf | 39 | [ ] | [x] | [ ] | [x] |
| 3.6-Pool-Dropout.pdf | 40 | [ ] | [x] | [ ] | [x] |
| 3.7-CNN-Building-Blocks.pdf | 40 | [ ] | [x] | [ ] | [x] |
| 3.8-CNN-Architectures.pdf | 61 | [ ] | [x] | [ ] | [x] |
| 3.9-Augmentation.pdf | 50 | [ ] | [x] | [ ] | [x] |
| 4.1-RNN-Summary.pdf | 42 | [ ] | [x] | [ ] | [x] |
| 5.1-Positional-Mask-Training-Basics.pdf | 53 | [ ] | [x] | [ ] | [x] |
| 5.2-Attention-Transformer-Core.pdf | 42 | [ ] | [x] | [ ] | [x] |
| 5.3-Model-Families-BERT-GPT-T5-ViT.pdf | 43 | [ ] | [x] | [ ] | [x] |
| 5.4-Practical-Finetuning-and-Efficiency.pdf | 61 | [ ] | [x] | [ ] | [x] |
| 5.5-Lecture1-Transformer-Core-slides.pdf | 57 | [ ] | [x] | [ ] | [x] |
| 5.6-Lecture2-Families-and-Practice-slides.pdf | 55 | [ ] | [x] | [ ] | [x] |
| 5.7-Transformers-notes.pdf | 17 | [ ] | [x] | [ ] | [x] |
| 6.1-Lecture-SelfSupervised-slides.pdf | 72 | [ ] | [x] | [ ] | [x] |
| 6.2-SelfSupervised-notes.pdf | 10 | [ ] | [x] | [ ] | [x] |
| 7.1-Segmentation.ENE.pdf | 92 | [ ] | [x] | [ ] | [x] |
| 8.1-Detection.ENE.pdf | 85 | [ ] | [x] | [ ] | [x] |
| 9.1-Generative4IM.ENE.pdf | 58 | [ ] | [x] | [ ] | [x] |
| 10.1-Gen4TXT.ENE.pdf | 18 | [ ] | [x] | [ ] | [x] |
| 10.2-GPTDecArch.ENE.pdf | 20 | [ ] | [x] | [ ] | [x] |
| 10.3-ModernLLMs.ENE.pdf | 60 | [ ] | [x] | [ ] | [x] |
| 11.1-mm.ENE.pdf | 94 | [ ] | [x] | [ ] | [x] |

## Nguồn cần chú ý đã phát hiện

| File · trang PDF | Quan sát | Hành động khi xử lý |
|---|---|---|
| `2.6-Metrics.pdf` · 20 | Phần diễn giải dưới confusion matrix bị cắt ở mép dưới | Dùng dữ liệu nhìn rõ, đối chiếu trang 21; không đoán chữ mất |
| `3.2-Conv2d-Efficient.pdf` · 25 | Chú thích shape cuối khung code bị cắt | Đối chiếu trang 19 và 24–27, ghi rõ nguồn thay thế |
| `3.3-Conv2d-Transposed.pdf` · 10 | Công thức dài sát sidebar | Đối chiếu ví dụ trang 12 và kiểm chứng trước khi trình bày lại |
| `8.1-Detection.ENE.pdf` · 76 | Tiêu đề lấn sidebar; bảng cost đọc được | Dùng bảng đã xác nhận, tránh lấy nguyên tiêu đề làm hình đề |

## Nhật ký tiến độ và bằng chứng

| Mốc | Kết quả | Kiểm chứng / phần còn lại |
|---|---|---|
| Khảo sát trước triển khai | 36 PDF / 1.606 trang; đã xem trực quan 36 trang trọng điểm | Chưa xác nhận toàn bộ hình và công thức; checklist module chưa hoàn thành |
| Câu mẫu | Dice = 2/3, IoU = 1/2; TP=2, FP=1, FN=1, TN=5 | Nguồn PDF 53–54, số slide in 52–53 của `7.1-Segmentation.ENE.pdf`; đã tính lại |
| Lập task | Tạo `TASKS.md`, T01–T14 và checklist 36 module | Chưa tạo mã ứng dụng, chưa cài thư viện |
| 2026-11-22: T01 | `prepare_slides.py`: 36 PDF/1.606 trang, SHA256, text từng trang; `render_pages.py`: ảnh WebP toàn bộ trang | Không sửa file gốc. Visual review mọi trang chưa hoàn tất. |
| 2026-11-22: T02–T04 | React/TS/Vite, Node API, DESIGN/UX contract, schema/domain, hình SVG/crop | npm install và build thành công; 5 domain tests PASS. Node sandbox chặn child process nên build/dev/Playwright chạy qua quyền thực thi phù hợp. |
| 2026-11-22: T06 | 356 câu unique, 36 module; notes liên kết cùng ID thay vì sao chép câu | Mỗi câu bốn lựa chọn/lời giải riêng và nguồn; cần validator toàn ngân hàng, kiểm tra crop và độ phủ. Ước lượng 654 không là chỉ tiêu cứng. |
| 2026-11-22: browser QA vòng đầu | CUA không có browser/native host; dùng Chrome headless qua Playwright với dữ liệu riêng | Phát hiện production static `/assets/` bị route public chặn bundle. Đã sửa fallback dist; cần chạy lại. |

### Quyết định thực thi
- Ruling: Workspace chưa là Git repository; triển khai trong workspace người dùng chỉ định, không tạo worktree/commit giả. TASKS.md làm ledger bền vững.
- Ruling: Dùng Node test runner sẵn có thay Vitest cho domain, giảm dependency; `--test-isolation=none` tránh sandbox child-process EPERM. Browser QA vẫn dùng Playwright/Chrome riêng, không dùng profile trình duyệt cá nhân.
- Ruling: Thực hiện phần ingest/render toàn bộ nguồn trước, sau đó xây app và ngân hàng song song trong cùng phiên; giữ trạng thái đọc kỹ chưa xong nếu chưa có bằng chứng. Không đánh dấu task chỉ từ số file được tạo.

## Quy tắc cập nhật để tiếp tục sau gián đoạn

- Trước mỗi phiên: đọc trạng thái, bước tiếp theo, ràng buộc và nhật ký; kiểm tra file thực tế trước khi tin một mục đã xong.
- Khi bắt đầu task: ghi `Việc đang làm` và tên task; không chạy lại phần đã có bằng chứng trừ khi có thay đổi.
- Sau mỗi task/module: cập nhật checkbox, file đầu ra, số câu ready, kết quả kiểm tra và nguồn chưa xử lý.
- Khi dừng: ghi chính xác việc đã làm dở, lỗi còn gặp, bước tiếp theo và lệnh cần chạy; không chỉ ghi 'tiếp tục triển khai'.
- Nếu đổi công nghệ, đường dẫn, phạm vi hoặc cách chấm: ghi quyết định và lý do tại đây trước khi tiếp tục công việc phụ thuộc.

## Kết quả bản local 2026-11-22

- 356 câu unique, 382 liên kết cho đủ 36 module; 27 câu có hình, 1.606 ảnh toàn trang và 534 trang làm nguồn trực tiếp.
- `npm test`: 9/9 PASS; Playwright: 7/7 PASS, bao gồm mở đủ 36 module; TypeScript/Vite build PASS. Validator 0 lỗi, mọi hash PDF gốc không đổi.
- Reviewer độc lập phát hiện 4 Important: marker ID đáp án, race đổi câu khi chờ lời giải, hình DINO lộ đáp án, trang notes sai. Đã sửa và thêm hồi quy fail trước/pass sau; migration giữ record cũ. Chi tiết `reports/review.md`.
- Minor deferred: câu ôn đã làm chưa tự điền lựa chọn cũ khi mở lại; record và trạng thái vẫn lưu. Thi vẫn khôi phục lựa chọn đầy đủ.
- UI audit strict 0 findings; DESIGN lint 0 errors, warning token chưa tham chiếu chỉ ở component config.
- App đang phục vụ local ở http://127.0.0.1:5173 (API 4173); không có deploy ngoài máy. README có lệnh chạy và giới hạn.
- T01 đọc sâu/visual toàn bộ và T06 xác nhận phủ toàn bộ từng ý còn để mở: xem `reports/reading-status.md`. Không lấy 356 câu hoặc 1.606 ảnh render làm bằng chứng hoàn thành các bước này.

## Chuyển sang GitHub Pages — 2026-11-22

- [x] G01: xuất dữ liệu tĩnh và bản sao PDF, kiểm tra hash và đủ 1.606 ảnh.
- [x] G02: IndexedDB transaction, snapshot đề, lưu đáp án/đánh dấu, chấm điểm/làm lại và deadline khi mở lại.
- [x] G03: bỏ phụ thuộc API trong app, dùng đường dẫn tương đối cho ảnh/PDF dưới tên repo bất kỳ.
- [x] G04: workflow Pages push `main`, `.gitignore`, preview static và hướng dẫn lệnh ở `docs/deploy-github-pages.md`.
- [x] G05: 18/18 unit, 8/8 browser dưới `/pages-proof/`, validator 0 lỗi, hash gốc giữ nguyên, build PASS, UI audit strict 0 findings.
- Reviewer độc lập phát hiện clock được lấy trước transaction có thể nhận thao tác trễ hạn khi chờ ghi. Đã tái hiện bằng test thất bại rồi sửa lấy giờ bên trong transaction; test PASS.
- Build gồm 1.739 file, 127,41 MiB, file lớn nhất 3,71 MiB; không chứa `.local` hay tiến độ cá nhân. Bản public dùng tiến độ riêng từng browser; chưa import lịch sử Node cũ.
- Chưa có repo/remote được chỉ định, chưa push hoặc xuất bản GitHub. Người dùng chạy lệnh và bật Settings → Pages → GitHub Actions. Các mục rà học thuật T01/T06 vẫn giữ nguyên trạng thái chưa hoàn tất.
- Ghi chú kết quả local/API ở mục trước là lịch sử bản cũ; lệnh chạy hiện hành theo README, dev 5173 và preview 4174, không cần API.
