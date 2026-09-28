# -*- coding: utf-8 -*-
"""Assemble Week 1 of August (Aug 1-7): 8 posts/day x 7 = 56 rows.
Reuses existing image/card/reel assets + 7 long videos + 28 new text posts."""
import csv, re, json, os

ROOT="/home/user/rex-trading-blog"
RAW="https://raw.githubusercontent.com/buithithuytrinhfamily-sketch/rex-trading-blog/claude/facebook-channel-scheduling-29clrd/facebook/"
IG=RAW+"infographics/"; CARD=RAW+"infographics/cards/"; REEL=RAW+"reels/"; LV=RAW+"reels/long/"
PLAN="https://rextradingsignal.com/business-plan/"

img_caps=re.findall(r"```\n(.*?)\n```", open(ROOT+"/facebook/infographics/captions-en.md",encoding="utf-8").read(), re.S)
IMGF=["rex_01_anatomy","rex_02_engulfing","rex_03_pinbar","rex_04_doji","rex_05_trade","rex_06_rr","rex_07_sizing","rex_08_ceiling","rex_09_sr","rex_10_trend","rex_11_bos","rex_12_rules"]
imgcap={n:img_caps[i] for i,n in enumerate(IMGF)}
cards=json.load(open(ROOT+"/facebook/infographics/cards/cards.json",encoding="utf-8"))
cardcap={c["file"]:c["caption"] for c in cards}

