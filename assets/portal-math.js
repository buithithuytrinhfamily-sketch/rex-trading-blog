/* Pure calculations, shared by the browser and regression tests. */
(function (root, factory) {
  const math = factory();
  if (typeof module === 'object' && module.exports) module.exports = math;
  else root.RexMath = math;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function number(n, label, zero = false) {
    n = Number(n);
    if (!Number.isFinite(n) || (zero ? n < 0 : n <= 0)) throw new Error(label + (zero ? ' must be zero or greater.' : ' must be greater than zero.'));
    return n;
  }
  function position(equity, riskPercent, distance, contract, rate, step, costs) {
    equity=number(equity,'Equity'); riskPercent=number(riskPercent,'Risk percentage');
    if(riskPercent>100) throw new Error('Risk percentage must not exceed 100.');
    distance=number(distance,'Stop distance'); contract=number(contract,'Contract size');rate=number(rate,'Conversion rate');step=number(step,'Lot step');costs=number(costs,'Costs per lot',true);
    const budget=equity*riskPercent/100, perLot=distance*contract*rate+costs;
    const lots=Math.floor((budget/perLot+Number.EPSILON)/step)*step;
    return {budget, lots:Number(lots.toFixed(8)), plannedLoss:lots*perLot, units:lots*contract};
  }
  function pip(pipSize, units, lots, rate) { return number(pipSize,'Pip size')*number(units,'Units per lot')*number(lots,'Lots')*number(rate,'Conversion rate'); }
  function gain(start,end) { start=number(start,'Starting equity');end=number(end,'Ending equity',true);return {change:end-start,percent:(end/start-1)*100,recovery:end===0?null:end<start?(start/end-1)*100:0}; }
  function pivot(high,low,close,method='classic',open=close) {
    high=number(high,'High');low=number(low,'Low');close=number(close,'Close');open=number(open,'Open');
    if(high<low||close>high||close<low||open>high||open<low)throw new Error('Open and close must be between the low and high.');
    const range=high-low;let p=(high+low+close)/3;
    if(method==='woodie')p=(high+low+2*close)/4;
    if(method==='fibonacci')return {P:p,R1:p+.382*range,R2:p+.618*range,R3:p+range,S1:p-.382*range,S2:p-.618*range,S3:p-range};
    if(method==='camarilla')return {P:p,R1:close+range*1.1/12,R2:close+range*1.1/6,R3:close+range*1.1/4,R4:close+range*1.1/2,S1:close-range*1.1/12,S2:close-range*1.1/6,S3:close-range*1.1/4,S4:close-range*1.1/2};
    if(method==='demark'){const x=close<open?high+2*low+close:close>open?2*high+low+close:high+low+2*close;return {P:x/4,R1:x/2-low,S1:x/2-high};}
    return {P:p,R1:2*p-low,R2:p+range,R3:high+2*(p-low),S1:2*p-high,S2:p-range,S3:low-2*(high-p)};
  }
  function reward(entry,stop,target,side) {
    entry=number(entry,'Entry');stop=number(stop,'Stop');target=number(target,'Target');
    if(side==='long'?!(stop<entry&&target>entry):!(stop>entry&&target<entry))throw new Error('For a long trade: stop < entry < target. For a short trade: target < entry < stop.');
    return {risk:Math.abs(entry-stop),reward:Math.abs(target-entry),ratio:Math.abs(target-entry)/Math.abs(entry-stop)};
  }
  function returns(prices) { if(prices.length<2||prices.some(p=>!Number.isFinite(p)||p<=0))throw new Error('Provide at least two positive prices.');return prices.slice(1).map((p,i)=>p/prices[i]-1); }
  function mean(a){return a.reduce((s,x)=>s+x,0)/a.length;}
  function stdev(a){if(a.length<2)throw new Error('At least two returns are required.');const m=mean(a);return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/(a.length-1));}
  function correlation(a,b){if(a.length!==b.length||a.length<3)throw new Error('Use the same dates and at least four prices in each series.');const ma=mean(a),mb=mean(b);let cross=0,va=0,vb=0;a.forEach((x,i)=>{cross+=(x-ma)*(b[i]-mb);va+=(x-ma)**2;vb+=(b[i]-mb)**2;});if(!va||!vb)throw new Error('Correlation is undefined for a series with no variation.');return Math.max(-1,Math.min(1,cross/Math.sqrt(va*vb)));}
  return {number,position,pip,gain,pivot,reward,returns,mean,stdev,correlation};
});
