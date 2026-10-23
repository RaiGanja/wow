/* Profile pages (roster, profile, u): game data, the player card, the big card, achievement tiles, page chrome.
   Inlined by build_me.py before the page script; Russian strings are translated at build like the rest of the site.
   The pages talk to the API only through window.GabellaMe (me.js), which runs before DOMContentLoaded. */
const GD = @@GD@@;
const ROOT = '@@ROOT@@', HOME = '@@HOME@@', LANG = '@@LANG@@', HL = document.documentElement.lang;
const $ = (s, el) => (el || document).querySelector(s), $$ = (s, el) => [...(el || document).querySelectorAll(s)];
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
const fill = (s, o) => s.replace(/%(\w)/g, (m, k) => (k in o ? o[k] : m));
const ROLE = { tank: 'Танк', heal: 'Лекарь', dps: 'Урон' };
const TIME = { morning: 'Утро', evening: 'Вечер', night: 'Сова' };
const FACN = { alliance: 'Альянс', horde: 'Орда' };
const LFG = { dungeon: 'Подземелье', raid: 'Рейд', quest: 'Задания' };
const TICO = { morning: 'sun', evening: 'moon', night: 'moon' };
const ico = n => `<svg class="ico" aria-hidden="true"><use href="#i-${n}"/></svg>`;
const race = id => GD.races[id] || { f: 'alliance', n: id, slug: 'human', cls: [] };
const cls = id => GD.classes[id] || { n: id, color: '#c9a54a', roles: [] };
const face = (c, portrait) => `${ROOT}assets/art/${portrait === 'class' ? c.class : race(c.race).slug}-face.webp`;
const ring = (frame, src, extra) => `<span class="me-ring fr-${esc(frame || 'recruit')}${extra ? ' ' + extra : ''}"><img src="${src}" alt="" width="64" height="64" loading="lazy" decoding="async"></span>`;
const subline = c => `${esc(race(c.race).n)} · ${esc(cls(c.class).n)}`;
const profLine = (c, hi) => [[c.prof1, c.prof1_skill], [c.prof2, c.prof2_skill]].filter(p => p[0])
  .map(([p, s]) => (p === hi ? '<b>' : '') + esc(GD.profs[p] || p) + (s ? ` ${s}` : '') + (p === hi ? '</b>' : '')).join(', ');
