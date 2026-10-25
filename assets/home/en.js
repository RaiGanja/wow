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
const PV = /*PV*/'?v=6114caef';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Faster by ${-p}%` : p > 0 ? `Slower by ${p}%` : 'Average pace';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>faster</span><span>slower</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Class</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Leveling</span><span>In raids</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Roles: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Race</span><span>Classes</span><span class="abl">Abilities <span class="abt">active</span><span class="abt p">passive</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">paid</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Classes: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', new' : v ? '' : ', not available')); }).join('')}</span>
    <span class="abs">${r.rac.map(x => `<span><b class="${x[0] === 'a' ? '' : 'p'}">${bi(x[1])}</b><span>${esc(x[2])}</span></span>`).join('')}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('') + '</div>').join('');
}
/* ref:end */
const $ = s => document.querySelector(s);
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
const ROOT = '../';
function raceName(r) { return r.name || r.n; }
/* Class roster: tall portraits, the hovered or focused one expands */
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
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext}${PV} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">More about the class</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
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

/* Classes / races: one block, two tabs (arrow keys, Home, End); #peoples (menu, old links) opens the races */
const TABS = [...document.querySelectorAll('#classes [role="tab"]')];
function showTab(t, focus) {
  TABS.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute('aria-controls')).hidden = !on; });
  if (focus) t.focus();
}
TABS.forEach((t, i) => {
  t.addEventListener('click', () => showTab(t));
  t.addEventListener('keydown', e => {
    const k = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: TABS.length - 1 }[e.key];
    if (k === undefined) return;
    e.preventDefault(); showTab(TABS[(k + TABS.length) % TABS.length], true);
  });
});
function hashTab() { if (location.hash === '#peoples') { showTab(TABS[1]); document.getElementById('classes').scrollIntoView(); } }
addEventListener('hashchange', hashTab);
hashTab();
