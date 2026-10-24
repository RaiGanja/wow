const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Guerrier', s:'Guerrier', roles:['tank','dps'],
    specs:[['Armes','Dégâts en mêlée (arme à deux mains)',['dps']],['Fureur','Dégâts en mêlée (deux armes)',['dps']],['Protection','Tank',['tank']]],
    lvl:'La progression la plus lente, environ 12% plus longue que la moyenne',
    lp:12,
    raid:'Cri de guerre affecte tout le raid',
    forever:'Plus de rage, meilleure menace sur les groupes de cibles, le talent Weapon Master. Fureur et Sanguinaire sont affaiblis.' },
  { id:'paladin', n:'Paladin', roles:['tank','heal','dps'],
    specs:[['Sacré','Soigneur',['heal']],['Protection','Tank',['tank']],['Vindicte','Dégâts en mêlée',['dps']]],
    lvl:'Rythme de progression moyen',
    lp:0,
    raid:'Bénédiction des rois est désormais de base. Selon les classements de la bêta, Protection compte parmi les meilleurs tanks, et Vindicte a reculé après le patch du 15 octobre.',
    forever:'Frappe sacrée dès le niveau 6, Jugement ne consomme pas le sceau. Les morts-vivants peuvent désormais être paladins, la classe arrive donc dans la Horde.' },
  { id:'hunter', n:'Chasseur', roles:['dps'],
    specs:[['Maîtrise des bêtes','Dégâts à distance, beaucoup de dégâts du familier',['dps']],['Précision','Dégâts à distance',['dps']],['Survie','Mêlée et distance, pièges',['dps']]],
    lvl:'La progression la plus rapide, environ 8% plus rapide que la moyenne',
    lp:-8,
    raid:'Aura de précision affecte tout le raid',
    forever:'Vous pouvez jouer sans familier, les pièges fonctionnent en combat, les renards arrivent comme famille de familiers. Survie peut jouer en mêlée.' },
  { id:'rogue', n:'Voleur', roles:['dps'],
    specs:[['Assassinat','Dégâts de poison',['dps']],['Combat','Attaques rapides à l’arme',['dps']],['Finesse','Embuscades, saignements',['dps']]],
    lvl:'Rythme de progression moyen',
    lp:0,
    raid:'Dégâts de mêlée purs, sans amélioration pour le raid',
    forever:'Les haches à une main sont désormais utilisables. Assassinat repose sur les poisons, Finesse sur les saignements et le camouflage.' },
  { id:'priest', n:'Prêtre', roles:['heal','dps'],
    specs:[['Discipline','Soigneur, boucliers et absorption',['heal']],['Sacré','Soigneur',['heal']],['Ombre','Dégâts à distance',['dps']]],
    lvl:'Environ 5% plus lent que la moyenne',
    lp:5,
    raid:'Esprit divin est désormais de base. Les dégâts d’ombre et Peste dévorante (24 s de temps de recharge) ont été renforcés par le patch du 15 octobre.',
    forever:'Gardien de peur et Peste dévorante sont disponibles dès le niveau 20 pour toutes les races. Chaque race a deux sorts de prêtre qui lui sont propres.' },
  { id:'shaman', n:'Chaman', roles:['heal','dps','tank?'],
    specs:[['Élémentaire','Dégâts à distance',['dps']],['Amélioration','Dégâts en mêlée. La capacité à tanker reste incertaine',['dps','tank?']],['Restauration','Soigneur',['heal']]],
    lvl:'Rythme de progression moyen',
    lp:0,
    raid:'Les totems Force de la Terre, Furie-des-vents, Langue de feu et Grâce aérienne améliorent leur groupe',
    forever:'Les nains peuvent désormais être chamans, la classe arrive donc dans l’Alliance. Explosion de lave a été renforcée, Élémentaire est monté dans les classements de dégâts.' },
  { id:'mage', n:'Mage', roles:['dps'],
    specs:[['Arcanes','Pics de dégâts, beaucoup de mana',['dps']],['Feu','Critiques et enflammer',['dps']],['Givre','Dégâts et contrôle',['dps']]],
    lvl:'La progression la plus rapide, environ 8% plus rapide que la moyenne (environ 12 heures gagnées)',
    lp:-8,
    raid:'Portails, nourriture et eau pour tout le groupe',
    forever:'Feu reçoit Chaleur continue, Arcanes Déflagration des arcanes, Givre Javelot de glace. Éclair de givrefeu est disponible dès le niveau 40.' },
  { id:'warlock', n:'Démoniste', roles:['dps'],
    specs:[['Affliction','Dégâts des malédictions et de la corruption',['dps']],['Démonologie','Dégâts par les démons',['dps']],['Destruction','Dégâts directs de feu et d’ombre',['dps']]],
    lvl:'Rythme de progression moyen',
    lp:0,
    raid:'Maîtrise de l’ombre donne désormais 2–10% de dégâts d’ombre (avant 1–5%)',
    forever:'Affliction a un nouveau sort canalisé, le démon reste avec Sacrifice démoniaque, Destruction gagne Incinérer et des dégâts de zone.' },
  { id:'druid', n:'Druide', roles:['tank','heal','dps'],
    specs:[['Équilibre','Dégâts à distance',['dps']],['Combat farouche','Tank (ours) et dégâts en mêlée (félin)',['tank','dps']],['Restauration','Soigneur, beaucoup de soins sur la durée',['heal']]],
    lvl:'Environ 5% plus lent que la moyenne',
    lp:5,
    raid:'Chef de la meute et Aura de sélénien affectent tout le raid et se cumulent',
    forever:'Chaque spécialisation a reçu un rôle clair, les formes fonctionnent avec les potions et les enchantements d’arme. Vous pouvez être tank, soigneur et combattant sur un seul personnage.' }
];
const ROLE_RU = { tank:'Tank', heal:'Soigneur', dps:'Dégâts', 'tank?':'Tank (incertain)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Cri de guerre', paladin:'Bénédiction des rois', hunter:'Aura de précision', priest:'Mot de pouvoir : Robustesse, Esprit divin', shaman:'Totems (Force de la Terre, Furie-des-vents, Langue de feu, Grâce aérienne)', mage:'Intelligence des arcanes, portails, nourriture et eau', druid:'Marque du fauve, Chef de la meute, Aura de sélénien' };