const playerUrl = id => `${HOME}u/#${id}`;
const achIcon = id => `${ROOT}assets/me/ach/${id}.webp`;   // painted icons; secret.webp hides an unfound secret
const tl = k => (T.gl || {})[k] || k;
const guildUrl = id => `${HOME}g/#${id}`;
const SHIELD = {
  heater: 'M8 6h84v38c0 26-18 42-42 50C26 86 8 70 8 44z',
  round: 'M50 4a46 46 0 1 1 0 92a46 46 0 1 1 0-92z',
  kite: 'M12 6h76v32c0 28-18 48-38 58C30 86 12 66 12 38z',
  banner: 'M14 4h72v90L50 78L14 94z',
};
const FIELD = { plain: '', pale: 'M50 0h50v100H50z', fess: 'M0 50h100v50H0z', quarterly: 'M50 0h50v50H50zM0 50h50v50H0z', chevron: 'M0 100L50 46L100 100z', bend: 'M0 0h40L100 60v40z' };
const BORDER = { gold: '#c9a54a', silver: '#b9bec6', bronze: '#8a5a2b' };
let crestN = 0;
/** Shield from catalog ids; the texture only from 48 px up (it turns to mud on a mini crest). */
function crestSvg(c, px, o = {}) {
  const P = GD.guilds.palette, id = 'gc' + (++crestN);
  const tex = GD.guilds.texture && o.texture !== false && px >= 48
    ? `<image href="${ROOT}assets/me/crest/metal.webp" width="100" height="100" preserveAspectRatio="none" class="gl-tex"/>` : '';
  const edge = c.b !== 'none' ? `<path d="${SHIELD[c.s]}" fill="none" stroke="${BORDER[c.b]}" stroke-width="${px >= 48 ? 3 : 5}"/>` : '';
  return `<svg class="gl-crest" viewBox="0 0 100 100" width="${px}" height="${px}" role="img" aria-label="${esc(o.label || tl('crest'))}">`
    + `<defs><clipPath id="${id}"><path d="${SHIELD[c.s]}"/></clipPath></defs><g clip-path="url(#${id})">`
    + `<rect width="100" height="100" fill="${P[c.c[0]]}"/>${FIELD[c.f] ? `<path d="${FIELD[c.f]}" fill="${P[c.c[1]]}"/>` : ''}`
    + `<use href="${ROOT}assets/me/crest/charges.svg#c-${esc(c.i)}" x="24" y="20" width="52" height="52" fill="${P[c.ic]}"/>${tex}</g>${edge}</svg>`;
}
const DOWN = ['Сервер профилей не отвечает', 'Попробуйте через пару минут. Остальной гид работает как обычно.', 'Повторить'];   // same words as the player page
const guildName = g => g.name || fill(tl('hidden'), { n: g.id });
const crestMini = g => `<a class="gl-mini" href="${guildUrl(g.id)}">${crestSvg(g.crest, 24, { label: guildName(g) })}<span>${esc(guildName(g))}</span></a>`;
const dateOf = t => new Date(t).toLocaleDateString(HL);
const unit = (n, u) => new Intl.NumberFormat(HL, { style: 'unit', unit: u, unitDisplay: 'short', maximumFractionDigits: 0 }).format(n);
function ago(t) {
  const s = (t - Date.now()) / 1000, rtf = new Intl.RelativeTimeFormat(HL, { numeric: 'auto' });
  for (const [u, k] of [['day', 86400], ['hour', 3600], ['minute', 60]]) if (Math.abs(s) >= k) return rtf.format(Math.round(s / k), u);
  return rtf.format(0, 'minute');
}
function left(until) {
  const m = Math.max(1, Math.round((until - Date.now()) / 60000)), h = Math.floor(m / 60);
  return (h ? unit(h, 'hour') + ' ' : '') + (m % 60 ? unit(m % 60, 'minute') : '');
}

// texts of achievements, ranks and frames (assets/me/i18n-<lang>.json), loaded once by ready()
let T = { ui: {}, cats: {}, ranks: {}, frames: {}, ach: {}, pts: {}, secret: [], g: {}, titles: {}, bg: {} };
const achName = id => (T.ach[id] ? T.ach[id][0] : id);
/** Name of a title: an achievement's, or one of its own (pioneer) from T.titles. */
const titleName = id => (T.ach[id] ? T.ach[id][0] : (T.titles || {})[id] || id);
const rankName = id => T.ranks[id] || id;
const frameName = id => T.frames[id] || id;
const rankPts = id => (GD.ranks.find(r => r.id === id) || { pts: 0 }).pts;
const nextRank = pts => GD.ranks.find(r => r.pts > pts) || null;
const rankOf = pts => GD.ranks.filter(r => r.pts <= pts).pop().id;

/** Runs the page once me.js is there and the texts are loaded; M is null when me.js did not load. */
function ready(cb) {
  addEventListener('DOMContentLoaded', () => {
    const M = window.GabellaMe;
    if (!M) return cb(null);
    M.texts().then(t => { T = t; cb(M); }, () => cb(M));
  });
}

/** Level badge on a portrait; a check mark after a level an admin has confirmed. c: {level, verified}. */
const lvBadge = c => `<span class="lv${c.verified ? ' ver' : ''}" aria-label="Уровень ${c.level}${c.verified ? ', ' + esc(tg('verified')) : ''}">${c.level}${c.verified ? '<i aria-hidden="true">✓</i>' : ''}</span>`;

