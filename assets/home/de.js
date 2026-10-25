const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Krieger', s:'Krieger', roles:['tank','dps'],
    specs:[['Waffen','Nahkampfschaden (Zweihandwaffe)',['dps']],['Furor','Nahkampfschaden (zwei Waffen)',['dps']],['Schutz','Tank',['tank']]],
    lvl:'Das langsamste Leveln, etwa 12 % länger als der Durchschnitt',
    lp:12,
    raid:'Schlachtruf wirkt auf den ganzen Raid',
    forever:'Mehr Wut, bessere Bedrohung gegen mehrere Ziele, das Talent Weapon Master. Furor und Blutdurst wurden abgeschwächt.' },
  { id:'paladin', n:'Paladin', roles:['tank','heal','dps'],
    specs:[['Heilig','Heiler',['heal']],['Schutz','Tank',['tank']],['Vergeltung','Nahkampfschaden',['dps']]],
    lvl:'Durchschnittliches Leveltempo',
    lp:0,
    raid:'Segen der Könige ist jetzt Grundfähigkeit. Laut Beta-Listen gehört Schutz zu den stärksten Tanks, Vergeltung ist nach dem Patch vom 15. Oktober abgerutscht.',
    forever:'Heiliger Stoß ab Stufe 6, Richturteil verbraucht das Siegel nicht. Untote können jetzt Paladine sein, so kam die Klasse zur Horde.' },
  { id:'hunter', n:'Jäger', roles:['dps'],
    specs:[['Tierherrschaft','Fernkampfschaden, viel Schaden vom Begleiter',['dps']],['Treffsicherheit','Fernkampfschaden',['dps']],['Überleben','Nah- und Fernkampf, Fallen',['dps']]],
    lvl:'Das schnellste Leveln, etwa 8 % schneller als der Durchschnitt',
    lp:-8,
    raid:'Aura des Volltreffers wirkt auf den ganzen Raid',
    forever:'Du kannst ohne Begleiter spielen, Fallen funktionieren im Kampf, Füchse sind als Begleiterfamilie dazugekommen. Überleben kann in den Nahkampf gehen.' },
  { id:'rogue', n:'Schurke', roles:['dps'],
    specs:[['Meucheln','Giftschaden',['dps']],['Kampf','Schnelle Waffenangriffe',['dps']],['Täuschung','Hinterhalte, Blutungen',['dps']]],
    lvl:'Durchschnittliches Leveltempo',
    lp:0,
    raid:'Reiner Nahkampfschaden ohne raidweite Buffs',
    forever:'Einhandäxte sind jetzt nutzbar. Meucheln baut auf Gifte, Täuschung auf Blutungen und Verstohlenheit.' },
  { id:'priest', n:'Priester', roles:['heal','dps'],
    specs:[['Disziplin','Heiler, Schilde und Absorption',['heal']],['Heilig','Heiler',['heal']],['Schatten','Fernkampfschaden',['dps']]],
    lvl:'Etwa 5 % langsamer als der Durchschnitt',
    lp:5,
    raid:'Göttlicher Willen ist jetzt Grundfähigkeit. Schattenschaden und Verschlingende Seuche (24 Sek. Abklingzeit) wurden mit dem Patch vom 15. Oktober verstärkt.',
    forever:'Furchtzauberschutz und Verschlingende Seuche sind ab Stufe 20 für jedes Volk verfügbar. Jedes Volk hat zwei eigene Priesterzauber.' },
  { id:'shaman', n:'Schamane', roles:['heal','dps','tank?'],
    specs:[['Elementar','Fernkampfschaden',['dps']],['Verstärkung','Nahkampfschaden. Ob er tanken kann, ist noch offen',['dps','tank?']],['Wiederherstellung','Heiler',['heal']]],
    lvl:'Durchschnittliches Leveltempo',
    lp:0,
    raid:'Die Totems Erdstärke, Windzorn, Flammenzunge und Anmut der Luft buffen die eigene Gruppe',
    forever:'Zwerge können jetzt Schamanen sein, so kam die Klasse zur Allianz. Lavaexplosion wurde verstärkt, Elementar ist in den Schadensranglisten gestiegen.' },
  { id:'mage', n:'Magier', roles:['dps'],
    specs:[['Arkan','Burst, viel Mana',['dps']],['Feuer','Krits und Entzünden',['dps']],['Frost','Schaden und Kontrolle',['dps']]],
    lvl:'Das schnellste Leveln, etwa 8 % schneller als der Durchschnitt (etwa 12 Stunden gespart)',
    lp:-8,
    raid:'Portale sowie Essen und Wasser für die ganze Gruppe',
    forever:'Feuer bekam Kampfeshitze, Arkan den Arkanschlag, Frost die Eislanze. Frostfeuerblitz ist ab Stufe 40 verfügbar.' },
  { id:'warlock', n:'Hexenmeister', roles:['dps'],
    specs:[['Gebrechen','Schaden durch Flüche und Verderbnis',['dps']],['Dämonologie','Schaden durch Dämonen',['dps']],['Zerstörung','Direkter Feuer- und Schattenschaden',['dps']]],
    lvl:'Durchschnittliches Leveltempo',
    lp:0,
    raid:'Schattenbeherrschung gibt jetzt 2–10 % Schattenschaden (vorher 1–5 %)',
    forever:'Gebrechen hat einen neuen kanalisierten Zauber, der Dämon bleibt bei Dämonischer Opferung, Zerstörung bekam Verbrennen und Flächenschaden.' },
  { id:'druid', n:'Druide', roles:['tank','heal','dps'],
    specs:[['Gleichgewicht','Fernkampfschaden',['dps']],['Wilder Kampf','Tank (Bär) und Nahkampfschaden (Katze)',['tank','dps']],['Wiederherstellung','Heiler, viel Heilung über Zeit',['heal']]],
    lvl:'Etwa 5 % langsamer als der Durchschnitt',
    lp:5,
    raid:'Rudelführer und Aura des Moonkin wirken auf den ganzen Raid und sind stapelbar',
    forever:'Jede Spezialisierung hat eine klare Rolle, Gestalten funktionieren mit Tränken und Waffenverzauberungen. Du kannst Tank, Heiler und Kämpfer auf einem Charakter sein.' }
];
const ROLE_RU = { tank:'Tank', heal:'Heiler', dps:'Schaden', 'tank?':'Tank (unsicher)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Schlachtruf', paladin:'Segen der Könige', hunter:'Aura des Volltreffers', priest:'Machtwort: Seelenstärke, Göttlicher Willen', shaman:'Totems (Erdstärke, Windzorn, Flammenzunge, Anmut der Luft)', mage:'Arkane Intelligenz, Portale, Essen und Wasser', druid:'Mal der Wildnis, Rudelführer, Aura des Moonkin' };

