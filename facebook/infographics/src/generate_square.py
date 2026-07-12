# -*- coding: utf-8 -*-
import os

OUT = "/tmp/claude-0/-home-user/471ed8c8-7e86-57d6-a0c0-40d913ed0c1d/scratchpad/ig_sq"
os.makedirs(OUT, exist_ok=True)

RED="#D6262C"; GREEN="#1E7A4E"; GOLD="#C4892B"; INK="#16130F"; BROWN="#7a6a4c"; MUTE="#a99a7c"
RTR="rgba(214,38,44,.13)"; GTR="rgba(30,122,78,.13)"; GDTR="rgba(196,137,43,.14)"

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--ink:{INK};--red:{RED};--green:{GREEN};--gold:{GOLD};--brown:{BROWN}}}
html,body{{width:1080px;height:1080px}}
body{{font-family:'Arial','Helvetica Neue',sans-serif;color:var(--ink);width:1080px;height:1080px;position:relative;overflow:hidden;
background:radial-gradient(900px 520px at 88% -6%,rgba(196,137,43,.16),transparent 60%),radial-gradient(760px 460px at -8% 106%,rgba(214,38,44,.08),transparent 60%),#F7F2E9}}
.frame{{position:absolute;inset:24px;border:2px solid rgba(22,19,15,.14);border-radius:22px}}
.pad{{position:absolute;inset:0;padding:42px 68px 92px;display:flex;flex-direction:column}}
.kicker{{display:flex;align-items:center;gap:13px;font-weight:800;letter-spacing:.18em;font-size:21px;color:#7a6a4c}}
.kicker .dot{{width:12px;height:12px;border-radius:50%;background:var(--red)}}
.head{{display:flex;align-items:center;gap:22px;margin-top:16px}}
.badge{{width:94px;height:94px;border-radius:50%;border:5px solid var(--ink);display:flex;align-items:center;justify-content:center;gap:8px;flex:none;background:#fff}}
.badge .c{{width:16px;border-radius:3px}} .badge .cr{{height:46px;background:var(--red)}} .badge .cg{{height:36px;background:var(--green)}}
h1{{font-weight:900;line-height:.92;letter-spacing:-.5px}}
h1 .l1{{display:block;font-size:42px;color:var(--gold)}}
h1 .l2{{display:block;font-size:{L2SIZE}px;text-transform:uppercase}}
.stage{{flex:1;display:flex;align-items:center;justify-content:center;margin-top:0;min-height:0}}
.stage svg{{width:100%;height:100%}}
.foot{{display:flex;align-items:flex-end;justify-content:space-between}}
.logo .r{{font-weight:900;font-size:46px;letter-spacing:2px}} .logo .r b{{color:var(--red)}}
.logo .s{{font-weight:800;letter-spacing:.40em;font-size:16px;color:#7a6a4c;margin-top:2px}}
.site{{text-align:right;font-weight:700;font-size:20px;color:#7a6a4c}} .site b{{display:block;color:var(--ink);font-size:22px}}
text{{font-family:'Arial','Helvetica Neue',sans-serif}}
</style></head><body>
<div class="frame"></div>
<div class="pad">
  <div class="kicker"><span class="dot"></span> {KICKER}</div>
  <div class="head"><div class="badge"><span class="c cr"></span><span class="c cg"></span></div>
    <h1><span class="l1">{L1}</span><span class="l2">{L2}</span></h1></div>
  <div class="stage">{SVG}</div>
  <div class="foot">
    <div class="logo"><div class="r">RE<b>X</b></div><div class="s">TRADING SIGNAL</div></div>
    <div class="site">{TAG}<b>rextradingsignal.com</b></div>
  </div>
</div></body></html>"""

MARK = ('<defs>'
 '<marker id="ar" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="%s"/></marker>'
 '<marker id="arG" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="%s"/></marker>'
 '<marker id="arR" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="%s"/></marker>'
 '</defs>') % (BROWN, GREEN, RED)

def svg(inner, vbw=900, vbh=640, w=880):
    # responsive: scale to fit the (shorter) square stage while keeping aspect ratio
    return '<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet">%s%s</svg>' % (vbw,vbh,MARK,inner)

def page(fname, kicker, l1, l2, inner, tag="Every signal has a stop loss.&nbsp;", l2size=62, vbw=900, vbh=640, w=880):
    html = TEMPLATE.format(INK=INK,RED=RED,GREEN=GREEN,GOLD=GOLD,BROWN=BROWN,
        KICKER=kicker, L1=l1, L2=l2, SVG=svg(inner,vbw,vbh,w), TAG=tag, L2SIZE=l2size)
    p = os.path.join(OUT, fname+".html")
    open(p,"w",encoding="utf-8").write(html)
    return p

def candle(cx, top, bot, bodytop, bodybot, color, bw=88):
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="6"/>'
            '<rect x="%d" y="%d" width="%d" height="%d" rx="7" fill="%s"/>'
            ) % (cx,top,cx,bot,color, cx-bw//2,bodytop,bw,bodybot-bodytop,color)

def T(x,y,s,txt,anchor="middle",w=800,fill=INK):
    return '<text x="%d" y="%d" text-anchor="%s" font-size="%d" font-weight="%d" fill="%s">%s</text>'%(x,y,anchor,s,w,fill,txt)

def L(x1,y1,x2,y2,marker="ar",color=BROWN,sw=2.6):
    return '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s" marker-end="url(#%s)"/>'%(x1,y1,x2,y2,color,sw,marker)

pages=[]

# ---------- 1. ANATOMY OF A CANDLE ----------
s = candle(250,60,560,190,430,GREEN)
s+= T(250,600,30,"BULLISH",fill=GREEN)
s+= L(120,60,247,60)+T(112,68,24,"HIGH","end")
s+= L(120,190,205,190)+T(112,198,24,"CLOSE","end")
s+= L(120,430,205,430)+T(112,438,24,"OPEN","end")
s+= L(120,560,247,560)+T(112,568,24,"LOW","end")
s+= candle(650,60,560,190,430,RED)
s+= T(650,600,30,"BEARISH",fill=RED)
s+= L(780,60,653,60)+T(788,68,24,"HIGH","start")
s+= L(780,190,695,190)+T(788,198,24,"OPEN","start")
s+= L(780,430,695,430)+T(788,438,24,"CLOSE","start")
s+= L(780,560,653,560)+T(788,568,24,"LOW","start")
s+= T(450,150,22,"WICK",fill=BROWN)+T(450,178,17,"the extreme",fill=MUTE)
s+= T(450,320,22,"BODY",fill=BROWN)+T(450,348,17,"open &#8594; close",fill=MUTE)
pages.append(page("rex_01_anatomy","REX TRADING SIGNAL &middot; XAUUSD BASICS","Anatomy of a","Candlestick",s))

# ---------- 2. ENGULFING ----------
s = T(258,70,26,"&#10003; BULLISH",fill=GREEN)
s+= candle(210,150,340,210,300,RED,54)          # small red
s+= candle(300,120,430,170,410,GREEN,78)        # big green engulfs
s+= L(360,150,410,110,"arG",GREEN,5)
s+= T(258,500,17,"green body swallows the red",fill=MUTE)
s+= T(258,470,26,"buyers take control",fill=INK)
s+= '<line x1="450" y1="90" x2="450" y2="520" stroke="%s" stroke-width="2" stroke-dasharray="7 8"/>'%("rgba(22,19,15,.20)")
s+= T(688,70,26,"&#10003; BEARISH",fill=RED)
s+= candle(640,150,340,210,300,GREEN,54)
s+= candle(730,120,430,170,410,RED,78)
s+= L(670,410,620,470,"arR",RED,5)
s+= T(688,470,26,"sellers take control",fill=INK)
s+= T(688,500,17,"red body swallows the green",fill=MUTE)
pages.append(page("rex_02_engulfing","REX TRADING SIGNAL &middot; CANDLE PATTERNS","The reversal candle","Engulfing",s))

# ---------- 3. PIN BAR ----------
s = T(250,70,26,"BULLISH PIN",fill=GREEN)
s+= candle(250,120,470,120,190,GREEN,72)   # small body top, long lower wick
s+= L(250,520,250,478,"arG",GREEN,5)
s+= T(250,560,20,"buyers rejected",fill=BROWN)+T(250,586,20,"lower prices",fill=BROWN)
s+= T(650,70,26,"BEARISH PIN",fill=RED)
s+= candle(650,120,470,400,470,RED,72)    # small body bottom, long upper wick
s+= L(650,120,650,162,"arR",RED,5)
s+= T(650,560,20,"sellers rejected",fill=BROWN)+T(650,586,20,"higher prices",fill=BROWN)
s+= T(450,300,24,"long wick",fill=INK)+T(450,332,20,"= rejection",fill=MUTE)
pages.append(page("rex_03_pinbar","REX TRADING SIGNAL &middot; CANDLE PATTERNS","Rejection candle","The Pin Bar",s))

# ---------- 4. DOJI ----------
s = '<line x1="450" y1="120" x2="450" y2="470" stroke="%s" stroke-width="6"/>'%INK
s+= '<rect x="405" y="286" width="90" height="18" rx="4" fill="%s"/>'%INK
s+= L(600,295,505,295)+T(612,303,24,"open &#8776; close","start")
s+= T(450,520,26,"The market is undecided",fill=INK)
s+= T(450,552,20,"wait for confirmation before you act",fill=MUTE)
# three mini types
def mini(cx,label,btop,bbot,top,bot):
    g='<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4"/>'%(cx,top,cx,bot,BROWN)
    g+='<rect x="%d" y="%d" width="34" height="%d" rx="3" fill="%s"/>'%(cx-17,btop,max(6,bbot-btop),BROWN)
    g+=T(cx,660,17,label,fill=MUTE)
    return g
s+= mini(210,"STANDARD",600,612,570,640)
s+= mini(450,"GRAVESTONE",632,640,570,640)
s+= mini(690,"DRAGONFLY",570,578,570,640)
pages.append(page("rex_04_doji","REX TRADING SIGNAL &middot; CANDLE PATTERNS","Indecision","The Doji",s,vbh=680))

# ---------- 5. ANATOMY OF A TRADE ----------
s = '<rect x="150" y="150" width="470" height="150" fill="%s"/>'%GTR
s+= '<rect x="150" y="360" width="470" height="150" fill="%s"/>'%RTR
for y,txt,col,sub in [(150,"TAKE PROFIT",GREEN,"your target"),(360,"ENTRY",GOLD,"where you buy"),(510,"STOP LOSS",RED,"what you risk")]:
    s+='<line x1="150" y1="%d" x2="620" y2="%d" stroke="%s" stroke-width="5" stroke-dasharray="%s"/>'%(y,y,col,("1 0" if txt=="ENTRY" else "12 8"))
    s+=T(650,y-4,26,txt,"start",900,col)+T(650,y+22,18,sub,"start",700,MUTE)
# entry candle/arrow (a buy)
s+= '<path d="M300 360 L300 175" stroke="%s" stroke-width="5" marker-end="url(#arG)"/>'%GREEN
s+= T(240,235,22,"REWARD",fill=GREEN)
s+= '<path d="M410 360 L410 495" stroke="%s" stroke-width="5" marker-end="url(#arR)"/>'%RED
s+= T(470,445,22,"RISK",fill=RED)
pages.append(page("rex_05_trade","REX TRADING SIGNAL &middot; RISK MANAGEMENT","Every trade has three lines","Anatomy of a Trade",s,l2size=64,vbh=600))

# ---------- 6. RISK : REWARD ----------
base=560
s = '<rect x="220" y="%d" width="150" height="120" rx="8" fill="%s"/>'%(base-120,RED)
s+= T(295,base+42,26,"RISK",fill=RED)+T(295,base-140,30,"1R",fill=RED)+T(295,base-40,22,"$20","middle",800,"#fff")
s+= '<rect x="560" y="%d" width="150" height="360" rx="8" fill="%s"/>'%(base-360,GREEN)
s+= T(635,base+42,26,"REWARD",fill=GREEN)+T(635,base-380,30,"3R",fill=GREEN)+T(635,base-160,22,"$60","middle",800,"#fff")
s+= T(465,base-190,64,"1:3",fill=GOLD)
s+= T(450,base+110,22,"Risk $20 to make $60 &mdash; be wrong 6 of 10 and still grow.",fill=BROWN)
pages.append(page("rex_06_rr","REX TRADING SIGNAL &middot; RISK MANAGEMENT","Win small, lose smaller","Risk : Reward",s,vbh=720))

# ---------- 7. POSITION SIZING ----------
s = '<rect x="150" y="120" width="600" height="120" rx="14" fill="#fff" stroke="%s" stroke-width="3"/>'%("rgba(22,19,15,.18)")
s+= T(450,178,30,"LOT SIZE",fill=INK,w=900)
s+= T(450,222,24,"= Risk ($)  &#247;  Stop distance",fill=BROWN)
# two examples
s+= candle(280,330,560,410,470,GREEN,70)
s+= '<line x1="180" y1="470" x2="380" y2="470" stroke="%s" stroke-width="3" stroke-dasharray="10 7"/>'%RED
s+= T(280,610,22,"TIGHT stop",fill=INK)+T(280,640,19,"&#8594; bigger size",fill=GREEN)
s+= candle(650,300,600,410,540,RED,70)
s+= '<line x1="550" y1="540" x2="750" y2="540" stroke="%s" stroke-width="3" stroke-dasharray="10 7"/>'%RED
s+= T(650,610,22,"WIDE stop",fill=INK)+T(650,640,19,"&#8594; smaller size",fill=RED)
s+= T(450,420,20,"same $",fill=MUTE)+T(450,446,20,"risk",fill=MUTE)
pages.append(page("rex_07_sizing","REX TRADING SIGNAL &middot; RISK MANAGEMENT","One division, not a headache","Position Sizing",s,vbh=680))

# ---------- 8. RISK CEILING ----------
steps=[("MONTH","-6%",180,760),("WEEK","-3%",300,600),("DAY","-1.5%",420,440),("PER TRADE","-0.5%",540,280)]
s=""
cx=450
for i,(lab,val,y,w) in enumerate(steps):
    s+='<rect x="%d" y="%d" width="%d" height="70" rx="10" fill="%s"/>'%(cx-w//2,y,w,GDTR if i%2 else "rgba(214,38,44,.10)")
    s+='<rect x="%d" y="%d" width="%d" height="70" rx="10" fill="none" stroke="%s" stroke-width="2.5"/>'%(cx-w//2,y,w,GOLD)
    s+=T(cx-w//2+26,y+45,26,lab,"start",900,INK)
    s+=T(cx+w//2-26,y+45,26,val,"end",900,RED)
    if i<len(steps)-1:
        s+='<path d="M450 %d L450 %d" stroke="%s" stroke-width="4" marker-end="url(#ar)"/>'%(y+72,y+108,BROWN)
s+=T(450,660,20,"Set the ceiling while you're calm. Cascade it down. Never breach it.",fill=BROWN)
pages.append(page("rex_08_ceiling","REX TRADING SIGNAL &middot; RISK MANAGEMENT","Decide it while you're calm","The Risk Ceiling",s,vbh=700))

# ---------- 9. SUPPORT & RESISTANCE ----------
s = '<line x1="120" y1="140" x2="780" y2="140" stroke="%s" stroke-width="5" stroke-dasharray="12 8"/>'%RED
s+= T(120,120,24,"RESISTANCE &mdash; the ceiling","start",800,RED)
# price zigzag between 140 and 500
poly="120,470 230,150 340,480 470,150 600,485 720,150"
s+= '<polyline points="%s" fill="none" stroke="%s" stroke-width="6" stroke-linejoin="round"/>'%(poly, INK)
s+= L(230,210,230,165,"arR",RED,4)+L(470,210,470,165,"arR",RED,4)
s+= L(340,420,340,470,"arG",GREEN,4)+L(600,425,600,478,"arG",GREEN,4)
s+= '<line x1="120" y1="500" x2="780" y2="500" stroke="%s" stroke-width="5" stroke-dasharray="12 8"/>'%GREEN
s+= T(120,540,24,"SUPPORT &mdash; the floor","start",800,GREEN)
pages.append(page("rex_09_sr","REX TRADING SIGNAL &middot; MARKET STRUCTURE","The floor and the ceiling","Support &amp; Resistance",s,vbh=600))

# ---------- 10. READING THE TREND ----------
def dot(x,y,c): return '<circle cx="%d" cy="%d" r="8" fill="%s"/>'%(x,y,c)
# UPTREND: clean rising staircase of higher highs + higher lows
up=[(100,470),(170,330),(235,405),(305,255),(370,325),(430,175)]
s = T(262,74,28,"UPTREND",fill=GREEN)
s+= '<polyline points="%s" fill="none" stroke="%s" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'%(" ".join("%d,%d"%p for p in up),GREEN)
for x,y in up: s+=dot(x,y,GREEN)
s+= T(305,238,20,"HH",fill=GREEN)+T(430,158,20,"HH",fill=GREEN)
s+= T(235,440,20,"HL",fill=GREEN)+T(370,360,20,"HL",fill=GREEN)
s+= T(262,600,22,"higher highs + higher lows",fill=BROWN)
s+= '<line x1="460" y1="130" x2="460" y2="560" stroke="rgba(22,19,15,.18)" stroke-width="2" stroke-dasharray="7 8"/>'
# DOWNTREND: clean falling staircase of lower highs + lower lows
dn=[(500,175),(560,320),(625,250),(690,400),(750,330),(810,470)]
s+= T(672,74,28,"DOWNTREND",fill=RED)
s+= '<polyline points="%s" fill="none" stroke="%s" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'%(" ".join("%d,%d"%p for p in dn),RED)
for x,y in dn: s+=dot(x,y,RED)
s+= T(625,234,20,"LH",fill=RED)+T(750,314,20,"LH",fill=RED)
s+= T(690,440,20,"LL",fill=RED)+T(810,508,20,"LL",fill=RED)
s+= T(672,600,22,"lower highs + lower lows",fill=BROWN)
pages.append(page("rex_10_trend","REX TRADING SIGNAL &middot; MARKET STRUCTURE","Structure over noise","Reading the Trend",s,vbh=640))

# ---------- 11. BREAK OF STRUCTURE ----------
# uptrend makes HH & HL, then price closes below the last higher low -> BOS
HLY=372
# dashed 'last higher low' level
s = '<line x1="95" y1="%d" x2="645" y2="%d" stroke="%s" stroke-width="3" stroke-dasharray="11 8"/>'%(HLY,HLY,GOLD)
s+= T(280,406,20,"last higher low","middle",800,GOLD)
# green structure: start low -> HH -> HL(on line) -> higher HH -> falling to the break level
s+= '<polyline points="120,430 205,300 280,372 370,240 479,372" fill="none" stroke="%s" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'%GREEN
# red leg after breaking below the last higher low
s+= '<polyline points="479,372 560,470" fill="none" stroke="%s" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" marker-end="url(#arR)"/>'%RED
# swing dots + labels
s+= dot(205,300,GREEN)+T(205,282,20,"HH",fill=GREEN)
s+= dot(370,240,GREEN)+T(370,222,20,"HH",fill=GREEN)
s+= dot(280,372,GOLD)
# break marker
s+= '<circle cx="479" cy="372" r="17" fill="none" stroke="%s" stroke-width="4"/>'%RED
s+= T(600,364,28,"BOS","start",900,RED)
s+= T(600,394,19,"break of structure","start",700,BROWN)
s+= T(450,600,20,"Price closes below the last higher low &#8594; the trend shifts.",fill=BROWN)
pages.append(page("rex_11_bos","REX TRADING SIGNAL &middot; MARKET STRUCTURE","When the trend cracks","Break of Structure",s,vbh=640))

# ---------- 12. THE 3 RULES ----------
rules=[("01","Every signal has a stop loss","you decide what you'll lose before profit"),
       ("02","I post my losses","the whole notebook, not the highlight reel"),
       ("03","I never promise profit","not guaranteed, not fixed, not risk-free")]
s=""
for i,(n,t,sub) in enumerate(rules):
    y=90+i*185
    s+='<rect x="80" y="%d" width="740" height="150" rx="18" fill="#fff" stroke="rgba(22,19,15,.14)" stroke-width="2"/>'%y
    s+='<rect x="80" y="%d" width="12" height="150" rx="6" fill="%s"/>'%(y,RED if i==2 else (GREEN if i==0 else GOLD))
    s+=T(150,y+95,60,n,"start",900,GOLD)
    s+=T(255,y+62,30,t,"start",900,INK)
    s+=T(255,y+104,21,sub,"start",700,BROWN)
pages.append(page("rex_12_rules","REX TRADING SIGNAL &middot; THE HOUSE RULES","What this channel is built on","The 3 Rules",s,tag="",vbw=900,vbh=650))

# strip accidental bad token
print("Generated", len(pages), "pages")
for p in pages: print(os.path.basename(p))