/** Player card of the roster and the character lists. p: {id, nick, title, frame, rank, portrait, lfg, main, alts}. */
function pcard(p, o) {
  o = o || {};
  const c = p.main, f = race(c.race).f;
  const meta = [`<span>${ico(c.role)}${esc(ROLE[c.role] || '')}</span>`];
  const pl = profLine(c, o.prof);
  if (pl) meta.push(`<span>${pl}</span>`);
  meta.push(`<span>${ico(TICO[c.playtime] || 'moon')}${esc(TIME[c.playtime] || '')}</span>`);
  if (p.lfg) meta.push(`<span class="lfg">${esc(LFG[p.lfg.kind] || '')} · ${esc(left(p.lfg.until))}</span>`);
  const qc = p.name_color ? ` class="${nameCls(p.name_color)}"` : '';
  const name = o.link === false ? `<b${qc}>${esc(c.name)}</b>` : `<a${qc} href="${playerUrl(p.id)}">${esc(c.name)}</a>`;
  const glory = o.glory && p.glory ? `<small class="g-gl">${esc(tg('glory_n', { n: p.glory }))}</small>` : '';
  const alts = (p.alts || []).length ? `<div class="alts">Твинки: ${p.alts.map(a => `<i style="--ac:${cls(a.class).color}">${esc(a.name)}</i>`).join(', ')}</div>` : '';
  return `<article class="pcard${o.cls ? ' ' + o.cls : ''}" style="--cc:${cls(c.class).color}"${o.attrs || ''}>
    <span class="pic">${ring(p.frame || p.rank, face(c, p.portrait))}${lvBadge(c)}</span>
    <span class="fx ${f}">${esc(o.tag || FACN[f])}</span>
    <div class="nm">${p.title ? `<span class="ttl">${esc(titleName(p.title))}</span>` : ''}${name}${glory}</div>
    <span class="sub">${subline(c)}</span>
    <div class="meta">${meta.join('')}</div>${alts}${p.member || p.nick ? `<div class="nick">${p.member ? `<span class="team"><img src="${ROOT}assets/brand/mark.webp" alt="" width="14" height="14">Gabella Team</span>` : ''}${p.nick ? `<span>${esc(p.nick)}</span>` : ''}</div>` : ''}${o.after || ''}
  </article>`;
}

/** Showcase item: an achievement (id) or a season badge (badge:<id>). */
const showName = id => (id.startsWith('badge:') ? tg('ch_badge') : achName(id));
const showIcon = id => achIcon(id.startsWith('badge:') ? id.slice(6) : id);

/** Check mark after a level an admin has confirmed. */
const verMark = c => (c.verified ? `<span class="g-ver" role="img" aria-label="${esc(tg('verified'))}" title="${esc(tg('verified'))}">✓</span>` : '');

/** Card menu («…» with the report item) for signed-in people looking at somebody else. */
const cardMenu = (id, cls) => `<details class="g-menu${cls ? ' ' + cls : ''}"><summary aria-label="${esc(tg('menu'))}" title="${esc(tg('menu'))}">⋯</summary><button type="button" data-report="${esc(id)}">${esc(tg('report'))}</button></details>`;

