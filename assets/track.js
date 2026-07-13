/* REX site event tracking — GA4 (G-WL6P2VP6P9). Loaded on every page. */
(function(){
  function send(name, params){
    if (typeof gtag === 'function') gtag('event', name, params || {});
  }
  var page = location.pathname;

  document.addEventListener('click', function(e){
    var t = e.target;

    // copy-to-clipboard buttons (wallet addresses on the kit page)
    var copyBtn = t.closest ? t.closest('[data-copy]') : null;
    if (copyBtn){
      var txt = copyBtn.getAttribute('data-copy');
      if (navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(txt);
      } else {
        var ta = document.createElement('textarea');
        ta.value = txt; document.body.appendChild(ta);
        ta.select(); try{ document.execCommand('copy'); }catch(err){}
        document.body.removeChild(ta);
      }
      var old = copyBtn.textContent;
      copyBtn.classList.add('copied');
      copyBtn.textContent = 'Copied ✓';
      setTimeout(function(){ copyBtn.classList.remove('copied'); copyBtn.textContent = old; }, 1600);
      send('wallet_copy', { wallet: copyBtn.getAttribute('data-coin') || '', page: page });
      return;
    }

    var a = t.closest ? t.closest('a') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    var text = (a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80);

    if (href.indexOf('/business-plan') !== -1){
      send('cta_gift_click', { link_text: text, page: page });
    } else if (href.indexOf('#pay') !== -1){
      send('cta_pay_view', { link_text: text, page: page });
    } else if (href.indexOf('Rextrading_gold') !== -1){
      send('receipt_dm_click', { link_text: text, tier: a.getAttribute('data-tier') || '', page: page });
    } else if (href.indexOf('t.me/') !== -1){
      send('telegram_click', { link_url: href, link_text: text, page: page });
    } else if (href.indexOf('kit.html') !== -1){
      send('cta_kit_click', { link_text: text, page: page });
    } else if (href.indexOf('REX-Traders-Business-Plan.pdf') !== -1){
      send('gift_pdf_download', { page: page });
    }
  }, true);

  // member review videos
  var vids = document.querySelectorAll('#reviews video');
  Array.prototype.forEach.call(vids, function(v){
    var fired = {};
    function vname(){ return (v.currentSrc || v.getAttribute('poster') || '').split('/').pop(); }
    v.addEventListener('play', function(){
      if (fired.play) return; fired.play = 1;
      send('review_video_play', { video: vname(), page: page });
    });
    v.addEventListener('ended', function(){
      if (fired.end) return; fired.end = 1;
      send('review_video_complete', { video: vname(), page: page });
    });
  });

  // opt-in form submit (GetResponse embedded form on /business-plan/)
  document.addEventListener('submit', function(){
    send('lead_form_submit', { page: page });
  }, true);
})();
