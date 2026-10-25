const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Warrior', s:'Warrior', roles:['tank','dps'],
    specs:[['Arms','Obrażenia w zwarciu (broń dwuręczna)',['dps']],['Fury','Obrażenia w zwarciu (dual wield)',['dps']],['Protection','Tank',['tank']]],
    lvl:'Najwolniejsze levelowanie, ok. 12% dłużej niż średnio',
    lp:12,
    raid:'Battle Shout działa na cały raid',
    forever:'Więcej Rage, lepsze aggro na grupach celów, talent Weapon Master. Fury i Bloodthirst osłabione.' },
  { id:'paladin', n:'Paladin', roles:['tank','heal','dps'],
    specs:[['Holy','Healer',['heal']],['Protection','Tank',['tank']],['Retribution','Obrażenia w zwarciu',['dps']]],
    lvl:'Średnie tempo levelowania',
    lp:0,
    raid:'Blessing of Kings jest teraz bazowe. Według list z bety Protection to jeden z najmocniejszych tanków, a Retribution spadł po patchu z 15 października.',
    forever:'Holy Strike od levelu 6, Judgement nie zużywa seala. Undead mogą teraz być paladynami, więc klasa pojawiła się w Horde.' },
  { id:'hunter', n:'Hunter', roles:['dps'],
    specs:[['Beast Mastery','Obrażenia dystansowe, dużo obrażeń od peta',['dps']],['Marksmanship','Obrażenia dystansowe',['dps']],['Survival','Zwarcie i dystans, pułapki',['dps']]],
    lvl:'Najszybsze levelowanie, ok. 8% szybciej niż średnio',
    lp:-8,
    raid:'Trueshot Aura działa na cały raid',
    forever:'Można grać bez peta, pułapki działają w walce, pojawiła się rodzina petów lisy. Survival może grać w zwarciu.' },
  { id:'rogue', n:'Rogue', roles:['dps'],
    specs:[['Assassination','Obrażenia od trucizn',['dps']],['Combat','Szybkie ataki bronią',['dps']],['Subtlety','Zasadzki, krwawienia',['dps']]],
    lvl:'Średnie tempo levelowania',
    lp:0,
    raid:'Czyste obrażenia w zwarciu, bez buffów na cały raid',
    forever:'Można teraz używać jednoręcznych toporów. Assassination opiera się na truciznach, Subtlety na krwawieniach i stealthu.' },
  { id:'priest', n:'Priest', roles:['heal','dps'],
    specs:[['Discipline','Healer, tarcze i absorpcja',['heal']],['Holy','Healer',['heal']],['Shadow','Obrażenia dystansowe',['dps']]],
    lvl:'Ok. 5% wolniej niż średnio',
    lp:5,
    raid:'Divine Spirit jest teraz bazowe. Obrażenia Shadow i Devouring Plague (24 sek. cooldownu) zostały wzmocnione w patchu z 15 października.',
    forever:'Fear Ward i Devouring Plague są dostępne od levelu 20 dla każdej rasy. Każda rasa ma dwa własne zaklęcia priesta.' },
  { id:'shaman', n:'Shaman', roles:['heal','dps','tank?'],
    specs:[['Elemental','Obrażenia dystansowe',['dps']],['Enhancement','Obrażenia w zwarciu. Możliwość tankowania wciąż pod znakiem zapytania',['dps','tank?']],['Restoration','Healer',['heal']]],
    lvl:'Średnie tempo levelowania',
    lp:0,
    raid:'Totemy Strength of Earth, Windfury, Flametongue i Grace of Air buffują swoją grupę',
    forever:'Krasnoludy mogą teraz być szamanami, więc klasa pojawiła się w Alliance. Lava Burst wzmocniony, Elemental poszedł w górę w rankingach obrażeń.' },
  { id:'mage', n:'Mage', roles:['dps'],
    specs:[['Arcane','Burst, dużo many',['dps']],['Fire','Kryty i ignite',['dps']],['Frost','Obrażenia i kontrola',['dps']]],
    lvl:'Najszybsze levelowanie, ok. 8% szybciej niż średnio (ok. 12 godzin oszczędności)',
    lp:-8,
    raid:'Portale oraz jedzenie i woda dla całej drużyny',
    forever:'Fire dostał Hotstreak, Arcane Arcane Blast, Frost Ice Lance. Frostfire Bolt jest dostępny od levelu 40.' },
  { id:'warlock', n:'Warlock', roles:['dps'],
    specs:[['Affliction','Obrażenia od klątw i korupcji',['dps']],['Demonology','Obrażenia przez demony',['dps']],['Destruction','Bezpośrednie obrażenia od ognia i cienia',['dps']]],
    lvl:'Średnie tempo levelowania',
    lp:0,
    raid:'Shadow Mastery daje teraz 2–10% obrażeń od cienia (było 1–5%)',
    forever:'Affliction ma nowe zaklęcie channelowane, demon zostaje przy Demonic Sacrifice, Destruction dostał Incinerate i AoE.' },
  { id:'druid', n:'Druid', roles:['tank','heal','dps'],
    specs:[['Balance','Obrażenia dystansowe',['dps']],['Feral','Tank (miś) i obrażenia w zwarciu (kot)',['tank','dps']],['Restoration','Healer, dużo leczenia w czasie',['heal']]],
    lvl:'Ok. 5% wolniej niż średnio',
    lp:5,
    raid:'Leader of the Pack i Moonkin Aura działają na cały raid i się stackują',
    forever:'Każda specjalizacja dostała jasną rolę, formy działają z miksturami i enchantami broni. Na jednej postaci możesz być tankiem, healerem i DPS-em.' }
];
const ROLE_RU = { tank:'Tank', heal:'Healer', dps:'DPS', 'tank?':'Tank (niepewne)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Battle Shout', paladin:'Blessing of Kings', hunter:'Trueshot Aura', priest:'Power Word: Fortitude, Divine Spirit', shaman:'Totemy (Strength of Earth, Windfury, Flametongue, Grace of Air)', mage:'Arcane Intellect, portale, jedzenie i woda', druid:'Mark of the Wild, Leader of the Pack, Moonkin Aura' };

