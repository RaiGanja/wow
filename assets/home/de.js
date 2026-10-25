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
const PV = /*PV*/'?v=6114caef';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Schneller um ${-p}%` : p > 0 ? `Langsamer um ${p}%` : 'Durchschnittstempo';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>schneller</span><span>langsamer</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Klasse</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Leveln</span><span>In Raids</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Rollen: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Volk</span><span>Klassen</span><span class="abl">Fähigkeiten <span class="abt">aktiv</span><span class="abt p">passiv</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">bezahlt</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Klassen: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', neu' : v ? '' : ', nicht verfügbar')); }).join('')}</span>
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
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext}${PV} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Mehr zur Klasse</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
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
