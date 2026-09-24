"""Build homepage carousel and curated paths without modifying daily article cards."""
from pathlib import Path
import json,re,html,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
courses=json.loads((R/'content/courses.json').read_text())
fx=courses['forex']
gold_ids=['intermarket-and-sentiment','candlesticks-and-charts','support-resistance','economic-news','how-to-manage-risk-in-gold-trading','position-sizing-for-gold-trading','how-to-take-profit-like-a-business','trading-journal-template','graduation-checklist']
exclude=set(gold_ids)|{'how-to-get-funded-by-a-prop-firm','what-happens-if-you-fail-a-prop-firm-challenge'}
forex=[x for x in fx if x['id'] not in exclude]
assert len(forex)==33
byid={x['id']:x for x in fx}
gold=[byid[x] for x in gold_ids]
paths=[('/learn/forex-33/','Học Forex','33 bài',forex),('/learn/gold/','Học vàng','9 bài',gold)]
template=(R/'learn/forex/index.html').read_text()
for url,title,count,entries in paths:
 body='<main id="main" class="portal-shell portal-main" lang="vi"><p class="portal-eyebrow">REX LEARNING PATH</p><h1 class="portal-title">'+title+'</h1><p class="portal-intro">Lộ trình '+count+' — đọc lần lượt và đánh dấu bài đã hoàn thành. Nội dung bài học bằng tiếng Anh.</p><div class="portal-note">Tiến độ được lưu trên thiết bị này. <a href="/my-learning/">Xem tiến độ học</a>.</div><ol class="banner-lessons">'
 for x in entries:body+='<li><a href="'+html.escape(x['url'])+'">'+html.escape(x['title'])+'</a><input type="checkbox" data-complete="'+x['id']+'" aria-label="Đã học: '+html.escape(x['title'],quote=True)+'"></li>'
 body+='</ol><a class="rex-button" href="/learn/forex/">Xem toàn bộ thư viện Forex và vàng →</a></main>'
 out=re.sub(r'<main\b.*?</main>',lambda m:body,template,flags=re.S)
 out=re.sub(r'<title>.*?</title>','<title>'+title+' · '+count+' | REX Trading Signal</title>',out)
 out=out.replace('https://rextradingsignal.com/learn/forex/','https://rextradingsignal.com'+url)
 out=re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*',lambda m:m[1]+title+' — lộ trình '+count,out)
 out=re.sub(r'(<meta property="og:title" content=")[^"]*',lambda m:m[1]+title+' · '+count+' | REX Trading Signal',out)
 out=out.replace('</head>','<link rel="stylesheet" href="/assets/home-banner.css"></head>')
 target=R/url.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(out)
slides=[('Học Forex','33 bài học. Một lộ trình rõ ràng.','Từ cách đọc cặp tiền đến xây dựng quy trình giao dịch có kỷ luật.','/learn/forex-33/','Bắt đầu học Forex','33','BÀI HỌC'),('Nhận sách','Open For Business.','Chọn gói Trader’s Business Kit phù hợp và tiếp tục đến phần thanh toán.','/kit.html#pay','Chọn gói và thanh toán','REX','TRADER’S BUSINESS KIT'),('Học vàng','9 bài học dành cho vàng.','Hiểu thị trường, quản lý rủi ro và xác định khối lượng trước mỗi giao dịch.','/learn/gold/','Bắt đầu học vàng','09','BÀI HỌC')]
banner='<section class="rex-carousel" aria-label="Lộ trình học và sách" aria-roledescription="carousel" lang="vi"><div class="rex-slides">'
for i,(name,title,desc,url,cta,num,caption) in enumerate(slides):
 banner+=f'<article class="rex-slide rex-slide-{i}" data-slide="{i}" role="group" aria-roledescription="slide" aria-label="{i+1} / 3: {name}"'+(' hidden' if i else '')+f'><div><p class="rex-slide-label">{name}</p><h2>{title}</h2><p>{desc}</p><a class="rex-slide-cta" href="{url}">{cta} <span aria-hidden="true">→</span></a></div><div class="rex-slide-art" aria-hidden="true"><strong>{num}</strong><span>{caption}</span></div></article>'
banner+='</div><div class="rex-slide-controls"><div class="rex-slide-choices">'+''.join(f'<button type="button" data-slide-to="{i}" aria-label="Xem slide {name}" aria-pressed="'+('true' if i==0 else 'false')+f'">{name}</button>' for i,(name,*_) in enumerate(slides))+'</div><button type="button" class="rex-slide-pause" aria-label="Tạm dừng chuyển slide">Tạm dừng</button></div></section>'
p=R/'index.html';s=p.read_text()
if '<section class="rex-carousel"' in s:s=re.sub(r'<section class="rex-carousel".*?</section>',lambda m:banner,s,count=1,flags=re.S)
else:s=re.sub(r'<div class="path-grid">.*?</a></div>',lambda m:banner,s,count=1,flags=re.S)
if '/assets/home-banner.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/assets/home-banner.css"></head>')
if '/assets/home-banner.js' not in s:s=s.replace('</body>','<script defer src="/assets/home-banner.js"></script></body>')
p.write_text(s)
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
p=R/'sitemap.xml';tree=ET.parse(p);root=tree.getroot();existing={x.text for x in root.findall('{'+ns+'}url/{'+ns+'}loc')}
for url,*_ in paths:
 full='https://rextradingsignal.com'+url
 if full not in existing:ET.SubElement(ET.SubElement(root,'{'+ns+'}url'),'{'+ns+'}loc').text=full
# Preserve current sitemap formatting and metadata when appending new locations.
s=p.read_text();s=s.replace('</urlset>',''.join('<url><loc>https://rextradingsignal.com'+url+'</loc></url>\n' for url,*_ in paths if 'https://rextradingsignal.com'+url not in existing)+'</urlset>');p.write_text(s)
print('Built 3 banner slides and learning paths: Forex 33, Gold 9.')