const RACES = [
  { id:'human', n:'Human', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Will to Survive','Usuwa ogłuszenie'],['a','Perception','Ujawnia niewidzialnych wrogów na 20 sek.'],['p','Ruthless','+2% szansy na kryta'],['p','The Human Spirit','+5% spirit']],
    tip:'Spirit przekłada się na leczenie u Holy Priesta, więc Human priest dobrze sprawdza się w leczeniu.' },
  { id:'dwarf', n:'Dwarf', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Stoneform','Odporność na krwawienia, trucizny i choroby przez 8 sek. oraz mniejsze obrażenia fizyczne'],['a','Find Treasure','Pokazuje pobliskie skrzynie'],['p','Earth Fury','+2% obrażeń krytycznych i mocy leczenia'],['p','Big Game Hunter','+5% obrażeń przeciw bestiom']],
    tip:'Stoneform przydaje się tankom i w PvP.' },
  { id:'nightelf', n:'Night Elf', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Elune’s Light','+10% szansy na kryta przez 15 sek.'],['a','Shadowmeld','Niewidzialność w miejscu'],['p','Quickness','+1% uniku i +2% szybkości biegu'],['p','Wisp Spirit','+75% szybkości biegu jako duch']],
    tip:'Jedyna rasa Alliance z druidem, chyba że weźmiesz Skyborne.' },
  { id:'gnome', n:'Gnome', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Escape Artist','Krótka odporność na spowolnienia i unieruchomienia'],['a','Eureka!','Następne 3 zdolności są tańsze i o 10% silniejsze'],['p','Expansive Mind','+5% maksymalnej many, rage lub energii'],['p','Engineering Specialization','Urządzenia inżynieryjne działają bardziej niezawodnie']],
    tip:'Expansive Mind szczególnie pomaga klasom na energii.' },
  { id:'skyA', n:'Skyborne (Alliance)', f:'alliance', paid:true, name:'High Order Skyborne',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Szybowanie w dół przez 10 sek., bez obrażeń od upadku'],['a','Read Ley Line','+100% regeneracji zdrowia i many'],['p','Wind Blessed','+3% szybkości ataku i rzucania zaklęć'],['p','Elemental Insight','+5% obrażeń przeciw żywiołakom']],
    tip:'Płatna rasa: Heroic Pack od $29.99. Start w lokacji Zephras Isle (levele 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Blood Fury','+10% attack power i spell power przez 15 sek.'],['a','Shatter Curse','Usuwa klątwy i korupcję, −5% otrzymywanych obrażeń magicznych przez 8 sek.'],['p','Savage','+1% szansy na kryta'],['p','Hardiness','Ogłuszenia są o 20% krótsze']],
    tip:'Blood Fury daje mocne okno na obrażenia.' },
  { id:'undead', n:'Undead', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Will of the Forsaken','Usuwa charm, fear i sen'],['a','Cannibalize','Przywraca 35% zdrowia i many w czasie'],['p','Underwater Breathing','Dłuższe oddychanie pod wodą'],['p','Touch of the Grave','Szansa na wyssanie zdrowia przy ataku']],
    tip:'Nowa kombinacja: paladyn dla Horde, w której tej klasy wcześniej nie było.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','War Stomp','Ogłusza pobliskich wrogów na 2 sek.'],['a','Cultivation','Wyhodowane zioła można zbierać bez Herbalism'],['p','Plainsrunning','Szybkość rośnie, gdy biegniesz'],['p','Endurance','+5% zdrowia i +2% obrażeń krytycznych']],
    tip:'Jedyna rasa Horde z druidem, chyba że weźmiesz Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserking','+10% szybkości ataku i rzucania zaklęć przez 10 sek.'],['a','Rapid Regeneration','Przywraca zdrowie w czasie'],['p','Beast Slaying','+5% obrażeń przeciw bestiom'],['p','Regeneration','Zdrowie regeneruje się także w walce']],
    tip:'Najwięcej opcji klas w Horde: siedem.' },
  { id:'skyH', n:'Skyborne (Horde)', f:'horde', paid:true, name:'Windshaper Skyborne',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Szybowanie w dół przez 10 sek., bez obrażeń od upadku'],['a','Skysight','+10% szybkości biegu'],['p','Wind Blessed','+3% szybkości ataku i rzucania zaklęć'],['p','Elemental Insight','+5% obrażeń przeciw żywiołakom']],
    tip:'Płatna rasa: Heroic Pack od $29.99. Tylko Horde może mieć szamana, tylko Alliance maga.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "Najliczniejsza rasa Alliance. Wszechstronna i mocna w PvP dzięki Will to Survive.", "dwarf": "Twardzi górnicy i strzelcy z Ironforge. Pierwszy raz w Classic Alliance ma szamanów i są to krasnoludy.", "nightelf": "Starożytny lud lasów. Nieuchwytni: własny sposób na ukrycie się, uniki i szybki bieg.", "gnome": "Wynalazcy z Gnomeregan. Mali, sprytni i z najlepszą zdolnością ucieczki w grze.", "skyA": "Nowa rasa w Forever. High Order: elfy wiatru szukające utraconej magii arkanów swoich przodków.", "orc": "Serce Horde. Najsilniejsi wojownicy i mistrzowie PvP dzięki Blood Fury i Hardiness.", "undead": "Forsaken: dawni ludzie, którzy wyrwali się spod władzy Lich Kinga. Odporni na fear i sen, kiedy to się liczy.", "tauren": "Pokojowe olbrzymy z równin. Najwięcej zdrowia i własne obszarowe ogłuszenie.", "troll": "Plemię Darkspear. Najwięcej klas w Horde i mocny Berserking na obrażenia.", "skyH": "Nowa rasa w Forever. Windshaper: duchowi przywódcy Skyborne, bliscy żywiołom."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Arms':'Arms','Fury':'Fury','Protection':'Protection','Holy':'Holy','Retribution':'Retribution',
  'Beast Mastery':'Beast Mastery','Marksmanship':'Marksmanship','Survival':'Survival',
  'Assassination':'Assassination','Combat':'Combat','Subtlety':'Subtlety',
  'Discipline':'Discipline','Shadow':'Shadow','Elemental':'Elemental','Enhancement':'Enhancement','Restoration':'Restoration',
  'Arcane':'Arcane','Fire':'Fire','Frost':'Frost','Affliction':'Affliction','Demonology':'Demonology','Destruction':'Destruction',
  'Balance':'Balance','Feral':'Feral',
  'Will to Survive':'Will to Survive','Perception':'Perception','Ruthless':'Ruthless','The Human Spirit':'The Human Spirit',
  'Stoneform':'Stoneform','Find Treasure':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Elune’s Light':"Elune’s Light",'Shadowmeld':'Shadowmeld','Quickness':'Quickness','Wisp Spirit':'Wisp Spirit',
  'Escape Artist':'Escape Artist','Eureka!':'Eureka!','Expansive Mind':'Expansive Mind','Engineering Specialization':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Blood Fury':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Hardiness':'Hardiness',
  'Will of the Forsaken':'Will of the Forsaken','Cannibalize':'Cannibalize','Underwater Breathing':'Underwater Breathing','Touch of the Grave':'Touch of the Grave',
  'War Stomp':'War Stomp','Cultivation':'Cultivation','Plainsrunning':'Plainsrunning','Endurance':'Endurance',
  'Berserking':'Berserking','Rapid Regeneration':'Rapid Regeneration','Beast Slaying':'Beast Slaying','Regeneration':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Porada</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Alliance' : 'Horde'; }
const PV = /*PV*/'?v=b4d0adfa';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Szybciej o ${-p}%` : p > 0 ? `Wolniej o ${p}%` : 'Średnie tempo';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>szybciej</span><span>wolniej</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Klasa</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Levelowanie</span><span>Na raidach</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Role: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Rasa</span><span>Klasy</span><span class="abl">Zdolności <span class="abt">aktywna</span><span class="abt p">pasywna</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">płatna</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Klasy: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nowe' : v ? '' : ', niedostępne')); }).join('')}</span>
    <span class="abs">${r.rac.map(x => `<span><b class="${x[0] === 'a' ? '' : 'p'}">${bi(x[1])}</b><span>${esc(x[2])}</span></span>`).join('')}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('') + '</div>').join('');
}
/* ref:end */
const state = { f:'all', r:'all', race:'dwarf', cls:'shaman' };
const $ = s => document.querySelector(s);

function roleMatch(c, role) { return role === 'all' || c.roles.includes(role); }
function raceVisible(r) { return state.f === 'all' || r.f === state.f; }
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
function roleChips(c) { return c.roles.map(x => `<span class="chip ${state.r === x ? 'on' : ''} ${x.endsWith('?') ? 'q' : ''}">${ri(x)}${ROLE_RU[x]}</span>`).join(''); }

function pickValid() {
  let r = RC[state.race];
  if (!raceVisible(r)) { r = RACES.find(raceVisible); state.race = r.id; }
  if (!r.can[state.cls]) { state.cls = Object.keys(r.can).find(c => roleMatch(CL[c], state.r)) || Object.keys(r.can)[0]; }
}
function pickClass(id) {
  state.cls = id;
  if (!RC[state.race].can[id]) { const r = RACES.filter(raceVisible).find(x => x.can[id]) || RACES.find(x => x.can[id]); if (r) state.race = r.id; }
  if (!raceVisible(RC[state.race])) { state.f = 'all'; syncSeg('segF', 'all'); }
}
function syncSeg(id, v) { document.querySelectorAll(`#${id} button`).forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v ? 'true' : 'false')); }

function renderMatrix() {
  let h = '<thead><tr><th scope="col">Rasa</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">płatna</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: niedozwolone"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', nowa kombinacja' : ''}`;
        const mark = '<i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>';
        h += `<td><button class="cell ${v}${dim}${sel}" style="--cc:${CCOL[c.id]}" data-r="${r.id}" data-c="${c.id}" aria-label="${esc(label)}" aria-pressed="${sel ? 'true' : 'false'}">${mark}</button></td>`;
      });
      h += '</tr>';
    });
  });
  const mx = $('#matrix');
  mx.innerHTML = h + '</tbody>';
  mx._hc = -1;
}
/* Crosshair: the hovered cell lights up its row (CSS) and its column (here) */
(function () {
  const mx = document.getElementById('matrix');
  const mark = i => {
    if (i === mx._hc) return;
    mx._hc = i;
    mx.querySelectorAll('.hcol').forEach(x => x.classList.remove('hcol'));
    if (i > 0) mx.querySelectorAll(`thead th:nth-child(${i + 1}), tbody tr:not(.fh) > :nth-child(${i + 1})`).forEach(x => x.classList.add('hcol'));
  };
  mx.addEventListener('mouseover', e => { const td = e.target.closest('td'); mark(td ? td.cellIndex : -1); });
  mx.addEventListener('mouseleave', () => mark(-1));
})();

