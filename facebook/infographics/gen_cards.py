# -*- coding: utf-8 -*-
"""Generate 18 branded quote/stat cards + a manifest of (file, caption-with-CTA)."""
import os, json
OUT = "/home/user/rex-trading-blog/facebook/infographics/cards"
os.makedirs(OUT, exist_ok=True)
RED="#D6262C"; GOLD="#C4892B"; INK="#16130F"; BROWN="#7a6a4c"
TG="https://t.me/+CR21qcOU0QI4ZDg9"
PLAN="https://rextradingsignal.com/business-plan/"

BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1080px}}
body{{font-family:'Arial','Helvetica Neue',sans-serif;color:{INK};width:1080px;height:1080px;position:relative;overflow:hidden;
background:radial-gradient(900px 520px at 88% -6%,rgba(196,137,43,.18),transparent 60%),radial-gradient(760px 460px at -8% 106%,rgba(214,38,44,.10),transparent 60%),#F7F2E9}}
.frame{{position:absolute;inset:24px;border:2px solid rgba(22,19,15,.14);border-radius:22px}}
.pad{{position:absolute;inset:0;padding:60px 80px 92px;display:flex;flex-direction:column}}
.kicker{{display:flex;align-items:center;gap:13px;font-weight:800;letter-spacing:.18em;font-size:22px;color:{BROWN}}}
.kicker .dot{{width:12px;height:12px;border-radius:50%;background:{RED}}}
.mid{{flex:1;display:flex;flex-direction:column;justify-content:center}}
.quote{{font-size:150px;line-height:.6;color:{GOLD};font-weight:900;height:64px}}
h1{{font-weight:900;line-height:1.04;letter-spacing:-1px;font-size:{H1}px}}
h1 .g{{color:{GOLD}}} h1 .r{{color:{RED}}}
.body{{margin-top:28px;font-size:31px;line-height:1.45;color:#3d372e;font-weight:500;max-width:850px}}
.stat{{font-weight:900;font-size:210px;line-height:.9;color:{RED};letter-spacing:-4px}}
.label{{font-size:39px;font-weight:800;margin-top:6px}}
.foot{{display:flex;align-items:flex-end;justify-content:space-between}}
.logo .r{{font-weight:900;font-size:50px;letter-spacing:2px}} .logo .r b{{color:{RED}}}
.logo .s{{font-weight:800;letter-spacing:.40em;font-size:17px;color:{BROWN};margin-top:2px}}
.site{{text-align:right;font-weight:700;font-size:21px;color:{BROWN}}} .site b{{display:block;color:{INK};font-size:23px}}
</style></head><body><div class="frame"></div><div class="pad">
<div class="kicker"><span class="dot"></span> {KICKER}</div>
<div class="mid">{MID}</div>
<div class="foot"><div class="logo"><div class="r">RE<b>X</b></div><div class="s">TRADING SIGNAL</div></div>
<div class="site">Every signal has a stop loss.<b>rextradingsignal.com</b></div></div>
</div></body></html>"""

def quote(h, body): return f'<div class="quote">&ldquo;</div><h1>{h}</h1><div class="body">{body}</div>'
def stat(num, label, body): return f'<div class="stat">{num}</div><div class="label">{label}</div><div class="body">{body}</div>'

# (file, kicker, mid, H1, caption)
SAVE="📌 Save this so it's there when you need it."
def cards():
    return [
 ("card01_cut", "REX TRADING SIGNAL · MINDSET",
  quote('Cut losers <span class="g">fast</span>.<br>Let winners <span class="g">run</span>.',
        'Most traders do the opposite — small wins, big losses. That math kills accounts.'), 86,
  "The one habit that separates traders who last from traders who blow up.\n\nCut losers fast — that's your stop. Let winners breathe — that's your target.\n\n📌 SAVE this and read it before your next trade.\n\n#XAUUSD #gold #forex #goldtrading"),

 ("card02_risk", "REX TRADING SIGNAL · RISK RULE",
  stat("1–2%", "the most you risk per trade",
       "On $1,000 that's just $10–$20. Boring is what keeps you here next year."), 88,
  "How much should you risk on one gold trade? 1–2%. That's it.\n\nAt 1% you can lose 20 in a row and still keep 80% of your account. That's how you survive.\n\n📌 SAVE this number. It matters more than any signal.\n\n#XAUUSD #gold #riskmanagement #forex"),

 ("card03_rr", "REX TRADING SIGNAL · RISK RULE",
  stat("1:3", "risk to reward",
       "Risk $20 to make $60. Be wrong 6 of 10 times and still grow your account."), 88,
  "The one number that decides if you survive: risk-to-reward.\n\nAt 1:3 you can be WRONG more than half the time and still profit. Pros chase the ratio, not the win rate.\n\n📌 SAVE this.\n\n#XAUUSD #gold #riskreward #forex"),

 ("card04_r1", "REX TRADING SIGNAL · HOUSE RULE",
  quote('Every signal has a <span class="r">stop loss</span>.',
        'Before we ever talk about profit. Capital is oxygen — no oxygen, no next trade.'), 82,
  "Rule 01 of this channel: every signal comes with a stop loss. No exceptions.\n\nIf you know a trader who still 'closes it manually when it gets bad' — they need to see this.\n\n🔁 SHARE it with them.\n\n#XAUUSD #gold #stoploss #forex"),

 ("card05_r2", "REX TRADING SIGNAL · HOUSE RULE",
  quote('I post my <span class="r">losses</span>.',
        'A page that only shows winners is showing you a fantasy — and fantasies empty accounts.'), 86,
  "Rule 02: I post my losing trades too. On purpose.\n\nYou get the whole notebook here, not the highlight reel. That's the only honest way to earn trust.\n\n🔁 SHARE if you're tired of 'guru' pages that only show wins.\n\n#XAUUSD #gold #forex #trading"),

 ("card06_r3", "REX TRADING SIGNAL · HOUSE RULE",
  quote('I never <span class="r">promise profit</span>.',
        'Not "guaranteed." Not "fixed." Not "risk-free." Anyone who says those is selling a dream.'), 84,
  "Rule 03: I will never promise you profit. I can't, and I won't.\n\nReal trading has losses. Anyone hiding that is selling a fantasy.\n\n🔁 SHARE to protect a friend from the next 'guaranteed returns' scam.\n\n#XAUUSD #gold #forex #scamalert"),

 ("card07_nostop", "REX TRADING SIGNAL · RISK",
  quote('No stop loss = <span class="r">no trade</span>.',
        'You decide what you are willing to lose BEFORE you think about profit.'), 88,
  "Say it with me: no stop loss = no trade.\n\nThe stop isn't admitting defeat — it's the price of staying in the game long enough for your edge to show up.\n\n📌 SAVE this reminder.\n\n#XAUUSD #gold #stoploss #riskmanagement"),

 ("card08_move", "REX TRADING SIGNAL · RISK",
  quote('Don\'t move your <span class="r">stop</span>.',
        'The moment you slide it "to give it room," you\'ve stopped trading and started hoping.'), 86,
  "The number one account killer isn't a bad strategy. It's a stop loss that keeps sliding.\n\nSet it when you're calm. Then honor it when you're scared.\n\n📌 SAVE this — read it the next time you're tempted.\n\n#XAUUSD #gold #discipline #forex"),

 ("card09_rent", "REX TRADING SIGNAL · MINDSET",
  quote('The market doesn\'t know your <span class="g">rent</span> is due.',
        'Trade what you SEE, not what you NEED. The chart owes you nothing.'), 76,
  "The second you trade what you NEED instead of what you SEE, you've already lost.\n\nGold doesn't care that you're down this month. Trade the chart in front of you.\n\n🔁 SHARE with a trader who's forcing trades right now.\n\n#XAUUSD #gold #tradingpsychology"),

 ("card10_boring", "REX TRADING SIGNAL · MINDSET",
  quote('Boring trading is <span class="g">winning</span> trading.',
        'One clean setup. Stop in. Target set. Walk away. If it feels like a casino, that\'s the problem.'), 80,
  "Good trading is boring. One or two clean setups, then you close the laptop.\n\nThe traders glued to the screen all day aren't disciplined — they're emotional.\n\n🔁 SHARE if your best trades were your calmest ones.\n\n#XAUUSD #gold #forex #trading"),

 ("card11_scam", "REX TRADING SIGNAL · PROTECT YOURSELF",
  quote('"Fixed returns. Zero risk." <span class="r">→ RUN.</span>',
        'Those three words cost me three years of company profit. Don\'t let them cost you yours.'), 74,
  "If anyone ever guarantees you profit — run.\n\n'Fixed returns.' 'Zero risk.' 'Can't lose.' I believed a man who said those words. It cost me everything.\n\n🔁 SHARE to save someone from the same trap.\n\n#XAUUSD #gold #scamalert #forex"),

 ("card12_plan", "REX TRADING SIGNAL · DISCIPLINE",
  quote('Plan at <span class="g">night</span>.<br>Trade the plan by <span class="g">day</span>.',
        'Decisions made in a quiet room beat decisions made mid-candle with your heart pounding.'), 80,
  "Do your thinking BEFORE the money's on the line.\n\nAt night, calm: what setup, what stop, what target, how much risk? Then morning-you just follows the plan.\n\n📌 SAVE this routine.\n\n#XAUUSD #gold #tradingplan #discipline"),

 ("card13_winrate", "REX TRADING SIGNAL · RISK",
  quote('Win rate <span class="r">lies</span>.',
        'A 70% win rate still bleeds you dry if your losers are huge. The ratio is the whole game.'), 88,
  "'I win 70% of my trades!' Cool — are you profitable? Often, no.\n\nStop counting how OFTEN you're right. Measure how BIG you win vs how small you lose.\n\n📌 SAVE this.\n\n#XAUUSD #gold #riskreward #forex"),

 ("card14_3rules", "REX TRADING SIGNAL · FREE PLAYBOOK",
  quote('3 rules keep an account <span class="g">alive</span>.',
        'Stop loss on every trade · post the losses · never promise profit. Want the full playbook?'), 78,
  "These 3 rules have kept this account alive longer than any signal ever could.\n\nWant the full system written on one page — plus the daily routine and the 5 rookie mistakes?\n\n📩 Grab it FREE (just your email) 👉 " + PLAN + "\n\n#XAUUSD #gold #forex"),

 ("card15_onepage", "REX TRADING SIGNAL · FREE PLAYBOOK",
  quote('Your trading business fits on <span class="g">one page</span>.',
        'Mission · risk ceiling · trade ticket · journal · nightly audit. Fill it in tonight.'), 76,
  "You don't need a 40-page course. You need one page you'll actually use.\n\nSix fields, filled in tonight, and your trading finally runs like a business.\n\n📩 Get the free one-page template (leave your email) 👉 " + PLAN + "\n\n#XAUUSD #gold #tradingplan"),

 ("card16_5mistakes", "REX TRADING SIGNAL · FREE GUIDE",
  quote('5 mistakes that quietly <span class="r">bankrupt</span> new gold traders.',
        'Know them before they cost you a single dollar.'), 72,
  "Most new gold traders blow up the same 5 ways. You can skip that tuition.\n\n📩 Get the free guide + one-page business plan (just your email) 👉 " + PLAN + "\n\nCheaper than learning it the hard way.\n\n#XAUUSD #gold #forex #goldtrading"),

 ("card17_ceiling", "REX TRADING SIGNAL · RISK",
  quote('Set your max monthly loss while you\'re <span class="g">calm</span>.',
        'The Risk Ceiling. Cascade it down: month → week → day → trade. Never breach it.'), 76,
  "The market can't blow your account past a ceiling you set in advance. But you can — if you never set one.\n\nDecide your max monthly loss while calm, then cascade it down.\n\n📌 SAVE this.\n\n#XAUUSD #gold #riskmanagement"),

 ("card18_freeplan", "REX TRADING SIGNAL · FREE GIFT",
  quote('Free: The Trader\'s <span class="g">Business Plan</span>.',
        'One page. The daily operating routine. The 5 mistakes that bankrupt beginners. No cost.'), 76,
  "A gift from us, no strings: The Trader's Business Plan — one page, the daily routine, and the 5 mistakes that quietly bankrupt new gold traders.\n\n📩 Download it free (just drop your email) 👉 " + PLAN + "\n\n#XAUUSD #gold #forex #freedownload"),
    ]

def build():
    manifest = []
    for fname, kicker, mid, h1, caption in cards():
        html = BASE.format(INK=INK, RED=RED, GOLD=GOLD, BROWN=BROWN, KICKER=kicker, MID=mid, H1=h1)
        open(os.path.join(OUT, fname + ".html"), "w").write(html)
        manifest.append({"file": fname + ".png", "caption": caption})
    json.dump(manifest, open(os.path.join(OUT, "cards.json"), "w"), ensure_ascii=False, indent=2)
    print("built", len(manifest), "cards")

if __name__ == "__main__":
    build()