/** Report dialog: what is wrong (name, motto, other; fields = [[value, label]] for a guild), an optional reason, POST /reports; success is a quiet toast. */
function reportDialog(M, target, name, fields) {
  const opts = fields || ['name', 'motto', 'other'].map(k => [k, tg('report_' + k)]);
  const d = document.createElement('dialog');
  d.className = 'g-dlg';
  d.setAttribute('aria-labelledby', 'repH');
  d.innerHTML = `<form class="g-rf"><h2 id="repH">${esc(tg('report'))}: ${esc(name)}</h2>
    <fieldset><legend>${esc(tg('report_field'))}</legend>${opts.map(([k, label], i) => `<label class="g-rr"><input type="radio" name="f" value="${k}"${i ? '' : ' checked'}>${esc(label)}</label>`).join('')}</fieldset>
    <label class="g-rl">${esc(tg('report_reason'))}<input type="text" name="r" maxlength="80" autocomplete="off"></label>
    <p class="msg err" role="alert"></p>
    <div class="row"><button type="submit" class="btn">${esc(tg('report_send'))}</button><button type="button" class="btn ghost" data-x>${esc(tg('report_cancel'))}</button></div></form>`;
  document.body.append(d);
  const f = $('form', d), msg = $('.msg', d), ok = $('[type=submit]', d);
  const close = () => { d.close ? d.close() : d.removeAttribute('open'); };
  d.addEventListener('close', () => d.remove());
  $('[data-x]', d).onclick = close;
  d.addEventListener('click', e => { if (e.target === d) close(); });
  f.onsubmit = e => {
    e.preventDefault();
    const field = f.elements.f.value, reason = f.elements.r.value.trim() || opts.find(o => o[0] === field)[1];   // the API wants a reason: the field's own name when none is typed
    ok.disabled = true; msg.textContent = '';
    M.api('/reports', { body: { target, field, reason } }).then(() => { close(); M.toast({ kind: 'note', id: 'report_sent' }); }, err => {
      ok.disabled = false;
      msg.textContent = tg(err.code === 'report_limit' ? 'report_limit' : 'err_report');
    });
  };
  if (d.showModal) d.showModal(); else d.setAttribute('open', '');
  f.elements.f.focus();
}

/** Rank block of the big card: points, rank, bar to the next one. */
function rankBlock(pts) {
  const r = rankOf(pts), nx = nextRank(pts), from = rankPts(r);
  const pct = nx ? Math.round(100 * (pts - from) / (nx.pts - from)) : 100;
  return `<div class="rk"><span class="pts"><span class="shield" aria-hidden="true">★</span>${pts}</span>
    <span class="rn">Ранг: ${esc(rankName(r))}</span><span class="bar"><i style="width:${pct}%"></i></span>
    <small>${nx ? esc(fill('До ранга «%r»: %n', { n: nx.pts - pts, r: rankName(nx.id) })) : 'Высший ранг'}</small></div>`;
}

/** The big card, «how others see you». p: player shape plus background, motto, points, joined or since. */
function bcard(p, o) {
  o = o || {};
  const c = p.main, bg = p.background || race(c.race).slug;
  const src = /^hero_/.test(bg) ? `${ROOT}assets/art/${bg}-960.webp` : `${ROOT}assets/art/${bg}-896.webp`;
  const who = [];
  if (p.nick) who.push(esc(p.nick));
  if (p.joined) who.push(esc(fill('В Gabella Team с %d', { d: dateOf(p.joined) })));
  else if (p.member) who.push('Gabella Team');
  else if (p.since) who.push(esc(fill('В составе с %d', { d: dateOf(p.since) })));
  const h = o.h || 'h1';
  return `<section class="bcard" style="--cc:${cls(c.class).color}" aria-label="Карточка игрока">
    <img class="bg" src="${src}" alt="" decoding="async">
    <div class="in">${ring(p.frame || p.rank, face(c, p.portrait), o.reveal ? 'reveal' : '')}
      <div>${p.title ? `<span class="ttl">${esc(titleName(p.title))}</span>` : ''}<${h}${p.name_color ? ` class="${nameCls(p.name_color)}"` : ''}>${esc(c.name)}</${h}>
        <span class="sub">${subline(c)} · ${c.level}${verMark(c)} · ${esc(ROLE[c.role] || '')}</span>
        ${who.length ? `<p class="who">${who.join(' · ')}</p>` : ''}${p.motto ? `<p class="motto">«${esc(p.motto)}»</p>` : ''}</div>
      ${rankBlock(p.points || 0)}</div></section>`;
}

/** Progress of an achievement toward its goal: {v, goal, text} or null when it is all-or-nothing.
    ctx: {progress, user, chars, have:Set}; user and chars are known only for the person themself. */