function renderPickM() {
  const r = RC[state.race];
  const races = RACES.filter(raceVisible).map(x => `<button type="button" data-pr="${x.id}" aria-pressed="${x.id === state.race}"><span class="f ${x.f}"></span>${esc(x.n)}</button>`).join('');
  const cls = CLASSES.filter(c => roleMatch(c, state.r)).map(c => {
    const v = r.can[c.id];
    return `<button type="button" data-pc="${c.id}" class="${v ? '' : 'na'}" aria-pressed="${c.id === state.cls}">${esc(c.n)}${v === 'new' ? ' · nowe' : ''}</button>`;
  }).join('');
  $('#pickm').innerHTML = `<div><div class="lbl">1. Rasa</div><div class="chiprow">${races}</div></div>
    <div><div class="lbl">2. Klasa (przerywana linia: niedostępna dla tej rasy, kliknij, aby zmienić rasę)</div><div class="chiprow">${cls}</div></div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Aktywne' : 'Pasywne'}</span><b>${bi(x[1])}</b><span>${esc(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', wymaga pakietu Skyborne' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><img src="../assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}${face(c.id, CCOL[c.id])}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Nowa kombinacja</span>' : ''}${r.paid ? '<span class="tag paid">Płatna rasa</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Specjalizacje</h4><div class="cards">${specs}</div></div>
        <div><h4>Zdolności rasowe</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Levelowanie</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>Na raidach</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Co nowego</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Mój wybór">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Kopiuj mój wybór</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Skopiowano');
  $('#qPick').textContent = `Teraz: ${r.n} · ${c.n}`;
}

function render() { pickValid(); renderMatrix(); renderPickM(); renderDetail(); }
function toPicker() { $('#detail').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'nearest' }); }

document.addEventListener('click', e => {
  const seg = e.target.closest('#segF button, #segR button');
  if (seg) {
    const which = seg.parentElement.id === 'segF' ? 'f' : 'r';
    state[which] = seg.dataset.v; syncSeg(seg.parentElement.id, seg.dataset.v);
    render(); return;
  }
  const cell = e.target.closest('button.cell');
  if (cell) { state.race = cell.dataset.r; state.cls = cell.dataset.c; render(); toPicker(); return; }
  const pr = e.target.closest('[data-pr]');
  if (pr) { state.race = pr.dataset.pr; render(); return; }
  const pc = e.target.closest('[data-pc]');
  if (pc) { pickClass(pc.dataset.pc); render(); return; }
  const go = e.target.closest('button.go');
  if (go) {
    if (go.dataset.r) { state.race = go.dataset.r; if (!raceVisible(RC[state.race])) { state.f = 'all'; syncSeg('segF', 'all'); } }
    if (go.dataset.c) pickClass(go.dataset.c);
    render(); document.getElementById('picker').scrollIntoView({ behavior: 'smooth' });
  }
});
render();
/* Deep link from class pages: #pick=shaman or #pick=dwarf.shaman */
(function () {
  const m = location.hash.match(/^#pick=(?:(\w+)\.)?(\w+)$/);
  if (!m || !CL[m[2]]) return;
  if (m[1] && RC[m[1]] && RC[m[1]].can[m[2]]) { state.race = m[1]; state.cls = m[2]; } else pickClass(m[2]);
  state.f = 'all'; state.r = 'all'; syncSeg('segF', 'all'); syncSeg('segR', 'all'); render();
  setTimeout(() => document.getElementById('picker').scrollIntoView(), 0);
})();
/* Class roster: tall portraits, the hovered or focused one expands */
const ROOT = '../';
const DESC = {
  warrior: 'Plate, rage i pierwsza linia. Przyjmuje ciosy jako tank albo kosi dwuręczniakiem.',
  paladin: 'Święty wojownik w plate: leczy, tankuje i wymachuje młotem. Teraz także w Horde.',
  hunter: 'Łuk, pułapki i wierna bestia u boku. Jedna z najszybciej levelujących klas.',
  rogue: 'Trucizny, ostrza i cień. Czyste obrażenia z zasadzki i kontrola tłumu.',
  priest: 'Światło i Cień w jednych rękach. Główny healer drużyny albo mroczny caster.',
  shaman: 'Totemy i żywioły: leczy, uderza piorunami albo bronią. Teraz także w Alliance.',
  mage: 'Magia ognia, mrozu i arkanów. Portale, jedzenie i woda dla całej ekipy.',
  warlock: 'Klątwy, demony i ogień. Obrażenia w czasie i własny demon do pomocy.',
  druid: 'Miś, kot, sowa albo healer: wszystkie trzy role na jednej postaci.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext}${PV} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Więcej o klasie</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">płatna</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">Więcej o rasie</span></span>
  </a>`).join('');
  });
}
renderPeoples();
function activate(card) { if (!card || card.classList.contains('on')) return; card.parentElement.querySelectorAll('.hc.on').forEach(x => x.classList.remove('on')); card.classList.add('on'); }
document.querySelectorAll('.roster').forEach(ro => {
  ro.addEventListener('mouseover', e => activate(e.target.closest('.hc')));
  ro.addEventListener('focusin', e => activate(e.target.closest('.hc')));
});

