# -*- coding: utf-8 -*-
"""Build the August content calendar: 8 posts/day x 31 days = 248 slots.
Each slot: date, time(ET), format, weekly theme, concrete topic, CTA purpose."""
import csv, datetime

# 8 daily slots (US Eastern time) -> format
SLOTS = [
    ("06:30", "Short post"),
    ("08:30", "Image (infographic)"),
    ("10:30", "Quote card"),
    ("12:30", "Reel (short video)"),
    ("15:00", "Long post"),
    ("17:30", "Story / interactive"),
    ("20:00", "Long video"),
    ("22:00", "Short post / interactive"),
]

# Weekly themes (Aug)
def theme(day):
    if day <= 7:  return "W1 · Candlesticks & Chart Basics"
    if day <= 14: return "W2 · Risk Management"
    if day <= 21: return "W3 · Market Structure & Strategy"
    if day <= 28: return "W4 · Trading Psychology & Discipline"
    return "W5 · Recap + Free Business Plan"

# Topic banks per theme (rotated)
TOPICS = {
 "W1": ["What a candle really is","Bullish vs bearish body","Wicks = rejection","Engulfing pattern",
        "Pin bar / rejection candle","Doji / indecision","Hammer & shooting star","Morning/Evening star",
        "Three soldiers / crows","Reading a candle in 10s","Body vs wick meaning","Marubozu (strong candle)",
        "Inside bar","Candle colors & psychology"],
 "W2": ["Every trade has a stop loss","The 1–2% rule","Risk : Reward 1:3","Position sizing (one division)",
        "The risk ceiling","Never move your stop","Win rate vs the ratio","Break-even stop",
        "Partial take profit","Leverage is a magnifier","Demo first","Capital is oxygen",
        "Revenge trading kills accounts","Compounding slowly"],
 "W3": ["Support & resistance","Reading the trend (HH/HL)","Change of Character (CHoCH)","Break of Structure (BOS)",
        "Support becomes resistance","Trend lines","Trading sessions (London/NY)","News spikes (NFP/CPI)",
        "DXY vs gold correlation","Multi-timeframe view","Confluence zones","Fibonacci levels",
        "Liquidity & stop hunts","Trade the level, not the middle"],
 "W4": ["FOMO — chasing candles","Patience beats activity","Overtrading","Boring trading wins",
        "Trade what you see, not what you need","Plan at night, trade by day","The 2am 'should I close'",
        "Discipline over excitement","'This time is different' trap","Journaling your trades",
        "Cut losers, let winners run","Emotions are the enemy","Consistency is the edge","Process over outcome"],
 "W5": ["The 3 rules REX never breaks","Why I post my losses","Never promise profit",
        "Your trading business on one page","Free: The Trader's Business Plan","5 mistakes that bankrupt beginners"],
}
def bank(day):
    if day<=7: return TOPICS["W1"]
    if day<=14: return TOPICS["W2"]
    if day<=21: return TOPICS["W3"]
    if day<=28: return TOPICS["W4"]
    return TOPICS["W5"]

# CTA rotation per format
CTA = {
 "Short post":"💬 Comment",
 "Image (infographic)":"📌 Save",
 "Quote card":"🔁 Share",
 "Reel (short video)":"📌 Save + Follow",
 "Long post":"📖 Read blog / 💬 Comment",
 "Story / interactive":"💬 Poll / Comment",
 "Long video":"📌 Save + Follow",
 "Short post / interactive":"📩 Email (free plan) / 💬 Comment",
}

rows=[]
for day in range(1,32):
    date=f"2026-08-{day:02d}"
    tb=bank(day); th=theme(day)
    for i,(time,fmt) in enumerate(SLOTS):
        # pick a topic; vary across the day and days
        topic=tb[(day*8+i) % len(tb)]
        rows.append((date,time,fmt,th,topic,CTA[fmt]))

out="/home/user/rex-trading-blog/facebook/schedule/august_calendar.csv"
with open(out,"w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    w.writerow(["Date","Time_ET","Format","Theme","Topic","CTA"])
    for r in rows: w.writerow(r)

from collections import Counter
print("total slots:",len(rows))
print("per day:",len(SLOTS),"| days:",31)
fc=Counter(r[2] for r in rows)
for k,v in fc.items(): print(f"  {k}: {v}")
print("wrote",out)
