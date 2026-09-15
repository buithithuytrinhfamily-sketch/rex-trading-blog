#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlparse,unquote
import json,re,subprocess,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=[];self.refs=[];self.h1=0;self.main=0;self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t=='h1':self.h1+=1
  if t=='main':self.main+=1
  if t in ['a','img','script','link','source','video']:
   self.refs.extend(a[k] for k in ['href','src','poster'] if a.get(k))
cache={}
def parsed(p):
 if p not in cache:cache[p]=Page(p.read_text())
 return cache[p]
routes=json.loads((ROOT/'content/portal-routes.json').read_text());errors=[]
for route in routes:
 p=ROOT/route.strip('/')/'index.html';doc=parsed(p)
 if doc.h1!=1 or doc.main!=1:errors.append(str(p)+' heading/main mismatch')
 if len(doc.ids)!=len(set(doc.ids)):errors.append(str(p)+' duplicate IDs')
 if 'https://rextradingsignal.com'+route not in p.read_text():errors.append(route+' canonical missing')
 for ref in doc.refs:
  u=urlparse(urljoin('https://rextradingsignal.com'+route,ref))
  if u.netloc!='rextradingsignal.com':continue
  target=ROOT/unquote(u.path).lstrip('/');target=target/'index.html' if target.is_dir() else target
  if not target.exists():errors.append(route+' missing '+ref)
  elif u.fragment and target.suffix=='.html' and unquote(u.fragment) not in parsed(target).ids:errors.append(route+' missing fragment '+ref)
for p in (ROOT/'assets').glob('portal*.js'):subprocess.run(['node','--check',str(p)],check=True)
ET.fromstring((ROOT/'sitemap.xml').read_text())
for p in (ROOT/'content').glob('*.json'):json.loads(p.read_text())
assert not errors,'\n'.join(errors)
print('PASS:',len(routes),'routes, local references, fragments, IDs, canonical URLs, script syntax, JSON and sitemap.')