/* Faction banners open the picker with that faction */
document.querySelectorAll('.go-f').forEach(b => b.addEventListener('click', () => {
  state.f = b.dataset.fac; syncSeg('segF', state.f); render();
  document.getElementById('picker').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
}));

function raceName(r) { return r.name || r.n; }
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Nie udało się skopiować, zaznacz tekst i naciśnij Ctrl+C'; }
}

/* Dungeons: [name, min, max, entrance zone, new, other sites' ranges where they differ] */
const DUNGEONS = [
  ['Ragefire Chasm', 13, 18, 'Orgrimmar', 0, [], 'horde'],
  ['Hall of Thanes', 13, 18, 'Ironforge', 1, [['Icy Veins', '13–20']]],
  ['Ruins of Lordaeron', 15, 20, 'Tirisfal Glades', 1, [['Icy Veins', '15–22']]],
  ['The Deadmines', 15, 22, 'Westfall', 0, [['Icy Veins', '17–26']]],
  ['Wailing Caverns', 17, 24, 'The Barrens', 0, [['Icy Veins', '15–24']]],
  ['Shadowfang Keep', 20, 26, 'Silverpine Forest', 0, [['Icy Veins', '20–30']]],
  ['Blackfathom Deeps', 22, 28, 'Ashenvale', 0, [['Sportskeeda', '22–26'], ['Icy Veins', '24–32']]],
  ['Excavation Site: Wetlands', 24, 29, 'Wetlands', 1, [['ClassicWoW.gg', '26–31'], ['Icy Veins', '26–33']]],
  ['The Stockade', 25, 29, 'Stormwind City', 0, [['Icy Veins', '24–32']], 'alliance'],
  ['City of Dalaran', 28, 33, 'Alterac Mountains', 1, [['Icy Veins', '28–35']]],
  ['Gnomeregan', 29, 38, 'Dun Morogh', 0],
  ['Razorfen Kraul', 29, 38, 'The Barrens', 0],
  ['Scarlet Monastery: Graveyard', 30, 38, 'Tirisfal Glades', 0],
  ['Scarlet Monastery: Library', 33, 41, 'Tirisfal Glades', 0],
  ['The Drowned City', 35, 40, 'Stranglethorn Vale', 1],
  ['Scarlet Monastery: Armory', 36, 44, 'Tirisfal Glades', 0],
  ['Uldaman', 36, 45, 'Badlands', 0, [['Icy Veins', '41–51']]],
  ['Razorfen Downs', 37, 46, 'The Barrens', 0],
  ['Scarlet Monastery: Cathedral', 38, 46, 'Tirisfal Glades', 0],
  ["Zul'Farrak", 40, 47, 'Tanaris', 0, [['Icy Veins', '44–54']]],
  ["Krol'dok Stronghold", 40, 45, 'Riverglades', 1],
  ['Maraudon', 45, 51, 'Desolace', 0, [['Icy Veins', '46–55']]],
  ['Alcaz Island Prison', 48, 53, 'Dustwallow Marsh', 1],
  ["Temple of Atal'Hakkar", 50, 55, 'Swamp of Sorrows', 0, [['Icy Veins', '50–60']]],
  ['Blackrock Depths', 52, 60, 'Blackrock Mountain', 0],
  ['Blackmaw Hold', 55, 60, 'Azshara', 1],
  ['Lower Blackrock Spire', 57, 60, 'Blackrock Mountain', 0, [['Icy Veins', '55–60']]],
  ['Dire Maul: East', 58, 60, 'Feralas', 0, [['Icy Veins', '54–60']]],
  ["Shaper's Terrace", 58, 60, "Un'Goro Crater", 1],
  ['Stratholme: Living', 58, 60, 'Eastern Plaguelands', 0],
  ['Stratholme: Undead', 58, 60, 'Eastern Plaguelands', 0],
  ['Scholomance', 58, 60, 'Western Plaguelands', 0],
  ['Upper Blackrock Spire', 60, 60, 'Blackrock Mountain', 0, [['Icy Veins', '59–60']]],
  ['Dire Maul: West', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]],
  ['Dire Maul: North', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]]
];
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
const facOk = (d, f) => !f || !d[6] || d[6] === f;   // Ragefire Chasm and The Stockade open from a capital

