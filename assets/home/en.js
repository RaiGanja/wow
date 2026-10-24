const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Warrior', s:'Warrior', roles:['tank','dps'],
    specs:[['Arms','Melee damage (two-handed weapon)',['dps']],['Fury','Melee damage (dual wield)',['dps']],['Protection','Tank',['tank']]],
    lvl:'The slowest leveling, about 12% longer than average',
    lp:12,
    raid:'Battle Shout affects the whole raid',
    forever:'More Rage, better threat on groups of targets, the Weapon Master talent. Fury and Bloodthirst are weakened.' },
  { id:'paladin', n:'Paladin', roles:['tank','heal','dps'],
    specs:[['Holy','Healer',['heal']],['Protection','Tank',['tank']],['Retribution','Melee damage',['dps']]],
    lvl:'Average leveling pace',
    lp:0,
    raid:'Blessing of Kings is now baseline. Per beta lists, Protection is among the strongest tanks, and Retribution dropped after the 15 October patch.',
    forever:'Holy Strike from level 6, Judgement does not consume the seal. Undead can now be paladins, so the class appeared for the Horde.' },
  { id:'hunter', n:'Hunter', roles:['dps'],
    specs:[['Beast Mastery','Ranged damage, a lot of damage from the pet',['dps']],['Marksmanship','Ranged damage',['dps']],['Survival','Melee and ranged, traps',['dps']]],
    lvl:'The fastest leveling, about 8% faster than average',
    lp:-8,
    raid:'Trueshot Aura affects the whole raid',
    forever:'You can play without a pet, traps work in combat, foxes appeared as a pet family. Survival can go melee.' },
  { id:'rogue', n:'Rogue', roles:['dps'],
    specs:[['Assassination','Poison damage',['dps']],['Combat','Fast weapon attacks',['dps']],['Subtlety','Ambushes, bleeds',['dps']]],
    lvl:'Average leveling pace',
    lp:0,
    raid:'Pure melee damage with no raid-wide buffs',
    forever:'One-handed axes can now be used. Assassination is built on poisons, Subtlety on bleeds and stealth.' },
  { id:'priest', n:'Priest', roles:['heal','dps'],
    specs:[['Discipline','Healer, shields and absorption',['heal']],['Holy','Healer',['heal']],['Shadow','Ranged damage',['dps']]],
    lvl:'About 5% slower than average',
    lp:5,
    raid:'Divine Spirit is now baseline. Shadow damage and Devouring Plague (24 sec cooldown) were buffed by the 15 October patch.',
    forever:'Fear Ward and Devouring Plague are available from level 20 to any race. Each race has two of its own priest spells.' },
  { id:'shaman', n:'Shaman', roles:['heal','dps','tank?'],
    specs:[['Elemental','Ranged damage',['dps']],['Enhancement','Melee damage. Tanking ability is still in question',['dps','tank?']],['Restoration','Healer',['heal']]],
    lvl:'Average leveling pace',
    lp:0,
    raid:'Strength of Earth, Windfury, Flametongue and Grace of Air totems buff their own party',
    forever:'Dwarves can now be shamans, so the class appeared for the Alliance. Lava Burst was buffed, Elemental rose in the damage rankings.' },
  { id:'mage', n:'Mage', roles:['dps'],
    specs:[['Arcane','Burst, lots of mana',['dps']],['Fire','Crits and ignites',['dps']],['Frost','Damage and control',['dps']]],
    lvl:'The fastest leveling, about 8% faster than average (about 12 hours saved)',
    lp:-8,
    raid:'Portals and food and water for the whole group',
    forever:'Fire got Hotstreak, Arcane got Arcane Blast, Frost got Ice Lance. Frostfire Bolt is available from level 40.' },
  { id:'warlock', n:'Warlock', roles:['dps'],
    specs:[['Affliction','Damage from curses and corruption',['dps']],['Demonology','Damage through demons',['dps']],['Destruction','Direct fire and shadow damage',['dps']]],
    lvl:'Average leveling pace',
    lp:0,
    raid:'Shadow Mastery now gives 2–10% shadow damage (was 1–5%)',
    forever:'Affliction has a new channeled spell, the demon stays with Demonic Sacrifice, Destruction gained Incinerate and AoE.' },
  { id:'druid', n:'Druid', roles:['tank','heal','dps'],
    specs:[['Balance','Ranged damage',['dps']],['Feral','Tank (bear) and melee damage (cat)',['tank','dps']],['Restoration','Healer, lots of healing over time',['heal']]],
    lvl:'About 5% slower than average',
    lp:5,
    raid:'Leader of the Pack and Moonkin Aura affect the whole raid and stack',
    forever:'Each specialization got a clear role, forms work with potions and weapon enchants. You can be a tank, healer and fighter on one character.' }
];
const ROLE_RU = { tank:'Tank', heal:'Healer', dps:'Damage', 'tank?':'Tank (uncertain)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Battle Shout', paladin:'Blessing of Kings', hunter:'Trueshot Aura', priest:'Power Word: Fortitude, Divine Spirit', shaman:'Totems (Strength of Earth, Windfury, Flametongue, Grace of Air)', mage:'Arcane Intellect, portals, food and water', druid:'Mark of the Wild, Leader of the Pack, Moonkin Aura' };