function achProgress(a, ctx) {
  const r = a.rule || {}, P = (ctx.progress || {})[r.key] || { value: 0, items: [] };
  let v = null, goal = null;
  if (a.kind === 'progress' && r.key) {
    if (r.items) return null;
    if (r.all) { goal = (GD.sets[r.key] || []).length; v = (P.items || []).filter(x => GD.sets[r.key].includes(x)).length; }
    else { goal = r.goal; v = r.set ? (P.items || []).length : P.value || 0; }
    if (goal <= 1) return null;
  } else if (ctx.user) {
    const u = ctx.user;
    if (r.days && u.joined_guild_at) { goal = r.days; v = Math.floor((Date.now() - u.joined_guild_at) / 86400000); }
    else if (r.refs) { goal = r.refs; v = u.refs || 0; }
    else if (r.streak) { goal = r.streak; v = u.streak || 0; }
    else if (a.id === 'three_chars') { goal = 3; v = (ctx.chars || []).length; }
    else if (r.all_cat) { const ids = GD.ach.filter(x => x.cat === r.all_cat && x.id !== a.id).map(x => x.id); goal = ids.length; v = ids.filter(x => ctx.have.has(x)).length; }
  }
  if (goal === null) return null;
  v = Math.max(0, Math.min(v, goal));
  const text = r.key === 'radio_min' ? `${unit(Math.floor(v / 60), 'hour')} / ${unit(goal / 60, 'hour')}` : fill('%v из %g', { v, g: goal });
  return { v, goal, text };
}

/** Achievement tile. st: {at} when owned; marks: [[label, on]] for the comparison. */
function achTile(a, st, ctx, marks) {
  const own = !!st, hide = a.secret && !own && !(marks && marks.some(m => m[1]));
  const t = T.ach[a.id] || [a.id, ''];
  const name = hide ? 'Секрет' : t[0];
  const desc = hide ? fill('Подсказка: %h', { h: t[2] || '?' }) : t[1];
  let foot = '';
  if (marks) foot = `<span class="marks">${marks.map(([l, on]) => `<span class="${on ? 'on' : ''}">${esc(l)}</span>`).join('')}</span>`;
  else if (own) foot = `<span class="when">${esc(fill('Получено %d', { d: dateOf(st.at) }))}</span>`;
  else if (ctx && !hide) {
    const pr = achProgress(a, ctx);
    if (pr) foot = `<span class="prog"><span class="bar"><i style="width:${Math.round(100 * pr.v / pr.goal)}%"></i></span>${esc(pr.text)}</span>`;
  }
  return `<div class="ach${own || (marks && marks.some(m => m[1])) ? '' : ' lock'}${hide ? ' secret' : ''}">
    <span class="ic"><img src="${achIcon(hide ? 'secret' : a.id)}" alt="" width="46" height="46" loading="lazy"></span><b>${esc(name)}</b>
    <span class="shield" aria-label="${a.pts} ${esc(T.ui.pts || '')}">${a.pts}</span><p>${esc(desc)}</p>${foot}</div>`;
}


/* ---------- growth: Glory bar, name colours, weekly task lines, chronicle ---------- */
/** Text of the growth set (T.g): {n}, {d}, {x} ... are filled from o. texts: the dict to take it from, T.g by default. */
const tg = (k, o, texts) => Object.keys(o || {}).reduce((s, x) => s.split('{' + x + '}').join(o[x]), (texts || T.g || {})[k] || k);
const num = n => new Intl.NumberFormat(HL).format(n);

/** Glory bar. glory: {level, into, need, rested}: gold fill into/need, the blue rested stretch right behind it
    (min(rested, need - into) / need). At the top level only «Glory N», no bar. */
