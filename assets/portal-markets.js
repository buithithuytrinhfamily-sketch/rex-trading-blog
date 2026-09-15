(function () {
 'use strict';
 const root=document.querySelector('[data-market]');if(!root)return;
 const math=window.RexMath,output=root.querySelector('[data-market-output]'),status=root.querySelector('.market-status'),button=root.querySelector('[data-refresh]');
 const currencies=['USD','EUR','GBP','JPY','CHF','CAD','AUD','NZD'];
 const pairs=[['EUR','USD'],['GBP','USD'],['USD','JPY'],['USD','CHF'],['USD','CAD'],['AUD','USD'],['NZD','USD'],['EUR','JPY'],['GBP','JPY'],['AUD','JPY'],['EUR','GBP']];
 const fmt=(n,d=4)=>new Intl.NumberFormat('en-US',{maximumFractionDigits:d,minimumFractionDigits:Math.min(d,2)}).format(n);
 function cell(text,tag='td'){const c=document.createElement(tag);c.textContent=text;return c;}
 function table(headers){const t=document.createElement('table');t.className='portal-table';const head=document.createElement('thead'),tr=document.createElement('tr');headers.forEach(h=>tr.append(cell(h,'th')));head.append(tr);t.append(head);const body=document.createElement('tbody');t.append(body);output.replaceChildren(t);return body;}
 function signed(n){const c=cell((n>0?'+':'')+fmt(n,2)+'%');c.className=n>0?'up':n<0?'down':'neutral';return c;}
 async function get(url){const response=await fetch(url,{signal:AbortSignal.timeout(18000)});if(!response.ok)throw new Error('Provider unavailable');return response.json();}
 async function data(force){
  const key='rex-daily-fx-v1';if(!force)try{const stored=JSON.parse(sessionStorage.getItem(key));if(stored&&Date.now()-stored.saved<600000&&stored.rows.length>2)return stored;}catch(_e){}
  const latest=await get('https://api.frankfurter.dev/v1/latest?base=USD&symbols=EUR,GBP,JPY,CHF,CAD,AUD,NZD');
  if(!/^\d{4}-\d{2}-\d{2}$/.test(latest.date))throw new Error('Invalid effective date');
  const start=new Date(latest.date+'T12:00:00Z');start.setUTCDate(start.getUTCDate()-50);
  const raw=await get('https://api.frankfurter.dev/v1/'+start.toISOString().slice(0,10)+'..'+latest.date+'?base=USD&symbols=EUR,GBP,JPY,CHF,CAD,AUD,NZD');
  if(!raw.rates||typeof raw.rates!=='object')throw new Error('Invalid rates');
  const rows=Object.entries(raw.rates).sort(([a],[b])=>a.localeCompare(b)).map(([date,rates])=>({date,rates:{...rates,USD:1}})).filter(row=>currencies.every(c=>Number.isFinite(row.rates[c])&&row.rates[c]>0)).slice(-31);
  if(rows.length<4)throw new Error('Insufficient data');
  const result={saved:Date.now(),rows};try{sessionStorage.setItem(key,JSON.stringify(result));}catch(_e){}return result;
 }
 async function render(force=false){button.disabled=true;status.className='market-status';status.textContent='Loading daily reference data…';output.replaceChildren();
  try{
   const {rows}=await data(force);const last=rows.at(-1),prev=rows.at(-2);const quote=(r,a,b)=>r.rates[b]/r.rates[a];
   const stats=pairs.map(([a,b])=>{const prices=rows.map(r=>quote(r,a,b)),rs=math.returns(prices);return {name:a+'/'+b,rate:prices.at(-1),change:(prices.at(-1)/prices.at(-2)-1)*100,vol:math.stdev(rs)*100,returns:rs};});
   const kind=root.dataset.market;
   if(kind==='currency-strength'){
    const body=table(['Rank','Currency','Mean change vs basket']);
    const ranks=currencies.map(a=>({a,change:math.mean(currencies.filter(b=>b!==a).map(b=>(quote(last,a,b)/quote(prev,a,b)-1)*100))})).sort((a,b)=>b.change-a.change);
    ranks.forEach((r,i)=>{const tr=document.createElement('tr');tr.append(cell(String(i+1)),cell(r.a),signed(r.change));body.append(tr);});
   }else if(kind==='heatmap'){
    const body=table(['Base / quote',...currencies]);currencies.forEach(a=>{const tr=document.createElement('tr');tr.append(cell(a,'th'));currencies.forEach(b=>{const c=a===b?cell('—'):signed((quote(last,a,b)/quote(prev,a,b)-1)*100);if(a!==b){const change=(quote(last,a,b)/quote(prev,a,b)-1);c.style.background=change>0?'#edf8f1':change<0?'#fff0f0':'#f6f8fa';}tr.append(c);});body.append(tr);});
   }else if(kind==='correlation'){
    const sample=stats.slice(0,7);const body=table(['Pair',...sample.map(p=>p.name)]);sample.forEach(a=>{const tr=document.createElement('tr');tr.append(cell(a.name,'th'));sample.forEach(b=>{try{const r=math.correlation(a.returns,b.returns);const c=cell(fmt(r,2));c.className=r>.3?'up':r<-.3?'down':'neutral';tr.append(c);}catch(_e){tr.append(cell('Undefined'));}});body.append(tr);});
   }else{
    const ranked=[...stats];if(kind==='volatility')ranked.sort((a,b)=>b.vol-a.vol);if(kind==='movers')ranked.sort((a,b)=>b.change-a.change);
    const body=table(['Pair','Reference rate','One-day change','Daily volatility']);ranked.forEach(r=>{const tr=document.createElement('tr');tr.append(cell(r.name,'th'),cell(fmt(r.rate,5)),signed(r.change),cell(fmt(r.vol,3)+'%'));body.append(tr);});
   }
   status.textContent='Effective '+last.date+' · change from '+prev.date+' · '+(rows.length-1)+' aligned daily returns from '+rows[0].date+'. Source: Frankfurter reference rates. Updated view '+new Date().toLocaleTimeString()+'.';
  }catch(_e){status.className='market-status error';status.textContent='Daily reference data is unavailable. No substitute prices are shown. Try Refresh data later.';const p=document.createElement('p');const a=document.createElement('a');a.href='https://frankfurter.dev/';a.textContent='Open the data provider';p.append(a);output.replaceChildren(p);}
  finally{button.disabled=false;}
 }
 button.addEventListener('click',()=>render(true));render();
})();