/* Professions: camp object (tier 1) and the class buff it stands in for */
const PROFS = [
  ['alchemy', 'Alchemy', 1, 'Mana Well', 'jak Blessing of Wisdom'],
  ['blacksmithing', 'Blacksmithing', 1, 'Sharpening Wheel', 'jak Strength of Earth Totem'],
  ['enchanting', 'Enchanting', 1, 'Enchanted Lute', 'jak Mark of the Wild'],
  ['engineering', 'Engineering', 1, 'Reagent Bot', 'sprzedawca reagentów, naprawy na tier 2'],
  ['herbalism', 'Herbalism', 1, 'Incense Candle', 'jak Arcane Intellect'],
  ['leatherworking', 'Leatherworking', 1, 'Camp Tent', 'więcej rested experience'],
  ['mining', 'Mining', 1, 'Lodestone', 'jak Blessing of Might'],
  ['skinning', 'Skinning', 1, 'Camp Chair', 'jak Moonkin Aura'],
  ['tailoring', 'Tailoring', 1, 'Faction Banner', 'jak Divine Spirit'],
  ['cooking', 'Cooking', 0, 'Basic Campfire', 'więcej slotów na obiekty w campie'],
  ['firstaid', 'First Aid', 0, 'First Aid Kit', 'jak Power Word: Fortitude'],
  ['fishing', 'Fishing', 0, 'Fish Bowl', 'jak Blessing of Kings']
];
const PR = Object.fromEntries(PROFS.map(p => [p[0], p]));

