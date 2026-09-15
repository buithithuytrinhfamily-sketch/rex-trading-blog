(function () {
 'use strict';
 const common={colorTheme:'light',locale:'en',width:'100%',height:'100%',isTransparent:false};
 const definitions={
  'crypto-heatmap':['crypto-coins-heatmap',{...common,dataSource:'Crypto',blockSize:'market_cap_calc',blockColor:'change',locale:'en',hasTopBar:true,isDataSetEnabled:true,isZoomEnabled:true,hasSymbolTooltip:true}],
  calendar:['events',{...common,importanceFilter:'-1,0,1',countryFilter:'us,eu,gb,jp,au,ca,ch,nz,cn'}],
  news:['timeline',{...common,feedMode:'all_symbols',displayMode:'regular'}],
  'gold-chart':['advanced-chart',{...common,autosize:true,symbol:'OANDA:XAUUSD',interval:'D',timezone:'Etc/UTC',theme:'light',style:'1',allow_symbol_change:true,calendar:false,hide_side_toolbar:false,support_host:'https://www.tradingview.com'}],
  overview:['market-overview',{...common,dateRange:'12M',showChart:true,showSymbolLogo:true,showFloatingTooltip:true,plotLineColorGrowing:'rgba(21,115,73,1)',plotLineColorFalling:'rgba(179,27,40,1)',tabs:[{title:'Gold & FX',symbols:[{s:'OANDA:XAUUSD',d:'Gold / US Dollar'},{s:'FX:EURUSD',d:'Euro / US Dollar'},{s:'FX:GBPUSD',d:'British Pound / US Dollar'},{s:'FX:USDJPY',d:'US Dollar / Yen'}]},{title:'Global markets',symbols:[{s:'FOREXCOM:SPXUSD',d:'S&P 500'},{s:'TVC:US10Y',d:'US 10-year yield'},{s:'TVC:DXY',d:'US Dollar Index'},{s:'BITSTAMP:BTCUSD',d:'Bitcoin / USD'}]}]}],
  crypto:['screener',{...common,defaultColumn:'overview',screener_type:'crypto_mkt',displayCurrency:'USD'}],
  'crypto-volatility':['screener',{...common,defaultColumn:'performance',defaultScreen:'general',market:'crypto',showToolbar:true}]
 };
 document.querySelectorAll('[data-tv]').forEach(container=>{
  const def=definitions[container.dataset.tv];if(!def)return;
  const script=document.createElement('script');script.src='https://s3.tradingview.com/external-embedding/embed-widget-'+def[0]+'.js';script.async=true;script.textContent=JSON.stringify(def[1]);
  script.onerror=()=>{const box=container.querySelector('.tradingview-widget-container__widget');box.textContent='The external display could not load. Use the provider link below.';box.style.padding='25px';};container.append(script);
 });
})();
