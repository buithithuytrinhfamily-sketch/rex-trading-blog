(function () {
 'use strict';
 const root = document.querySelector('.rex-carousel');
 if (!root) return;
 const slides = [...root.querySelectorAll('[data-slide]')];
 const choices = [...root.querySelectorAll('[data-slide-to]')];
 const pause = root.querySelector('.rex-slide-pause');
 let current = 0, timer, paused = false;
 function schedule() {
  clearTimeout(timer);
  if (!paused && !document.hidden) timer = setTimeout(() => show((current + 1) % slides.length), 6500);
 }
 function show(index) {
  const focusInside = slides[current].contains(document.activeElement);
  current = index;
  slides.forEach((slide, i) => { slide.hidden = i !== current; });
  choices.forEach((button, i) => button.setAttribute('aria-pressed', String(i === current)));
  if (focusInside) choices[current].focus({preventScroll:true});
  schedule();
 }
 choices.forEach((button, i) => button.addEventListener('click', () => show(i)));
 pause.addEventListener('click', () => {
  paused = !paused;
  pause.textContent = paused ? 'Resume' : 'Pause';
  pause.setAttribute('aria-label', paused ? 'Resume slideshow' : 'Pause slideshow');
  schedule();
 });
 document.addEventListener('visibilitychange', schedule);
 schedule();
})();
