# Lên lịch tự động 3 bài infographic bằng Publer

File lịch: `REX_Facebook_Publer_Infographics.csv` — 3 bài, mỗi bài 4 ảnh, ảnh đã có
link công khai sẵn (Publer tự tải về khi import).

> Dùng **ảnh vuông 1080×1080** (`infographics/square/`) để lưới 4 ảnh trên Facebook
> KHÔNG bị cắt tiêu đề / logo. (Bản dọc 4:5 vẫn còn trong `infographics/` nếu cần đăng lẻ.)

## Các bước (làm 1 lần)
1. Vào **publer.com** → chọn workspace có kết nối **trang Facebook Rex Trading Signals**.
   (Nếu chưa kết nối: Settings → Social Accounts → Connect → Facebook Page → chọn Rex Trading Signals.)
2. Bấm **Bulk** (hoặc *Create → Import CSV*).
3. Tải lên `REX_Facebook_Publer_Infographics.csv`.
4. Khớp cột: `Date` · `Time` · `Content` · `Media URL` (bỏ trống cột Link).
   - Đặt **timezone** của workspace về giờ Việt Nam để giờ đăng đúng.
5. Xem trước → thấy đủ 4 ảnh mỗi bài + caption → bấm **Schedule All**.
   → Xong. Publer tự đăng đúng lịch.

## Lịch mặc định (sửa cột Date/Time nếu muốn)
| Bài | Ngày | Giờ | Nội dung |
|-----|------|-----|----------|
| 1 | 2026-07-14 | 19:30 | Candlestick Basics |
| 2 | 2026-07-17 | 19:30 | Risk Management |
| 3 | 2026-07-20 | 19:30 | Market Structure |

## Phần bình luận (4 comment mỗi bài)
Publer bản miễn phí chỉ hỗ trợ **1 "first comment"** cho mỗi bài, không tự đăng 4 comment
riêng. Có 2 cách:
- **Cách A (tự động 1 phần):** trong Publer, ở mỗi bài bấm thêm **First Comment** và dán
  gộp 4 đoạn giải thích (lấy trong `infographics/post-batches-en.md`) vào 1 comment.
- **Cách B (thủ công):** để Publer đăng ảnh + caption, sau khi bài lên chị tự dán 4 comment
  riêng vào phần bình luận (như cách đang làm).

## Lưu ý
- Link ảnh trỏ vào branch `claude/facebook-channel-scheduling-29clrd`. Giữ nguyên branch này
  cho tới khi cả 3 bài đã được Publer import xong (Publer tải ảnh về kho của nó lúc import,
  nên sau đó có xoá branch cũng không sao).
- Nếu Publer chỉ nhận 1 ảnh/bài từ CSV, chị import rồi vào từng bài kéo thêm 3 ảnh còn lại
  (link ảnh nằm trong `infographics/`).
