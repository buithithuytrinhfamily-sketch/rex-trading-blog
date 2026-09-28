# REX Trading Signal — Infographics (12 ảnh)

Bộ 12 infographic giáo dục, cùng một phong cách thương hiệu (nền giấy sáng, đỏ tín hiệu +
vàng hoàng hôn, logo REX + "Every signal has a stop loss"). Mỗi ảnh là **PNG 1080×1350 (4:5)**,
đăng thẳng lên Facebook/Instagram.

## Danh sách + caption sẵn (copy khi đăng)

Mỗi caption đã kèm hashtag. Ảnh trong file cùng tên `.png`.

---
**1. `rex_01_anatomy.png` — Anatomy of a Candlestick**
```
Before any pattern, read the candle itself. Body = open to close. Wick = the extreme the price reached and got rejected from. Green closes above it opened; red closes below. Master this and every chart starts to speak.

Every signal we post comes with a stop loss. Join us 👉 https://t.me/+CR21qcOU0QI4ZDg9

#XAUUSD #goldtrading #forex #candlestick #pricetaction
```

**2. `rex_02_engulfing.png` — Engulfing Pattern**
```
The engulfing candle is one of the cleanest reversal signals on the chart. A big body that completely swallows the one before it means control just changed hands — buyers took over (bullish) or sellers did (bearish). Context matters: it's strongest at support or resistance.

#XAUUSD #goldtrading #forex #engulfing #candlestickpatterns
```

**3. `rex_03_pinbar.png` — The Pin Bar**
```
A long wick is a story of rejection. Bullish pin: price dropped, buyers slammed it back up — they rejected lower prices. Bearish pin: the opposite. The longer the wick, the louder the rejection. We wait for these at key levels.

#XAUUSD #goldtrading #pinbar #priceaction #forex
```

**4. `rex_04_doji.png` — The Doji**
```
Open ≈ close = the market can't decide. A doji isn't a buy or a sell signal on its own — it's a pause. The move comes from the candle AFTER it. Patience beats guessing.

#XAUUSD #goldtrading #doji #candlestick #forex
```

**5. `rex_05_trade.png` — Anatomy of a Trade**
```
Every trade we take has three lines drawn before we click: entry, stop loss (what we're willing to lose), take profit (the target). No stop = no trade. Capital is oxygen — protect it first.

This is Rule 01. Join the channel 👉 https://t.me/+CR21qcOU0QI4ZDg9

#XAUUSD #riskmanagement #stoploss #goldtrading #forex
```

**6. `rex_06_rr.png` — Risk : Reward**
```
The one number that decides if you survive: risk-to-reward. Risk $20 to make $60 and you can be WRONG 6 times out of 10 and still grow your account. Professionals obsess over the ratio, not the win rate.

#XAUUSD #riskreward #riskmanagement #goldtrading #forex
```

**7. `rex_07_sizing.png` — Position Sizing**
```
Position sizing isn't maths homework — it's one division. Lot size = the $ you'll risk ÷ your stop distance. A wider stop means a SMALLER trade, so your dollar risk stays fixed no matter where the stop sits.

#XAUUSD #positionsizing #riskmanagement #goldtrading #forex
```

**8. `rex_08_ceiling.png` — The Risk Ceiling**
```
Set your maximum monthly loss while you're calm, then cascade it down to the week, the day, the trade. The market can't blow your account past a ceiling you set in advance — but you can, if you never set one.

#XAUUSD #riskmanagement #tradingdiscipline #goldtrading #forex
```

**9. `rex_09_sr.png` — Support & Resistance**
```
The floor and the ceiling of price. Resistance = where sellers keep stepping in. Support = where buyers keep defending. Price bounces between them until one breaks. Trade the reaction at the level, not the middle of nowhere.

#XAUUSD #supportandresistance #priceaction #goldtrading #forex
```

**10. `rex_10_trend.png` — Reading the Trend**
```
Structure over noise. Uptrend = higher highs + higher lows. Downtrend = lower highs + lower lows. Trade WITH the structure and the odds are on your side. Fight it and you're just donating.

#XAUUSD #trendtrading #priceaction #goldtrading #forex
```

**11. `rex_11_bos.png` — Break of Structure**
```
When price closes below the last higher low, the uptrend just cracked — that's a Break of Structure. It's the market's early warning that control is shifting. Respect it.

#XAUUSD #breakofstructure #smartmoney #priceaction #goldtrading
```

**12. `rex_12_rules.png` — The 3 Rules**
```
This channel is built on three rules I will never break:
01 — Every signal has a stop loss.
02 — I post my losses.
03 — I never promise profit.

If you want a track record instead of a story, the door is open 👉 https://t.me/+CR21qcOU0QI4ZDg9

#XAUUSD #goldtrading #tradingsignals #riskmanagement #forex
```
---

## Gợi ý lịch đăng
Đăng xen kẽ 2–3 ảnh/tuần, mỗi ảnh kèm caption trên. Có thể ghép chung lịch với file
`../REX_Facebook_Publer_Bulk.csv` (dán URL ảnh vào cột `Media URL` nếu upload lên host công khai).

## Sửa / tạo thêm ảnh
Mã nguồn nằm trong `src/`:
- `src/*.html` — mỗi ảnh 1 file HTML (sửa chữ/màu trực tiếp).
- `src/generate.py` — script sinh toàn bộ HTML.

Xuất lại PNG bằng Chromium headless:
```bash
chrome --headless --no-sandbox --force-device-scale-factor=2 \
  --window-size=1080,1350 --screenshot=rex_01_anatomy.png src/rex_01_anatomy.html
```
(hoặc mở file HTML trong trình duyệt rồi chụp màn hình vùng 1080×1350).