/* Game stages: f = fact from the sources, t = our tip */
const SRC = {
  names: ['Icy Veins: rezerwacja nicków', 'https://www.icy-veins.com/wow-forever/name-reservation'],
  names2: ['Team Overpowered: imiona i nazwiska', 'https://teamoverpowered.com/forever/guides/name-reservation/'],
  prof: ['Warcraft Tavern: profesje', 'https://www.warcrafttavern.com/forever/guides/professions/'],
  camp: ['Warcraft Tavern: camping', 'https://www.warcrafttavern.com/forever/guides/camping/'],
  legacy: ['Blizzard: Legacy', 'https://news.blizzard.com/en-gb/article/24307383'],
  dung: ['Warcraft Tavern: dungeony', 'https://www.warcrafttavern.com/forever/guides/dungeons/'],
  ride: ['Warcraft Tavern: jazda wierzchem', 'https://www.warcrafttavern.com/forever/guides/riding/'],
  cwg: ['ClassicWoW.gg: daty i raidy', 'https://classicwow.gg/forever']
};
const STAGES = [
  { id: 'pre', n: 'Przed startem', sub: 'do 04.11', lo: 0, hi: 0,
    todo: [['f', 'Wczesna rezerwacja nicków 27.10 – 03.11 dla posiadaczy pakietów Heroic, Epic i Collection. Kto pierwszy, ten lepszy.'],
      ['f', 'Możesz zarezerwować do trzech postaci na konto. Postać ma imię i nazwisko, a para musi być unikalna w regionie.'],
      ['f', 'Od 04.11 do gry potrzebna jest subskrypcja albo game time.'],
      ['t', 'Wybierz trzy imiona z nazwiskami, plus zapasowe, przed 27.10.']],
    dnote: 'Pierwsze dungeony otwierają się na levelu 13.',
    prof: [['f', 'Każda postać dostaje dwie profesje główne plus wszystkie trzy dodatkowe: Cooking, First Aid i Fishing.'],
      ['f', 'Każda profesja stawia własny obiekt w campie z buffem podobnym do buffa klasowego.'],
      ['t', 'Podzielcie profesje z góry: jedna osoba bierze Cooking do ogniska, reszta wybiera różne, żeby buffy w campie się nie powtarzały.']],
    legacy: [['f', 'Legacy otwiera się z pierwszym punktem: level 25, 150 w profesji (nie zbierackiej) albo odkrycie całej mapy.'],
      ['f', 'Na starcie postać może wydać maksymalnie 16 punktów, reszta trafia na ścieżkę nagród.']],
    group: [['t', 'Ustalcie jedną frakcję i jeden tryb: grupować się można tylko w obrębie trybu, a w PvP konto ma jedną frakcję.'],
      ['t', 'Złóż skład w kreatorze drużyny: tank, healer i różne klasy dla buffów.']],
    src: ['names', 'names2', 'prof', 'legacy'] },
  { id: 'first', n: 'Pierwsze dni', sub: 'levele 1–15', lo: 1, hi: 15,
    todo: [['f', 'Skyborne zaczynają na Zephras Isle, levele 1–12.'],
      ['f', 'Talenty otwierają się na levelu 10 albo na 9 z perkiem Legacy Talented (przy 5 rangach na 5).'],
      ['f', 'Większość gotowanego jedzenia daje bonus do expa. Stackuje się z campem i Cozy Sleeping Bag.'],
      ['t', 'Zbieraj rest: wyloguj się w karczmie albo w campie z namiotem.']],
    prof: [['f', 'Podstawowe ognisko nie wymaga Cooking i mieści 3 obiekty. Pali się ok. 10 minut, a nowe możesz postawić po 5.'],
      ['f', 'Aby dostać buffy z campu, usiądź obok (/sit) na co najmniej minutę.'],
      ['t', 'Zacznij zbieranie od pierwszych leveli: zioła, ruda i skóry napędzają rzemiosło, a 150 w profesji rzemieślniczej otwiera Legacy.']],
    legacy: [['f', 'Na razie bez perków: pierwszy punkt przychodzi na levelu 25 albo ze 150 w profesji.'],
      ['t', 'Gdy Legacy się otworzy, najpierw bierz perki na exp i camp: Well Rested, Field Guide, Permanence. Talented przyda się altom.']],
    group: [['t', 'Leveluj w tej samej strefie i rozbijaj camp na każdym postoju: pięć minut przy ognisku zwraca się buffami dla całej grupy.'],
      ['t', 'Złóż pierwszą piątkę do levelu 13–15.']],
    src: ['camp', 'legacy', 'dung'] },
  { id: 'dung', n: 'Dungeony', sub: 'levele 15–40', lo: 15, hi: 40,
    todo: [['f', 'Najwięcej expa z dungeonu dają jego łańcuchy questów. Powtórne runy po nich dają wyraźnie mniej expa niż questowanie w świecie.'],
      ['f', 'Każdy przedmiot, który wypadnie, odblokowuje swój wygląd do transmogu dla każdego, kto może go nosić, nawet jeśli przedmiot dostał ktoś inny.'],
      ['f', 'Legacy otwiera się na levelu 25.'],
      ['t', 'Najpierw zbierzcie questy do dungeonu całą grupą i wejdźcie, gdy wszyscy je mają.']],
    prof: [['f', 'Cooking 140 daje 5 slotów w campie, 220 daje 10.'],
      ['f', 'Każda profesja robi trzy obiekty do campu, po jednym na tier. Źródła różnią się co do skilla potrzebnego na tier 2 i 3.'],
      ['t', 'Jeśli do levelu 25 jeszcze daleko, podnieś profesję rzemieślniczą do 150: Legacy otworzy się szybciej.']],
    legacy: [['f', 'Każde wyzwanie daje 1 punkt. Jest ich 65: klasy 27, profesje 18, PvP 12, dungeony 3, raidy 3, przygoda 2.'],
      ['t', 'Warto wziąć Reagent Economy (bez kupowanych reagentów do zdolności) i Field Guide (krótszy cooldown obiektów campu).']],
    group: [['f', 'Dungeon jest zaprojektowany na 5 graczy: tank, healer i trzech DPS-ów.'],
      ['f', 'Nie ma skalowania leveli, więc znajomy, który jest daleko w tyle, będzie miał ciężko w dungeonie.'],
      ['t', 'Trzymajcie levele blisko: kto zostaje w tyle, nadrabia na questach, a dungeony robicie razem.']],
    src: ['dung', 'camp', 'legacy'] },
  { id: 'path', n: 'Droga do 60', sub: 'levele 40–60', lo: 40, hi: 60,
    todo: [['f', 'Wierzchowiec na levelu 40 (60% szybkości), szybki na 60 (100%). Trenuj u trenera swojej rasy.'],
      ['f', 'Paladyni i warlocki dostają wierzchowca przez questy klasowe.'],
      ['f', 'Honored u własnej frakcji daje 10% zniżki na trening jazdy i wierzchowce. Według Warcraft Tavern: 100 + 20 golda na 40 levelu, 1000 + 200 na 60.'],
      ['t', 'Oszczędzaj złoto na level 40: jazda wierzchem będzie twoim największym wydatkiem w drodze do 60.']],
    prof: [['f', 'Każda profesja ma własne obiekty campu na tier 2 i 3. Drugi obiekt Engineering, Repair Bot, naprawia ekwipunek.'],
      ['t', 'Miejcie w grupie Cooking 220, żeby camp mieścił 10 obiektów: na raidy starczy miejsca dla wszystkich.']],
    legacy: [['f', 'Maksymalnie 16 punktów na postać, reszta trafia na ścieżkę nagród: zabawka za 15, zwierzak za 25, tabard za 40, wierzchowiec za 55.']],
    group: [['f', 'Raidy otwierają się 09.12: Barrow Deeps na 10 graczy, Hyjal Summit na 20, Onyxia’s Lair na 40.'],
      ['t', 'Raid na 10 graczy wymaga 10 graczy: jeśli jest was mniej, poszukajcie reszty w gildii z wyprzedzeniem.']],
    src: ['ride', 'prof', 'legacy', 'cwg'] },
  { id: 'raid', n: '60 i raidy', sub: 'od 09.12', lo: 60, hi: 60,
    todo: [['f', '09.12 otwierają się Barrow Deeps (10 graczy), Hyjal Summit (20) i Onyxia’s Lair (40, Dustwallow Marsh).'],
      ['f', 'Wyczyszczenie każdego z trzech raidów daje punkt Legacy.'],
      ['f', 'Nowy battleground 15v15: Darkspear Islands u wybrzeży Dustwallow Marsh.'],
      ['t', 'Zanim zbierzecie ludzi na raid, róbcie dungeony na level 60 dla ekwipunku.']],
    prof: [['f', 'Buffy z campu są trochę słabsze od klasowych i się z nimi nie stackują: Blessing of Kings daje 10% do wszystkich statystyk, camp daje 8%.'],
      ['t', 'Rozbij camp przy wejściu do raidu: jego buffy pokryją to, czego brakuje waszym klasom.']],
    legacy: [['f', 'Wyzwania na level 60: dungeony 3, raidy 3, PvP 12. PvP ma rangi z tygodniowym limitem i ulepszenia ekwipunku za Honor.']],
    group: [['f', 'Te same buffy od dwóch graczy jednej klasy się nakładają, różne klasy się stackują.'],
      ['t', 'Złóż skład raidu w kreatorze drużyny i wrzuć link na czat.']],
    src: ['cwg', 'prof', 'legacy'] }
];
const ST = Object.fromEntries(STAGES.map(s => [s.id, s]));
const D_REL = new Date('2026-11-04T23:00:00Z'), D_RAID = new Date('2026-12-09T00:00:00');