const RACES = [
  { id:'human', n:'Human', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Will to Survive','Removes stun'],['a','Perception','Reveals invisible enemies for 20 sec'],['p','Ruthless','+2% crit chance'],['p','The Human Spirit','+5% spirit']],
    tip:'Spirit goes into healing for a Holy Priest, so a Human priest is good for healing.' },
  { id:'dwarf', n:'Dwarf', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Stoneform','Immunity to bleeds, poisons and diseases for 8 sec and reduced physical damage'],['a','Find Treasure','Shows nearby chests'],['p','Earth Fury','+2% crit damage and healing power'],['p','Big Game Hunter','+5% damage to beasts']],
    tip:'Stoneform is useful for tanks and in PvP.' },
  { id:'nightelf', n:'Night Elf', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Elune’s Light','+10% crit chance for 15 sec'],['a','Shadowmeld','Invisibility on the spot'],['p','Quickness','+1% dodge and +2% run speed'],['p','Wisp Spirit','+75% run speed as a spirit']],
    tip:'The only Alliance race with a druid, unless you take Skyborne.' },
  { id:'gnome', n:'Gnome', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Escape Artist','Brief immunity to slows and roots'],['a','Eureka!','The next 3 abilities are cheaper and 10% stronger'],['p','Expansive Mind','+5% maximum mana, rage or energy'],['p','Engineering Specialization','Engineering devices work more reliably']],
    tip:'Expansive Mind especially helps energy classes.' },
  { id:'skyA', n:'Skyborne (Alliance)', f:'alliance', paid:true, name:'High Order Skyborne',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Glide down for 10 sec, no fall damage'],['a','Read Ley Line','+100% health and mana regeneration'],['p','Wind Blessed','+3% attack and spell speed'],['p','Elemental Insight','+5% damage to elementals']],
    tip:'Paid race: Heroic Pack from $29.99. Starts in the Zephras Isle location (levels 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Blood Fury','+10% attack power and spell power for 15 sec'],['a','Shatter Curse','Removes curses and corruption, −5% magic damage taken for 8 sec'],['p','Savage','+1% crit chance'],['p','Hardiness','Stuns are 20% shorter']],
    tip:'Blood Fury gives a powerful damage window.' },
  { id:'undead', n:'Undead', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Will of the Forsaken','Removes charm, fear and sleep'],['a','Cannibalize','Restores 35% health and mana over time'],['p','Underwater Breathing','Breathe underwater longer'],['p','Touch of the Grave','Chance to drain health on attack']],
    tip:'New combination: a paladin for the Horde, where this class did not exist before.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','War Stomp','Stuns nearby enemies for 2 sec'],['a','Cultivation','Grows herbs that can be gathered without Herbalism'],['p','Plainsrunning','Speed increases while you run'],['p','Endurance','+5% health and +2% crit damage']],
    tip:'The only Horde race with a druid, unless you take Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserking','+10% attack and spell speed for 10 sec'],['a','Rapid Regeneration','Restores health over time'],['p','Beast Slaying','+5% damage to beasts'],['p','Regeneration','Health regenerates in combat too']],
    tip:'The most class options in the Horde: seven.' },
  { id:'skyH', n:'Skyborne (Horde)', f:'horde', paid:true, name:'Windshaper Skyborne',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Glide down for 10 sec, no fall damage'],['a','Skysight','+10% run speed'],['p','Wind Blessed','+3% attack and spell speed'],['p','Elemental Insight','+5% damage to elementals']],
    tip:'Paid race: Heroic Pack from $29.99. Only the Horde can have a shaman, only the Alliance a mage.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "The most numerous race of the Alliance. Versatile and strong in PvP thanks to Will to Survive.", "dwarf": "Sturdy miners and riflemen of Ironforge. For the first time in Classic the Alliance has shamans, and they are dwarves.", "nightelf": "An ancient people of the forests. Elusive: their own way to hide, dodge and fast running.", "gnome": "The inventors of Gnomeregan. Small, cunning and with the best escape ability in the game.", "skyA": "A new race in Forever. The High Order: wind elves seeking the lost arcane magic of their ancestors.", "orc": "The heart of the Horde. The strongest warriors and PvP masters thanks to Blood Fury and Hardiness.", "undead": "The Forsaken: former humans who broke free of the Lich King. Immune to fear and sleep when it counts.", "tauren": "Peaceful giants of the plains. The most health and their own area stun.", "troll": "The Darkspear tribe. The most classes in the Horde and a strong Berserking for damage.", "skyH": "A new race in Forever. The Windshapers: spiritual leaders of the Skyborne, close to the elements."}; // race page leads and URL slugs, filled in by build.py
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
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Tip</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Alliance' : 'Horde'; }
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp?v=0003354e" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Faster by ${-p}%` : p > 0 ? `Slower by ${p}%` : 'Average pace';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>faster</span><span>slower</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Class</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Leveling</span><span>In raids</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp?v=0003354e')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Roles: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Race</span><span>Classes</span><span class="abl">Abilities <span class="abt">active</span><span class="abt p">passive</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp?v=0003354e')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">paid</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Classes: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', new' : v ? '' : ', not available')); }).join('')}</span>
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
  let h = '<thead><tr><th scope="col">Race</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">paid</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: not allowed"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', new combination' : ''}`;
        const mark = v === 'new' && !sel ? '<span class="nw">new</span>' : '<i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>';
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
    return `<button type="button" data-pc="${c.id}" class="${v ? '' : 'na'}" aria-pressed="${c.id === state.cls}">${esc(c.n)}${v === 'new' ? ' · new' : ''}</button>`;
  }).join('');
  $('#pickm').innerHTML = `<div><div class="lbl">1. Race</div><div class="chiprow">${races}</div></div>
    <div><div class="lbl">2. Class (dashed: not available to this race, tap to switch race)</div><div class="chiprow">${cls}</div></div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Active' : 'Passive'}</span><b>${bi(x[1])}</b><span>${esc(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', Skyborne pack required' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><img src="../assets/art/${c.id}-600.webp?v=0003354e" width="600" height="804" alt="" loading="lazy" decoding="async"></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}${face(c.id, CCOL[c.id])}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">New combination</span>' : ''}${r.paid ? '<span class="tag paid">Paid race</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Specializations</h4><div class="cards">${specs}</div></div>
        <div><h4>Racial abilities</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Leveling</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>In raids</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>What’s new</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="My choice">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copy my choice</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copied');
  $('#qPick').textContent = `Now: ${r.n} · ${c.n}`;
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
  warrior: 'Plate, rage and the front line. Takes the hits as a tank or cleaves with a two-hander.',
  paladin: 'A holy warrior in plate: heals, tanks and swings a hammer. Now on the Horde too.',
  hunter: 'Bow, traps and a loyal beast at your side. One of the fastest classes to level.',
  rogue: 'Poisons, blades and shadow. Pure damage from ambush and crowd control.',
  priest: 'Light and Shadow in one pair of hands. The group’s main healer or a dark caster.',
  shaman: 'Totems and elements: heals, strikes with lightning or weapons. Now on the Alliance too.',
  mage: 'Fire, frost and arcane magic. Portals, food and water for the whole crew.',
  warlock: 'Curses, demons and fire. Damage over time and a demon of your own to help.',
  druid: 'Bear, cat, owl or healer: all three roles on one character.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext}?v=0003354e ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp?v=0003354e" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">More about the class</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp?v=0003354e" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">paid</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">More about the race</span></span>
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

/* Group builder */
const MAXT = 40, PARTY = 5;
const SIZES = [5, 6, 8, 10, 15, 20, 25, 40];
const RR = ['tank', 'heal', 'dps'];
const POOL = {
  tank: ['paladin', 'warrior', 'druid'],
  heal: ['priest', 'shaman', 'paladin', 'druid'],
  dps: ['mage', 'hunter', 'warlock', 'rogue', 'shaman', 'druid', 'warrior']
};
const RAIDS = [[10, 'Barrow Deeps'], [20, 'Hyjal Summit'], [40, 'Onyxia’s Lair']];
const team = { f: 'alliance', list: [] };

function roleOpts(c) { return RR.filter(x => c.roles.includes(x) || (x === 'tank' && c.roles.includes('tank?'))); }
function raceFor(cls, f, k) {
  const free = RACES.filter(r => r.f === f && !r.paid && r.can[cls]);
  return free.length ? free[k % free.length].id : (RACES.find(r => r.f === f && r.can[cls]) || RACES.find(r => r.f === f)).id;
}
function partyRoles(k) {
  if (k >= 5) return ['tank', 'heal', 'dps', 'dps', 'dps'];
  return { 1: ['dps'], 2: ['tank', 'heal'], 3: ['tank', 'heal', 'dps'], 4: ['tank', 'heal', 'dps', 'dps'] }[k];
}
function autoTeam(n, f) {
  const out = [], used = { tank: 0, heal: 0, dps: 0 };
  for (let left = n, g = 0; left > 0; left -= PARTY, g++) {
    partyRoles(Math.min(PARTY, left)).forEach(role => {
      const pool = POOL[role].filter(c => RACES.some(r => r.f === f && r.can[c]));
      const cls = pool[used[role]++ % pool.length];
      out.push({ race: raceFor(cls, f, out.length), cls, role });
    });
  }
  return out;
}
function fixSlot(s) {
  const races = RACES.filter(r => r.f === team.f);
  let r = RC[s.race]; if (!r || r.f !== team.f) r = races.find(x => x.can[s.cls]) || races[0];
  s.race = r.id;
  const cls = Object.keys(r.can); if (!r.can[s.cls]) s.cls = cls[0];
  const ro = roleOpts(CL[s.cls]); if (!ro.includes(s.role)) s.role = ro[0];
}
function readHash() {
  const m = location.hash.match(/^#team=([^;]+);(.*)$/);
  if (!m || !['alliance', 'horde'].includes(m[1])) return false;
  const list = m[2].split(',').map(x => x.split('.')).filter(x => x.length === 3 && RC[x[0]] && CL[x[1]] && RR.includes(x[2])).slice(0, MAXT);
  if (!list.length) return false;
  team.f = m[1]; team.list = list.map(x => ({ race: x[0], cls: x[1], role: x[2] }));
  return true;
}
const fromLink = readHash();
function teamLink() { return location.origin + location.pathname + '#team=' + team.f + ';' + team.list.map(s => `${s.race}.${s.cls}.${s.role}`).join(','); }
function raceName(r) { return r.name || r.n; }
function countRoles(list) { const c = { tank: 0, heal: 0, dps: 0 }; list.forEach(s => c[s.role]++); return c; }
let teamTouched = fromLink;
function renderTeam() {
  team.list.forEach(fixSlot);
  const n = team.list.length;
  syncSeg('segBF', team.f);
  $('#sizes').innerHTML = SIZES.map(x => `<button type="button" data-n="${x}" aria-pressed="${x === n}">${x}</button>`).join('');
  $('#szOut').textContent = n;
  const parties = Math.ceil(n / PARTY);
  $('#szNote').textContent = n ? `${parties} groups of 5${n % PARTY ? ', the last one is incomplete' : ''}` : '';
  const races = RACES.filter(r => r.f === team.f);
  let html = '';
  for (let g = 0; g < parties; g++) {
    const part = team.list.slice(g * PARTY, g * PARTY + PARTY), c = countRoles(part);
    const need = [];
    if (!c.tank) need.push('no tank'); if (!c.heal) need.push('no healer'); if (part.length < PARTY) need.push(`missing ${PARTY - part.length}`);
    const status = need.length ? `<span class="miss">${need.join(', ')}</span>` : '<span class="ok">full group</span>';
    html += `<div class="party"><div class="party-h"><h4>Group ${g + 1}</h4><span class="pc"><span>${ri('tank')}${c.tank}</span><span>${ri('heal')}${c.heal}</span><span>${ri('dps')}${c.dps}</span>${status}</span></div>`;
    part.forEach((s, k) => {
      const i = g * PARTY + k, r = RC[s.race], ro = roleOpts(CL[s.cls]);
      html += `<div class="slot" style="--cc:${CCOL[s.cls]}" data-i="${i}"><span class="no av"><img src="${ROOT}assets/art/${s.cls}-face.webp?v=0003354e" width="160" height="160" alt="" loading="lazy" decoding="async"><b>${i + 1}</b></span>
      <select class="srace" aria-label="Player race ${i + 1}">${races.map(x => `<option value="${x.id}"${x.id === s.race ? ' selected' : ''}>${esc(x.n)}${x.paid ? ' (paid)' : ''}</option>`).join('')}</select>
      <select class="scls" aria-label="Player class ${i + 1}">${Object.keys(r.can).map(c2 => `<option value="${c2}"${c2 === s.cls ? ' selected' : ''}>${esc(CL[c2].n)}</option>`).join('')}</select>
      <select class="srole" aria-label="Player role ${i + 1}">${ro.map(x => `<option value="${x}"${x === s.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('')}</select>
      <button class="del" aria-label="Remove player ${i + 1}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></div>`;
    });
    html += '</div>';
  }
  $('#slots').innerHTML = html;
  $('#bAdd').disabled = n >= MAXT;
  const cnt = countRoles(team.list);
  $('#roleSum').innerHTML = RR.map(x => `<div class="rs ${cnt[x] ? 'ok' : 'zero'}"><b>${cnt[x]}</b><span>${ri(x)}${ROLE_RU[x]}</span></div>`).join('');
  const v = [];
  if (!n) v.push(['', 'Tap a group size or add a player.']);
  else {
    const full = Array.from({ length: parties }, (_, g) => team.list.slice(g * PARTY, g * PARTY + PARTY)).filter(p => p.length === PARTY && p.some(s => s.role === 'tank') && p.some(s => s.role === 'heal')).length;
    if (full) v.push(['good', `Ready groups for a dungeon: ${full} of ${parties}. Each has a tank and a healer.`]);
    if (full < parties) v.push(['warn', 'Some groups lack a tank, a healer or players. They are highlighted in the list.']);
    RAIDS.forEach(([size, name]) => v.push([n >= size ? 'good' : '', n >= size ? `Raid for ${size} (${name}): enough players.` : `Raid for ${size} (${name}): short by ${size - n}.`]));
    const byCls = {}; team.list.forEach(s => byCls[s.cls] = (byCls[s.cls] || 0) + 1);
    const dup = Object.keys(byCls).filter(c => byCls[c] > 1 && BUFF[c]);
    if (dup.length && n <= 10) v.push(['', `Identical classes (${dup.map(c => CL[c].n).join(', ')}): their buffs overlap, the second one adds less.`]);
    const sky = team.list.filter(s => RC[s.race].paid).length;
    if (sky) v.push(['', `Skyborne is a paid race: the Heroic Pack from $29.99 is needed by ${sky} of ${n} players.`]);
  }
  $('#verdict').innerHTML = v.map(x => `<li class="${x[0]}">${esc(x[1])}</li>`).join('');
  const have = [...new Set(team.list.map(s => s.cls))];
  const withB = have.filter(c => BUFF[c]), noB = have.filter(c => !BUFF[c]);
  $('#buffs').innerHTML = (withB.length ? withB.map(c => `<li class="good"><span class="cdot" style="--cc:${CCOL[c]}"></span><b>${esc(CL[c].n)}:</b> ${esc(BUFF[c])}</li>`).join('') : '<li>No classes with group buffs yet.</li>')
    + (noB.length ? `<li>Without a group buff: ${noB.map(c => CL[c].n).join(', ')}. They deal pure damage.</li>` : '');
  $('#teamText').value = n ? Array.from({ length: parties }, (_, g) => (parties > 1 ? `Group ${g + 1}: ` : '') + team.list.slice(g * PARTY, g * PARTY + PARTY).map(s => `${raceName(RC[s.race])} ${CL[s.cls].n} (${ROLE_RU[s.role]})`).join(', ')).join('; ') + ` — ${facName(team.f)}` : '';
  $('#qTeam').textContent = n ? `${facName(team.f)}, players: ${n}, tanks ${cnt.tank}, healers ${cnt.heal}` : 'From one to forty players';
  if (teamTouched) { try { history.replaceState(null, '', n ? teamLink() : location.pathname); } catch (e) {} }
}
function touch() { teamTouched = true; renderTeam(); }
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Could not copy, select the text and press Ctrl+C'; }
}
$('#segBF').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; team.f = b.dataset.v; touch(); });
$('#sizes').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { team.list = autoTeam(+b.dataset.n, team.f); touch(); } });
$('#szMinus').onclick = () => { if (team.list.length > 1) { team.list.pop(); touch(); } };
$('#szPlus').onclick = () => { if (team.list.length < MAXT) addPlayer(); };
function addPlayer() {
  const k = team.list.length, role = k % PARTY === 0 ? 'tank' : k % PARTY === 1 ? 'heal' : 'dps';
  const pool = POOL[role].filter(c => RACES.some(r => r.f === team.f && r.can[c])), cls = pool[k % pool.length];
  team.list.push({ race: raceFor(cls, team.f, k), cls, role }); touch();
}
$('#bClear').onclick = () => { team.list = []; touch(); };
$('#bAdd').onclick = () => { if (team.list.length < MAXT) addPlayer(); };
$('#slots').addEventListener('change', e => {
  const row = e.target.closest('.slot'); if (!row) return; const s = team.list[+row.dataset.i];
  if (e.target.classList.contains('srace')) s.race = e.target.value;
  if (e.target.classList.contains('scls')) s.cls = e.target.value;
  if (e.target.classList.contains('srole')) s.role = e.target.value;
  touch();
});
$('#slots').addEventListener('click', e => { const d = e.target.closest('.del'); if (!d) return; team.list.splice(+d.closest('.slot').dataset.i, 1); touch(); });
$('#copyTeam').onclick = () => copyTo($('#teamText').value, $('#teamMsg'), 'Group copied');
$('#copyLink').onclick = () => copyTo(teamLink(), $('#teamMsg'), 'Link copied');
if (!fromLink) team.list = autoTeam(5, team.f);
renderTeam();
if (fromLink) setTimeout(() => document.getElementById('builder').scrollIntoView(), 0);

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
  ['alchemy', 'Alchemy', 1, 'Mana Well', 'like Blessing of Wisdom'],
  ['blacksmithing', 'Blacksmithing', 1, 'Sharpening Wheel', 'like Strength of Earth Totem'],
  ['enchanting', 'Enchanting', 1, 'Enchanted Lute', 'like Mark of the Wild'],
  ['engineering', 'Engineering', 1, 'Reagent Bot', 'reagent vendor, repairs at tier 2'],
  ['herbalism', 'Herbalism', 1, 'Incense Candle', 'like Arcane Intellect'],
  ['leatherworking', 'Leatherworking', 1, 'Camp Tent', 'more rested experience'],
  ['mining', 'Mining', 1, 'Lodestone', 'like Blessing of Might'],
  ['skinning', 'Skinning', 1, 'Camp Chair', 'like Moonkin Aura'],
  ['tailoring', 'Tailoring', 1, 'Faction Banner', 'like Divine Spirit'],
  ['cooking', 'Cooking', 0, 'Basic Campfire', 'more object slots in camp'],
  ['firstaid', 'First Aid', 0, 'First Aid Kit', 'like Power Word: Fortitude'],
  ['fishing', 'Fishing', 0, 'Fish Bowl', 'like Blessing of Kings']
];
const PR = Object.fromEntries(PROFS.map(p => [p[0], p]));

