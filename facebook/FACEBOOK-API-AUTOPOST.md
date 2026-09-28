# Tự động đăng Facebook bằng Developer API (không cần Publer)

Hệ thống này để **GitHub Actions tự đăng bài** lên trang Facebook theo lịch, dùng
Facebook Graph API. Áp dụng cho 2 trang: **Rex Trading Signals** và **harcosfx**.

```
File lịch (CSV)  ──►  scripts/fb_autopost.py  ──►  Facebook Graph API  ──►  Bài lên trang
        ▲                        ▲
  chị sửa nội dung        GitHub Actions chạy mỗi ngày 19:30 (giờ VN)
```

Phần code em đã làm sẵn. Chị chỉ cần làm **PHẦN A** (lấy token) một lần.

---

## PHẦN A — Việc chị làm 1 lần (khoảng 15 phút)

### A1. Tạo App trên Facebook Developers
1. Vào **developers.facebook.com** → góc phải **My Apps** → **Create App**.
2. Chọn loại **Business** → đặt tên (vd: "REX Autopost") → tạo.
3. Vào **App Settings → Basic**, ghi lại **App ID** và **App Secret** (bấm Show).

### A2. Lấy token quyền đăng bài (qua Graph API Explorer)
1. Vào **developers.facebook.com/tools/explorer**.
2. Ô **Meta App**: chọn App vừa tạo.
3. Bấm **Add a Permission** → tick 3 quyền:
   `pages_show_list`, `pages_manage_posts`, `pages_read_engagement`.
4. Bấm **Generate Access Token** → đăng nhập → **chọn trang** Rex Trading Signals
   (và harcosfx) → Cấp quyền (Allow).
5. Copy chuỗi token hiện ra (đây là *User token ngắn hạn*, chỉ sống ~1–2 giờ — dùng ngay ở bước sau).

### A3. Đổi sang Page Token dài hạn
Chạy lệnh này trên máy có Python (hoặc nhờ em chạy giúp nếu chị gửi App ID/Secret — **nhưng tốt nhất chị tự chạy để giữ bí mật**):
```
python scripts/get_page_token.py <APP_ID> <APP_SECRET> <USER_TOKEN_NGẮN_HẠN>
```
Nó in ra cho **từng trang**:
```
• Rex Trading Signals
  PAGE_ID   = 1234567890
  PAGE_TOKEN= EAAG...rất dài...
• harcosfx
  PAGE_ID   = 9876543210
  PAGE_TOKEN= EAAG...rất dài...
```

### A4. Dán vào GitHub Secrets
Repo trên GitHub → **Settings → Secrets and variables → Actions → New repository secret**.
Tạo 4 secret (đúng tên):
| Tên secret | Giá trị |
|------------|---------|
| `REX_PAGE_ID` | PAGE_ID của Rex Trading Signals |
| `REX_PAGE_TOKEN` | PAGE_TOKEN của Rex Trading Signals |
| `HARCOS_PAGE_ID` | PAGE_ID của harcosfx |
| `HARCOS_PAGE_TOKEN` | PAGE_TOKEN của harcosfx |

### A5. Bật Actions + đưa lên nhánh chính
- Repo → tab **Actions** → nếu hỏi thì bấm **Enable**.
- **Merge nhánh `claude/facebook-channel-scheduling-29clrd` vào `main`** (lịch tự động
  chỉ chạy trên nhánh mặc định; ảnh cũng lên `rextradingsignal.com` sau khi merge).
  → Nhắn em, em mở Pull Request giúp chị.

### A6. Chạy thử
- Repo → **Actions → "Facebook auto-post" → Run workflow** (chạy tay).
- Xem log: nếu thấy `-> {'id': ...}` là đăng thành công. Vào trang Facebook kiểm tra.

---

## PHẦN B — Dùng hằng ngày (chỉ sửa nội dung)

- **Sửa lịch REX:** mở `facebook/schedule/rex_schedule.csv`
  - Cột `Date` (YYYY-MM-DD), `Time`, `Content` (caption), `Media URL` (link ảnh công khai,
    nhiều ảnh ngăn nhau bằng dấu phẩy — để trống nếu chỉ đăng chữ).
- **Sửa lịch HARCOS:** mở `facebook/schedule/harcos_schedule.csv` (đang là dòng mẫu, thay bằng nội dung thật).
- Mỗi ngày 19:30 (giờ VN) Actions tự chạy, đăng những dòng **tới hạn** (Date ≤ hôm nay)
  mà **chưa đăng**. Đã đăng rồi thì bỏ qua (ghi nhớ trong `.posted_*.json`).
- Đổi giờ chạy: sửa dòng `cron` trong `.github/workflows/fb-autopost.yml`
  (định dạng UTC; `30 12 * * *` = 19:30 VN).

---

## Lưu ý quan trọng
- **App để chế độ Development là đủ** để đăng lên trang **chính chị làm admin** — không cần
  Facebook duyệt (App Review) rườm rà.
- **Token dài hạn** thường không hết hạn khi chị còn là admin trang. Nếu một ngày log báo
  lỗi `190`/`401` (token hết hạn) → chạy lại `scripts/get_page_token.py` lấy token mới,
  cập nhật lại secret.
- **Bí mật:** không bao giờ dán token vào file trong repo — chỉ để trong **GitHub Secrets**.
- Ảnh trong `Media URL` phải là **link công khai**. Bản `rextradingsignal.com/...` chỉ hoạt
  động **sau khi merge vào main** (site tự cập nhật). Nếu muốn chạy trước khi merge, đổi link
  sang dạng `raw.githubusercontent.com/.../<branch>/...`.