const RACES = [
  { id:'human', n:'Humain', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Volonté de survie','Supprime l’étourdissement'],['a','Perception','Révèle les ennemis invisibles pendant 20 s'],['p','Ruthless','+2% de chances de critique'],['p','L’esprit humain','+5% d’esprit']],
    tip:'L’esprit sert aux soins d’un prêtre Sacré, un prêtre humain est donc bon pour soigner.' },
  { id:'dwarf', n:'Nain', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Forme de pierre','Immunité aux saignements, poisons et maladies pendant 8 s et dégâts physiques réduits'],['a','Découverte de trésors','Affiche les coffres proches'],['p','Earth Fury','+2% de dégâts critiques et de puissance de soins'],['p','Big Game Hunter','+5% de dégâts contre les bêtes']],
    tip:'Forme de pierre est utile aux tanks et en JcJ.' },
  { id:'nightelf', n:'Elfe de la nuit', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Lumière d’Élune','+10% de chances de critique pendant 15 s'],['a','Camouflage dans l’ombre','Invisibilité sur place'],['p','Rapidité','+1% d’esquive et +2% de vitesse de course'],['p','Esprit feu follet','+75% de vitesse de course sous forme d’esprit']],
    tip:'La seule race de l’Alliance avec un druide, à moins de prendre un Skyborne.' },
  { id:'gnome', n:'Gnome', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Maître de l’évasion','Brève immunité aux ralentissements et immobilisations'],['a','Eureka!','Les 3 prochaines techniques coûtent moins cher et sont 10% plus fortes'],['p','Pensée expansive','+5% de mana, rage ou énergie maximum'],['p','Spécialisation en ingénierie','Les appareils d’ingénierie fonctionnent de façon plus fiable']],
    tip:'Pensée expansive aide surtout les classes à énergie.' },
  { id:'skyA', n:'Skyborne (Alliance)', f:'alliance', paid:true, name:'Skyborne High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Planez pendant 10 s, sans dégâts de chute'],['a','Read Ley Line','+100% de régénération de vie et de mana'],['p','Wind Blessed','+3% de vitesse d’attaque et d’incantation'],['p','Elemental Insight','+5% de dégâts contre les élémentaires']],
    tip:'Race payante : pack Héroïque dès $29.99. Débute sur Zephras Isle (niveaux 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Fureur sanguinaire','+10% de puissance d’attaque et de puissance des sorts pendant 15 s'],['a','Shatter Curse','Retire malédictions et corruption, −5% de dégâts magiques subis pendant 8 s'],['p','Savage','+1% de chances de critique'],['p','Solidité','Étourdissements 20% plus courts']],
    tip:'Fureur sanguinaire offre une puissante fenêtre de dégâts.' },
  { id:'undead', n:'Mort-vivant', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Volonté des Réprouvés','Supprime charme, peur et sommeil'],['a','Cannibalisme','Rend 35% de la vie et du mana sur la durée'],['p','Respiration aquatique','Respirez plus longtemps sous l’eau'],['p','Toucher du tombeau','Chance de drainer de la vie en attaquant']],
    tip:'Nouvelle combinaison : un paladin pour la Horde, où cette classe n’existait pas.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Choc martial','Étourdit les ennemis proches pendant 2 s'],['a','Culture','Fait pousser des herbes récoltables sans Herboristerie'],['p','Course dans les plaines','La vitesse augmente pendant que vous courez'],['p','Endurcissement','+5% de vie et +2% de dégâts critiques']],
    tip:'La seule race de la Horde avec un druide, à moins de prendre un Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserker','+10% de vitesse d’attaque et d’incantation pendant 10 s'],['a','Régénération rapide','Rend de la vie sur la durée'],['p','Tueur de bêtes','+5% de dégâts contre les bêtes'],['p','Régénération','La vie se régénère aussi en combat']],
    tip:'Le plus de choix de classes dans la Horde : sept.' },
  { id:'skyH', n:'Skyborne (Horde)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Planez pendant 10 s, sans dégâts de chute'],['a','Skysight','+10% de vitesse de course'],['p','Wind Blessed','+3% de vitesse d’attaque et d’incantation'],['p','Elemental Insight','+5% de dégâts contre les élémentaires']],
    tip:'Race payante : pack Héroïque dès $29.99. Seule la Horde peut avoir un chaman, seule l’Alliance un mage.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "La race la plus nombreuse de l’Alliance. Polyvalente et forte en JcJ grâce à Volonté de survie.", "dwarf": "Robustes mineurs et fusiliers de Ironforge. Pour la première fois dans Classic, l’Alliance a des chamans, et ce sont des nains.", "nightelf": "Un peuple ancien des forêts. Insaisissables : leur propre façon de se cacher, d’esquiver et de courir vite.", "gnome": "Les inventeurs de Gnomeregan. Petits, rusés et avec la meilleure capacité d’évasion du jeu.", "skyA": "Une nouvelle race dans Forever. Le High Order : des elfes du vent en quête de la magie des arcanes perdue de leurs ancêtres.", "orc": "Le cœur de la Horde. Les meilleurs guerriers et maîtres du JcJ grâce à Fureur sanguinaire et Solidité.", "undead": "Les Réprouvés : d’anciens humains libérés du roi-liche. Immunisés contre la peur et le sommeil quand ça compte.", "tauren": "Paisibles géants des plaines. Le plus de vie et leur propre étourdissement de zone.", "troll": "La tribu Sombrelance. Le plus de classes de la Horde et un puissant Berserker pour les dégâts.", "skyH": "Une nouvelle race dans Forever. Les Windshapers : guides spirituels des Skyborne, proches des éléments."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Armes':'Arms','Fureur':'Fury','Protection':'Protection','Sacré':'Holy','Vindicte':'Retribution',
  'Maîtrise des bêtes':'Beast Mastery','Précision':'Marksmanship','Survie':'Survival',
  'Assassinat':'Assassination','Combat':'Combat','Finesse':'Subtlety',
  'Discipline':'Discipline','Ombre':'Shadow','Élémentaire':'Elemental','Amélioration':'Enhancement','Restauration':'Restoration',
  'Arcanes':'Arcane','Feu':'Fire','Givre':'Frost','Affliction':'Affliction','Démonologie':'Demonology','Destruction':'Destruction',
  'Équilibre':'Balance','Combat farouche':'Feral',
  'Volonté de survie':'Will to Survive','Perception':'Perception','Ruthless':'Ruthless','L’esprit humain':'The Human Spirit',
  'Forme de pierre':'Stoneform','Découverte de trésors':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Lumière d’Élune':"Elune’s Light",'Camouflage dans l’ombre':'Shadowmeld','Rapidité':'Quickness','Esprit feu follet':'Wisp Spirit',
  'Maître de l’évasion':'Escape Artist','Eureka!':'Eureka!','Pensée expansive':'Expansive Mind','Spécialisation en ingénierie':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Fureur sanguinaire':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Solidité':'Hardiness',
  'Volonté des Réprouvés':'Will of the Forsaken','Cannibalisme':'Cannibalize','Respiration aquatique':'Underwater Breathing','Toucher du tombeau':'Touch of the Grave',
  'Choc martial':'War Stomp','Culture':'Cultivation','Course dans les plaines':'Plainsrunning','Endurcissement':'Endurance',
  'Berserker':'Berserking','Régénération rapide':'Rapid Regeneration','Tueur de bêtes':'Beast Slaying','Régénération':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Conseil</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Alliance' : 'Horde'; }
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Plus rapide de ${-p}%` : p > 0 ? `Plus lent de ${p}%` : 'Rythme moyen';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>plus rapide</span><span>plus lent</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Classe</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Progression</span><span>En raid</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Rôles : ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Race</span><span>Classes</span><span class="abl">Capacités <span class="abt">active</span><span class="abt p">passive</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">payant</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Classes : ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nouveau' : v ? '' : ', indisponible')); }).join('')}</span>
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
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">payant</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: impossible"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', nouvelle combinaison' : ''}`;
        const mark = v === 'new' && !sel ? '<span class="nw">nouveau</span>' : '<i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>';
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
    return `<button type="button" data-pc="${c.id}" class="${v ? '' : 'na'}" aria-pressed="${c.id === state.cls}">${esc(c.n)}${v === 'new' ? ' · nouveau' : ''}</button>`;
  }).join('');
  $('#pickm').innerHTML = `<div><div class="lbl">1. Race</div><div class="chiprow">${races}</div></div>
    <div><div class="lbl">2. Classe (pointillés : indisponible pour cette race, touchez pour changer de race)</div><div class="chiprow">${cls}</div></div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Active' : 'Passive'}</span><b>${bi(x[1])}</b><span>${esc(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', pack Skyborne requis' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><img src="../assets/art/${c.id}-600.webp" width="600" height="804" alt="" loading="lazy" decoding="async"></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}${face(c.id, CCOL[c.id])}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Nouvelle combinaison</span>' : ''}${r.paid ? '<span class="tag paid">Race payante</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Spécialisations</h4><div class="cards">${specs}</div></div>
        <div><h4>Capacités raciales</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Progression</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>En raid</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Nouveautés</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Mon choix">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copier mon choix</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copié');
  $('#qPick').textContent = `Maintenant : ${r.n} · ${c.n}`;
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
  warrior: 'Plaques, rage et première ligne. Encaisse les coups en tank ou fauche avec une arme à deux mains.',
  paladin: 'Un guerrier sacré en plaques : soigne, tanke et frappe au marteau. Désormais aussi dans la Horde.',
  hunter: 'Arc, pièges et une bête fidèle à vos côtés. L’une des classes les plus rapides à monter.',
  rogue: 'Poisons, lames et ombre. Dégâts purs depuis l’embuscade et contrôle des foules.',
  priest: 'La Lumière et l’Ombre dans les mêmes mains. Le soigneur principal du groupe ou un lanceur de sorts obscur.',
  shaman: 'Totems et éléments : soigne, frappe avec la foudre ou les armes. Désormais aussi dans l’Alliance.',
  mage: 'Magie du feu, du givre et des arcanes. Portails, nourriture et eau pour toute l’équipe.',
  warlock: 'Malédictions, démons et feu. Dégâts sur la durée et votre propre démon pour vous aider.',
  druid: 'Ours, félin, sélénien ou soigneur : les trois rôles sur un seul personnage.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">En savoir plus sur la classe</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">payant</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">En savoir plus sur la race</span></span>
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
  $('#szNote').textContent = n ? `${parties} groupes de 5${n % PARTY ? ', le dernier est incomplet' : ''}` : '';
  const races = RACES.filter(r => r.f === team.f);
  let html = '';
  for (let g = 0; g < parties; g++) {
    const part = team.list.slice(g * PARTY, g * PARTY + PARTY), c = countRoles(part);
    const need = [];
    if (!c.tank) need.push('pas de tank'); if (!c.heal) need.push('pas de soigneur'); if (part.length < PARTY) need.push(`manque ${PARTY - part.length}`);
    const status = need.length ? `<span class="miss">${need.join(', ')}</span>` : '<span class="ok">groupe complet</span>';
    html += `<div class="party"><div class="party-h"><h4>Groupe ${g + 1}</h4><span class="pc"><span>${ri('tank')}${c.tank}</span><span>${ri('heal')}${c.heal}</span><span>${ri('dps')}${c.dps}</span>${status}</span></div>`;
    part.forEach((s, k) => {
      const i = g * PARTY + k, r = RC[s.race], ro = roleOpts(CL[s.cls]);
      html += `<div class="slot" style="--cc:${CCOL[s.cls]}" data-i="${i}"><span class="no av"><img src="${ROOT}assets/art/${s.cls}-face.webp" width="160" height="160" alt="" loading="lazy" decoding="async"><b>${i + 1}</b></span>
      <select class="srace" aria-label="Race du joueur ${i + 1}">${races.map(x => `<option value="${x.id}"${x.id === s.race ? ' selected' : ''}>${esc(x.n)}${x.paid ? ' (payant)' : ''}</option>`).join('')}</select>
      <select class="scls" aria-label="Classe du joueur ${i + 1}">${Object.keys(r.can).map(c2 => `<option value="${c2}"${c2 === s.cls ? ' selected' : ''}>${esc(CL[c2].n)}</option>`).join('')}</select>
      <select class="srole" aria-label="Rôle du joueur ${i + 1}">${ro.map(x => `<option value="${x}"${x === s.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('')}</select>
      <button class="del" aria-label="Retirer le joueur ${i + 1}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></div>`;
    });
    html += '</div>';
  }
  $('#slots').innerHTML = html;
  $('#bAdd').disabled = n >= MAXT;
  const cnt = countRoles(team.list);
  $('#roleSum').innerHTML = RR.map(x => `<div class="rs ${cnt[x] ? 'ok' : 'zero'}"><b>${cnt[x]}</b><span>${ri(x)}${ROLE_RU[x]}</span></div>`).join('');
  const v = [];
  if (!n) v.push(['', 'Touchez une taille de groupe ou ajoutez un joueur.']);
  else {
    const full = Array.from({ length: parties }, (_, g) => team.list.slice(g * PARTY, g * PARTY + PARTY)).filter(p => p.length === PARTY && p.some(s => s.role === 'tank') && p.some(s => s.role === 'heal')).length;
    if (full) v.push(['good', `Groupes prêts pour un donjon : ${full} sur ${parties}. Chacun a un tank et un soigneur.`]);
    if (full < parties) v.push(['warn', 'Certains groupes manquent de tank, de soigneur ou de joueurs. Ils sont mis en évidence dans la liste.']);
    RAIDS.forEach(([size, name]) => v.push([n >= size ? 'good' : '', n >= size ? `Raid de ${size} (${name}) : assez de joueurs.` : `Raid de ${size} (${name}) : il en manque ${size - n}.`]));
    const byCls = {}; team.list.forEach(s => byCls[s.cls] = (byCls[s.cls] || 0) + 1);
    const dup = Object.keys(byCls).filter(c => byCls[c] > 1 && BUFF[c]);
    if (dup.length && n <= 10) v.push(['', `Classes identiques (${dup.map(c => CL[c].n).join(', ')}) : leurs améliorations se chevauchent, la deuxième apporte moins.`]);
    const sky = team.list.filter(s => RC[s.race].paid).length;
    if (sky) v.push(['', `Skyborne est une race payante : le pack Héroïque dès $29.99 est nécessaire pour ${sky} sur ${n} joueurs.`]);
  }
  $('#verdict').innerHTML = v.map(x => `<li class="${x[0]}">${esc(x[1])}</li>`).join('');
  const have = [...new Set(team.list.map(s => s.cls))];
  const withB = have.filter(c => BUFF[c]), noB = have.filter(c => !BUFF[c]);
  $('#buffs').innerHTML = (withB.length ? withB.map(c => `<li class="good"><span class="cdot" style="--cc:${CCOL[c]}"></span><b>${esc(CL[c].n)}:</b> ${esc(BUFF[c])}</li>`).join('') : '<li>Pas encore de classes avec des améliorations de groupe.</li>')
    + (noB.length ? `<li>Sans amélioration de groupe : ${noB.map(c => CL[c].n).join(', ')}. Ils font des dégâts purs.</li>` : '');
  $('#teamText').value = n ? Array.from({ length: parties }, (_, g) => (parties > 1 ? `Groupe ${g + 1}: ` : '') + team.list.slice(g * PARTY, g * PARTY + PARTY).map(s => `${raceName(RC[s.race])} ${CL[s.cls].n} (${ROLE_RU[s.role]})`).join(', ')).join('; ') + ` — ${facName(team.f)}` : '';
  $('#qTeam').textContent = n ? `${facName(team.f)}, joueurs : ${n}, tanks ${cnt.tank}, soigneurs ${cnt.heal}` : 'De un à quarante joueurs';
  if (teamTouched) { try { history.replaceState(null, '', n ? teamLink() : location.pathname); } catch (e) {} }
}
function touch() { teamTouched = true; renderTeam(); }
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Copie impossible, sélectionnez le texte et appuyez sur Ctrl+C'; }
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
$('#copyTeam').onclick = () => copyTo($('#teamText').value, $('#teamMsg'), 'Groupe copié');
$('#copyLink').onclick = () => copyTo(teamLink(), $('#teamMsg'), 'Lien copié');
if (!fromLink) team.list = autoTeam(5, team.f);
renderTeam();
if (fromLink) setTimeout(() => document.getElementById('builder').scrollIntoView(), 0);