/* Game stages: f = fact from the sources, t = our tip */
const SRC = {
  names: ['Icy Veins: name reservation', 'https://www.icy-veins.com/wow-forever/name-reservation'],
  names2: ['Team Overpowered: names and surnames', 'https://teamoverpowered.com/forever/guides/name-reservation/'],
  prof: ['Warcraft Tavern: professions', 'https://www.warcrafttavern.com/forever/guides/professions/'],
  camp: ['Warcraft Tavern: camping', 'https://www.warcrafttavern.com/forever/guides/camping/'],
  legacy: ['Blizzard: Legacy', 'https://news.blizzard.com/en-gb/article/24307383'],
  dung: ['Warcraft Tavern: dungeons', 'https://www.warcrafttavern.com/forever/guides/dungeons/'],
  ride: ['Warcraft Tavern: riding', 'https://www.warcrafttavern.com/forever/guides/riding/'],
  cwg: ['ClassicWoW.gg: dates and raids', 'https://classicwow.gg/forever']
};
const STAGES = [
  { id: 'pre', n: 'Before launch', sub: 'until Nov 4', lo: 0, hi: 0,
    todo: [['f', 'Early name reservation Oct 27 – Nov 3 for owners of the Heroic, Epic and Collection packs. First come, first served.'],
      ['f', 'You can reserve up to three characters per account. A character has a first name and a surname, and the pair must be unique within the region.'],
      ['f', 'From Nov 4 a subscription or game time is required to play.'],
      ['t', 'Pick three names with surnames, plus backups, before Oct 27.']],
    dnote: 'The first dungeons open at level 13.',
    prof: [['f', 'Each character gets two primary professions plus all three secondary ones: Cooking, First Aid and Fishing.'],
      ['f', 'Each profession places its own camp object with a buff similar to a class buff.'],
      ['t', 'Split professions in advance: one of you takes Cooking for the campfire, the rest pick different ones so camp buffs do not repeat.']],
    legacy: [['f', 'Legacy opens with your first point: level 25, 150 in a profession (not gathering) or exploring the whole map.'],
      ['f', 'At launch a character can spend at most 16 points, the rest go to the reward track.']],
    group: [['t', 'Agree on one faction and one mode: you can only group within a mode, and in PvP an account has one faction.'],
      ['t', 'Build your roster in the group builder: a tank, a healer and different classes for buffs.']],
    src: ['names', 'names2', 'prof', 'legacy'] },
  { id: 'first', n: 'First days', sub: 'levels 1–15', lo: 1, hi: 15,
    todo: [['f', 'Skyborne start on Zephras Isle, levels 1–12.'],
      ['f', 'Talents open at level 10, or at 9 with the Legacy perk Talented.'],
      ['f', 'Most cooked food gives an experience bonus. It stacks with the camp and the Cozy Sleeping Bag.'],
      ['t', 'Build up rest: log out at an inn or at a camp with a tent.']],
    prof: [['f', 'The basic campfire needs no Cooking and holds 3 objects. It burns for about 10 minutes, and you can place a new one after 5.'],
      ['f', 'To get camp buffs, sit nearby (/sit) for at least a minute.'],
      ['t', 'Pick up gathering from the first levels: herbs, ore and hides feed crafting, and 150 in a crafting profession opens Legacy.']],
    legacy: [['f', 'No perks yet: the first point comes at level 25 or with 150 in a profession.'],
      ['t', 'When Legacy opens, take experience and camp perks first: Well Rested, Field Guide, Permanence. Talented helps alts.']],
    group: [['t', 'Level in the same zone and set up camp at every stop: five minutes on a campfire pay off with buffs for the whole group.'],
      ['t', 'Form your first group of five by level 13–15.']],
    src: ['camp', 'legacy', 'dung'] },
  { id: 'dung', n: 'Dungeons', sub: 'levels 15–40', lo: 15, hi: 40,
    todo: [['f', 'Most dungeon experience comes from its quest chains. Repeat runs after them give noticeably less experience than questing in the world.'],
      ['f', 'Every item that drops unlocks its transmog appearance for everyone who can wear it, even if someone else got the item.'],
      ['f', 'Legacy opens at level 25.'],
      ['t', 'Collect the dungeon quests as a group first and go in once everyone has them.']],
    prof: [['f', 'Cooking 140 gives 5 camp slots, 220 gives 10.'],
      ['f', 'Each profession makes three camp objects, one per tier. Sources disagree on the skill needed for tiers 2 and 3.'],
      ['t', 'If level 25 is still far off, take a crafting profession to 150: Legacy will open sooner.']],
    legacy: [['f', 'Each challenge gives 1 point. There are 65: classes 27, professions 18, PvP 12, dungeons 3, raids 3, adventure 2.'],
      ['t', 'Reagent Economy (no bought reagents for abilities) and Field Guide (shorter camp object cooldown) are worth it.']],
    group: [['f', 'A dungeon is built for 5 players: a tank, a healer and three damage dealers.'],
      ['f', 'There is no level scaling, so a friend who is far behind will struggle in the dungeon.'],
      ['t', 'Keep levels close: whoever falls behind catches up on quests, and you run dungeons together.']],
    src: ['dung', 'camp', 'legacy'] },
  { id: 'path', n: 'Road to 60', sub: 'levels 40–60', lo: 40, hi: 60,
    todo: [['f', 'A mount at level 40 (60% speed), a fast one at 60 (100%). Train with your race’s trainer.'],
      ['f', 'Paladins and warlocks get their mount through class quests.'],
      ['f', 'Honored with your own faction gives a 10% discount on riding training and mounts. Per Warcraft Tavern: 100 + 20 gold at level 40, 1,000 + 200 at 60.'],
      ['t', 'Save gold for level 40: riding will be your biggest expense on the road to 60.']],
    prof: [['f', 'Each profession has its own tier 2 and 3 camp objects. Engineering’s second object, Repair Bot, repairs gear.'],
      ['t', 'Keep Cooking 220 in the group for a 10-object camp: by raid time there will be room for everyone.']],
    legacy: [['f', 'At most 16 points per character, the rest go to the reward track: a toy at 15, a pet at 25, a tabard at 40, a mount at 55.']],
    group: [['f', 'Raids open on Dec 9: Barrow Deeps for 10 players, Hyjal Summit for 20, Onyxia’s Lair for 40.'],
      ['t', 'The 10-player raid needs 10 players: if you have fewer, find the rest in your guild early.']],
    src: ['ride', 'prof', 'legacy', 'cwg'] },
  { id: 'raid', n: '60 and raids', sub: 'from Dec 9', lo: 60, hi: 60,
    todo: [['f', 'On Dec 9 Barrow Deeps (10 players), Hyjal Summit (20) and Onyxia’s Lair (40, Dustwallow Marsh) open.'],
      ['f', 'Clearing each of the three raids gives a Legacy point.'],
      ['f', 'New 15v15 battleground: Darkspear Islands off the coast of Dustwallow Marsh.'],
      ['t', 'While you gather people for the raid, run level 60 dungeons for gear.']],
    prof: [['f', 'Camp buffs are a bit weaker than class buffs and do not stack with them: Blessing of Kings gives 10% to all stats, the camp gives 8%.'],
      ['t', 'Set up camp at the raid entrance: its buffs cover what your classes lack.']],
    legacy: [['f', 'Challenges for level 60: dungeons 3, raids 3, PvP 12. PvP has ranks with a weekly cap and gear upgrades for Honor.']],
    group: [['f', 'The same buffs from two players of one class overlap, different classes stack.'],
      ['t', 'Build your raid roster in the group builder and post the link in chat.']],
    src: ['cwg', 'prof', 'legacy'] }
];
const ST = Object.fromEntries(STAGES.map(s => [s.id, s]));
const D_REL = new Date('2026-11-04T23:00:00Z'), D_RAID = new Date('2026-12-09T00:00:00');