function gloryBar(g, texts) {
  const head = `<b class="g-lvl">${esc(tg('glory_n', { n: g.level }, texts))}</b>`;
  if (g.level >= GD.prog.glory_max || !g.need) return `<div class="g-glory g-max">${head}</div>`;
  const into = Math.max(0, Math.min(g.into, g.need)), pct = Math.round(1000 * into / g.need) / 10;
  const rest = Math.max(0, Math.min(g.rested || 0, g.need - into)), rpct = Math.round(1000 * rest / g.need) / 10;
  return `<div class="g-glory"><div class="g-head">${head}<span class="g-num">${num(into)} / ${num(g.need)}</span></div>
    <div class="g-bar" role="progressbar" aria-label="${esc(tg('glory', null, texts))}" aria-valuemin="0" aria-valuemax="${g.need}" aria-valuenow="${into}"><i class="g-fill" style="width:${pct}%"></i>${rest ? `<i class="g-rest" style="left:${pct}%;width:${rpct}%"></i>` : ''}</div>
    ${rest ? `<small class="g-rtxt">${esc(tg('glory_rested', null, texts))}</small>` : ''}</div>`;
}

/** Class of a name colour (q-poor ... q-legendary); anything unknown is the default white. */
const nameCls = color => 'q-' + (/^[a-z]+$/.test(color || '') ? color : 'common');

const TASK_ACT = {   // [text key of T.g, where it leads]
  radio_min: ['act_radio', 'radio'], station: ['act_radio', 'radio'], guide: ['act_guides', 'guides/'], class: ['act_classes', 'classes/'],
  race: ['act_races', 'races/'], party5: ['act_party', 'tools/#raid'], raid40: ['act_raid', 'tools/#raid'], share_team: ['act_party', 'tools/#raid'],
  compare3: ['act_compare', 'tools/#compare'], search: ['act_search', 'tools/#search'], lfg: ['act_lfg', 'lfg'], show_card: ['act_copy', 'card'],
  play_page: ['act_play', 'play/'],
};
/** Name of a weekly task: its own text, or a template filled with the station, guide or class. o.itemName(key, item) may name stations and guides. */
function taskName(task, texts, o) {
  const tx = texts || T.g || {}, m = /^(st|g|c)_/.exec(task.id), w = GD.prog.weekly[task.id] || {};
  if (tx['task_' + task.id] || !m || !w.item) return tx['task_' + task.id] || task.id;
  const k = { st: 'station', g: 'guide', c: 'class' }[m[1]];
  const x = (o && o.itemName && o.itemName(k, w.item)) || (k === 'class' ? cls(w.item).n : w.item);
  return tg('task_' + m[1], { x }, tx);
}
/** Line of a weekly task. task: {id, value, goal, done}; o.extra: more buttons after the main one. The button leads where the task is done (the same as «What next»):
    radio -> data-act="radio", guides/classes/races/tools/play -> a link, lfg -> data-act="lfgOn", link copy -> data-act="card". */
function taskLine(task, texts, o) {
  const w = GD.prog.weekly[task.id] || {}, act = TASK_ACT[w.key || task.key];
  let btn = '';
  if (!task.done && act) {
    const label = esc(tg(act[0], null, texts)), aria = ` aria-label="${esc(tg(act[0], null, texts) + ': ' + taskName(task, texts, o))}"`;
    if (['radio', 'card'].includes(act[1])) btn = `<button type="button" class="btn ghost g-go" data-act="${act[1]}"${aria}>${label}</button>`;
    else if (act[1] === 'lfg') btn = `<button type="button" class="btn ghost g-go" data-act="lfgOn"${aria}>${label}</button>`;
    else {
      const sub = w.item && ['guide', 'class', 'race'].includes(w.key) ? w.item + '/' : '';
      btn = `<a class="btn ghost g-go" href="${HOME}${act[1]}${act[1].endsWith('/') ? sub : ''}"${aria}>${label}</a>`;
    }
  }
  const pct = task.goal ? Math.round(100 * Math.min(task.value, task.goal) / task.goal) : 0;
  const state = task.done ? `<span class="g-done" role="img" aria-label="${esc(tg('task_done', null, texts))}">✓</span>` : `<span class="g-tv">${task.value} / ${task.goal}</span>`;
  return `<div class="g-task${task.done ? ' done' : ''}"><div class="g-tt"><b>${esc(taskName(task, texts, o))}</b>${state}</div>
    <div class="g-bar g-sm" aria-hidden="true"><i class="g-fill" style="width:${pct}%"></i></div>${btn || (o && o.extra) ? `<span class="g-acts">${btn}${(o && o.extra) || ''}</span>` : ''}</div>`;
}