/* My character, saved in this browser */
const RR = ['tank', 'heal', 'dps'];
function roleOpts(c) { return RR.filter(x => c.roles.includes(x) || (x === 'tank' && c.roles.includes('tank?'))); }
const MEKEY = 'gabella-wf-me';
const me = { race: '', cls: '', role: '', lvl: 0, p1: '', p2: '', sec: [] };
try { const v = JSON.parse(localStorage.getItem(MEKEY) || '{}'); if (v && typeof v === 'object') Object.keys(me).forEach(k => { if (v[k] !== undefined) me[k] = v[k]; }); } catch (e) {}
function fixMe() {
  if (!RC[me.race]) me.race = '';
  if (!CL[me.cls] || (me.race && !RC[me.race].can[me.cls])) me.cls = '';
  const ro = me.cls ? roleOpts(CL[me.cls]) : [];
  if (!ro.includes(me.role)) me.role = (me.cls && CL[me.cls].roles.find(r => ro.includes(r))) || ro[0] || '';
  me.lvl = Math.max(0, Math.min(60, parseInt(me.lvl, 10) || 0));
  if (!PR[me.p1] || !PR[me.p1][2]) me.p1 = '';
  if (!PR[me.p2] || !PR[me.p2][2] || me.p2 === me.p1) me.p2 = '';
  me.sec = Array.isArray(me.sec) ? me.sec.filter(x => PR[x] && !PR[x][2]) : [];
}
function saveMe() { try { localStorage.setItem(MEKEY, JSON.stringify(me)); } catch (e) {} }
const meSet = () => !!(me.race || me.cls || me.lvl);
let stageSel = null, stageAuto = true;
function autoStage() {
  const now = new Date();
  if (now < D_REL) return ['pre', 'Wybrane według daty: przed startem 04.11.'];
  if (me.lvl) return [me.lvl < 15 ? 'first' : me.lvl < 40 ? 'dung' : me.lvl < 60 ? 'path' : 'raid', 'Wybrane według levelu twojej postaci.'];
  if (now >= D_RAID) return ['raid', 'Wybrane według daty: raidy są otwarte.'];
  return [now < new Date('2026-11-11T00:00:00') ? 'first' : 'dung', 'Wybrane według daty. Dodaj level swojej postaci, a etap będzie za nim podążał.'];
}
const START = { pre: 'hero_dawn-960', first: 'hero_campfire-960', dung: 'warlock-360', path: 'hunter-360', raid: 'paladin-360' };
const ARTV = /*ARTV*/{"hero_campfire-960.avif":"?v=93981d6a","hero_campfire-960.webp":"?v=5aa0e1b2","hero_dawn-960.avif":"?v=447302fd","hero_dawn-960.webp":"?v=b2d0d95b"};   // ?v= of the scene arts, filled in by build.art_version (same names, redrawn pictures)
const pic = f => `<picture><source type="image/avif" srcset="${ROOT}assets/art/${f}.avif${ARTV[f + '.avif'] || ''}"><img src="${ROOT}assets/art/${f}.webp${ARTV[f + '.webp'] || ''}" alt="" loading="lazy" decoding="async"></picture>`;
const tipL = () => '<span class="tl">Porada</span>';
function liC(x) { return x[0] === 't' ? `<li class="tip">${tipL()}${esc(x[1])}</li>` : `<li>${esc(x[1])}</li>`; }
function dLi(d) {
  const mine = me.lvl && nearLvl(d, me.lvl);
  return `<li class="${mine ? 'mine' : ''}"><b>${esc(d[0])}</b><span class="lvl${mine ? ' gold' : ''}">${lvRange(d)}</span><span class="z">${esc(d[3])}${d[4] ? ' · <i>nowe</i>' : ''}${mine ? '<span class="sr"> · na twój level</span>' : ''}</span></li>`;
}
function renderStage() {
  const [auto, why] = autoStage();
  if (stageAuto) stageSel = auto;
  const s = ST[stageSel];
  $('#stageBar').innerHTML = STAGES.map(x => `<button type="button" class="stile" role="tab" id="tab-${x.id}" data-st="${x.id}" aria-controls="stagePanel" aria-selected="${x.id === stageSel}" tabindex="${x.id === stageSel ? 0 : -1}">${pic(START[x.id])}<b>${esc(x.n)}</b><span class="lv">${esc(x.sub)}${x.id === auto ? ' · <span class="now">teraz</span>' : ''}</span></button>`).join('');
  let ds;
  if (s.id === 'pre') ds = DUNGEONS.filter(d => d[1] <= 15);
  else ds = DUNGEONS.filter(d => d[1] <= s.hi && d[2] >= s.lo);
  if (me.lvl && s.lo <= me.lvl && me.lvl <= Math.max(s.hi, 1)) ds = ds.filter(d => nearLvl(d, me.lvl)).concat(ds.filter(d => !nearLvl(d, me.lvl)));
  const MAXD = 6, extra = ds.length - MAXD;
  let k = 0;
  const steps = s.todo.map(x => x[0] === 't'
    ? `<li class="tip"><p>${tipL()}${esc(x[1])}</p></li>`
    : `<li><span class="n">${++k}</span><p>${esc(x[1])}</p></li>`).join('');
  $('#stagePanel').setAttribute('aria-labelledby', 'tab-' + s.id);
  $('#stagePanel').innerHTML = `<div class="st-head"><div class="t"><h3>${esc(s.n)}</h3><span class="when">${esc(s.sub)}</span></div><p class="why">${stageAuto ? esc(why) : 'Etap wybrany ręcznie.'}</p></div>
    <ol class="steps-c">${steps}</ol>
    <div class="st-cols">
      <div><h4>Dungeony na ten level</h4>${s.dnote ? `<p class="small" style="margin:-4px 0 10px">${esc(s.dnote)}</p>` : ''}<ul class="dlist">${ds.slice(0, MAXD).map(dLi).join('')}</ul>
        <a class="more-l" href="guides/dungeons/">${extra > 0 ? `Więcej dungeonów w tabeli: ${extra}` : 'Wszystkie 35 dungeonów'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
      <div style="display:grid;gap:24px;align-content:start"><div><h4>Profesje i camp</h4><ul class="clean">${s.prof.map(liC).join('')}</ul></div>
        <div><h4>Perki Legacy</h4><ul class="clean">${s.legacy.map(liC).join('')}</ul></div></div>
    </div>
    <div class="gtip"><h4 style="margin:0 0 10px;font-size:var(--fs-16)">Porady dla grupy</h4><ul class="clean">${s.group.map(liC).join('')}</ul></div>
    <p class="st-src"><span>Źródła:</span>${s.src.map(k2 => `<a href="${SRC[k2][1]}" target="_blank" rel="noopener">${esc(SRC[k2][0])}</a>`).join('')}</p>`;
}
function optList(items, cur, none) { return `<option value="">${esc(none)}</option>` + items.map(([v, t]) => `<option value="${v}"${v === cur ? ' selected' : ''}>${esc(t)}</option>`).join(''); }
function renderMe() {
  fixMe();
  const races = f => RACES.filter(r => r.f === f).map(r => `<option value="${r.id}"${r.id === me.race ? ' selected' : ''}>${esc(r.n)}</option>`).join('');
  $('#meRace').innerHTML = `<option value="">Nie wybrano</option><optgroup label="${facName('alliance')}">${races('alliance')}</optgroup><optgroup label="${facName('horde')}">${races('horde')}</optgroup>`;
  const cls = (me.race ? Object.keys(RC[me.race].can) : CLASSES.map(c => c.id)).map(id => [id, CL[id].n]);
  $('#meCls').innerHTML = optList(cls, me.cls, 'Nie wybrano');
  $('#meRole').innerHTML = me.cls ? roleOpts(CL[me.cls]).map(x => `<option value="${x}"${x === me.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('') : `<option value="">Najpierw wybierz klasę</option>`;
  $('#meRole').disabled = !me.cls;
  const prim = PROFS.filter(p => p[2]);
  $('#meP1').innerHTML = optList(prim.filter(p => p[0] !== me.p2).map(p => [p[0], p[1]]), me.p1, 'Brak');
  $('#meP2').innerHTML = optList(prim.filter(p => p[0] !== me.p1).map(p => [p[0], p[1]]), me.p2, 'Brak');
  $('#meSec').innerHTML = PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${me.sec.includes(p[0])}">${esc(p[1])}</button>`).join('');
  document.querySelectorAll('.lvin').forEach(i => { if (document.activeElement !== i) i.value = me.lvl || ''; });
  const who = [me.race ? RC[me.race].n : '', me.cls ? CL[me.cls].n : ''].filter(Boolean).join(' · ');
  const sub = me.cls ? [ROLE_RU[me.role], me.race ? facName(RC[me.race].f) : ''].filter(Boolean).join(' · ') : 'Wybierz rasę, klasę i level poniżej';
  const hero = $('#meHero');
  hero.style.setProperty('--cc', me.cls ? CCOL[me.cls] : '#c9a54a');
  hero.innerHTML = pic(me.cls ? `${me.cls}-600` : 'hero_campfire-960') + (me.lvl ? `<span class="lvb" aria-label="Level ${me.lvl}">${me.lvl}</span>` : '')
    + `<span class="k">Moja postać</span><b>${who ? esc(who) : 'Jeszcze nie utworzono'}</b><span class="s">${esc(sub)}</span>`;
  let out = '';
  if (meSet()) {
    const b = [];
    if (me.cls) b.push(BUFF[me.cls] ? `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span><b>${esc(CL[me.cls].n)}:</b> ${esc(BUFF[me.cls])}</span></li>` : `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-dps"/></svg></span><span>${esc(CL[me.cls].n)}: brak buffa grupowego, czyste obrażenia.</span></li>`);
    [me.p1, me.p2, ...me.sec].filter(Boolean).forEach(id => { const p = PR[id]; b.push(`<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg></span><span><b>${esc(p[3])}</b> <span class="m">· ${esc(p[1])}</span><br>${esc(p[4])}</span></li>`); });
    if (!b.length) b.push('<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span>Wybierz klasę i profesje, aby zobaczyć swoje buffy.</span></li>');
    out += `<div><h4>Co wnosisz do grupy</h4><ul class="buffs">${b.join('')}</ul></div>`;
    if (me.lvl) {
      const ds = DUNGEONS.filter(d => nearLvl(d, me.lvl) && facOk(d, me.race && RC[me.race].f));
      out += `<div><h4>Dungeony na twój level</h4>` + (ds.length ? `<ul class="dlist">${ds.slice(0, 4).map(dLi).join('')}</ul>` : '<p class="small">Pierwsze dungeony zaczynają się od levelu 13.</p>')
        + `<a class="more-l" href="guides/dungeons/">${ds.length > 4 ? `Więcej dungeonów w tabeli: ${ds.length - 4}` : 'Tabela dungeonów'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`;
    }
  }
  $('#meOut').innerHTML = out;
  $('#meReset').disabled = !meSet() && !me.p1 && !me.p2 && !me.sec.length;
}
function renderJourney() { renderMe(); renderStage(); }
function meChanged() { fixMe(); saveMe(); stageAuto = true; renderJourney(); }
$('#meRace').addEventListener('change', e => { me.race = e.target.value; meChanged(); });
$('#meCls').addEventListener('change', e => { me.cls = e.target.value; if (me.cls && !me.race) { const r = RACES.find(x => x.can[me.cls] && !x.paid); if (r) me.race = r.id; } meChanged(); });
$('#meRole').addEventListener('change', e => { me.role = e.target.value; meChanged(); });
$('#meP1').addEventListener('change', e => { me.p1 = e.target.value; meChanged(); });
$('#meP2').addEventListener('change', e => { me.p2 = e.target.value; meChanged(); });
$('#meSec').addEventListener('click', e => { const b = e.target.closest('[data-sec]'); if (!b) return; const id = b.dataset.sec; me.sec = me.sec.includes(id) ? me.sec.filter(x => x !== id) : me.sec.concat(id); meChanged(); });
$('#meReset').onclick = () => { Object.assign(me, { race: '', cls: '', role: '', lvl: 0, p1: '', p2: '', sec: [] }); meChanged(); };
document.querySelectorAll('.stepper .lvm, .stepper .lvp').forEach(b => b.addEventListener('click', () => { me.lvl = Math.max(1, Math.min(60, (me.lvl || (b.classList.contains('lvp') ? 0 : 2)) + (b.classList.contains('lvp') ? 1 : -1))); meChanged(); }));
document.querySelectorAll('.lvin').forEach(i => {
  i.addEventListener('change', () => { me.lvl = i.value === '' ? 0 : parseInt(i.value, 10) || 0; meChanged(); });
  i.addEventListener('keydown', e => { if (e.key === 'Enter') i.blur(); });
});
$('#stageBar').addEventListener('click', e => { const b = e.target.closest('[data-st]'); if (!b) return; stageSel = b.dataset.st; stageAuto = false; renderStage(); $('#tab-' + stageSel).focus(); });
$('#stageBar').addEventListener('keydown', e => {
  const k = { ArrowRight: 1, ArrowLeft: -1 }[e.key]; if (!k) return;
  const i = (STAGES.findIndex(s => s.id === stageSel) + k + STAGES.length) % STAGES.length;
  stageSel = STAGES[i].id; stageAuto = false; renderStage(); const t = $('#tab-' + stageSel); t.focus(); t.scrollIntoView({ block: 'nearest', inline: 'nearest' }); e.preventDefault();
});
if (meSet() && matchMedia('(max-width: 980px)').matches) $('#meD').open = false;
renderJourney();
setTimeout(() => { const t = $('#tab-' + stageSel), bar = $('#stageBar'); if (t && matchMedia('(max-width: 719px)').matches) bar.scrollLeft += t.getBoundingClientRect().left - bar.getBoundingClientRect().left - 16; }, 0);