/* My character, saved in this browser */
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
  if (now < D_REL) return ['pre', 'Picked by date: before the Nov 4 launch.'];
  if (me.lvl) return [me.lvl < 15 ? 'first' : me.lvl < 40 ? 'dung' : me.lvl < 60 ? 'path' : 'raid', 'Picked by your character’s level.'];
  if (now >= D_RAID) return ['raid', 'Picked by date: raids are open.'];
  return [now < new Date('2026-11-11T00:00:00') ? 'first' : 'dung', 'Picked by date. Add your character’s level and the stage will follow it.'];
}
const START = { pre: 'hero_dawn-960', first: 'hero_campfire-960', dung: 'warlock-360', path: 'hunter-360', raid: 'paladin-360' };
const ARTV = /*ARTV*/{"hero_campfire-960.avif":"?v=2654726f","hero_campfire-960.webp":"?v=d73f1e16","hero_dawn-960.avif":"?v=72b3acf6","hero_dawn-960.webp":"?v=4eae2c5c"};   // ?v= of the scene arts, filled in by build.art_version (same names, redrawn pictures)
const pic = f => `<picture><source type="image/avif" srcset="${ROOT}assets/art/${f}.avif${ARTV[f + '.avif'] || ''}"><img src="${ROOT}assets/art/${f}.webp${ARTV[f + '.webp'] || ''}" alt="" loading="lazy" decoding="async"></picture>`;
const tipL = () => '<span class="tl">Tip</span>';
function liC(x) { return x[0] === 't' ? `<li class="tip">${tipL()}${esc(x[1])}</li>` : `<li>${esc(x[1])}</li>`; }
function dLi(d) {
  const mine = me.lvl && nearLvl(d, me.lvl);
  return `<li class="${mine ? 'mine' : ''}"><b>${esc(d[0])}</b><span class="pill${mine ? ' gold' : ''}">${lvRange(d)}</span><span class="z">${esc(d[3])}${d[4] ? ' · <i>new</i>' : ''}${mine ? '<span class="sr"> · for your level</span>' : ''}</span></li>`;
}
function renderStage() {
  const [auto, why] = autoStage();
  if (stageAuto) stageSel = auto;
  const s = ST[stageSel];
  $('#stageBar').innerHTML = STAGES.map(x => `<button type="button" class="stile" role="tab" id="tab-${x.id}" data-st="${x.id}" aria-controls="stagePanel" aria-selected="${x.id === stageSel}" tabindex="${x.id === stageSel ? 0 : -1}">${pic(START[x.id])}${x.id === auto ? '<span class="now">now</span>' : ''}<b>${esc(x.n)}</b><span class="lv">${esc(x.sub)}</span></button>`).join('');
  let ds;
  if (s.id === 'pre') ds = DUNGEONS.filter(d => d[1] <= 15);
  else ds = DUNGEONS.filter(d => d[1] <= s.hi && d[2] >= s.lo);
  if (me.lvl && s.lo <= me.lvl && me.lvl <= Math.max(s.hi, 1)) ds = ds.filter(d => nearLvl(d, me.lvl)).concat(ds.filter(d => !nearLvl(d, me.lvl)));
  const MAXD = 6, extra = ds.length - MAXD;
  let k = 0;
  const steps = s.todo.map(x => x[0] === 't'
    ? `<li class="tip"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p>${tipL()}${esc(x[1])}</p></li>`
    : `<li><span class="n">${String(++k).padStart(2, '0')}</span><p>${esc(x[1])}</p></li>`).join('');
  $('#stagePanel').setAttribute('aria-labelledby', 'tab-' + s.id);
  $('#stagePanel').innerHTML = `<div class="st-head"><div class="t"><h3>${esc(s.n)}</h3><span class="pill gold">${esc(s.sub)}</span></div><p class="why">${stageAuto ? esc(why) : 'Stage chosen manually.'}</p></div>
    <ol class="steps-c">${steps}</ol>
    <div class="st-cols">
      <div><h4>Dungeons for this level</h4>${s.dnote ? `<p class="small" style="margin:-4px 0 10px">${esc(s.dnote)}</p>` : ''}<ul class="dlist">${ds.slice(0, MAXD).map(dLi).join('')}</ul>
        <a class="more-l" href="guides/dungeons/">${extra > 0 ? `More dungeons in the table: ${extra}` : 'All 35 dungeons'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
      <div style="display:grid;gap:24px;align-content:start"><div><h4>Professions and camp</h4><ul class="clean">${s.prof.map(liC).join('')}</ul></div>
        <div><h4>Legacy perks</h4><ul class="clean">${s.legacy.map(liC).join('')}</ul></div></div>
    </div>
    <div class="gtip"><h4 style="margin:0 0 10px;font-size:1.02rem">Tips for the group</h4><ul class="clean">${s.group.map(liC).join('')}</ul></div>
    <p class="st-src"><span>Sources:</span>${s.src.map(k2 => `<a href="${SRC[k2][1]}" target="_blank" rel="noopener">${esc(SRC[k2][0])}</a>`).join('')}</p>`;
}
function optList(items, cur, none) { return `<option value="">${esc(none)}</option>` + items.map(([v, t]) => `<option value="${v}"${v === cur ? ' selected' : ''}>${esc(t)}</option>`).join(''); }
function renderMe() {
  fixMe();
  const races = f => RACES.filter(r => r.f === f).map(r => `<option value="${r.id}"${r.id === me.race ? ' selected' : ''}>${esc(r.n)}</option>`).join('');
  $('#meRace').innerHTML = `<option value="">Not chosen</option><optgroup label="${facName('alliance')}">${races('alliance')}</optgroup><optgroup label="${facName('horde')}">${races('horde')}</optgroup>`;
  const cls = (me.race ? Object.keys(RC[me.race].can) : CLASSES.map(c => c.id)).map(id => [id, CL[id].n]);
  $('#meCls').innerHTML = optList(cls, me.cls, 'Not chosen');
  $('#meRole').innerHTML = me.cls ? roleOpts(CL[me.cls]).map(x => `<option value="${x}"${x === me.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('') : `<option value="">Pick a class first</option>`;
  $('#meRole').disabled = !me.cls;
  const prim = PROFS.filter(p => p[2]);
  $('#meP1').innerHTML = optList(prim.filter(p => p[0] !== me.p2).map(p => [p[0], p[1]]), me.p1, 'None');
  $('#meP2').innerHTML = optList(prim.filter(p => p[0] !== me.p1).map(p => [p[0], p[1]]), me.p2, 'None');
  $('#meSec').innerHTML = PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${me.sec.includes(p[0])}">${esc(p[1])}</button>`).join('');
  document.querySelectorAll('.lvin').forEach(i => { if (document.activeElement !== i) i.value = me.lvl || ''; });
  const who = [me.race ? RC[me.race].n : '', me.cls ? CL[me.cls].n : ''].filter(Boolean).join(' · ');
  const sub = me.cls ? [ROLE_RU[me.role], me.race ? facName(RC[me.race].f) : ''].filter(Boolean).join(' · ') : 'Choose race, class and level below';
  const hero = $('#meHero');
  hero.style.setProperty('--cc', me.cls ? CCOL[me.cls] : '#c9a54a');
  hero.innerHTML = pic(me.cls ? `${me.cls}-600` : 'hero_campfire-960') + (me.lvl ? `<span class="lvb" aria-label="Level ${me.lvl}">${me.lvl}</span>` : '')
    + `<span class="k">My character</span><b>${who ? esc(who) : 'Not created yet'}</b><span class="s">${esc(sub)}</span>`;
  let out = '';
  if (meSet()) {
    const b = [];
    if (me.cls) b.push(BUFF[me.cls] ? `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span><b>${esc(CL[me.cls].n)}:</b> ${esc(BUFF[me.cls])}</span></li>` : `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-dps"/></svg></span><span>${esc(CL[me.cls].n)}: no group buff, pure damage.</span></li>`);
    [me.p1, me.p2, ...me.sec].filter(Boolean).forEach(id => { const p = PR[id]; b.push(`<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg></span><span><b>${esc(p[3])}</b> <span class="m">· ${esc(p[1])}</span><br>${esc(p[4])}</span></li>`); });
    if (!b.length) b.push('<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span>Choose a class and professions to see your buffs.</span></li>');
    out += `<div><h4>What you bring to the group</h4><ul class="buffs">${b.join('')}</ul></div>`;
    if (me.lvl) {
      const ds = DUNGEONS.filter(d => nearLvl(d, me.lvl) && facOk(d, me.race && RC[me.race].f));
      out += `<div><h4>Dungeons for your level</h4>` + (ds.length ? `<ul class="dlist">${ds.slice(0, 4).map(dLi).join('')}</ul>` : '<p class="small">The first dungeons start at level 13.</p>')
        + `<a class="more-l" href="guides/dungeons/">${ds.length > 4 ? `More dungeons in the table: ${ds.length - 4}` : 'Dungeon table'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`;
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
