# REX Trading Signal — Bộ tài liệu Facebook

Thư mục này chứa mọi thứ để dựng và chạy trang Facebook cho kênh REX Trading Signal.

## Các file

| File | Dùng để làm gì |
|------|----------------|
| `REX_Facebook_Page_Description.md` | Mô tả trang: tên, bio, About, câu chuyện thương hiệu, nút CTA, thông tin liên hệ. Copy dán trực tiếp khi tạo/chỉnh trang. |
| `REX_Facebook_Publer_Bulk.csv` | Lịch 14 bài đăng (2 tuần, 1 bài/ngày lúc 19:30), nội dung rút từ các bài blog + dẫn về Telegram. Import thẳng vào **Publer**. |

## Cách lên lịch bằng Publer (giống quy trình HARCOS)

1. Vào Publer → chọn workspace/kênh **REX Trading Signal** (kết nối trang Facebook trước).
2. Bấm **Bulk** (hoặc *Import → CSV*).
3. Tải lên `REX_Facebook_Publer_Bulk.csv`.
4. Khớp cột: `Date`, `Time`, `Content`, `Link`, `Media URL` (múi giờ đặt theo giờ Việt Nam / giờ khán giả mục tiêu).
5. Xem trước → **Schedule All**.

> File dùng đúng định dạng như `HARCOS_Publer_Bulk.csv` (có BOM UTF-8, 5 cột), nên
> import y hệt cách chị đã làm cho HARCOS.

## Nội dung được lấy từ đâu

Mỗi bài bám sát một bài blog trên [rextradingsignal.com](https://rextradingsignal.com)
và cột `Link` trỏ về đúng bài đó để kéo traffic:

- Manifesto "run your account like a business" → trang chủ
- Câu chuyện "Fixed returns. Zero risk." → `/about.html`
- Rule 01 stop loss + Risk Ceiling → `/how-to-manage-risk-in-gold-trading.html`
- Position sizing → `/position-sizing-for-gold-trading.html`
- Vì sao trader cháy tài khoản → `/why-do-most-traders-blow-their-accounts.html`
- Treat trading like a business → `/treat-trading-like-a-business.html`
- Trade journal → `/trading-journal-template.html`
- One-page business plan (miễn phí) → `/business-plan/`
- Rule 02 (post losses) & Rule 03 (join Telegram) → CTA về Telegram `t.me/+CR21qcOU0QI4ZDg9`

## Điều chỉnh nhanh

- **Đổi ngày bắt đầu:** sửa cột `Date` (đang bắt đầu 2026-07-14).
- **Đổi giờ đăng:** sửa cột `Time` (đang để 19:30).
- **Thêm ảnh:** điền URL ảnh công khai vào cột `Media URL` cho từng bài (Publer sẽ đính kèm).
- **Đăng nhiều lần/ngày:** thêm dòng cùng ngày với giờ khác (HARCOS đăng 5 khung/ngày — tham khảo `HARCOS_Publer_Bulk.csv` bên repo brian-2-trinh).
