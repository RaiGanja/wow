/* Time of day of the home hero (tod.py puts the variant in place before the first paint): changes it on an open page
   when the reader's hour crosses 6/11/17/23 (a 20 s cross-fade; 1.2 s after a click; none with reduced motion) and builds
   the quiet switch under the hero buttons: "Evening · by your local time" opens "Morning · Day · Evening · Night · Local time".
   A picked time is kept in localStorage (GabellaTod.key) and wins over the hour; "Local time" forgets it.
   Fires gabella:tod-start before a change and gabella:tod after it (assets/living/living.js fades its layer around it). */
(() => {
  const G = window.GabellaTod, pic = document.querySelector('picture[data-tod-art]');
  if (!G || !pic) return;
  const amb = document.querySelector('img[data-tod-amb]');   // the blurred sides of an ultrawide hero follow the hero
  const ambSrc = t => amb.getAttribute('data-src').replace(/\{tod\}/g, t);
  const PARTS = ['dawn', 'day', 'dusk', 'night'];
  const STILL = matchMedia('(prefers-reduced-motion: reduce)');
  const fill = (root, t) => {
    root.querySelectorAll('[data-srcset]').forEach(e => { e.srcset = e.getAttribute('data-srcset').replace(/\{tod\}/g, t); });
    const i = root.querySelector('img');
    i.src = i.getAttribute('data-src').replace(/\{tod\}/g, t);
    return i;
  };
  // decode ok, failed or 3 s passed: a decode that never settles (hidden tab) must not wedge the transition
  const ready = i => Promise.race([i.decode(), new Promise(r => setTimeout(r, 3000))]).catch(() => {});
  const emit =(name, detail) => document.dispatchEvent(new CustomEvent(name, { detail }));
  let busy = null, want = null;   // want: the latest requested variant, so a pick made during a running fade is not lost

  function go(to, ms) {
    const from = G.now;
    want = to;
    if (to === from || busy) return busy || Promise.resolve();
    const next = pic.cloneNode(true);
    next.removeAttribute('data-fx');
    next.removeAttribute('data-tod-art');
    next.querySelectorAll('canvas').forEach(c => c.remove());
    next.classList.add('tod-next');
    const img = fill(next, to);
    let ambNext = null;
    if (amb) { ambNext = amb.cloneNode(); ambNext.removeAttribute('data-tod-amb'); ambNext.className = 'hero-amb tod-next'; ambNext.src = ambSrc(to); }
    busy = ready(img).then(() => new Promise(done => {
      emit('gabella:tod-start', { from, to });
      ms = STILL.matches ? 0 : ms;
      next.style.transitionDuration = ms + 'ms';
      pic.after(next);
      if (ambNext) amb.after(ambNext);
      requestAnimationFrame(() => requestAnimationFrame(() => { next.classList.add('in'); if (ambNext) ambNext.classList.add('in'); }));
      setTimeout(() => {
        fill(pic, to);
        if (amb) amb.src = ambSrc(to);
        const base = pic.querySelector('img');
        const swap = () => {
          G.now = to;
          document.documentElement.setAttribute('data-tod', to);
          next.remove();
          if (ambNext) ambNext.remove();
          busy = null;
          render();
          emit('gabella:tod', { from, to });
          if (want && want !== G.now) go(want, 1200); else want = null;
          done();
        };
        ready(base).then(swap);
      }, ms + 50);
    }));
    return busy;
  }

  // hour boundaries: one timer to the next of 6/11/17/23 (+ up to 30 s, so not every tab changes in the same second)
  function arm() {
    const d = new Date(), h = d.getHours();
    const nextH = G.bounds.find(b => b > h);
    const at = new Date(d);
    if (nextH === undefined) { at.setDate(at.getDate() + 1); at.setHours(G.bounds[0], 0, 0, 0); }
    else at.setHours(nextH, 0, 0, 0);
    setTimeout(tick, at - d + Math.random() * 30000);
  }
  function tick() {
    if (document.hidden) { document.addEventListener('visibilitychange', tick, { once: true }); return; }
    if (!G.pinned) go(G.part(new Date().getHours()), 20000);
    arm();
  }
  arm();

  // the switch
  const box = document.querySelector('[data-tod-sw]');
  let open = false;
  function pick(t) {
    try { t === 'auto' ? localStorage.removeItem(G.key) : localStorage.setItem(G.key, t); } catch (e) {}
    G.pinned = t !== 'auto';
    open = false;
    go(t === 'auto' ? G.part(new Date().getHours()) : t, 1200);
    render();
    box.querySelector('button').focus();
  }
  G.go = t => pick(t);
  function render() {
    if (!box) return;
    const had = box.contains(document.activeElement);
    const name = G.names[G.now];
    const keep = () => { if (had) (box.querySelector('[aria-pressed="true"]') || box.querySelector('button')).focus(); };
    if (!open) {
      box.innerHTML = `<button type="button" aria-expanded="false"><span class="sr">${G.text.label}: </span>`
        + `<b>${name}</b>${G.pinned ? '' : `<span> · ${G.text.auto}</span>`}</button>`;
      box.firstChild.addEventListener('click', () => { open = true; render(); box.querySelector('[aria-pressed="true"]').focus(); });
      keep();
      return;
    }
    const b = (id, label, on) => `<button type="button" data-t="${id}" aria-pressed="${on}">${label}</button>`;
    box.innerHTML = `<div role="group" aria-label="${G.text.label}">`
      + PARTS.map(t => b(t, G.names[t], G.pinned && G.now === t)).join('<i aria-hidden="true">·</i>')
      + '<i aria-hidden="true">·</i>' + b('auto', G.text.reset, !G.pinned) + '</div>';
    box.querySelectorAll('button').forEach(x => x.addEventListener('click', () => pick(x.dataset.t)));
    keep();
  }
  const close = () => { if (open) { open = false; render(); } };
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && open) { close(); box.querySelector('button').focus(); } });
  document.addEventListener('pointerdown', e => { if (open && !box.contains(e.target)) close(); });
  render();
})();