/* Dungeons: [name, min, max, entrance zone, new, other sites' ranges where they differ] */
const DUNGEONS = [
  ['Gouffre de Ragefeu', 13, 18, 'Orgrimmar', 0, [], 'horde'],
  ['Hall of Thanes', 13, 18, 'Ironforge', 1, [['Icy Veins', '13–20']]],
  ['Ruines de Lordaeron', 15, 20, 'Clairières de Tirisfal', 1, [['Icy Veins', '15–22']]],
  ['Les Mortemines', 15, 22, 'Marche de l’Ouest', 0, [['Icy Veins', '17–26']]],
  ['Cavernes des lamentations', 17, 24, 'Les Tarides', 0, [['Icy Veins', '15–24']]],
  ['Donjon d’Ombrecroc', 20, 26, 'Forêt des Pins argentés', 0, [['Icy Veins', '20–30']]],
  ['Profondeurs de Brassenoire', 22, 28, 'Ashenvale', 0, [['Sportskeeda', '22–26'], ['Icy Veins', '24–32']]],
  ['Excavation Site: Wetlands', 24, 29, 'Les Paluns', 1, [['ClassicWoW.gg', '26–31'], ['Icy Veins', '26–33']]],
  ['La Prison', 25, 29, 'Cité de Stormwind', 0, [['Icy Veins', '24–32']], 'alliance'],
  ['City of Dalaran', 28, 33, 'Montagnes d’Alterac', 1, [['Icy Veins', '28–35']]],
  ['Gnomeregan', 29, 38, 'Dun Morogh', 0],
  ['Kraal de Tranchebauge', 29, 38, 'Les Tarides', 0],
  ['Monastère écarlate : Cimetière', 30, 38, 'Clairières de Tirisfal', 0],
  ['Monastère écarlate : Bibliothèque', 33, 41, 'Clairières de Tirisfal', 0],
  ['The Drowned City', 35, 40, 'Vallée de Strangleronce', 1],
  ['Monastère écarlate : Armurerie', 36, 44, 'Clairières de Tirisfal', 0],
  ['Uldaman', 36, 45, 'Terres ingrates', 0, [['Icy Veins', '41–51']]],
  ['Souilles de Tranchebauge', 37, 46, 'Les Tarides', 0],
  ['Monastère écarlate : Cathédrale', 38, 46, 'Clairières de Tirisfal', 0],
  ["Zul’Farrak", 40, 47, 'Tanaris', 0, [['Icy Veins', '44–54']]],
  ["Krol’dok Stronghold", 40, 45, 'Riverglades', 1],
  ['Maraudon', 45, 51, 'Désolace', 0, [['Icy Veins', '46–55']]],
  ['Alcaz Island Prison', 48, 53, 'Marécage d’Âprefange', 1],
  ["Le temple d’Atal’Hakkar", 50, 55, 'Marais des Chagrins', 0, [['Icy Veins', '50–60']]],
  ['Profondeurs de Blackrock', 52, 60, 'Mont Blackrock', 0],
  ['Blackmaw Hold', 55, 60, 'Azshara', 1],
  ['Pic Blackrock inférieur', 57, 60, 'Mont Blackrock', 0, [['Icy Veins', '55–60']]],
  ['Hache-tripes : Est', 58, 60, 'Feralas', 0, [['Icy Veins', '54–60']]],
  ["Shaper’s Terrace", 58, 60, "Cratère d’Un’Goro", 1],
  ['Stratholme : vivants', 58, 60, 'Maleterres de l’est', 0],
  ['Stratholme : morts-vivants', 58, 60, 'Maleterres de l’est', 0],
  ['Scholomance', 58, 60, 'Maleterres de l’ouest', 0],
  ['Pic Blackrock supérieur', 60, 60, 'Mont Blackrock', 0, [['Icy Veins', '59–60']]],
  ['Hache-tripes : Ouest', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]],
  ['Hache-tripes : Nord', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]]
];
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
const facOk = (d, f) => !f || !d[6] || d[6] === f;   // Ragefire Chasm and The Stockade open from a capital

