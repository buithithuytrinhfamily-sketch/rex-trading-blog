/* The home page is also updated by the daily publisher. Merge new cards into
   the library without depending on the publisher regenerating its JSON file. */
(function () {
  'use strict';
  var q = document.getElementById('q');
  var list = document.querySelector('.list');
  var count = document.getElementById('count');
  var empty = document.getElementById('empty');
  q.value = new URLSearchParams(location.search).get('q') || '';
  function run() {
    var terms = q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    var n = 0;
    Array.from(list.children).forEach(function (li) {
      var text = li.getAttribute('data-k') || li.textContent.toLowerCase();
      var hit = terms.every(function (term) { return text.indexOf(term) !== -1; });
      li.hidden = !hit;
      if (hit) n++;
    });
    count.textContent = n + (n === 1 ? ' article' : ' articles');
    empty.style.display = n ? 'none' : 'block';
  }
  q.addEventListener('input', run);
  run();
  fetch('/', {cache: 'no-cache'}).then(function (response) {
    if (!response.ok) throw new Error('Home unavailable');
    return response.text();
  }).then(function (text) {
    var doc = new DOMParser().parseFromString(text, 'text/html');
    var known = new Map();
    Array.from(list.children).forEach(function (li) {
      known.set(new URL(li.querySelector('a').getAttribute('href'), location.origin).pathname, li);
    });
    var ordered = [];
    doc.querySelectorAll('.blog__grid .post').forEach(function (card) {
      var url = new URL(card.getAttribute('href'), location.origin);
      var title = card.querySelector('h3');
      if (url.origin !== location.origin || !title || !url.pathname.endsWith('.html') || url.pathname === '/about.html') return;
      var li = known.get(url.pathname);
      if (!li) {
        li = document.createElement('li');
        var a = document.createElement('a');
        a.href = url.pathname;
        var h = document.createElement('h2');
        h.textContent = title.textContent;
        a.appendChild(h);
        var category = card.querySelector('.post__cat');
        if (category) {
          var p = document.createElement('p');
          p.textContent = category.textContent;
          a.appendChild(p);
        }
        li.appendChild(a);
        li.setAttribute('data-k', a.textContent.toLowerCase());
        known.set(url.pathname, li);
      }
      if (ordered.indexOf(li) === -1) ordered.push(li);
    });
    ordered.forEach(function (li) { list.appendChild(li); });
    known.forEach(function (li) { if (ordered.indexOf(li) === -1) list.appendChild(li); });
    run();
  }).catch(function () { /* The complete static archive remains searchable offline. */ });
})();
