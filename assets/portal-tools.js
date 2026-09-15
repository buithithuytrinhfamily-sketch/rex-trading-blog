(function () {
 'use strict';
 const math=window.RexMath;
 const format=(n,d=5)=>{if(!Number.isFinite(n))throw new Error('These inputs exceed the supported numerical range.');return new Intl.NumberFormat('en-US',{maximumFractionDigits:d}).format(n);};
 const form=document.querySelector('[data-calculator]');
 if(form)form.addEventListener('submit',async event=>{
  event.preventDefault();const output=document.getElementById('tool-result'),button=form.querySelector('button[type=submit]');
  const value=n=>form.elements.namedItem(n).value;
  const n=name=>{const raw=value(name).trim();if(!raw)throw new Error('Fill in every input.');const x=Number(raw);if(!Number.isFinite(x))throw new Error('All numeric inputs must be finite numbers.');return x;};
  output.className='tool-result';button.disabled=true;
  try{
   let title='',detail='';const kind=form.dataset.calculator;
   if(kind==='position-size'){const r=math.position(n('equity'),n('risk'),n('distance'),n('contract'),n('rate'),n('step'),n('costs'));title=format(r.lots,8)+' lots';detail='Risk budget: '+format(r.budget,2)+'. Planned loss including entered costs: '+format(r.plannedLoss,2)+'. Base units: '+format(r.units,4)+'.'+(r.lots===0?' The budget is below one lot step; do not round up.':' Rounded down to the entered lot step.');}
   if(kind==='pip-value'){title=format(math.pip(n('pip'),n('units'),n('lots'),n('rate')),6)+' per pip';detail='In your account currency, using the conversion rate and contract size entered.';}
   if(kind==='gain-loss'){const r=math.gain(n('start'),n('end'));title=format(r.percent,2)+'% change';detail='Cash change: '+format(r.change,2)+'. '+(r.recovery===null?'The ending balance is zero; no percentage gain on zero capital can recover it.':r.recovery>0?'Gain needed to recover: '+format(r.recovery,2)+'%.':'No recovery is needed to reach the starting equity.');}
   if(kind==='pivot-points'){const r=math.pivot(n('high'),n('low'),n('close'),value('method'),n('open'));output.replaceChildren();const h=document.createElement('h2');h.textContent='Calculated reference levels';output.append(h);const table=document.createElement('table');Object.entries(r).forEach(([key,val])=>{const row=document.createElement('tr'),th=document.createElement('th'),td=document.createElement('td');th.textContent=key;td.textContent=format(val);row.append(th,td);table.append(row);});output.append(table);return;}
   if(kind==='risk-reward'){const r=math.reward(n('entry'),n('stop'),n('target'),value('side'));title='1 : '+format(r.ratio,2);detail='Risk distance: '+format(r.risk)+'. Reward distance: '+format(r.reward)+'. Before fees, spread and slippage.';}
   if(kind==='currency-converter'){
    const amount=math.number(n('amount'),'Amount',true),fee=math.number(n('fee'),'Fee',true);if(fee>100)throw new Error('Fee must be between 0 and 100%.');
    const base=value('base'),quote=value('quote');let rate=1,date='No conversion required';
    if(base!==quote){output.textContent='Fetching the reference rate…';const response=await fetch('https://api.frankfurter.dev/v1/latest?base='+encodeURIComponent(base)+'&symbols='+encodeURIComponent(quote),{signal:AbortSignal.timeout(15000)});if(!response.ok)throw new Error('The rate provider is unavailable. Try again later.');const data=await response.json();rate=math.number(data.rates[quote],'Reference rate');date=data.date;}
    title=format(amount*rate*(1-fee/100),2)+' '+quote;detail='Reference rate: 1 '+base+' = '+format(rate,6)+' '+quote+'. Effective date: '+date+'. Includes the entered '+format(fee,2)+'% fee estimate; other costs excluded.';
   }
   if(kind==='correlation'){
    const parse=s=>s.trim().split(/[\s,;]+/).filter(Boolean).map(x=>{if(!/^[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?$/i.test(x))throw new Error('Use plain numbers separated by commas or whitespace.');return Number(x);});
    const a=math.returns(parse(value('a'))),b=math.returns(parse(value('b')));title=format(math.correlation(a,b),4);detail='Pearson correlation of '+a.length+' aligned period returns. Inputs are assumed to have matching timestamps. Prices are not sent to a server.';
   }
   if(kind==='risk-on-risk-off'){const score=(Math.sign(n('stocks'))-Math.sign(n('vix'))-Math.sign(n('spreads')))/3*100;title=format(score,1)+' / 100';detail=score>0?'More entered observations point toward risk appetite.':score<0?'More entered observations point toward risk aversion.':'Entered observations are mixed or unchanged.';detail+=' Manual equal-weight directional score; not live data or a trade recommendation.';}
   const h=document.createElement('h2');h.textContent='Your result';const strong=document.createElement('strong');strong.textContent=title;const p=document.createElement('p');p.textContent=detail;output.replaceChildren(h,strong,p);
  }catch(error){output.className='tool-result error';output.textContent=error.name==='TimeoutError'?'The data request timed out. Try again later.':error.message||'Could not calculate. Check the inputs and try again.';}
  finally{button.disabled=false;}
 });
 const sessions=document.getElementById('sessions');if(sessions){
  const zones=[['Sydney','Australia/Sydney',8,17],['Tokyo','Asia/Tokyo',9,18],['London','Europe/London',8,17],['New York','America/New_York',8,17]];
  const parsers=new Map();function parts(date,zone){if(!parsers.has(zone))parsers.set(zone,new Intl.DateTimeFormat('en-US',{timeZone:zone,weekday:'short',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}));return Object.fromEntries(parsers.get(zone).formatToParts(date).map(p=>[p.type,p.value]));}
  function forexOpen(date){const p=parts(date,'America/New_York'),h=Number(p.hour)+Number(p.minute)/60;return p.weekday!=='Sat'&&!(p.weekday==='Sun'&&h<17)&&!(p.weekday==='Fri'&&h>=17);}
  const selector=document.getElementById('session-zone');
  function tick(){const now=new Date();const display=selector.value==='local'?Intl.DateTimeFormat().resolvedOptions().timeZone:selector.value;document.getElementById('session-now').textContent=new Intl.DateTimeFormat('en-GB',{dateStyle:'full',timeStyle:'short',timeZone:display}).format(now)+' · '+display+'. FX week: '+(forexOpen(now)?'open':'closed')+'.';sessions.replaceChildren();
   zones.forEach(([name,zone,open,close])=>{const p=parts(now,zone),hour=Number(p.hour)+Number(p.minute)/60;const active=forexOpen(now)&&!['Sat','Sun'].includes(p.weekday)&&hour>=open&&hour<close;
    let start=null,end=null;const base=new Date(Math.floor(now.getTime()/60000)*60000);
    // Session boundaries are whole local hours in these zones; scan hourly.
    const hourBase=new Date(Math.floor(base.getTime()/3600000)*3600000);
    for(let i=-24;i<192;i++){const t=new Date(hourBase.getTime()+i*3600000),v=parts(t,zone);if(Number(v.hour)!==open||Number(v.minute)!==0||['Sat','Sun'].includes(v.weekday)||!forexOpen(t))continue;const finish=new Date(t.getTime()+(close-open)*3600000);if(finish>now){start=t;end=finish;break;}}
    const card=document.createElement('section');card.className='portal-card';const h=document.createElement('h2');h.textContent=name;const clock=document.createElement('p');clock.className='session-clock';clock.textContent=p.hour+':'+p.minute;const status=document.createElement('p');status.className='session-state '+(active?'up':'neutral');status.textContent=active?'Session open':'Session closed';const windowText=document.createElement('p');const fmt=d=>new Intl.DateTimeFormat('en-GB',{weekday:'short',hour:'2-digit',minute:'2-digit',timeZone:display}).format(d);windowText.textContent=start?(active?'Current window: ':'Next window: ')+fmt(start)+' – '+fmt(end)+' ('+display+')':'Next session unavailable.';card.append(h,clock,status,windowText);sessions.append(card);
   });
  }selector.addEventListener('change',tick);tick();setInterval(tick,60000);
 }
})();