/* Professions: camp object (tier 1) and the class buff it stands in for */
const PROFS = [
  ['alchemy', 'Alchimie', 1, 'Mana Well', 'comme Bénédiction de sagesse'],
  ['blacksmithing', 'Forge', 1, 'Sharpening Wheel', 'comme Totem de Force de la Terre'],
  ['enchanting', 'Enchantement', 1, 'Enchanted Lute', 'comme Marque du fauve'],
  ['engineering', 'Ingénierie', 1, 'Reagent Bot', 'vendeur de composants, réparations au rang 2'],
  ['herbalism', 'Herboristerie', 1, 'Incense Candle', 'comme Intelligence des arcanes'],
  ['leatherworking', 'Travail du cuir', 1, 'Camp Tent', 'plus d’expérience de repos'],
  ['mining', 'Minage', 1, 'Lodestone', 'comme Bénédiction de puissance'],
  ['skinning', 'Dépeçage', 1, 'Camp Chair', 'comme Aura de sélénien'],
  ['tailoring', 'Couture', 1, 'Faction Banner', 'comme Esprit divin'],
  ['cooking', 'Cuisine', 0, 'Basic Campfire', 'plus d’emplacements d’objets au camp'],
  ['firstaid', 'Premiers soins', 0, 'First Aid Kit', 'comme Mot de pouvoir : Robustesse'],
  ['fishing', 'Pêche', 0, 'Fish Bowl', 'comme Bénédiction des rois']
];
const PR = Object.fromEntries(PROFS.map(p => [p[0], p]));

