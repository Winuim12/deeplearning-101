# Push và deploy bằng GitHub Pages

Ứng dụng đã chạy hoàn toàn bằng file tĩnh. GitHub Actions cài dependency, kiểm tra dữ liệu và build `dist/`, rồi đưa artifact lên Pages. Không cần deploy Node API. Hướng dẫn chính thức: [Vite](https://vite.dev/guide/static-deploy.html#github-pages), [GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## 1. Tạo repository

Trên GitHub, tạo repository **Public** tên `DeepLearning-101`, để trống (không thêm README, license hay .gitignore). Nếu dùng tên khác, thay tên tương ứng trong các lệnh và URL. Bản build dùng đường dẫn tương đối nên không cần sửa Vite config.

## 2. Push từ PowerShell

Thay `TEN_GITHUB_CUA_BAN` bằng username hoặc organization sở hữu repo:

```powershell
cd C:\DeepLearning-101
git init -b main
git add .
git commit -m "Add Deep Learning study website"
git remote add origin https://github.com/TEN_GITHUB_CUA_BAN/DeepLearning-101.git
git push -u origin main
```

Nếu Git yêu cầu danh tính, cấu hình tên/email của bạn trong repo rồi chạy lại commit/push:

```powershell
git config user.name "Ten cua ban"
git config user.email "Email GitHub cua ban"
```

Git có thể mở trình duyệt để đăng nhập. Giữ nguyên `slides/`, `content/`, `public/assets/`, source, lockfile và `.github/` trong commit. `.gitignore` loại `node_modules/`, `dist/`, `.local/`, kết quả kiểm thử, `.env` và dữ liệu xuất tự động. Không cần upload thủ công thư mục build.

## 3. Bật Pages một lần

Trong repository: **Settings → Pages → Build and deployment → Source → GitHub Actions**.

Mở **Actions → Deploy study room to GitHub Pages**. Nếu lần chạy đầu đã thất bại vì chưa bật Pages, bấm **Run workflow**, chọn `main` rồi chạy lại. Khi job `deploy` thành công, URL hiển thị ở phần deployment/environment:

```text
https://TEN_GITHUB_CUA_BAN.github.io/DeepLearning-101/
```

Không chọn nhánh `gh-pages`: workflow xuất bản artifact từ `dist/`. Nếu Actions bị tắt, bật Actions cho repository trước.

## 4. Cập nhật website sau này

```powershell
cd C:\DeepLearning-101
git add .
git commit -m "Update study content"
git push
```

Mỗi push vào `main` tự chạy lại kiểm tra/build/deploy. Xem log ở Actions nếu thất bại; sửa lỗi rồi push tiếp. Không commit nếu Git báo không có thay đổi.

## Kiểm tra trước khi push

Máy mới cần Node.js 24, sau đó:

```powershell
npm ci
npm test
npm run validate
npm run build
npm start
```

Mở **http://127.0.0.1:4174/**. Để kiểm thử tự động đường dẫn dạng repo bằng Chrome, chạy `npm run test:e2e` sau build (xem cấu hình browser trong README).

## Lưu ý sử dụng

- Tiến độ lưu riêng trong trình duyệt, không đồng bộ giữa thiết bị, local và website public. Xóa dữ liệu website sẽ mất lịch sử; giữ URL ổn định để tiếp tục dùng cùng kho tiến độ.
- Dữ liệu `.local/state.json` của bản Node cũ không được xuất bản và chưa có chức năng import vào trình duyệt.
- PDF bài giảng, hình và ngân hàng sẽ được phục vụ công khai cùng website. Đáp án chỉ ẩn ở giao diện trước khi nộp, vẫn có trong dữ liệu tĩnh phục vụ tự học.
- Chưa push hoặc deploy vào tài khoản GitHub nào từ workspace này; các lệnh trên do bạn chạy sau khi tạo repo.