const RACES = [
  { id:'human', n:'Mensch', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Überlebenswille','Entfernt Betäubung'],['a','Wachsamkeit','Enthüllt unsichtbare Gegner für 20 Sek.'],['p','Ruthless','+2 % kritische Trefferchance'],['p','Unbeugsamkeit','+5 % Willenskraft']],
    tip:'Willenskraft fließt beim Heilig-Priester in die Heilung, deshalb ist ein menschlicher Priester gut zum Heilen.' },
  { id:'dwarf', n:'Zwerg', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Steingestalt','Immunität gegen Blutungen, Gifte und Krankheiten für 8 Sek. und weniger körperlicher Schaden'],['a','Schatzsucher','Zeigt Truhen in der Nähe'],['p','Earth Fury','+2 % kritischer Schaden und Heilkraft'],['p','Big Game Hunter','+5 % Schaden gegen Wildtiere']],
    tip:'Steingestalt ist nützlich für Tanks und im PvP.' },
  { id:'nightelf', n:'Nachtelf', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Elunes Licht','+10 % kritische Trefferchance für 15 Sek.'],['a','Schattenmimik','Unsichtbarkeit auf der Stelle'],['p','Schnelligkeit','+1 % Ausweichen und +2 % Laufgeschwindigkeit'],['p','Irrwischgeist','+75 % Laufgeschwindigkeit als Geist']],
    tip:'Das einzige Allianzvolk mit Druiden, außer du nimmst Skyborne.' },
  { id:'gnome', n:'Gnom', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Entfesselungskünstler','Kurze Immunität gegen Verlangsamung und Bewegungsunfähigkeit'],['a','Eureka!','Die nächsten 3 Fähigkeiten sind billiger und 10 % stärker'],['p','Wacher Geist','+5 % maximales Mana, Wut oder Energie'],['p','Ingenieursspezialisierung','Ingenieursgeräte funktionieren zuverlässiger']],
    tip:'Wacher Geist hilft besonders Energieklassen.' },
  { id:'skyA', n:'Skyborne (Allianz)', f:'alliance', paid:true, name:'High Order Skyborne',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','10 Sek. nach unten gleiten, kein Fallschaden'],['a','Read Ley Line','+100 % Gesundheits- und Manaregeneration'],['p','Wind Blessed','+3 % Angriffs- und Zaubertempo'],['p','Elemental Insight','+5 % Schaden gegen Elementare']],
    tip:'Bezahltes Volk: Heroic Pack ab 29,99 $. Startet im Gebiet Zephras Isle (Stufen 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Kochendes Blut','+10 % Angriffskraft und Zaubermacht für 15 Sek.'],['a','Shatter Curse','Entfernt Flüche und Verderbnis, −5 % erlittener Magieschaden für 8 Sek.'],['p','Savage','+1 % kritische Trefferchance'],['p','Zähigkeit','Betäubungen sind 20 % kürzer']],
    tip:'Kochendes Blut gibt ein starkes Schadensfenster.' },
  { id:'undead', n:'Untoter', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Wille der Verlassenen','Entfernt Bezauberung, Furcht und Schlaf'],['a','Kannibalismus','Stellt über Zeit 35 % Gesundheit und Mana wieder her'],['p','Unterwasseratmung','Länger unter Wasser atmen'],['p','Berührung des Grabes','Chance, bei Angriffen Gesundheit zu entziehen']],
    tip:'Neue Kombination: ein Paladin für die Horde, wo es diese Klasse vorher nicht gab.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Kriegsdonner','Betäubt Gegner in der Nähe für 2 Sek.'],['a','Grüner Daumen','Lässt Kräuter wachsen, die man ohne Kräuterkunde sammeln kann'],['p','Ebenenlaufen','Das Tempo steigt, während du läufst'],['p','Durchhaltevermögen','+5 % Gesundheit und +2 % kritischer Schaden']],
    tip:'Das einzige Hordevolk mit Druiden, außer du nimmst Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserker','+10 % Angriffs- und Zaubertempo für 10 Sek.'],['a','Rasche Regeneration','Stellt über Zeit Gesundheit wieder her'],['p','Wildtierschlächter','+5 % Schaden gegen Wildtiere'],['p','Regeneration','Gesundheit regeneriert auch im Kampf']],
    tip:'Die meisten Klassenoptionen der Horde: sieben.' },
  { id:'skyH', n:'Skyborne (Horde)', f:'horde', paid:true, name:'Windshaper Skyborne',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','10 Sek. nach unten gleiten, kein Fallschaden'],['a','Skysight','+10 % Laufgeschwindigkeit'],['p','Wind Blessed','+3 % Angriffs- und Zaubertempo'],['p','Elemental Insight','+5 % Schaden gegen Elementare']],
    tip:'Bezahltes Volk: Heroic Pack ab 29,99 $. Nur die Horde kann Schamanen haben, nur die Allianz Magier.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "Das zahlreichste Volk der Allianz. Vielseitig und stark im PvP dank Überlebenswille.", "dwarf": "Zähe Bergleute und Schützen aus Ironforge. Zum ersten Mal in Classic hat die Allianz Schamanen, und es sind Zwerge.", "nightelf": "Ein uraltes Volk der Wälder. Schwer zu fassen: eigenes Verstecken, Ausweichen und schnelles Laufen.", "gnome": "Die Erfinder von Gnomeregan. Klein, gerissen und mit der besten Fluchtfähigkeit im Spiel.", "skyA": "Ein neues Volk in Forever. Der High Order: Windelfen auf der Suche nach der verlorenen Arkanmagie ihrer Vorfahren.", "orc": "Das Herz der Horde. Die stärksten Krieger und PvP-Meister dank Kochendem Blut und Zähigkeit.", "undead": "Die Verlassenen: ehemalige Menschen, die sich vom Lichkönig befreit haben. Immun gegen Furcht und Schlaf, wenn es darauf ankommt.", "tauren": "Friedliche Riesen der Ebenen. Die meiste Gesundheit und eine eigene Flächenbetäubung.", "troll": "Der Stamm der Dunkelspeere. Die meisten Klassen der Horde und ein starkes Berserker für Schaden.", "skyH": "Ein neues Volk in Forever. Die Windshapers: spirituelle Anführer der Skyborne, den Elementen nah."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Waffen':'Arms','Furor':'Fury','Schutz':'Protection','Heilig':'Holy','Vergeltung':'Retribution',
  'Tierherrschaft':'Beast Mastery','Treffsicherheit':'Marksmanship','Überleben':'Survival',
  'Meucheln':'Assassination','Kampf':'Combat','Täuschung':'Subtlety',
  'Disziplin':'Discipline','Schatten':'Shadow','Elementar':'Elemental','Verstärkung':'Enhancement','Wiederherstellung':'Restoration',
  'Arkan':'Arcane','Feuer':'Fire','Frost':'Frost','Gebrechen':'Affliction','Dämonologie':'Demonology','Zerstörung':'Destruction',
  'Gleichgewicht':'Balance','Wilder Kampf':'Feral',
  'Überlebenswille':'Will to Survive','Wachsamkeit':'Perception','Ruthless':'Ruthless','Unbeugsamkeit':'The Human Spirit',
  'Steingestalt':'Stoneform','Schatzsucher':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Elunes Licht':"Elune’s Light",'Schattenmimik':'Shadowmeld','Schnelligkeit':'Quickness','Irrwischgeist':'Wisp Spirit',
  'Entfesselungskünstler':'Escape Artist','Eureka!':'Eureka!','Wacher Geist':'Expansive Mind','Ingenieursspezialisierung':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Kochendes Blut':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Zähigkeit':'Hardiness',
  'Wille der Verlassenen':'Will of the Forsaken','Kannibalismus':'Cannibalize','Unterwasseratmung':'Underwater Breathing','Berührung des Grabes':'Touch of the Grave',
  'Kriegsdonner':'War Stomp','Grüner Daumen':'Cultivation','Ebenenlaufen':'Plainsrunning','Durchhaltevermögen':'Endurance',
  'Berserker':'Berserking','Rasche Regeneration':'Rapid Regeneration','Wildtierschlächter':'Beast Slaying','Regeneration':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Tipp</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Allianz' : 'Horde'; }
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Schneller um ${-p}%` : p > 0 ? `Langsamer um ${p}%` : 'Durchschnittstempo';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>schneller</span><span>langsamer</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Klasse</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Leveln</span><span>In Raids</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Rollen: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Volk</span><span>Klassen</span><span class="abl">Fähigkeiten <span class="abt">aktiv</span><span class="abt p">passiv</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">bezahlt</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Klassen: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', neu' : v ? '' : ', nicht verfügbar')); }).join('')}</span>
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
  let h = '<thead><tr><th scope="col">Volk</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">bezahlt</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: nicht erlaubt"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', neue Kombination' : ''}`;
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
    return `<button type="button" data-pc="${c.id}" class="${v ? '' : 'na'}" aria-pressed="${c.id === state.cls}">${esc(c.n)}${v === 'new' ? ' · neu' : ''}</button>`;
  }).join('');
  $('#pickm').innerHTML = `<div><div class="lbl">1. Volk</div><div class="chiprow">${races}</div></div>
    <div><div class="lbl">2. Klasse (gestrichelt: für dieses Volk nicht verfügbar, tippen wechselt das Volk)</div><div class="chiprow">${cls}</div></div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Aktiv' : 'Passiv'}</span><b>${bi(x[1])}</b><span>${esc(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', Skyborne-Paket nötig' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><img src="../assets/art/${c.id}-600.webp" width="600" height="804" alt="" loading="lazy" decoding="async"></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}${face(c.id, CCOL[c.id])}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Neue Kombination</span>' : ''}${r.paid ? '<span class="tag paid">Bezahltes Volk</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Spezialisierungen</h4><div class="cards">${specs}</div></div>
        <div><h4>Volksfähigkeiten</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Leveln</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>In Raids</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Was ist neu</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Meine Wahl">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Meine Wahl kopieren</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Kopiert');
  $('#qPick').textContent = `Jetzt: ${r.n} · ${c.n}`;
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
  warrior: 'Platte, Wut und die vorderste Reihe. Steckt als Tank die Schläge ein oder mäht mit dem Zweihänder.',
  paladin: 'Ein heiliger Krieger in Platte: heilt, tankt und schwingt den Hammer. Jetzt auch bei der Horde.',
  hunter: 'Bogen, Fallen und ein treues Tier an deiner Seite. Eine der schnellsten Klassen beim Leveln.',
  rogue: 'Gifte, Klingen und Schatten. Reiner Schaden aus dem Hinterhalt und Gruppenkontrolle.',
  priest: 'Licht und Schatten in einer Hand. Der Hauptheiler der Gruppe oder ein dunkler Zauberwirker.',
  shaman: 'Totems und Elemente: heilt, schlägt mit Blitzen oder Waffen zu. Jetzt auch bei der Allianz.',
  mage: 'Feuer-, Frost- und Arkanmagie. Portale, Essen und Wasser für die ganze Truppe.',
  warlock: 'Flüche, Dämonen und Feuer. Schaden über Zeit und ein eigener Dämon als Helfer.',
  druid: 'Bär, Katze, Eule oder Heiler: alle drei Rollen auf einem Charakter.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Mehr zur Klasse</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">bezahlt</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">Mehr zum Volk</span></span>
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
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Kopieren fehlgeschlagen, markiere den Text und drücke Strg+C'; }
}

/* Dungeons: [name, min, max, entrance zone, new, other sites' ranges where they differ] */
const DUNGEONS = [
  ['Ragefireabgrund', 13, 18, 'Orgrimmar', 0, [], 'horde'],
  ['Hall of Thanes', 13, 18, 'Ironforge', 1, [['Icy Veins', '13–20']]],
  ['Ruinen von Lordaeron', 15, 20, 'Tirisfal', 1, [['Icy Veins', '15–22']]],
  ['Die Todesminen', 15, 22, 'Westfall', 0, [['Icy Veins', '17–26']]],
  ['Die Höhlen des Wehklagens', 17, 24, 'Brachland', 0, [['Icy Veins', '15–24']]],
  ['Burg Shadowfang', 20, 26, 'Silberwald', 0, [['Icy Veins', '20–30']]],
  ['Blackfathom-Tiefe', 22, 28, 'Ashenvale', 0, [['Sportskeeda', '22–26'], ['Icy Veins', '24–32']]],
  ['Excavation Site: Wetlands', 24, 29, 'Sumpfland', 1, [['ClassicWoW.gg', '26–31'], ['Icy Veins', '26–33']]],
  ['Das Verlies', 25, 29, 'Stormwind', 0, [['Icy Veins', '24–32']], 'alliance'],
  ['City of Dalaran', 28, 33, 'Alteracgebirge', 1, [['Icy Veins', '28–35']]],
  ['Gnomeregan', 29, 38, 'Dun Morogh', 0],
  ['Der Kral von Razorfen', 29, 38, 'Brachland', 0],
  ['Das Scharlachrote Kloster: Friedhof', 30, 38, 'Tirisfal', 0],
  ['Das Scharlachrote Kloster: Bibliothek', 33, 41, 'Tirisfal', 0],
  ['The Drowned City', 35, 40, 'Schlingendorntal', 1],
  ['Das Scharlachrote Kloster: Waffenkammer', 36, 44, 'Tirisfal', 0],
  ['Uldaman', 36, 45, 'Ödland', 0, [['Icy Veins', '41–51']]],
  ['Die Hügel von Razorfen', 37, 46, 'Brachland', 0],
  ['Das Scharlachrote Kloster: Kathedrale', 38, 46, 'Tirisfal', 0],
  ["Zul’Farrak", 40, 47, 'Tanaris', 0, [['Icy Veins', '44–54']]],
  ["Krol’dok Stronghold", 40, 45, 'Riverglades', 1],
  ['Maraudon', 45, 51, 'Desolace', 0, [['Icy Veins', '46–55']]],
  ['Alcaz Island Prison', 48, 53, 'Marschen von Dustwallow', 1],
  ["Der Tempel von Atal’Hakkar", 50, 55, 'Sümpfe des Elends', 0, [['Icy Veins', '50–60']]],
  ['Blackrocktiefen', 52, 60, 'Der Blackrock', 0],
  ['Blackmaw Hold', 55, 60, 'Azshara', 1],
  ['Untere Blackrockspitze', 57, 60, 'Der Blackrock', 0, [['Icy Veins', '55–60']]],
  ['Düsterbruch: Ost', 58, 60, 'Feralas', 0, [['Icy Veins', '54–60']]],
  ["Shaper’s Terrace", 58, 60, "Un’Goro-Krater", 1],
  ['Stratholme: Lebende', 58, 60, 'Östliche Pestländer', 0],
  ['Stratholme: Untote', 58, 60, 'Östliche Pestländer', 0],
  ['Scholomance', 58, 60, 'Westliche Pestländer', 0],
  ['Obere Blackrockspitze', 60, 60, 'Der Blackrock', 0, [['Icy Veins', '59–60']]],
  ['Düsterbruch: West', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]],
  ['Düsterbruch: Nord', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]]
];
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
const facOk = (d, f) => !f || !d[6] || d[6] === f;   // Ragefire Chasm and The Stockade open from a capital

/* Professions: camp object (tier 1) and the class buff it stands in for */
const PROFS = [
  ['alchemy', 'Alchimie', 1, 'Mana Well', 'wie Segen der Weisheit'],
  ['blacksmithing', 'Schmiedekunst', 1, 'Sharpening Wheel', 'wie Totem der Erdstärke'],
  ['enchanting', 'Verzauberkunst', 1, 'Enchanted Lute', 'wie Mal der Wildnis'],
  ['engineering', 'Ingenieurskunst', 1, 'Reagent Bot', 'Reagenzienhändler, Reparatur ab Stufe 2'],
  ['herbalism', 'Kräuterkunde', 1, 'Incense Candle', 'wie Arkane Intelligenz'],
  ['leatherworking', 'Lederverarbeitung', 1, 'Camp Tent', 'mehr Erholungserfahrung'],
  ['mining', 'Bergbau', 1, 'Lodestone', 'wie Segen der Macht'],
  ['skinning', 'Kürschnerei', 1, 'Camp Chair', 'wie Aura des Moonkin'],
  ['tailoring', 'Schneiderei', 1, 'Faction Banner', 'wie Göttlicher Willen'],
  ['cooking', 'Kochkunst', 0, 'Basic Campfire', 'mehr Objektplätze im Lager'],
  ['firstaid', 'Erste Hilfe', 0, 'First Aid Kit', 'wie Machtwort: Seelenstärke'],
  ['fishing', 'Angeln', 0, 'Fish Bowl', 'wie Segen der Könige']
];
const PR = Object.fromEntries(PROFS.map(p => [p[0], p]));

/* Game stages: f = fact from the sources, t = our tip */
const SRC = {
  names: ['Icy Veins: Namensreservierung', 'https://www.icy-veins.com/wow-forever/name-reservation'],
  names2: ['Team Overpowered: Namen und Nachnamen', 'https://teamoverpowered.com/forever/guides/name-reservation/'],
  prof: ['Warcraft Tavern: Berufe', 'https://www.warcrafttavern.com/forever/guides/professions/'],
  camp: ['Warcraft Tavern: Lager', 'https://www.warcrafttavern.com/forever/guides/camping/'],
  legacy: ['Blizzard: Legacy', 'https://news.blizzard.com/en-gb/article/24307383'],
  dung: ['Warcraft Tavern: Dungeons', 'https://www.warcrafttavern.com/forever/guides/dungeons/'],
  ride: ['Warcraft Tavern: Reiten', 'https://www.warcrafttavern.com/forever/guides/riding/'],
  cwg: ['ClassicWoW.gg: Termine und Raids', 'https://classicwow.gg/forever']
};
const STAGES = [
  { id: 'pre', n: 'Vor dem Start', sub: 'bis 04.11', lo: 0, hi: 0,
    todo: [['f', 'Frühe Namensreservierung 27.10 – 03.11 für Besitzer des Heroic, Epic und Collection Pack. Wer zuerst kommt, mahlt zuerst.'],
      ['f', 'Du kannst bis zu drei Charaktere pro Account reservieren. Ein Charakter hat Vor- und Nachnamen, und das Paar muss in der Region einzigartig sein.'],
      ['f', 'Ab 04.11 brauchst du zum Spielen ein Abo oder Spielzeit.'],
      ['t', 'Such dir vor dem 27.10 drei Namen mit Nachnamen aus, plus Reserve.']],
    dnote: 'Die ersten Dungeons öffnen ab Stufe 13.',
    prof: [['f', 'Jeder Charakter bekommt zwei Hauptberufe plus alle drei Nebenberufe: Kochkunst, Erste Hilfe und Angeln.'],
      ['f', 'Jeder Beruf stellt sein eigenes Lagerobjekt auf, mit einem Buff ähnlich einem Klassenbuff.'],
      ['t', 'Verteilt die Berufe vorher: Einer nimmt Kochkunst fürs Lagerfeuer, die anderen wählen verschiedene, damit sich Lagerbuffs nicht wiederholen.']],
    legacy: [['f', 'Legacy öffnet sich mit deinem ersten Punkt: Stufe 25, 150 in einem Beruf (kein Sammelberuf) oder die ganze Karte erkunden.'],
      ['f', 'Zum Start kann ein Charakter höchstens 16 Punkte ausgeben, der Rest geht in die Belohnungsleiste.']],
    group: [['t', 'Einigt euch auf eine Fraktion und einen Modus: Gruppen gehen nur innerhalb eines Modus, und im PvP hat ein Account eine Fraktion.'],
      ['t', 'Stellt euren Kader im Gruppenplaner zusammen: ein Tank, ein Heiler und verschiedene Klassen für Buffs.']],
    src: ['names', 'names2', 'prof', 'legacy'] },
  { id: 'first', n: 'Erste Tage', sub: 'Stufen 1–15', lo: 1, hi: 15,
    todo: [['f', 'Skyborne starten auf Zephras Isle, Stufen 1–12.'],
      ['f', 'Talente öffnen sich ab Stufe 10, oder ab 9 mit dem Legacy-Vorteil Talented (mit 5 Rängen ab Stufe 5).'],
      ['f', 'Das meiste gekochte Essen gibt einen Erfahrungsbonus. Er stapelt sich mit dem Lager und dem Gemütlichen Schlafsack.'],
      ['t', 'Sammle Erholung: Logge dich in einem Gasthaus oder in einem Lager mit Zelt aus.']],
    prof: [['f', 'Das einfache Lagerfeuer braucht keine Kochkunst und hält 3 Objekte. Es brennt etwa 10 Minuten, ein neues kannst du nach 5 aufstellen.'],
      ['f', 'Für Lagerbuffs setz dich mindestens eine Minute in die Nähe (/sit).'],
      ['t', 'Fang ab den ersten Stufen mit Sammelberufen an: Kräuter, Erz und Leder versorgen das Handwerk, und 150 in einem Handwerksberuf öffnet Legacy.']],
    legacy: [['f', 'Noch keine Vorteile: Der erste Punkt kommt mit Stufe 25 oder mit 150 in einem Beruf.'],
      ['t', 'Wenn Legacy offen ist, nimm zuerst Erfahrungs- und Lagervorteile: Well Rested, Field Guide, Permanence. Talented lohnt sich für Twinks.']],
    group: [['t', 'Levelt in derselben Zone und baut an jedem Halt ein Lager auf: Fünf Minuten am Lagerfeuer zahlen sich mit Buffs für die ganze Gruppe aus.'],
      ['t', 'Bildet eure erste Fünfergruppe bis Stufe 13–15.']],
    src: ['camp', 'legacy', 'dung'] },
  { id: 'dung', n: 'Dungeons', sub: 'Stufen 15–40', lo: 15, hi: 40,
    todo: [['f', 'Die meiste Dungeon-Erfahrung kommt aus den Questreihen. Wiederholte Runs danach geben spürbar weniger Erfahrung als Questen in der Welt.'],
      ['f', 'Jeder Gegenstand, der droppt, schaltet sein Transmog-Aussehen für alle frei, die ihn tragen können, auch wenn jemand anders ihn bekommen hat.'],
      ['f', 'Legacy öffnet sich ab Stufe 25.'],
      ['t', 'Sammelt die Dungeonquests zuerst als Gruppe und geht rein, wenn alle sie haben.']],
    prof: [['f', 'Kochkunst 140 gibt 5 Lagerplätze, 220 gibt 10.'],
      ['f', 'Jeder Beruf stellt drei Lagerobjekte her, eins pro Stufe. Die Quellen sind uneins, welcher Skill für Stufe 2 und 3 nötig ist.'],
      ['t', 'Wenn Stufe 25 noch weit weg ist, bring einen Handwerksberuf auf 150: Legacy öffnet sich früher.']],
    legacy: [['f', 'Jede Herausforderung gibt 1 Punkt. Es gibt 65: Klassen 27, Berufe 18, PvP 12, Dungeons 3, Raids 3, Abenteuer 2.'],
      ['t', 'Reagent Economy (keine gekauften Reagenzien für Fähigkeiten) und Field Guide (kürzere Abklingzeit für Lagerobjekte) lohnen sich.']],
    group: [['f', 'Ein Dungeon ist für 5 Spieler gebaut: ein Tank, ein Heiler und drei Schadensverursacher.'],
      ['f', 'Es gibt keine Stufenskalierung, ein Freund, der weit zurückliegt, hat es im Dungeon also schwer.'],
      ['t', 'Haltet die Stufen nah beieinander: Wer zurückfällt, holt mit Quests auf, und Dungeons lauft ihr gemeinsam.']],
    src: ['dung', 'camp', 'legacy'] },
  { id: 'path', n: 'Weg zur 60', sub: 'Stufen 40–60', lo: 40, hi: 60,
    todo: [['f', 'Ein Reittier ab Stufe 40 (60 % Tempo), ein schnelles ab 60 (100 %). Lerne es beim Lehrer deines Volkes.'],
      ['f', 'Paladine und Hexenmeister bekommen ihr Reittier über Klassenquests.'],
      ['f', 'Wohlwollend bei deiner eigenen Fraktion gibt 10 % Rabatt auf Reitausbildung und Reittiere. Laut Warcraft Tavern: 100 + 20 Gold auf Stufe 40, 1.000 + 200 auf 60.'],
      ['t', 'Spar Gold für Stufe 40: Reiten wird deine größte Ausgabe auf dem Weg zur 60.']],
    prof: [['f', 'Jeder Beruf hat eigene Lagerobjekte der Stufe 2 und 3. Das zweite Objekt der Ingenieurskunst, Reparaturbot, repariert Ausrüstung.'],
      ['t', 'Haltet Kochkunst 220 in der Gruppe für ein Lager mit 10 Objekten: Zur Raidzeit ist dann Platz für alle.']],
    legacy: [['f', 'Höchstens 16 Punkte pro Charakter, der Rest geht in die Belohnungsleiste: ein Spielzeug bei 15, ein Haustier bei 25, ein Wappenrock bei 40, ein Reittier bei 55.']],
    group: [['f', 'Raids öffnen am 09.12: Barrow Deeps für 10 Spieler, Hyjalgipfel für 20, Onyxias Hort für 40.'],
      ['t', 'Der Raid für 10 Spieler braucht 10 Spieler: Wenn ihr weniger seid, sucht den Rest früh in eurer Gilde.']],
    src: ['ride', 'prof', 'legacy', 'cwg'] },
  { id: 'raid', n: '60 und Raids', sub: 'ab 09.12', lo: 60, hi: 60,
    todo: [['f', 'Am 09.12 öffnen Barrow Deeps (10 Spieler), Hyjalgipfel (20) und Onyxias Hort (40, Marschen von Dustwallow).'],
      ['f', 'Jeder der drei Raids gibt beim Abschluss einen Legacy-Punkt.'],
      ['f', 'Neues Schlachtfeld 15 gegen 15: Darkspear Islands vor der Küste der Marschen von Dustwallow.'],
      ['t', 'Während ihr Leute für den Raid sammelt, lauft Dungeons der Stufe 60 für Ausrüstung.']],
    prof: [['f', 'Lagerbuffs sind etwas schwächer als Klassenbuffs und stapeln sich nicht mit ihnen: Segen der Könige gibt 10 % auf alle Werte, das Lager 8 %.'],
      ['t', 'Baut das Lager am Raideingang auf: Seine Buffs decken ab, was euren Klassen fehlt.']],
    legacy: [['f', 'Herausforderungen für Stufe 60: Dungeons 3, Raids 3, PvP 12. PvP hat Ränge mit Wochenlimit und Ausrüstungsupgrades für Ehre.']],
    group: [['f', 'Gleiche Buffs von zwei Spielern derselben Klasse überschneiden sich, verschiedene Klassen stapeln sich.'],
      ['t', 'Stellt euren Raidkader im Gruppenplaner zusammen und postet den Link im Chat.']],
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
  if (now < D_REL) return ['pre', 'Nach Datum gewählt: vor dem Start am 04.11.'];
  if (me.lvl) return [me.lvl < 15 ? 'first' : me.lvl < 40 ? 'dung' : me.lvl < 60 ? 'path' : 'raid', 'Nach der Stufe deines Charakters gewählt.'];
  if (now >= D_RAID) return ['raid', 'Nach Datum gewählt: Raids sind offen.'];
  return [now < new Date('2026-11-11T00:00:00') ? 'first' : 'dung', 'Nach Datum gewählt. Trag die Stufe deines Charakters ein, dann folgt die Phase ihr.'];
}
const START = { pre: 'hero_dawn-960', first: 'hero_campfire-960', dung: 'warlock-360', path: 'hunter-360', raid: 'paladin-360' };
const ARTV = /*ARTV*/{"hero_campfire-960.avif":"?v=93981d6a","hero_campfire-960.webp":"?v=5aa0e1b2","hero_dawn-960.avif":"?v=447302fd","hero_dawn-960.webp":"?v=b2d0d95b"};   // ?v= of the scene arts, filled in by build.art_version (same names, redrawn pictures)
const pic = f => `<picture><source type="image/avif" srcset="${ROOT}assets/art/${f}.avif${ARTV[f + '.avif'] || ''}"><img src="${ROOT}assets/art/${f}.webp${ARTV[f + '.webp'] || ''}" alt="" loading="lazy" decoding="async"></picture>`;
const tipL = () => '<span class="tl">Tipp</span>';
function liC(x) { return x[0] === 't' ? `<li class="tip">${tipL()}${esc(x[1])}</li>` : `<li>${esc(x[1])}</li>`; }
function dLi(d) {
  const mine = me.lvl && nearLvl(d, me.lvl);
  return `<li class="${mine ? 'mine' : ''}"><b>${esc(d[0])}</b><span class="lvl${mine ? ' gold' : ''}">${lvRange(d)}</span><span class="z">${esc(d[3])}${d[4] ? ' · <i>neu</i>' : ''}${mine ? '<span class="sr"> · für deine Stufe</span>' : ''}</span></li>`;
}
function renderStage() {
  const [auto, why] = autoStage();
  if (stageAuto) stageSel = auto;
  const s = ST[stageSel];
  $('#stageBar').innerHTML = STAGES.map(x => `<button type="button" class="stile" role="tab" id="tab-${x.id}" data-st="${x.id}" aria-controls="stagePanel" aria-selected="${x.id === stageSel}" tabindex="${x.id === stageSel ? 0 : -1}">${pic(START[x.id])}<b>${esc(x.n)}</b><span class="lv">${esc(x.sub)}${x.id === auto ? ' · <span class="now">jetzt</span>' : ''}</span></button>`).join('');
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
  $('#stagePanel').innerHTML = `<div class="st-head"><div class="t"><h3>${esc(s.n)}</h3><span class="when">${esc(s.sub)}</span></div><p class="why">${stageAuto ? esc(why) : 'Phase manuell gewählt.'}</p></div>
    <ol class="steps-c">${steps}</ol>
    <div class="st-cols">
      <div><h4>Dungeons für diese Stufe</h4>${s.dnote ? `<p class="small" style="margin:-4px 0 10px">${esc(s.dnote)}</p>` : ''}<ul class="dlist">${ds.slice(0, MAXD).map(dLi).join('')}</ul>
        <a class="more-l" href="guides/dungeons/">${extra > 0 ? `Mehr Dungeons in der Tabelle: ${extra}` : 'Alle 35 Dungeons'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
      <div style="display:grid;gap:24px;align-content:start"><div><h4>Berufe und Lager</h4><ul class="clean">${s.prof.map(liC).join('')}</ul></div>
        <div><h4>Legacy-Vorteile</h4><ul class="clean">${s.legacy.map(liC).join('')}</ul></div></div>
    </div>
    <div class="gtip"><h4 style="margin:0 0 10px;font-size:var(--fs-16)">Tipps für die Gruppe</h4><ul class="clean">${s.group.map(liC).join('')}</ul></div>
    <p class="st-src"><span>Quellen:</span>${s.src.map(k2 => `<a href="${SRC[k2][1]}" target="_blank" rel="noopener">${esc(SRC[k2][0])}</a>`).join('')}</p>`;
}
function optList(items, cur, none) { return `<option value="">${esc(none)}</option>` + items.map(([v, t]) => `<option value="${v}"${v === cur ? ' selected' : ''}>${esc(t)}</option>`).join(''); }
function renderMe() {
  fixMe();
  const races = f => RACES.filter(r => r.f === f).map(r => `<option value="${r.id}"${r.id === me.race ? ' selected' : ''}>${esc(r.n)}</option>`).join('');
  $('#meRace').innerHTML = `<option value="">Nicht gewählt</option><optgroup label="${facName('alliance')}">${races('alliance')}</optgroup><optgroup label="${facName('horde')}">${races('horde')}</optgroup>`;
  const cls = (me.race ? Object.keys(RC[me.race].can) : CLASSES.map(c => c.id)).map(id => [id, CL[id].n]);
  $('#meCls').innerHTML = optList(cls, me.cls, 'Nicht gewählt');
  $('#meRole').innerHTML = me.cls ? roleOpts(CL[me.cls]).map(x => `<option value="${x}"${x === me.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('') : `<option value="">Wähle zuerst eine Klasse</option>`;
  $('#meRole').disabled = !me.cls;
  const prim = PROFS.filter(p => p[2]);
  $('#meP1').innerHTML = optList(prim.filter(p => p[0] !== me.p2).map(p => [p[0], p[1]]), me.p1, 'Keine');
  $('#meP2').innerHTML = optList(prim.filter(p => p[0] !== me.p1).map(p => [p[0], p[1]]), me.p2, 'Keine');
  $('#meSec').innerHTML = PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${me.sec.includes(p[0])}">${esc(p[1])}</button>`).join('');
  document.querySelectorAll('.lvin').forEach(i => { if (document.activeElement !== i) i.value = me.lvl || ''; });
  const who = [me.race ? RC[me.race].n : '', me.cls ? CL[me.cls].n : ''].filter(Boolean).join(' · ');
  const sub = me.cls ? [ROLE_RU[me.role], me.race ? facName(RC[me.race].f) : ''].filter(Boolean).join(' · ') : 'Wähle unten Volk, Klasse und Stufe';
  const hero = $('#meHero');
  hero.style.setProperty('--cc', me.cls ? CCOL[me.cls] : '#c9a54a');
  hero.innerHTML = pic(me.cls ? `${me.cls}-600` : 'hero_campfire-960') + (me.lvl ? `<span class="lvb" aria-label="Stufe ${me.lvl}">${me.lvl}</span>` : '')
    + `<span class="k">Mein Charakter</span><b>${who ? esc(who) : 'Noch nicht erstellt'}</b><span class="s">${esc(sub)}</span>`;
  let out = '';
  if (meSet()) {
    const b = [];
    if (me.cls) b.push(BUFF[me.cls] ? `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span><b>${esc(CL[me.cls].n)}:</b> ${esc(BUFF[me.cls])}</span></li>` : `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-dps"/></svg></span><span>${esc(CL[me.cls].n)}: kein Gruppenbuff, reiner Schaden.</span></li>`);
    [me.p1, me.p2, ...me.sec].filter(Boolean).forEach(id => { const p = PR[id]; b.push(`<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg></span><span><b>${esc(p[3])}</b> <span class="m">· ${esc(p[1])}</span><br>${esc(p[4])}</span></li>`); });
    if (!b.length) b.push('<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span>Wähle Klasse und Berufe, um deine Buffs zu sehen.</span></li>');
    out += `<div><h4>Was du der Gruppe bringst</h4><ul class="buffs">${b.join('')}</ul></div>`;
    if (me.lvl) {
      const ds = DUNGEONS.filter(d => nearLvl(d, me.lvl) && facOk(d, me.race && RC[me.race].f));
      out += `<div><h4>Dungeons für deine Stufe</h4>` + (ds.length ? `<ul class="dlist">${ds.slice(0, 4).map(dLi).join('')}</ul>` : '<p class="small">Die ersten Dungeons beginnen ab Stufe 13.</p>')
        + `<a class="more-l" href="guides/dungeons/">${ds.length > 4 ? `Mehr Dungeons in der Tabelle: ${ds.length - 4}` : 'Dungeontabelle'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`;
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