/* Game stages: f = fact from the sources, t = our tip */
const SRC = {
  names: ['Icy Veins : réservation des noms', 'https://www.icy-veins.com/wow-forever/name-reservation'],
  names2: ['Team Overpowered : noms et noms de famille', 'https://teamoverpowered.com/forever/guides/name-reservation/'],
  prof: ['Warcraft Tavern : métiers', 'https://www.warcrafttavern.com/forever/guides/professions/'],
  camp: ['Warcraft Tavern : camp', 'https://www.warcrafttavern.com/forever/guides/camping/'],
  legacy: ['Blizzard: Legacy', 'https://news.blizzard.com/en-gb/article/24307383'],
  dung: ['Warcraft Tavern : donjons', 'https://www.warcrafttavern.com/forever/guides/dungeons/'],
  ride: ['Warcraft Tavern : monte', 'https://www.warcrafttavern.com/forever/guides/riding/'],
  cwg: ['ClassicWoW.gg : dates et raids', 'https://classicwow.gg/forever']
};
const STAGES = [
  { id: 'pre', n: 'Avant le lancement', sub: 'jusqu’au 04.11', lo: 0, hi: 0,
    todo: [['f', 'Réservation anticipée des noms du 27.10 au 03.11 pour les possesseurs des packs Héroïque, Épique et Collection. Premier arrivé, premier servi.'],
      ['f', 'Vous pouvez réserver jusqu’à trois personnages par compte. Un personnage a un prénom et un nom de famille, et la paire doit être unique dans la région.'],
      ['f', 'À partir du 04.11, un abonnement ou du temps de jeu est nécessaire pour jouer.'],
      ['t', 'Choisissez trois noms avec nom de famille, plus des noms de secours, avant le 27.10.']],
    dnote: 'Les premiers donjons ouvrent au niveau 13.',
    prof: [['f', 'Chaque personnage a deux métiers principaux plus les trois secondaires : Cuisine, Premiers soins et Pêche.'],
      ['f', 'Chaque métier pose son propre objet de camp, avec une amélioration proche d’une amélioration de classe.'],
      ['t', 'Répartissez les métiers à l’avance : l’un de vous prend Cuisine pour le feu de camp, les autres choisissent des métiers différents pour que les améliorations de camp ne se répètent pas.']],
    legacy: [['f', 'Legacy s’ouvre avec votre premier point : niveau 25, 150 dans un métier (hors récolte) ou l’exploration de toute la carte.'],
      ['f', 'Au lancement, un personnage peut dépenser au plus 16 points, le reste va dans la piste de récompenses.']],
    group: [['t', 'Mettez-vous d’accord sur une faction et un mode : on ne peut grouper qu’au sein d’un mode, et en JcJ un compte n’a qu’une faction.'],
      ['t', 'Composez votre équipe dans le créateur de groupe : un tank, un soigneur et des classes différentes pour les améliorations.']],
    src: ['names', 'names2', 'prof', 'legacy'] },
  { id: 'first', n: 'Premiers jours', sub: 'niveaux 1–15', lo: 1, hi: 15,
    todo: [['f', 'Les Skyborne débutent sur Zephras Isle, niveaux 1–12.'],
      ['f', 'Les talents s’ouvrent au niveau 10, ou au 9 avec le bonus Legacy Talented.'],
      ['f', 'La plupart des plats cuisinés donnent un bonus d’expérience. Il se cumule avec le camp et le Sac de couchage douillet.'],
      ['t', 'Accumulez du repos : déconnectez-vous dans une auberge ou dans un camp avec une tente.']],
    prof: [['f', 'Le feu de camp de base ne demande pas Cuisine et accueille 3 objets. Il brûle environ 10 minutes, et vous pouvez en poser un nouveau après 5.'],
      ['f', 'Pour recevoir les améliorations du camp, asseyez-vous à côté (/sit) pendant au moins une minute.'],
      ['t', 'Prenez un métier de récolte dès les premiers niveaux : herbes, minerai et peaux nourrissent l’artisanat, et 150 dans un métier d’artisanat ouvre Legacy.']],
    legacy: [['f', 'Pas encore de bonus : le premier point arrive au niveau 25 ou avec 150 dans un métier.'],
      ['t', 'Quand Legacy s’ouvre, prenez d’abord les bonus d’expérience et de camp : Well Rested, Field Guide, Permanence. Talented sert aux rerolls.']],
    group: [['t', 'Progressez dans la même zone et installez le camp à chaque étape : cinq minutes autour d’un feu de camp rapportent des améliorations pour tout le groupe.'],
      ['t', 'Formez votre premier groupe de cinq vers les niveaux 13–15.']],
    src: ['camp', 'legacy', 'dung'] },
  { id: 'dung', n: 'Donjons', sub: 'niveaux 15–40', lo: 15, hi: 40,
    todo: [['f', 'L’essentiel de l’expérience d’un donjon vient de ses chaînes de quêtes. Les passages répétés ensuite rapportent nettement moins que les quêtes dans le monde.'],
      ['f', 'Chaque objet obtenu débloque son apparence de transmogrification pour tous ceux qui peuvent le porter, même si quelqu’un d’autre a reçu l’objet.'],
      ['f', 'Legacy s’ouvre au niveau 25.'],
      ['t', 'Récupérez d’abord les quêtes du donjon en groupe et entrez une fois que tout le monde les a.']],
    prof: [['f', 'Cuisine 140 donne 5 emplacements de camp, 220 en donne 10.'],
      ['f', 'Chaque métier fabrique trois objets de camp, un par rang. Les sources divergent sur la compétence requise pour les rangs 2 et 3.'],
      ['t', 'Si le niveau 25 est encore loin, montez un métier d’artisanat à 150 : Legacy s’ouvrira plus tôt.']],
    legacy: [['f', 'Chaque défi rapporte 1 point. Il y en a 65 : classes 27, métiers 18, JcJ 12, donjons 3, raids 3, aventure 2.'],
      ['t', 'Reagent Economy (pas de composants achetés pour les techniques) et Field Guide (temps de recharge réduit des objets de camp) valent le coup.']],
    group: [['f', 'Un donjon est prévu pour 5 joueurs : un tank, un soigneur et trois DPS.'],
      ['f', 'Il n’y a pas d’ajustement de niveau, donc un ami loin derrière aura du mal dans le donjon.'],
      ['t', 'Gardez des niveaux proches : celui qui prend du retard le rattrape en quêtes, et vous faites les donjons ensemble.']],
    src: ['dung', 'camp', 'legacy'] },
  { id: 'path', n: 'En route vers le 60', sub: 'niveaux 40–60', lo: 40, hi: 60,
    todo: [['f', 'Une monture au niveau 40 (60% de vitesse), une rapide au 60 (100%). Apprenez la monte auprès de l’entraîneur de votre race.'],
      ['f', 'Les paladins et les démonistes obtiennent leur monture par des quêtes de classe.'],
      ['f', 'Honoré auprès de votre propre faction donne 10% de réduction sur l’apprentissage de la monte et les montures. Selon Warcraft Tavern : 100 + 20 pièces d’or au niveau 40, 1 000 + 200 au niveau 60.'],
      ['t', 'Économisez de l’or pour le niveau 40 : la monte sera votre plus grosse dépense sur la route du 60.']],
    prof: [['f', 'Chaque métier a ses propres objets de camp de rang 2 et 3. Le deuxième objet de l’Ingénierie, Robot réparateur, répare l’équipement.'],
      ['t', 'Gardez Cuisine 220 dans le groupe pour un camp à 10 objets : à l’heure des raids, il y aura de la place pour tous.']],
    legacy: [['f', 'Au plus 16 points par personnage, le reste va dans la piste de récompenses : un jouet à 15, une mascotte à 25, un tabard à 40, une monture à 55.']],
    group: [['f', 'Les raids ouvrent le 09.12 : Barrow Deeps pour 10 joueurs, Sommet d’Hyjal pour 20, Repaire d’Onyxia pour 40.'],
      ['t', 'Le raid à 10 demande 10 joueurs : si vous êtes moins nombreux, trouvez les autres dans votre guilde à l’avance.']],
    src: ['ride', 'prof', 'legacy', 'cwg'] },
  { id: 'raid', n: '60 et raids', sub: 'dès le 09.12', lo: 60, hi: 60,
    todo: [['f', 'Le 09.12 ouvrent Barrow Deeps (10 joueurs), Sommet d’Hyjal (20) et Repaire d’Onyxia (40, Marécage d’Âprefange).'],
      ['f', 'Terminer chacun des trois raids rapporte un point Legacy.'],
      ['f', 'Nouveau champ de bataille 15c15 : Darkspear Islands, au large du Marécage d’Âprefange.'],
      ['t', 'Pendant que vous réunissez du monde pour le raid, faites les donjons de niveau 60 pour l’équipement.']],
    prof: [['f', 'Les améliorations de camp sont un peu plus faibles que celles de classe et ne s’y cumulent pas : Bénédiction des rois donne 10% à toutes les caractéristiques, le camp 8%.'],
      ['t', 'Installez le camp à l’entrée du raid : ses améliorations couvrent ce qui manque à vos classes.']],
    legacy: [['f', 'Défis du niveau 60 : donjons 3, raids 3, JcJ 12. Le JcJ a des rangs avec un plafond hebdomadaire et des améliorations d’équipement contre de l’Honneur.']],
    group: [['f', 'Les mêmes améliorations venant de deux joueurs d’une même classe se chevauchent, celles de classes différentes se cumulent.'],
      ['t', 'Composez votre raid dans le créateur de groupe et postez le lien dans le chat.']],
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
  if (now < D_REL) return ['pre', 'Choisi selon la date : avant le lancement du 04.11.'];
  if (me.lvl) return [me.lvl < 15 ? 'first' : me.lvl < 40 ? 'dung' : me.lvl < 60 ? 'path' : 'raid', 'Choisi selon le niveau de votre personnage.'];
  if (now >= D_RAID) return ['raid', 'Choisi selon la date : les raids sont ouverts.'];
  return [now < new Date('2026-11-11T00:00:00') ? 'first' : 'dung', 'Choisi selon la date. Ajoutez le niveau de votre personnage et l’étape le suivra.'];
}
const START = { pre: 'hero_dawn-960', first: 'hero_campfire-960', dung: 'warlock-360', path: 'hunter-360', raid: 'paladin-360' };
const ARTV = /*ARTV*/{"hero_campfire-960.avif":"?v=2654726f","hero_campfire-960.webp":"?v=d73f1e16","hero_dawn-960.avif":"?v=72b3acf6","hero_dawn-960.webp":"?v=4eae2c5c"};   // ?v= of the scene arts, filled in by build.art_version (same names, redrawn pictures)
const pic = f => `<picture><source type="image/avif" srcset="${ROOT}assets/art/${f}.avif${ARTV[f + '.avif'] || ''}"><img src="${ROOT}assets/art/${f}.webp${ARTV[f + '.webp'] || ''}" alt="" loading="lazy" decoding="async"></picture>`;
const tipL = () => '<span class="tl">Conseil</span>';
function liC(x) { return x[0] === 't' ? `<li class="tip">${tipL()}${esc(x[1])}</li>` : `<li>${esc(x[1])}</li>`; }
function dLi(d) {
  const mine = me.lvl && nearLvl(d, me.lvl);
  return `<li class="${mine ? 'mine' : ''}"><b>${esc(d[0])}</b><span class="pill${mine ? ' gold' : ''}">${lvRange(d)}</span><span class="z">${esc(d[3])}${d[4] ? ' · <i>nouveau</i>' : ''}${mine ? '<span class="sr"> · pour votre niveau</span>' : ''}</span></li>`;
}
function renderStage() {
  const [auto, why] = autoStage();
  if (stageAuto) stageSel = auto;
  const s = ST[stageSel];
  $('#stageBar').innerHTML = STAGES.map(x => `<button type="button" class="stile" role="tab" id="tab-${x.id}" data-st="${x.id}" aria-controls="stagePanel" aria-selected="${x.id === stageSel}" tabindex="${x.id === stageSel ? 0 : -1}">${pic(START[x.id])}${x.id === auto ? '<span class="now">maintenant</span>' : ''}<b>${esc(x.n)}</b><span class="lv">${esc(x.sub)}</span></button>`).join('');
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
  $('#stagePanel').innerHTML = `<div class="st-head"><div class="t"><h3>${esc(s.n)}</h3><span class="pill gold">${esc(s.sub)}</span></div><p class="why">${stageAuto ? esc(why) : 'Étape choisie manuellement.'}</p></div>
    <ol class="steps-c">${steps}</ol>
    <div class="st-cols">
      <div><h4>Donjons pour ce niveau</h4>${s.dnote ? `<p class="small" style="margin:-4px 0 10px">${esc(s.dnote)}</p>` : ''}<ul class="dlist">${ds.slice(0, MAXD).map(dLi).join('')}</ul>
        <a class="more-l" href="guides/dungeons/">${extra > 0 ? `Plus de donjons dans le tableau : ${extra}` : 'Les 35 donjons'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
      <div style="display:grid;gap:24px;align-content:start"><div><h4>Métiers et camp</h4><ul class="clean">${s.prof.map(liC).join('')}</ul></div>
        <div><h4>Bonus Legacy</h4><ul class="clean">${s.legacy.map(liC).join('')}</ul></div></div>
    </div>
    <div class="gtip"><h4 style="margin:0 0 10px;font-size:1.02rem">Conseils pour le groupe</h4><ul class="clean">${s.group.map(liC).join('')}</ul></div>
    <p class="st-src"><span>Sources :</span>${s.src.map(k2 => `<a href="${SRC[k2][1]}" target="_blank" rel="noopener">${esc(SRC[k2][0])}</a>`).join('')}</p>`;
}
function optList(items, cur, none) { return `<option value="">${esc(none)}</option>` + items.map(([v, t]) => `<option value="${v}"${v === cur ? ' selected' : ''}>${esc(t)}</option>`).join(''); }
function renderMe() {
  fixMe();
  const races = f => RACES.filter(r => r.f === f).map(r => `<option value="${r.id}"${r.id === me.race ? ' selected' : ''}>${esc(r.n)}</option>`).join('');
  $('#meRace').innerHTML = `<option value="">Non choisi</option><optgroup label="${facName('alliance')}">${races('alliance')}</optgroup><optgroup label="${facName('horde')}">${races('horde')}</optgroup>`;
  const cls = (me.race ? Object.keys(RC[me.race].can) : CLASSES.map(c => c.id)).map(id => [id, CL[id].n]);
  $('#meCls').innerHTML = optList(cls, me.cls, 'Non choisi');
  $('#meRole').innerHTML = me.cls ? roleOpts(CL[me.cls]).map(x => `<option value="${x}"${x === me.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('') : `<option value="">Choisissez d’abord une classe</option>`;
  $('#meRole').disabled = !me.cls;
  const prim = PROFS.filter(p => p[2]);
  $('#meP1').innerHTML = optList(prim.filter(p => p[0] !== me.p2).map(p => [p[0], p[1]]), me.p1, 'Aucun');
  $('#meP2').innerHTML = optList(prim.filter(p => p[0] !== me.p1).map(p => [p[0], p[1]]), me.p2, 'Aucun');
  $('#meSec').innerHTML = PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${me.sec.includes(p[0])}">${esc(p[1])}</button>`).join('');
  document.querySelectorAll('.lvin').forEach(i => { if (document.activeElement !== i) i.value = me.lvl || ''; });
  const who = [me.race ? RC[me.race].n : '', me.cls ? CL[me.cls].n : ''].filter(Boolean).join(' · ');
  const sub = me.cls ? [ROLE_RU[me.role], me.race ? facName(RC[me.race].f) : ''].filter(Boolean).join(' · ') : 'Choisissez la race, la classe et le niveau ci-dessous';
  const hero = $('#meHero');
  hero.style.setProperty('--cc', me.cls ? CCOL[me.cls] : '#c9a54a');
  hero.innerHTML = pic(me.cls ? `${me.cls}-600` : 'hero_campfire-960') + (me.lvl ? `<span class="lvb" aria-label="Niveau ${me.lvl}">${me.lvl}</span>` : '')
    + `<span class="k">Mon personnage</span><b>${who ? esc(who) : 'Pas encore créé'}</b><span class="s">${esc(sub)}</span>`;
  let out = '';
  if (meSet()) {
    const b = [];
    if (me.cls) b.push(BUFF[me.cls] ? `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span><b>${esc(CL[me.cls].n)}:</b> ${esc(BUFF[me.cls])}</span></li>` : `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-dps"/></svg></span><span>${esc(CL[me.cls].n)}: pas d’amélioration de groupe, dégâts purs.</span></li>`);
    [me.p1, me.p2, ...me.sec].filter(Boolean).forEach(id => { const p = PR[id]; b.push(`<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg></span><span><b>${esc(p[3])}</b> <span class="m">· ${esc(p[1])}</span><br>${esc(p[4])}</span></li>`); });
    if (!b.length) b.push('<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span>Choisissez une classe et des métiers pour voir vos améliorations.</span></li>');
    out += `<div><h4>Ce que vous apportez au groupe</h4><ul class="buffs">${b.join('')}</ul></div>`;
    if (me.lvl) {
      const ds = DUNGEONS.filter(d => nearLvl(d, me.lvl) && facOk(d, me.race && RC[me.race].f));
      out += `<div><h4>Donjons pour votre niveau</h4>` + (ds.length ? `<ul class="dlist">${ds.slice(0, 4).map(dLi).join('')}</ul>` : '<p class="small">Les premiers donjons commencent au niveau 13.</p>')
        + `<a class="more-l" href="guides/dungeons/">${ds.length > 4 ? `Plus de donjons dans le tableau : ${ds.length - 4}` : 'Tableau des donjons'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`;
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