/** Chronicle line. item: {kind, ref, at}; the caller puts the lines into an <ol class="g-chron">. */
function chronicleItem(item, texts) {
  const r = item.ref || '', tx = texts || T.g;
  const text = item.kind === 'join' ? tg('ch_join', null, tx)
    : item.kind === 'glory' ? tg('ch_glory', { n: r }, tx)
    : item.kind === 'step' ? tg('ch_step', { n: r.split(':').pop() }, tx)
    : item.kind === 'badge' ? tg('ch_badge', null, tx)
    : item.kind === 'lvl60' ? tg('ch_lvl60', { name: r }, tx)
    : item.kind === 'rank' ? tg('ch_rank', { r: rankName(r) }, tx)
    : tg('ch_ach', { a: achName(r) }, tx);
  return `<li class="g-ch g-ch-${esc(item.kind)}"><time class="g-chd" datetime="${new Date(item.at).toISOString()}">${esc(dateOf(item.at))}</time><span>${esc(text)}</span></li>`;
}

/** Team feed line: who got what. */
function feedLine(x) {
  const who = `<a href="${playerUrl(x.user)}">${esc(x.name)}</a>`;
  const what = x.kind === 'rank' ? fill(esc('%n достигает ранга %r'), { n: who, r: `<em>${esc(rankName(x.ref))}</em>` })
    : x.ref === 'secret' ? fill(esc('%n находит секрет'), { n: who })
    : fill(esc('%n получает «%a»'), { n: who, a: `<em>${esc(achName(x.ref))}</em>` });
  return `<div class="it">${ring(x.frame || 'recruit', face(x, x.portrait))}<span>${what}</span><small>${esc(ago(x.at))}</small></div>`;
}

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch (e) { return false; }
}

/* ---------- page chrome: theme, top bar, menu sheet ---------- */
const themeBtns = document.querySelectorAll('.themebtn');
function paintTheme() { const t = document.documentElement.getAttribute('data-theme'); themeBtns.forEach(b => b.querySelector('use').setAttribute('href', t === 'light' ? '#i-moon' : '#i-sun')); const m = document.querySelector('meta[name="theme-color"]'); if (m) m.setAttribute('content', t === 'light' ? '#fbfaf7' : '#07080a'); }
themeBtns.forEach(b => b.onclick = () => { const t = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light'; document.documentElement.setAttribute('data-theme', t); try { localStorage.setItem('wf-theme', t); } catch (e) {} paintTheme(); });
paintTheme();
const topbar = $('#topbar');
let barTick = false;
const overArt = !!document.querySelector('.thero');   // without hero art under it the bar stays solid
function paintBar() { topbar.classList.toggle('solid', !overArt || window.scrollY > 24); barTick = false; }
window.addEventListener('scroll', () => { if (!barTick) { barTick = true; requestAnimationFrame(paintBar); } }, { passive: true });
paintBar();
const moreDlg = $('#moreDlg');
document.querySelectorAll('.menubtn, .morebtn').forEach(b => b.onclick = () => { if (moreDlg.showModal) moreDlg.showModal(); else moreDlg.setAttribute('open', ''); });
$('#moreClose').onclick = () => moreDlg.close();
moreDlg.addEventListener('click', e => { if (e.target === moreDlg || e.target.closest('.toc a')) moreDlg.close(); });