SHORT=[
"A green candle isn't \"good\" and a red candle isn't \"bad.\" Each one just tells you who won that round — buyers or sellers. Learn to read them and the chart stops being scary.\n\n💬 What confuses you most about candles?",
"The body shows where price opened and closed. The wick shows how far it tried to go and got rejected. That's the whole candle.\n\n📌 Save this.",
"Big body = strong move. Tiny body = indecision. Long wick = a level got rejected hard.\n\nCandles are a language. Start reading it. 💬",
"Beginners stare at indicators. Pros read the raw candles first. Price is the truth — everything else lags.\n\n💬 Indicators or pure price action?",
"One clean candle at a key level tells you more than 10 indicators. Simplicity wins.\n\n📌 Save this reminder.",
"Green, red, green… it's not random noise. It's a conversation between buyers and sellers. Your job is to listen, not predict.",
"You don't need to catch every candle. You need to read ONE clearly and act with a stop loss. Quality over noise. 💬",
]
LONG=[
"Before any strategy, learn to read a single candle.\n\n• The BODY = where price opened and closed.\n• The WICK = how far price tried to go before getting rejected.\n• Green closed up, red closed down.\n\nThat's it. Master this and every gold chart starts to make sense.\n\n📖 Full breakdown: https://rextradingsignal.com/how-to-manage-risk-in-gold-trading.html\n#XAUUSD #gold #priceaction",
"The engulfing candle is one of the cleanest reversal tells on the chart.\n\nA big body that completely swallows the candle before it means control just changed hands — buyers took over (bullish) or sellers did (bearish). It's strongest at support or resistance, not in the middle of nowhere.\n\n💬 Have you traded this one?\n#XAUUSD #gold #engulfing",
"A long wick is a story of rejection.\n\nBullish pin: price dropped, then buyers slammed it back up — they rejected lower prices. Bearish pin: the opposite. The longer the wick, the louder the rejection.\n\nWe wait for these at key levels, with a stop loss already set.\n#XAUUSD #gold #pinbar",
"Open ≈ close = the market is undecided.\n\nA doji isn't a buy or a sell on its own — it's a pause. The real move comes from the candle AFTER it. Rushing in on a doji is guessing.\n\nPatience beats guessing, every time.\n#XAUUSD #gold #doji",
"Every candle is emotion made visible.\n\nA long green body = greed and confidence. A long lower wick = fear that got rejected. A doji = hesitation. When you read candles, you're reading the crowd's psychology in real time.\n\nTrade the emotion, not your own.\n#XAUUSD #gold #tradingpsychology",
"A candle pattern in the middle of nowhere means nothing. The SAME pattern at a key support or resistance means everything.\n\nContext first, pattern second. That's the difference between gambling and trading.\n\n📌 Save this.\n#XAUUSD #gold #priceaction",
"The move comes from the candle AFTER the signal — not the signal itself.\n\nSee a reversal candle? Don't jump. Wait for the next candle to confirm the direction, set your stop, then act. One extra minute of patience saves a lot of losing trades.\n#XAUUSD #gold #discipline",
]
INTER=[
"Poll 📊 When you see a DOJI, do you:\nA) Wait for confirmation\nB) Enter anyway\nC) Ignore it\n\nComment A / B / C 👇",
"What candle pattern do you trust the MOST? 🕯️\nEngulfing? Pin bar? Something else?\nComment yours 👇",
"Real talk: do you actually READ candles, or just follow signals? 😅 No judgment — comment honestly 👇",
"Which color makes you more emotional when it's YOUR money on the line — green 🟢 or red 🔴? 💬",
"🔁 Tag a friend who still thinks a big green candle automatically means \"buy now.\"",
"What timeframe do you read candles on? ⏱️\n1m scalp? 15m? 4H swing?\nComment your style 👇",
"If you could master ONE candle pattern this week, which would it be? 💬 Drop it below 👇",
]
EMAIL=[
"Want a free one-page cheat sheet of the candles + how we actually trade them? 📩\n\nGrab The Trader's Business Plan (free) 👉 "+PLAN,
"Reading candles is step 1. Managing risk is step 2. Our free one-page plan covers both 👉 "+PLAN+" 📩",
"The 5 mistakes that quietly bankrupt new gold traders — free guide, just your email 👉 "+PLAN,
"Save yourself months of trial and error. Free Trader's Business Plan (one page) 📩 "+PLAN,
"Loved this week's candle lessons? Get them + the daily routine in one free PDF 👉 "+PLAN,
"Every signal we post has a stop loss. Want the 3 rules we never break? Free 📩 "+PLAN,
"One page. Your whole trading business. Free, no catch 👉 "+PLAN+" 📩",
]
# visual asset assignments per day (index 0..6)
IMGS=["rex_01_anatomy","rex_02_engulfing","rex_03_pinbar","rex_04_doji","rex_09_sr","rex_10_trend","rex_12_rules"]
CARDS=["card01_cut.png","card09_rent.png","card10_boring.png","card07_nostop.png","card13_winrate.png","card12_plan.png","card17_ceiling.png"]
REELS=["rex_01_anatomy","rex_02_engulfing","rex_03_pinbar","rex_04_doji","rex_05_trade","rex_06_rr","rex_12_rules"]
LVCAP="🎬 Candlestick lesson — save this and watch till the end.\n📌 SAVE + Follow @REXTradingSignal for the full series.\n#XAUUSD #gold #forex #priceaction"

rows=[]
for d in range(7):
    date=f"2026-08-{d+1:02d}"
    rows.append((date,"06:30","text",SHORT[d],""))
    rows.append((date,"08:30","photo",imgcap[IMGS[d]], IG+IMGS[d]+".png"))
    rows.append((date,"10:30","photo",cardcap[CARDS[d]], CARD+CARDS[d]))
    rows.append((date,"12:30","video",imgcap[REELS[d]], REEL+REELS[d]+".mp4"))
    rows.append((date,"15:00","text",LONG[d],""))
    rows.append((date,"17:30","text",INTER[d],""))
    rows.append((date,"20:00","video",LVCAP, LV+f"LV{d+1}.mp4"))
    rows.append((date,"22:00","text",EMAIL[d],""))

out=ROOT+"/facebook/schedule/week1_august.csv"
with open(out,"w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL); w.writerow(["Date","Time_ET","Kind","Content","MediaURL"])
    for r in rows: w.writerow(r)
print("week1 rows:",len(rows))
from collections import Counter
print(Counter(r[2] for r in rows))
print("wrote",out)
