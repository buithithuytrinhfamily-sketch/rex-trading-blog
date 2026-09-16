(function () {
  'use strict';
  const $ = (s, p = document) => p.querySelector(s);
  const $$ = (s, p = document) => Array.from(p.querySelectorAll(s));
  const toggle=$('.portal-menu-toggle'), primary=$('#rex-primary-nav');
  if(toggle&&primary){toggle.hidden=false;$('.portal-header').setAttribute('data-enhanced','');toggle.addEventListener('click',()=>{const open=primary.classList.toggle('is-open');toggle.setAttribute('aria-expanded',String(open));});}
  const menus = $$('.portal-nav details');
  menus.forEach(menu => menu.addEventListener('toggle', () => { if(menu.open) menus.forEach(other => {if(other!==menu)other.open=false;}); }));
  document.addEventListener('click', event => {if(!event.target.closest('.portal-nav'))menus.forEach(m=>m.open=false);});
  document.addEventListener('keydown', event => {if(event.key==='Escape')menus.forEach(m=>{if(m.open){m.open=false;$('summary',m).focus();}});});
  $$('.portal-nav a').forEach(a=>{if(new URL(a.href).pathname===location.pathname)a.setAttribute('aria-current','page');});
  const key='rex-learning-v1';
  let state={version:1,completed:[],scores:{}};
  try{const saved=JSON.parse(localStorage.getItem(key)||'null');if(saved&&saved.version===1&&Array.isArray(saved.completed)&&saved.scores&&typeof saved.scores==='object'){state=saved;}}catch(_e){}
  function save(){try{localStorage.setItem(key,JSON.stringify(state));return true;}catch(_e){return false;}}
  function saveNotice(ok){$$('[data-save-status]').forEach(p=>p.textContent=ok?'Saved in this browser on this device.':'Browser storage is unavailable. This change will last only while the page stays open.');}
  function setComplete(id,checked){const all=new Set(state.completed);checked?all.add(id):all.delete(id);state.completed=Array.from(all);saveNotice(save());updateProgress();}
  let courses=null;
  function updateProgress(){
    $$('[data-complete]').forEach(input=>input.checked=state.completed.includes(input.dataset.complete));
    $$('[data-mark]').forEach(b=>{const done=state.completed.includes(b.dataset.mark);b.textContent=done?'Completed — mark as unread':'Mark lesson complete';b.setAttribute('aria-pressed',String(done));});
    if(courses)Object.entries(courses).forEach(([track,entries])=>{const n=entries.filter(l=>state.completed.includes(l.id)).length;$$('[data-progress="'+track+'"]').forEach(p=>{p.max=entries.length;p.value=n;});$$('[data-progress-label="'+track+'"]').forEach(p=>p.textContent=n+' of '+entries.length+' lessons completed');});
  }
  $$('[data-complete]').forEach(input=>input.addEventListener('change',()=>setComplete(input.dataset.complete,input.checked)));
  $$('[data-mark]').forEach(button=>button.addEventListener('click',()=>setComplete(button.dataset.mark,!state.completed.includes(button.dataset.mark))));
  updateProgress();
  function renderDashboard(){
    const target=$('#learning-dashboard');if(!target||!courses)return;target.replaceChildren();
    const grid=document.createElement('div');grid.className='portal-grid two';
    Object.entries(courses).forEach(([track,entries])=>{
      const box=document.createElement('section');box.className='portal-card';const h=document.createElement('h2');h.textContent=track==='forex'?'Forex & gold':'Crypto';
      const n=entries.filter(l=>state.completed.includes(l.id)).length;const p=document.createElement('p');p.textContent=n+' of '+entries.length+' lessons completed';
      const next=entries.find(l=>!state.completed.includes(l.id));const a=document.createElement('a');a.className='rex-button';a.href=next?next.url:'/learn/'+track+'/';a.textContent=next?'Continue learning':'Review course';box.append(h,p,a);grid.append(box);
    });target.append(grid);
    const h=document.createElement('h2');h.textContent='Your best quiz scores';target.append(h);
    const scores=Object.entries(state.scores);if(!scores.length){const p=document.createElement('p');p.textContent='Complete a quiz to save your first score.';target.append(p);}
    else {const ul=document.createElement('ul');scores.forEach(([slug,s])=>{if(!/^[a-z0-9-]+$/.test(slug))return;const li=document.createElement('li');const a=document.createElement('a');a.href='/quizzes/'+slug+'/';a.textContent=slug.replace(/-/g,' ')+': '+s.correct+' / '+s.total;li.append(a);ul.append(li);});target.append(ul);}
  }
  if($('[data-progress]')||$('#learning-dashboard'))fetch('/content/courses.json').then(r=>{if(!r.ok)throw new Error();return r.json();}).then(data=>{courses=data;updateProgress();renderDashboard();}).catch(()=>{const p=$('#learning-dashboard');if(p)p.textContent='The course list could not load. Your saved progress has not been changed. Reload to try again.';});
  const exportButton=$('#export-progress');if(exportButton)exportButton.addEventListener('click',()=>{
    const blob=new Blob([JSON.stringify(state,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='rex-learning-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$('#progress-message').textContent='Progress backup downloaded. Keep it private if you do not want to share your scores.';
  });
  const importInput=$('#import-progress');if(importInput)importInput.addEventListener('change',async()=>{
    const message=$('#progress-message');try{
      const file=importInput.files[0];if(!file)return;if(file.size>131072)throw new Error('The file is too large for a progress backup.');
      const data=JSON.parse(await file.text());if(!courses)throw new Error('Wait for the course list to load before importing.');
      const ids=new Set(Object.values(courses).flat().map(x=>x.id));
      if(data.version!==1||!Array.isArray(data.completed)||data.completed.some(x=>typeof x!=='string'||!ids.has(x))||!data.scores||typeof data.scores!=='object'||Array.isArray(data.scores))throw new Error('This is not a supported REX progress backup.');
      const allowed=['forex-basics','risk-management','chart-and-system','macro-and-execution','crypto-1','crypto-2','crypto-3','crypto-4'];const scores={};
      for(const [slug,s] of Object.entries(data.scores)){const total=slug.startsWith('crypto-')?4:5;if(!allowed.includes(slug)||!s||!Number.isInteger(s.correct)||s.total!==total||s.correct<0||s.correct>total)throw new Error('The backup contains an invalid quiz score.');scores[slug]={correct:s.correct,total:s.total};}
      state={version:1,completed:Array.from(new Set(data.completed)),scores};const ok=save();updateProgress();renderDashboard();message.textContent=ok?'Backup imported. It replaces progress stored on this device.':'Imported for this page only; browser storage is unavailable.';
    }catch(error){message.textContent=error.message||'Could not import this file. Your saved data has not been changed.';}finally{importInput.value='';}
  });
  const search=$('#glossary-search');if(search){let letter='all';const items=$$('.glossary-item');function filter(){const query=search.value.trim().toLowerCase();let n=0;items.forEach(item=>{const hit=(letter==='all'||item.dataset.letter===letter)&&item.textContent.toLowerCase().includes(query);item.hidden=!hit;if(hit)n++;});$('#glossary-count').textContent=n+' terms';$('#glossary-empty').hidden=n!==0;}
    search.addEventListener('input',filter);$$('button[data-letter]').forEach(button=>button.addEventListener('click',()=>{letter=button.dataset.letter;$$('button[data-letter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));filter();}));}
  const quiz=$('[data-quiz]');if(quiz){
    quiz.addEventListener('submit',async event=>{event.preventDefault();const summary=$('.quiz-summary',quiz),button=$('button[type=submit]',quiz);button.disabled=true;
      try{const response=await fetch('/content/quizzes.json');if(!response.ok)throw new Error();const config=(await response.json())[quiz.dataset.quiz];let correct=0;
        config.forEach((q,i)=>{const answer=$('input[name="q'+i+'"]:checked',quiz);if(!answer)throw new Error('Answer every question first.');const ok=Number(answer.value)===q.correct;if(ok)correct++;const feedback=$('[data-feedback="'+i+'"]',quiz);feedback.hidden=false;feedback.className='quiz-feedback '+(ok?'correct':'incorrect');feedback.textContent=(ok?'Correct. ':'Review this answer. ')+q.explanation;});
        const slug=quiz.dataset.quiz;const previous=state.scores[slug];if(!previous||correct>previous.correct)state.scores[slug]={correct,total:config.length};const saved=save();summary.textContent=correct+' of '+config.length+' correct. '+(saved?'Your best score is saved on this device.':'Storage is unavailable; this score is not saved.');
      }catch(error){summary.textContent=error.message||'Could not load explanations. Please try again.';}finally{button.disabled=false;}
    });quiz.addEventListener('reset',()=>{$$('[data-feedback]',quiz).forEach(x=>x.hidden=true);$('.quiz-summary',quiz).textContent='';});
  }
})();

/* quote strip */
(function(){
  var Q=[["Discipline is the bridge between goals and accomplishment.", "Jim Rohn"], ["What gets measured gets managed.", "Peter Drucker"], ["Plans are worthless, but planning is everything.", "Dwight D. Eisenhower"], ["By failing to prepare, you are preparing to fail.", "Benjamin Franklin"], ["Beware of little expenses; a small leak will sink a great ship.", "Benjamin Franklin"], ["An investment in knowledge pays the best interest.", "Benjamin Franklin"], ["Energy and persistence conquer all things.", "Benjamin Franklin"], ["Amateurs think about how much money they can make. Professionals think about how much they could lose.", "Jack Schwager"], ["Risk comes from not knowing what you are doing.", "Warren Buffett"], ["The market is a device for transferring money from the impatient to the patient.", "Warren Buffett"], ["Price is what you pay. Value is what you get.", "Warren Buffett"], ["Losers average losers.", "Paul Tudor Jones"], ["The elements of good trading are cutting losses, cutting losses, and cutting losses.", "Ed Seykota"], ["Win or lose, everybody gets what they want out of the market.", "Ed Seykota"], ["There is a time to go long, a time to go short, and a time to go fishing.", "Jesse Livermore"], ["Markets are never wrong; opinions often are.", "Jesse Livermore"], ["The four most dangerous words in investing are: this time it is different.", "John Templeton"], ["In investing, what is comfortable is rarely profitable.", "Robert Arnott"], ["Know what you own, and know why you own it.", "Peter Lynch"], ["The goal of a successful trader is to make the best trades. Money is secondary.", "Alexander Elder"], ["The first principle is that you must not fool yourself, and you are the easiest person to fool.", "Richard Feynman"], ["Simplicity is the ultimate sophistication.", "Leonardo da Vinci"], ["Well begun is half done.", "Aristotle"], ["Quality is not an act, it is a habit.", "Aristotle"], ["Patience is bitter, but its fruit is sweet.", "Aristotle"], ["We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "Will Durant"], ["It does not matter how slowly you go as long as you do not stop.", "Confucius"], ["The man who moves a mountain begins by carrying away small stones.", "Confucius"], ["Our greatest glory is not in never falling, but in rising every time we fall.", "Confucius"], ["Victorious warriors win first and then go to war.", "Sun Tzu"], ["In the midst of chaos, there is also opportunity.", "Sun Tzu"], ["Know yourself and you need not fear the result of a hundred battles.", "Sun Tzu"], ["Success is the sum of small efforts repeated day in and day out.", "Robert Collier"], ["Do not be embarrassed by your failures, learn from them and start again.", "Richard Branson"], ["A goal without a plan is just a wish.", "Antoine de Saint-Exupery"], ["Whether you think you can, or you think you cannot, you are right.", "Henry Ford"], ["Courage is grace under pressure.", "Ernest Hemingway"], ["A person who never made a mistake never tried anything new.", "Albert Einstein"], ["Everything we hear is an opinion, not a fact.", "Marcus Aurelius"], ["The impediment to action advances action. What stands in the way becomes the way.", "Marcus Aurelius"], ["Nothing worth having comes easy.", "Theodore Roosevelt"], ["Luck is what happens when preparation meets opportunity.", "Seneca"], ["It is not that we have a short time to live, but that we waste a lot of it.", "Seneca"], ["He who has a why to live can bear almost any how.", "Friedrich Nietzsche"], ["However beautiful the strategy, you should occasionally look at the results.", "Winston Churchill"], ["If you do not know where you are going, any road will get you there.", "Lewis Carroll"], ["Beware of all enterprises that require new clothes.", "Henry David Thoreau"], ["Fall seven times, stand up eight.", "Japanese proverb"], ["The best time to plant a tree was twenty years ago. The second best time is now.", "Chinese proverb"], ["Rule number one: never lose money. Rule number two: never forget rule number one.", "Warren Buffett"]];
  function build(){
    var host=document.querySelector('[data-quote]');
    if(!host){
      var f=document.querySelector('footer.portal-footer')||document.querySelector('footer');
      if(!f)return null;
      var wrap=document.createElement('div');
      wrap.className='portal-quote';
      wrap.innerHTML='<div class="portal-shell"><blockquote data-quote><p class="pq-text"></p><cite class="pq-by"></cite></blockquote></div>';
      f.insertBefore(wrap,f.firstChild);
      host=wrap.querySelector('[data-quote]');
    }
    return host;
  }
  function run(){
    try{
      var host=build();
      if(!host)return;
      var t=host.querySelector('.pq-text'),b=host.querySelector('.pq-by');
      if(!t||!b)return;
      var q=Q[Math.floor(Math.random()*Q.length)];
      t.textContent='\u201C'+q[0]+'\u201D';
      b.textContent=q[1];
    }catch(e){}
  }
  if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',run);}else{run();}
})();
