---
version: alpha
colors:
  primary: '#3456c0'
  ink: '#192c4a'
  muted: '#596c84'
  background: '#f2f5fa'
  surface: '#ffffff'
  success: '#17765f'
  danger: '#b33143'
typography:
  display:
    fontFamily: 'Georgia, serif'
  body:
    fontFamily: 'Segoe UI, Arial, sans-serif'
rounded:
  control: '10px'
  panel: '18px'
spacing:
  unit: '6px'
components:
  button:
    height: '44px'
---

## Overview
Phòng tự học Deep Learning cho sinh viên Việt Nam. Product/tool, không phải landing page. Giao diện như bàn học số: một mục lục module bên trái, câu hỏi rõ ràng, slide nguyên bản bên cạnh. Dấu hiệu riêng là đường tiến độ theo trang tài liệu, nối câu hỏi với nơi học lại.

## Colors
Xanh cobalt cho hành động và module đang học; nền xanh giấy nhạt, chữ navy. Success/danger luôn đi với nhãn chữ. Không gradient, không dashboard KPI trang trí, không màu beige hoặc dark neon.

## Typography
Georgia dùng tiết chế cho tên phòng học và tiêu đề chính, Segoe UI cho nội dung tiếng Việt. Body 16px/1.65; metadata ít nhất 13px, điều khiển 14px trở lên. Font hệ thống không tải từ CDN. Số timer dùng tabular numerals.

## Layout
Desktop: sidebar 256px; vùng nội dung tối đa 1440px. Thư viện module là danh sách nhóm có hàng tiến độ. Ôn tập là hai panel 48/52: câu hỏi và slide. Dưới 1000px xếp dọc; dưới 720px sidebar thành thanh điều hướng gọn. Document cuộn tự nhiên; panel slide có vùng cuộn riêng khi cần.

## Elevation & Depth
Mặt phẳng trắng, viền nhạt, shadow chỉ cho modal. Không áp shadow cho mọi hàng/module.

## Shapes
Panel 18px, control 10px; khoảng cách theo nhịp 6px. Các lựa chọn là nút toàn chiều rộng, nhãn A/B/C/D cố định, không nhảy khi hiện lời giải.

## Components
Canonical owners: Button/Modal/Question/SourceViewer trong `src/components.tsx`; thanh trạng thái và lỗi ở App. CSS token runtime ở `src/tokens.css` (import từ style.css) là chủ sở hữu, DESIGN.md phản ánh cùng giá trị (Model B); mọi thành phần dùng biến semantic `--primary`, `--ink`, `--muted`, `--bg`, `--surface`, `--success`, `--danger`. Không sao chép palette vào từng component.

## Do's and Don'ts
Giữ trang nguồn và đề đọc được, có trạng thái loading/error/empty. Tôn trọng reduced motion, focus ring và bàn phím. Không alert/confirm/prompt native; dùng dialog có focus trap. Native select được chấp nhận cho bộ lọc vì menu hệ điều hành phù hợp; nhãn hoàn toàn tiếng Việt.
