# -*- coding: utf-8 -*-
"""Build a full-July content schedule for Rex Trading Signals (~60 posts)."""
import csv, os, re, datetime

ROOT = "/home/user/rex-trading-blog"
RAW = ("https://raw.githubusercontent.com/buithithuytrinhfamily-sketch/"
       "rex-trading-blog/claude/facebook-channel-scheduling-29clrd/facebook/infographics/")
TG = "https://t.me/+CR21qcOU0QI4ZDg9"

# ---- 14 reused text posts (from the earlier bulk CSV) ----
reused = [r["Content"] for r in csv.DictReader(
    open(os.path.join(ROOT, "facebook/REX_Facebook_Publer_Bulk.csv"), encoding="utf-8-sig"))]

# ---- 34 new text posts ----
new = [
"""That candle is flying without you. Every cell in your body says "get in NOW."

That feeling has a name: FOMO. And it's the most expensive emotion in trading.

The move you chase is usually the move that's ending — you buy the top, it reverses, your stop hits.

Missing a trade costs you nothing. Chasing one costs you money. There's always another setup tomorrow.""",

"""The best trade I made last week was the one I didn't take.

The setup was "almost" there. Almost is a no. So I closed the laptop.

Amateurs force trades out of boredom. Professionals wait — sometimes all day — for the one setup that fits their rules.

You don't get paid for activity. You get paid for precision. Wait for your pitch.""",

"""More trades does not mean more money. Usually the opposite.

Every extra trade you take out of boredom or FOMO is a fresh chance to lose. Ten mediocre trades beat you up. One clean trade pays you.

If you're trading every hour, you're not trading — you're gambling with extra steps.

Do less. Choose better.""",

"""It's 2am. You're still up, staring at a trade going the wrong way. "Should I close it? Should I wait?"

Here's the truth: if you have to ask, your stop loss should have already made the decision for you. That's what it's for.

Set the stop when you're calm, then let it do its job so you can sleep. A trade that costs you sleep is too big.""",

"""The market doesn't know your rent is due. It doesn't care that you're down this month.

The second you trade what you NEED instead of what you SEE, you've already lost.

Gold doesn't owe you a good month. Trade the chart in front of you, not the story in your head — and the results stop feeling personal.""",

"""Good trading is boring. Really boring.

One clean setup. Stop loss in. Target set. Click. Walk away.

No six-hour screen marathons. No ten panic trades. No screenshots of huge wins.

If your trading feels like a casino, that's the problem — not the strategy. Boring is what keeps you here next year.""",

"""Most traders do the exact opposite of what works.

They snatch tiny profits fast (scared to lose them) and let losers run (hoping they come back). Small wins, big losses. That math kills accounts.

Flip it: cut losers fast — that's your stop. Let winners breathe — that's your target. Boring rule. Life-changing results.""",

"""The moment you move your stop loss further away "just to give it room"… you've stopped trading and started hoping.

A stop is a promise you make to yourself when you're calm. Moving it is breaking that promise when you're scared.

The number one account killer isn't a bad strategy. It's a stop loss that keeps sliding.""",

""""This time is different." Four words that have emptied more accounts than any crash.

It's not different. The setup that failed you last month will fail you again if you skip your rules.

Discipline isn't exciting — but "exciting" is exactly what blows accounts. Be boring. Follow the plan.""",

"""How much should you risk on one gold trade? 1–2% of your account. That's it.

On $1,000 that's $10–$20 per trade. Sounds small. It's supposed to.

At 1%, you could lose 20 in a row and still keep 80% of your account. At 20% risk, three bad trades and you're done.

Survival first. Everything else is second.""",

"""Before you risk one real dollar on gold, trade a demo for a month.

Not to prove you can win — to prove you can FOLLOW YOUR RULES. Stop loss every time. Same risk every time. Journal every trade.

If you can't stay disciplined with fake money, real money will wreck you. The demo isn't beneath you. It's the exam.""",

"""Leverage feels like a superpower. It's actually a magnifying glass — for your mistakes.

High leverage doesn't make you more money. It makes each move hit your account harder, both directions.

The pros use less leverage than you'd think. Not because they're scared — because they plan to still be here in five years.""",

"""Big news drops (NFP, CPI) and gold goes vertical. Feels like free money. It's a trap.

Spreads widen. Price whips both ways. Your stop can get skipped entirely. This is where accounts die in seconds.

When the news hits, the professional move is often to do nothing. Let the chaos pass. Trade the clean chart after — not the explosion.""",

"""Quick gold tip: keep one eye on the US Dollar (DXY).

Gold and the dollar usually move opposite ways. Dollar up, gold tends down — and vice versa.

If you're long gold while the dollar is ripping higher, you're swimming against the current. Not a hard rule, but a strong hint. Context beats guessing.""",

"""Gold doesn't move the same all day.

The quiet Asian hours chop sideways and stop you out for no reason. The London and New York sessions bring the real volume and cleaner moves.

Trading the dead hours out of impatience is a great way to donate money. Know when your market actually wakes up.""",

"""Your trade moves nicely in your favor. Now what?

Move your stop loss to your entry (break-even). Now the worst case is: you lose nothing.

A trade that can't lose is a beautiful thing. You stop trading scared and start letting the winner run. Protect first, profit second.""",

"""Taking some profit off the table isn't weakness — it's how you stay sane.

Close part of your position at the first target, move the stop to break-even, let the rest ride.

Now you've banked a win AND you have a risk-free runner. Whatever happens next, you can't lose. That's how pros hold winners without white knuckles.""",

""""I win 70% of my trades!" Cool. Are you profitable? Often the answer is no.

If your winners are tiny and your losers are huge, a 70% win rate still bleeds you dry.

Stop counting how OFTEN you're right. Start measuring how BIG you win versus how small you lose. That ratio is the whole game.""",

"""Nobody wants to hear it, but the fastest way to grow an account is slowly.

2% a week doesn't sound sexy. Compounded over a year, it's life-changing.

The traders chasing 100% a month are usually at 0% by year end — or below. Aim for steady. Let compounding do the flashy part quietly.""",

"""Plan the trade at night. Trade the plan in the morning.

When the market is quiet and you're calm, decide: what setup will I take, where's my stop, where's my target, how much do I risk?

Decisions made in a quiet room beat decisions made mid-candle with your heart pounding. Do your thinking BEFORE the money's on the line.""",

"""What's the hardest part of trading for YOU? 🤔

For most people it's not finding trades — it's sitting on their hands and NOT trading.

Tell me in the comments 👇 I read every one.""",

"""Every trader has that one loss that taught them everything.

What did yours teach you? Drop it below 👇 Someone reading this needs to hear it before they learn it the hard way.""",

"""Quick one: do you keep a trading journal? 📓

Type YES or NO in the comments.

(If you typed NO — that might be the single biggest thing holding you back. More on that this week.)""",

"""Be honest: what's your max risk per trade? 🎯

1%? 2%? "…I don't really set one"?

Comment your number 👇 No judgment — but if you don't have one, that's lesson number one.""",

"""Scalper or swing trader? ⚡🐢

Quick trades all day, or a few positions held for days?

There's no wrong answer — but knowing which one YOU are changes everything about your rules. Comment your style 👇""",

"""What made you start trading gold? 🥇

The charts? A friend? A dream of quitting the 9–5?

Tell me your "why" below — it's the thing that keeps you disciplined when it gets hard.""",

"""Every week I post my losing trades. On purpose.

Why? Because a page that only shows winners is showing you a fantasy — and fantasies are what empty accounts.

You get the whole notebook here: the reds, the stops that fired, the boring wins. That's the only honest way to earn your trust.""",

"""If anyone guarantees you profit in trading — run.

"Fixed returns." "Zero risk." "Can't lose." Those words cost me three years of profit once, because I believed the man who said them.

Real trading has losses. Anyone hiding that is selling a dream, not a strategy. Protect your money by protecting your skepticism.""",

"""Don't trust this page. Seriously.

Don't trust me because I sound confident. Trust the proof, over time.

Watch how we handle losses. Watch if the stop losses are real. Judge slowly. A scammer needs you to believe fast — I'd rather you believe SLOWLY, and for good reasons.""",

"""The signal isn't the valuable part. The rules are.

Anyone can hand you a "buy here." Almost nobody teaches you where to put your stop, how much to risk, and when to walk away.

A signal feeds you for a day. The rules feed you for a career. That's what we actually care about here.""",

"""End of the week. Here's the honest scoreboard.

Green days and red days. We took losses — small ones, each with a stop that did its job. We let a couple of winners run.

No miracle screenshots. No "100% accuracy." Just a process repeated with discipline. That's the deal here, every week, out loud.""",

"""New week. Reset. 🔁

Last week is closed — the wins and the losses. This week starts at zero.

Before the first candle: what's your risk ceiling for the week? Which setups will you take? Write it down now, while you're calm. Plan first, trade second.""",

"""Want the 3 rules that have kept this account alive longer than any signal ever could?

Comment "RULES" below and I'll send you our 3 capital-protection rules — free, no catch.

Read them. If they make sense, you'll know if this is your kind of room.""",

"""Free from us, no email wall: a one-page Trader's Business Plan + the daily routine + the 5 mistakes that quietly bankrupt new gold traders.

Grab it 👉 https://rextradingsignal.com/business-plan/

One page you'll actually use beats a 40-page course you never open.""",
]

texts = reused + new  # 14 + 34 = 48

# ---- 12 image posts: portrait infographics + captions parsed from captions-en.md ----
cap_md = open(os.path.join(ROOT, "facebook/infographics/captions-en.md"), encoding="utf-8").read()
caps = re.findall(r"```\n(.*?)\n```", cap_md, re.S)
imgfiles = ["rex_01_anatomy","rex_02_engulfing","rex_03_pinbar","rex_04_doji","rex_05_trade",
            "rex_06_rr","rex_07_sizing","rex_08_ceiling","rex_09_sr","rex_10_trend",
            "rex_11_bos","rex_12_rules"]
assert len(caps) == 12, f"expected 12 captions, got {len(caps)}"
images = [(RAW + f + ".png", caps[i]) for i, f in enumerate(imgfiles)]

# ---- interleave: an image every ~5th slot ----
items = []
ti = ii = 0
for i in range(60):
    if i % 5 == 4 and ii < len(images):
        items.append(("img", images[ii])); ii += 1
    else:
        items.append(("txt", texts[ti])); ti += 1
# any leftover images -> append
while ii < len(images):
    items.append(("img", images[ii])); ii += 1

# ---- assign dates/times: 13-31 Jul, 4 posts on first 3 days then 3/day ----
slots = []
start = datetime.date(2026, 7, 13)
alltimes = ["08:00", "12:30", "18:00", "20:30"]
for d in range(19):
    n = 4 if d < 3 else 3
    for t in alltimes[:n]:
        slots.append((str(start + datetime.timedelta(days=d)), t))

rows = []
for (kind, payload), (date, time) in zip(items, slots):
    if kind == "img":
        url, cap = payload
        rows.append((date, time, cap, "", url))
    else:
        rows.append((date, time, payload, "", ""))

out = os.path.join(ROOT, "facebook/schedule/july_full.csv")
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(["Date", "Time", "Content", "Link", "Media URL"])
    for r in rows:
        w.writerow(r)

print(f"posts total: {len(rows)}  (texts={len(texts)}, images={len(images)}, slots={len(slots)})")
imgc = sum(1 for r in rows if r[4])
print(f"image posts: {imgc}, text posts: {len(rows)-imgc}")
print("wrote", out)
