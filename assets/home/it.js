const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Guerriero', s:'Guerriero', roles:['tank','dps'],
    specs:[['Armi','Danni in mischia (arma a due mani)',['dps']],['Furia','Danni in mischia (due armi)',['dps']],['Protezione','Difensore',['tank']]],
    lvl:'Il livellamento più lento, circa il 12% più lungo della media',
    lp:12,
    raid:'Urlo di Battaglia agisce su tutta l’incursione',
    forever:'Più Rabbia, minaccia migliore su gruppi di bersagli, il talento Weapon Master. Furia e Sete di Sangue sono indebolite.' },
  { id:'paladin', n:'Paladino', roles:['tank','heal','dps'],
    specs:[['Sacro','Guaritore',['heal']],['Protezione','Difensore',['tank']],['Castigo','Danni in mischia',['dps']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'Benedizione dei Re ora è di base. Secondo le classifiche della beta, Protezione è tra i difensori più forti, mentre Castigo è sceso dopo la patch del 15 ottobre.',
    forever:'Assalto Sacro dal livello 6, Giudizio non consuma il sigillo. I Non Morti ora possono essere paladini, quindi la classe è arrivata nell’Orda.' },
  { id:'hunter', n:'Cacciatore', roles:['dps'],
    specs:[['Affinità Animale','Danni a distanza, molti danni dal famiglio',['dps']],['Precisione','Danni a distanza',['dps']],['Sopravvivenza','Mischia e distanza, trappole',['dps']]],
    lvl:'Il livellamento più veloce, circa l’8% più rapido della media',
    lp:-8,
    raid:'Aura di Precisione agisce su tutta l’incursione',
    forever:'Puoi giocare senza famiglio, le trappole funzionano in combattimento, le volpi sono arrivate come famiglia di famigli. Sopravvivenza può giocare in mischia.' },
  { id:'rogue', n:'Ladro', roles:['dps'],
    specs:[['Assassinio','Danni da veleno',['dps']],['Combattimento','Attacchi rapidi con l’arma',['dps']],['Scaltrezza','Imboscate, sanguinamenti',['dps']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'Puri danni in mischia, senza potenziamenti per l’incursione',
    forever:'Ora può usare asce a una mano. Assassinio si basa sui veleni, Scaltrezza su sanguinamenti e furtività.' },
  { id:'priest', n:'Sacerdote', roles:['heal','dps'],
    specs:[['Disciplina','Guaritore, scudi e assorbimento',['heal']],['Sacro','Guaritore',['heal']],['Ombra','Danni a distanza',['dps']]],
    lvl:'Circa il 5% più lento della media',
    lp:5,
    raid:'Spirito Divino ora è di base. I danni d’Ombra e Piaga Divoratrice (recupero di 24 s) sono stati potenziati dalla patch del 15 ottobre.',
    forever:'Protezione dalla Paura e Piaga Divoratrice sono disponibili dal livello 20 per tutte le razze. Ogni razza ha due incantesimi da sacerdote propri.' },
  { id:'shaman', n:'Sciamano', roles:['heal','dps','tank?'],
    specs:[['Elementale','Danni a distanza',['dps']],['Potenziamento','Danni in mischia. Il ruolo da difensore è ancora in dubbio',['dps','tank?']],['Rigenerazione','Guaritore',['heal']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'I totem Forza della Terra, Furia del Vento, Lingua di Fuoco e Grazia dell’Aria potenziano il proprio gruppo',
    forever:'I Nani ora possono essere sciamani, quindi la classe è arrivata nell’Alleanza. Getto di Lava è stata potenziata, Elementale è salito nelle classifiche dei danni.' },
  { id:'mage', n:'Mago', roles:['dps'],
    specs:[['Arcano','Danni esplosivi, molto mana',['dps']],['Fuoco','Critici e incendi',['dps']],['Gelo','Danni e controllo',['dps']]],
    lvl:'Il livellamento più veloce, circa l’8% più rapido della media (circa 12 ore risparmiate)',
    lp:-8,
    raid:'Portali, cibo e acqua per tutto il gruppo',
    forever:'Fuoco ha ottenuto Serie Bollente, Arcano Detonazione Arcana, Gelo Lancia di Ghiaccio. Palla di Fuocogelo è disponibile dal livello 40.' },
  { id:'warlock', n:'Stregone', roles:['dps'],
    specs:[['Afflizione','Danni da maledizioni e corruzione',['dps']],['Demonologia','Danni tramite demoni',['dps']],['Distruzione','Danni diretti da fuoco e ombra',['dps']]],
    lvl:'Ritmo di livellamento nella media',
    lp:0,
    raid:'Maestria dell’Ombra ora dà il 2–10% di danni d’ombra (prima 1–5%)',
    forever:'Afflizione ha un nuovo incantesimo canalizzato, il demone resta con Sacrificio Demoniaco, Distruzione ha ottenuto Incenerimento e danni ad area.' },
  { id:'druid', n:'Druido', roles:['tank','heal','dps'],
    specs:[['Equilibrio','Danni a distanza',['dps']],['Aggressore Ferino','Difensore (orso) e danni in mischia (gatto)',['tank','dps']],['Rigenerazione','Guaritore, molte cure nel tempo',['heal']]],
    lvl:'Circa il 5% più lento della media',
    lp:5,
    raid:'Capobranco e Aura del Lunagufo agiscono su tutta l’incursione e si sommano',
    forever:'Ogni specializzazione ha un ruolo chiaro, le forme funzionano con pozioni e incantamenti delle armi. Puoi essere difensore, guaritore e combattente con un solo personaggio.' }
];
const ROLE_RU = { tank:'Difensore', heal:'Guaritore', dps:'Assaltatore', 'tank?':'Difensore (incerto)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Urlo di Battaglia', paladin:'Benedizione dei Re', hunter:'Aura di Precisione', priest:'Parola del Potere: Fermezza, Spirito Divino', shaman:'Totem (Forza della Terra, Furia del Vento, Lingua di Fuoco, Grazia dell’Aria)', mage:'Intelletto Arcano, portali, cibo e acqua', druid:'Marchio Selvaggio, Capobranco, Aura del Lunagufo' };

const RACES = [
  { id:'human', n:'Umano', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Volontà di Sopravvivenza','Rimuove lo stordimento'],['a','Percezione','Rivela i nemici invisibili per 20 s'],['p','Ruthless','+2% probabilità di critico'],['p','Spirito Umano','+5% spirito']],
    tip:'Per un Sacerdote Sacro lo spirito si traduce in cure, quindi un sacerdote Umano è ottimo per curare.' },
  { id:'dwarf', n:'Nano', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Forma di Pietra','Immunità a sanguinamenti, veleni e malattie per 8 s e danni fisici ridotti'],['a','Trova Tesori','Mostra i forzieri vicini'],['p','Earth Fury','+2% danni critici e potere di cura'],['p','Big Game Hunter','+5% danni alle bestie']],
    tip:'Forma di Pietra è utile ai difensori e nel PvP.' },
  { id:'nightelf', n:'Elfo della Notte', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Luce di Elune','+10% probabilità di critico per 15 s'],['a','Fondersi nelle Ombre','Invisibilità sul posto'],['p','Rapidità','+1% schivata e +2% velocità di corsa'],['p','Spirito di Fuoco Fatuo','+75% velocità di corsa da spirito']],
    tip:'L’unica razza dell’Alleanza con il druido, a meno di scegliere gli Skyborne.' },
  { id:'gnome', n:'Gnomo', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Artista della Fuga','Breve immunità a rallentamenti e immobilizzazioni'],['a','Eureka!','Le prossime 3 abilità costano meno e sono più forti del 10%'],['p','Apertura Mentale','+5% mana, rabbia o energia massimi'],['p','Specializzazione: Ingegneria','I congegni d’ingegneria funzionano in modo più affidabile']],
    tip:'Apertura Mentale aiuta soprattutto le classi a energia.' },
  { id:'skyA', n:'Skyborne (Alleanza)', f:'alliance', paid:true, name:'Skyborne dell’High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Plani per 10 s, senza danni da caduta'],['a','Read Ley Line','+100% rigenerazione di salute e mana'],['p','Wind Blessed','+3% velocità d’attacco e degli incantesimi'],['p','Elemental Insight','+5% danni agli elementali']],
    tip:'Razza a pagamento: Heroic Pack da $29.99. Inizia nella zona di Zephras Isle (livelli 1–12).' },
  { id:'orc', n:'Orco', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Furia Sanguinaria','+10% potenza d’attacco e potere magico per 15 s'],['a','Shatter Curse','Rimuove maledizioni e corruzione, −5% di danni magici subiti per 8 s'],['p','Savage','+1% probabilità di critico'],['p','Audacia','Stordimenti più brevi del 20%']],
    tip:'Furia Sanguinaria offre una potente finestra di danni.' },
  { id:'undead', n:'Non Morto', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Volontà dei Reietti','Rimuove ammaliamento, paura e sonno'],['a','Cannibalismo','Ripristina nel tempo il 35% di salute e mana'],['p','Respiro Subacqueo','Respiri più a lungo sott’acqua'],['p','Tocco Tombale','Probabilità di sottrarre salute quando attacchi']],
    tip:'Nuova combinazione: un paladino per l’Orda, dove prima questa classe non esisteva.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Urto di Guerra','Stordisce i nemici vicini per 2 s'],['a','Coltivazione','Fa crescere erbe raccoglibili senza Erbalismo'],['p','Vagapianure','La velocità aumenta mentre corri'],['p','Vigore','+5% salute e +2% danni critici']],
    tip:'L’unica razza dell’Orda con il druido, a meno di scegliere gli Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserker','+10% velocità d’attacco e degli incantesimi per 10 s'],['a','Rapid Regeneration','Ripristina salute nel tempo'],['p','Cacciatore di Bestie','+5% danni alle bestie'],['p','Rigenerazione','La salute si rigenera anche in combattimento']],
    tip:'Più scelte di classe di tutta l’Orda: sette.' },
  { id:'skyH', n:'Skyborne (Orda)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Plani per 10 s, senza danni da caduta'],['a','Skysight','+10% velocità di corsa'],['p','Wind Blessed','+3% velocità d’attacco e degli incantesimi'],['p','Elemental Insight','+5% danni agli elementali']],
    tip:'Razza a pagamento: Heroic Pack da $29.99. Solo nell’Orda può essere sciamano, solo nell’Alleanza mago.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "La razza più numerosa dell’Alleanza. Versatile e forte nel PvP grazie a Volontà di Sopravvivenza.", "dwarf": "Robusti minatori e fucilieri di Forgiardente. Per la prima volta in Classic l’Alleanza ha gli sciamani, e sono nani.", "nightelf": "Un antico popolo delle foreste. Sfuggenti: un modo tutto loro per nascondersi, schivate e corsa veloce.", "gnome": "Gli inventori di Gnomeregan. Piccoli, astuti e con la migliore abilità di fuga del gioco.", "skyA": "Una nuova razza di Forever. L’High Order: elfi del vento in cerca della magia arcana perduta dei loro antenati.", "orc": "Il cuore dell’Orda. I guerrieri più forti e maestri del PvP grazie a Furia Sanguinaria e Audacia.", "undead": "I Reietti: ex umani liberatisi dal Re dei Lich. Immuni a paura e sonno quando conta.", "tauren": "Pacifici giganti delle pianure. La salute più alta e uno stordimento ad area tutto loro.", "troll": "La tribù Lanciascura. Più classi di tutta l’Orda e un potente Berserker per i danni.", "skyH": "Una nuova razza di Forever. I Windshaper: guide spirituali degli Skyborne, vicini agli elementi."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Armi':'Arms','Furia':'Fury','Protezione':'Protection','Sacro':'Holy','Castigo':'Retribution',
  'Affinità Animale':'Beast Mastery','Precisione':'Marksmanship','Sopravvivenza':'Survival',
  'Assassinio':'Assassination','Combattimento':'Combat','Scaltrezza':'Subtlety',
  'Disciplina':'Discipline','Ombra':'Shadow','Elementale':'Elemental','Potenziamento':'Enhancement','Rigenerazione':'Restoration',
  'Arcano':'Arcane','Fuoco':'Fire','Gelo':'Frost','Afflizione':'Affliction','Demonologia':'Demonology','Distruzione':'Destruction',
  'Equilibrio':'Balance','Aggressore Ferino':'Feral',
  'Volontà di Sopravvivenza':'Will to Survive','Percezione':'Perception','Ruthless':'Ruthless','Spirito Umano':'The Human Spirit',
  'Forma di Pietra':'Stoneform','Trova Tesori':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Luce di Elune':"Elune’s Light",'Fondersi nelle Ombre':'Shadowmeld','Rapidità':'Quickness','Spirito di Fuoco Fatuo':'Wisp Spirit',
  'Artista della Fuga':'Escape Artist','Eureka!':'Eureka!','Apertura Mentale':'Expansive Mind','Specializzazione: Ingegneria':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Furia Sanguinaria':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Audacia':'Hardiness',
  'Volontà dei Reietti':'Will of the Forsaken','Cannibalismo':'Cannibalize','Respiro Subacqueo':'Underwater Breathing','Tocco Tombale':'Touch of the Grave',
  'Urto di Guerra':'War Stomp','Coltivazione':'Cultivation','Vagapianure':'Plainsrunning','Vigore':'Endurance',
  'Berserker':'Berserking','Rapid Regeneration':'Rapid Regeneration','Cacciatore di Bestie':'Beast Slaying','Rigenerazione':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Consiglio</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Alleanza' : 'Orda'; }
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Più veloce del ${-p}%` : p > 0 ? `Più lento del ${p}%` : 'Ritmo nella media';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>più veloce</span><span>più lento</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Classe</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Livellamento</span><span>In incursione</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Ruoli: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Razza</span><span>Classi</span><span class="abl">Abilità <span class="abt">attiva</span><span class="abt p">passiva</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">a pagamento</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Classi: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nuova' : v ? '' : ', non disponibile')); }).join('')}</span>
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
  let h = '<thead><tr><th scope="col">Razza</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">a pagamento</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: non possibile"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', nuova combinazione' : ''}`;
        const mark = v === 'new' && !sel ? '<span class="nw">nuova</span>' : '<i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>';
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
    return `<button type="button" data-pc="${c.id}" class="${v ? '' : 'na'}" aria-pressed="${c.id === state.cls}">${esc(c.n)}${v === 'new' ? ' · nuova' : ''}</button>`;
  }).join('');
  $('#pickm').innerHTML = `<div><div class="lbl">1. Razza</div><div class="chiprow">${races}</div></div>
    <div><div class="lbl">2. Classe (tratteggiata: non disponibile per questa razza, tocca per cambiare razza)</div><div class="chiprow">${cls}</div></div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Attive' : 'Passive'}</span><b>${bi(x[1])}</b><span>${esc(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', serve il pacchetto Skyborne' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><img src="../assets/art/${c.id}-600.webp" width="600" height="804" alt="" loading="lazy" decoding="async"></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}${face(c.id, CCOL[c.id])}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Nuova combinazione</span>' : ''}${r.paid ? '<span class="tag paid">Razza a pagamento</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Specializzazioni</h4><div class="cards">${specs}</div></div>
        <div><h4>Abilità razziali</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Livellamento</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>In incursione</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Novità</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="La mia scelta">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copia la mia scelta</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copiato');
  $('#qPick').textContent = `Ora: ${r.n} · ${c.n}`;
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
  warrior: 'Piastre, rabbia e prima linea. Incassa i colpi da difensore o falcia con un’arma a due mani.',
  paladin: 'Un guerriero sacro in piastre: cura, difende e mena il martello. Ora anche nell’Orda.',
  hunter: 'Arco, trappole e una bestia fedele al tuo fianco. Una delle classi più veloci da livellare.',
  rogue: 'Veleni, lame e ombra. Danni puri dall’imboscata e controllo dei nemici.',
  priest: 'Luce e Ombra nelle stesse mani. Il guaritore principale del gruppo o un incantatore oscuro.',
  shaman: 'Totem ed elementi: cura, colpisce con fulmini o armi. Ora anche nell’Alleanza.',
  mage: 'Magia del fuoco, del gelo e arcana. Portali, cibo e acqua per tutta la squadra.',
  warlock: 'Maledizioni, demoni e fuoco. Danni nel tempo e un demone tutto tuo che ti aiuta.',
  druid: 'Orso, gatto, gufo o guaritore: tutti e tre i ruoli in un solo personaggio.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Di più sulla classe</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">a pagamento</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">Di più sulla razza</span></span>
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
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Impossibile copiare, seleziona il testo e premi Ctrl+C'; }
}

/* Dungeons: [name, min, max, entrance zone, new, other sites' ranges where they differ] */
const DUNGEONS = [
  ['Baratro di Fiamma Furente', 13, 18, 'Orgrimmar', 0, [], 'horde'],
  ['Hall of Thanes', 13, 18, 'Forgiardente', 1, [['Icy Veins', '13–20']]],
  ['Rovine di Lordaeron', 15, 20, 'Radure di Tirisfal', 1, [['Icy Veins', '15–22']]],
  ['Miniere della Morte', 15, 22, 'Marche Occidentali', 0, [['Icy Veins', '17–26']]],
  ['Caverna dei Lamenti', 17, 24, 'Savane', 0, [['Icy Veins', '15–24']]],
  ['Forte di Zannascura', 20, 26, 'Selva Pinargento', 0, [['Icy Veins', '20–30']]],
  ['Abissi di Fondocupo', 22, 28, 'Valtetra', 0, [['Sportskeeda', '22–26'], ['Icy Veins', '24–32']]],
  ['Excavation Site: Wetlands', 24, 29, 'Paludi Grigie', 1, [['ClassicWoW.gg', '26–31'], ['Icy Veins', '26–33']]],
  ['Segrete di Roccavento', 25, 29, 'Roccavento', 0, [['Icy Veins', '24–32']], 'alliance'],
  ['City of Dalaran', 28, 33, 'Montagne d’Alterac', 1, [['Icy Veins', '28–35']]],
  ['Gnomeregan', 29, 38, 'Dun Morogh', 0],
  ['Gallerie di Lamaspina', 29, 38, 'Savane', 0],
  ['Monastero Scarlatto: Cimitero', 30, 38, 'Radure di Tirisfal', 0],
  ['Monastero Scarlatto: Biblioteca', 33, 41, 'Radure di Tirisfal', 0],
  ['The Drowned City', 35, 40, 'Valle di Rovotorto', 1],
  ['Monastero Scarlatto: Armeria', 36, 44, 'Radure di Tirisfal', 0],
  ['Uldaman', 36, 45, 'Maleterre', 0, [['Icy Veins', '41–51']]],
  ['Sotterranei di Lamaspina', 37, 46, 'Savane', 0],
  ['Monastero Scarlatto: Cattedrale', 38, 46, 'Radure di Tirisfal', 0],
  ["Zul’farrak", 40, 47, 'Tanaris', 0, [['Icy Veins', '44–54']]],
  ["Krol’dok Stronghold", 40, 45, 'Riverglades', 1],
  ['Maraudon', 45, 51, 'Desolanda', 0, [['Icy Veins', '46–55']]],
  ['Alcaz Island Prison', 48, 53, 'Acquemorte', 1],
  ["Temple of Atal’Hakkar", 50, 55, 'Palude del Dolore', 0, [['Icy Veins', '50–60']]],
  ['Sotterranei di Roccianera', 52, 60, 'Massiccio Roccianera', 0],
  ['Blackmaw Hold', 55, 60, 'Azshara', 1],
  ['Bastioni di Roccianera Inferiori', 57, 60, 'Massiccio Roccianera', 0, [['Icy Veins', '55–60']]],
  ['Maglio Infausto: Est', 58, 60, 'Feralas', 0, [['Icy Veins', '54–60']]],
  ["Shaper’s Terrace", 58, 60, "Cratere di Un’Goro", 1],
  ['Stratholme: vivi', 58, 60, 'Terre Infette Orientali', 0],
  ['Stratholme: non morti', 58, 60, 'Terre Infette Orientali', 0],
  ['Scholomance', 58, 60, 'Terre Infette Occidentali', 0],
  ['Bastioni di Roccianera Superiori', 60, 60, 'Massiccio Roccianera', 0, [['Icy Veins', '59–60']]],
  ['Maglio Infausto: Ovest', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]],
  ['Maglio Infausto: Nord', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]]
];
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
const facOk = (d, f) => !f || !d[6] || d[6] === f;   // Ragefire Chasm and The Stockade open from a capital

/* Professions: camp object (tier 1) and the class buff it stands in for */
const PROFS = [
  ['alchemy', 'Alchimia', 1, 'Mana Well', 'come Benedizione della Saggezza'],
  ['blacksmithing', 'Forgiatura', 1, 'Sharpening Wheel', 'come Totem della Forza della Terra'],
  ['enchanting', 'Incantamento', 1, 'Enchanted Lute', 'come Marchio Selvaggio'],
  ['engineering', 'Ingegneria', 1, 'Reagent Bot', 'venditore di reagenti, riparazioni al livello 2'],
  ['herbalism', 'Erbalismo', 1, 'Incense Candle', 'come Intelletto Arcano'],
  ['leatherworking', 'Conciatura', 1, 'Camp Tent', 'più esperienza da riposo'],
  ['mining', 'Estrazione', 1, 'Lodestone', 'come Benedizione del Vigore'],
  ['skinning', 'Scuoiatura', 1, 'Camp Chair', 'come Aura del Lunagufo'],
  ['tailoring', 'Sartoria', 1, 'Faction Banner', 'come Spirito Divino'],
  ['cooking', 'Cucina', 0, 'Basic Campfire', 'più posti per oggetti nell’accampamento'],
  ['firstaid', 'Primo Soccorso', 0, 'First Aid Kit', 'come Parola del Potere: Fermezza'],
  ['fishing', 'Pesca', 0, 'Fish Bowl', 'come Benedizione dei Re']
];
const PR = Object.fromEntries(PROFS.map(p => [p[0], p]));

/* Game stages: f = fact from the sources, t = our tip */
const SRC = {
  names: ['Icy Veins: prenotazione nomi', 'https://www.icy-veins.com/wow-forever/name-reservation'],
  names2: ['Team Overpowered: nomi e cognomi', 'https://teamoverpowered.com/forever/guides/name-reservation/'],
  prof: ['Warcraft Tavern: professioni', 'https://www.warcrafttavern.com/forever/guides/professions/'],
  camp: ['Warcraft Tavern: accampamento', 'https://www.warcrafttavern.com/forever/guides/camping/'],
  legacy: ['Blizzard: Legacy', 'https://news.blizzard.com/en-gb/article/24307383'],
  dung: ['Warcraft Tavern: spedizioni', 'https://www.warcrafttavern.com/forever/guides/dungeons/'],
  ride: ['Warcraft Tavern: equitazione', 'https://www.warcrafttavern.com/forever/guides/riding/'],
  cwg: ['ClassicWoW.gg: date e incursioni', 'https://classicwow.gg/forever']
};
const STAGES = [
  { id: 'pre', n: 'Prima del lancio', sub: 'fino al 04.11', lo: 0, hi: 0,
    todo: [['f', 'Prenotazione anticipata dei nomi dal 27.10 al 03.11 per chi possiede i pacchetti Heroic, Epic e Collection. Chi prima arriva, meglio alloggia.'],
      ['f', 'Puoi prenotare fino a tre personaggi per account. Un personaggio ha nome e cognome, e la coppia deve essere unica nella regione.'],
      ['f', 'Dal 04.11 per giocare serve un abbonamento o tempo di gioco.'],
      ['t', 'Scegli tre nomi con cognome, più delle riserve, prima del 27.10.']],
    dnote: 'Le prime spedizioni si aprono al livello 13.',
    prof: [['f', 'Ogni personaggio ha due professioni primarie più tutte e tre le secondarie: Cucina, Primo Soccorso e Pesca.'],
      ['f', 'Ogni professione piazza un proprio oggetto da accampamento con un potenziamento simile a quello di una classe.'],
      ['t', 'Dividetevi le professioni in anticipo: uno di voi prende Cucina per il fuoco da campo, gli altri ne scelgono di diverse così i potenziamenti dell’accampamento non si ripetono.']],
    legacy: [['f', 'Legacy si apre con il primo punto: livello 25, 150 in una professione (non di raccolta) o l’esplorazione di tutta la mappa.'],
      ['f', 'Al lancio un personaggio può spendere al massimo 16 punti, il resto va al percorso delle ricompense.']],
    group: [['t', 'Mettetevi d’accordo su una fazione e una modalità: si può fare gruppo solo nella stessa modalità, e nel PvP un account ha una sola fazione.'],
      ['t', 'Prepara la formazione nel creatore di gruppi: un difensore, un guaritore e classi diverse per i potenziamenti.']],
    src: ['names', 'names2', 'prof', 'legacy'] },
  { id: 'first', n: 'Primi giorni', sub: 'livelli 1–15', lo: 1, hi: 15,
    todo: [['f', 'Gli Skyborne iniziano su Zephras Isle, livelli 1–12.'],
      ['f', 'I talenti si aprono al livello 10, o al 9 con il vantaggio Legacy Talented.'],
      ['f', 'La maggior parte del cibo cucinato dà un bonus all’esperienza. Si somma all’accampamento e al Cozy Sleeping Bag.'],
      ['t', 'Accumula riposo: esci dal gioco in una locanda o in un accampamento con tenda.']],
    prof: [['f', 'Il fuoco da campo base non richiede Cucina e regge 3 oggetti. Arde per circa 10 minuti, e puoi accenderne uno nuovo dopo 5.'],
      ['f', 'Per ottenere i potenziamenti dell’accampamento, siediti vicino (/sit) per almeno un minuto.'],
      ['t', 'Inizia a raccogliere fin dai primi livelli: erbe, minerali e pelli alimentano la produzione, e 150 in una professione di produzione apre Legacy.']],
    legacy: [['f', 'Ancora nessun vantaggio: il primo punto arriva al livello 25 o con 150 in una professione.'],
      ['t', 'Quando si apre Legacy, prendi prima i vantaggi per esperienza e accampamento: Well Rested, Field Guide, Permanence. Talented serve agli alt.']],
    group: [['t', 'Livellate nella stessa zona e montate l’accampamento a ogni sosta: cinque minuti al fuoco ripagano con potenziamenti per tutto il gruppo.'],
      ['t', 'Forma il tuo primo gruppo da cinque entro il livello 13–15.']],
    src: ['camp', 'legacy', 'dung'] },
  { id: 'dung', n: 'Spedizioni', sub: 'livelli 15–40', lo: 15, hi: 40,
    todo: [['f', 'Gran parte dell’esperienza di una spedizione viene dalle sue catene di missioni. Ripeterla dopo dà molta meno esperienza delle missioni nel mondo.'],
      ['f', 'Ogni oggetto che cade sblocca il suo aspetto di trasmogrificazione per tutti quelli che possono indossarlo, anche se l’oggetto è andato a un altro.'],
      ['f', 'Legacy si apre al livello 25.'],
      ['t', 'Prima raccogliete in gruppo le missioni della spedizione ed entrate quando le hanno tutti.']],
    prof: [['f', 'Cucina a 140 dà 5 posti nell’accampamento, a 220 ne dà 10.'],
      ['f', 'Ogni professione crea tre oggetti da accampamento, uno per livello. Le fonti non concordano sulla competenza necessaria per i livelli 2 e 3.'],
      ['t', 'Se il livello 25 è ancora lontano, porta una professione di produzione a 150: Legacy si aprirà prima.']],
    legacy: [['f', 'Ogni sfida dà 1 punto. Sono 65: classi 27, professioni 18, PvP 12, spedizioni 3, incursioni 3, avventura 2.'],
      ['t', 'Reagent Economy (niente reagenti comprati per le abilità) e Field Guide (recupero più breve degli oggetti da accampamento) valgono la pena.']],
    group: [['f', 'Una spedizione è pensata per 5 giocatori: un difensore, un guaritore e tre assaltatori.'],
      ['f', 'Non c’è adattamento del livello, quindi un amico molto indietro farà fatica nella spedizione.'],
      ['t', 'Tenete i livelli vicini: chi resta indietro recupera con le missioni, e le spedizioni le fate insieme.']],
    src: ['dung', 'camp', 'legacy'] },
  { id: 'path', n: 'Verso il 60', sub: 'livelli 40–60', lo: 40, hi: 60,
    todo: [['f', 'Una cavalcatura al livello 40 (60% di velocità), una veloce al 60 (100%). Addestrati dall’istruttore della tua razza.'],
      ['f', 'Paladini e stregoni ottengono la cavalcatura con missioni di classe.'],
      ['f', 'Onorato con la tua fazione dà uno sconto del 10% su addestramento e cavalcature. Secondo Warcraft Tavern: 100 + 20 monete d’oro al livello 40, 1.000 + 200 al 60.'],
      ['t', 'Risparmia oro per il livello 40: la cavalcatura sarà la tua spesa più grande verso il 60.']],
    prof: [['f', 'Ogni professione ha i propri oggetti da accampamento di livello 2 e 3. Il secondo oggetto di Ingegneria, Riparabot, ripara l’equipaggiamento.'],
      ['t', 'Tenete Cucina a 220 nel gruppo per un accampamento da 10 oggetti: all’ora delle incursioni ci sarà posto per tutti.']],
    legacy: [['f', 'Al massimo 16 punti per personaggio, il resto va al percorso delle ricompense: un giocattolo a 15, una mascotte a 25, un tabarro a 40, una cavalcatura a 55.']],
    group: [['f', 'Le incursioni aprono il 09.12: Barrow Deeps da 10 giocatori, Sommità di Hyjal da 20, Antro di Onyxia da 40.'],
      ['t', 'L’incursione da 10 richiede 10 giocatori: se siete meno, trovate per tempo gli altri nella gilda.']],
    src: ['ride', 'prof', 'legacy', 'cwg'] },
  { id: 'raid', n: '60 e incursioni', sub: 'dal 09.12', lo: 60, hi: 60,
    todo: [['f', 'Il 09.12 aprono Barrow Deeps (10 giocatori), Sommità di Hyjal (20) e Antro di Onyxia (40, Acquemorte).'],
      ['f', 'Completare ognuna delle tre incursioni dà un punto Legacy.'],
      ['f', 'Nuovo campo di battaglia 15v15: Darkspear Islands al largo di Acquemorte.'],
      ['t', 'Mentre radunate la gente per l’incursione, fate le spedizioni di livello 60 per l’equipaggiamento.']],
    prof: [['f', 'I potenziamenti dell’accampamento sono un po’ più deboli di quelli di classe e non si sommano: Benedizione dei Re dà il 10% a tutte le caratteristiche, l’accampamento l’8%.'],
      ['t', 'Montate l’accampamento all’ingresso dell’incursione: i suoi potenziamenti coprono ciò che manca alle vostre classi.']],
    legacy: [['f', 'Sfide per il livello 60: spedizioni 3, incursioni 3, PvP 12. Il PvP ha gradi con un limite settimanale e miglioramenti dell’equipaggiamento con l’Onore.']],
    group: [['f', 'Gli stessi potenziamenti di due giocatori della stessa classe si sovrappongono, quelli di classi diverse si sommano.'],
      ['t', 'Prepara la formazione d’incursione nel creatore di gruppi e posta il link in chat.']],
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
  if (now < D_REL) return ['pre', 'Scelta in base alla data: prima del lancio del 04.11.'];
  if (me.lvl) return [me.lvl < 15 ? 'first' : me.lvl < 40 ? 'dung' : me.lvl < 60 ? 'path' : 'raid', 'Scelta in base al livello del tuo personaggio.'];
  if (now >= D_RAID) return ['raid', 'Scelta in base alla data: le incursioni sono aperte.'];
  return [now < new Date('2026-11-11T00:00:00') ? 'first' : 'dung', 'Scelta in base alla data. Aggiungi il livello del tuo personaggio e la fase lo seguirà.'];
}
const START = { pre: 'hero_dawn-960', first: 'hero_campfire-960', dung: 'warlock-360', path: 'hunter-360', raid: 'paladin-360' };
const ARTV = /*ARTV*/{"hero_campfire-960.avif":"?v=2654726f","hero_campfire-960.webp":"?v=d73f1e16","hero_dawn-960.avif":"?v=72b3acf6","hero_dawn-960.webp":"?v=4eae2c5c"};   // ?v= of the scene arts, filled in by build.art_version (same names, redrawn pictures)
const pic = f => `<picture><source type="image/avif" srcset="${ROOT}assets/art/${f}.avif${ARTV[f + '.avif'] || ''}"><img src="${ROOT}assets/art/${f}.webp${ARTV[f + '.webp'] || ''}" alt="" loading="lazy" decoding="async"></picture>`;
const tipL = () => '<span class="tl">Consiglio</span>';
function liC(x) { return x[0] === 't' ? `<li class="tip">${tipL()}${esc(x[1])}</li>` : `<li>${esc(x[1])}</li>`; }
function dLi(d) {
  const mine = me.lvl && nearLvl(d, me.lvl);
  return `<li class="${mine ? 'mine' : ''}"><b>${esc(d[0])}</b><span class="lvl${mine ? ' gold' : ''}">${lvRange(d)}</span><span class="z">${esc(d[3])}${d[4] ? ' · <i>nuova</i>' : ''}${mine ? '<span class="sr"> · per il tuo livello</span>' : ''}</span></li>`;
}
function renderStage() {
  const [auto, why] = autoStage();
  if (stageAuto) stageSel = auto;
  const s = ST[stageSel];
  $('#stageBar').innerHTML = STAGES.map(x => `<button type="button" class="stile" role="tab" id="tab-${x.id}" data-st="${x.id}" aria-controls="stagePanel" aria-selected="${x.id === stageSel}" tabindex="${x.id === stageSel ? 0 : -1}">${pic(START[x.id])}<b>${esc(x.n)}</b><span class="lv">${esc(x.sub)}${x.id === auto ? ' · <span class="now">ora</span>' : ''}</span></button>`).join('');
  let ds;
  if (s.id === 'pre') ds = DUNGEONS.filter(d => d[1] <= 15);
  else ds = DUNGEONS.filter(d => d[1] <= s.hi && d[2] >= s.lo);
  if (me.lvl && s.lo <= me.lvl && me.lvl <= Math.max(s.hi, 1)) ds = ds.filter(d => nearLvl(d, me.lvl)).concat(ds.filter(d => !nearLvl(d, me.lvl)));
  const MAXD = 6, extra = ds.length - MAXD;
  let k = 0;
  const steps = s.todo.map(x => x[0] === 't'
    ? `<li class="tip"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p>${tipL()}${esc(x[1])}</p></li>`
    : `<li><span class="n">${++k}</span><p>${esc(x[1])}</p></li>`).join('');
  $('#stagePanel').setAttribute('aria-labelledby', 'tab-' + s.id);
  $('#stagePanel').innerHTML = `<div class="st-head"><div class="t"><h3>${esc(s.n)}</h3><span class="when">${esc(s.sub)}</span></div><p class="why">${stageAuto ? esc(why) : 'Fase scelta a mano.'}</p></div>
    <ol class="steps-c">${steps}</ol>
    <div class="st-cols">
      <div><h4>Spedizioni per questo livello</h4>${s.dnote ? `<p class="small" style="margin:-4px 0 10px">${esc(s.dnote)}</p>` : ''}<ul class="dlist">${ds.slice(0, MAXD).map(dLi).join('')}</ul>
        <a class="more-l" href="guides/dungeons/">${extra > 0 ? `Altre spedizioni nella tabella: ${extra}` : 'Tutte le 35 spedizioni'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
      <div style="display:grid;gap:24px;align-content:start"><div><h4>Professioni e accampamento</h4><ul class="clean">${s.prof.map(liC).join('')}</ul></div>
        <div><h4>Vantaggi Legacy</h4><ul class="clean">${s.legacy.map(liC).join('')}</ul></div></div>
    </div>
    <div class="gtip"><h4 style="margin:0 0 10px;font-size:var(--fs-16)">Consigli per il gruppo</h4><ul class="clean">${s.group.map(liC).join('')}</ul></div>
    <p class="st-src"><span>Fonti:</span>${s.src.map(k2 => `<a href="${SRC[k2][1]}" target="_blank" rel="noopener">${esc(SRC[k2][0])}</a>`).join('')}</p>`;
}
function optList(items, cur, none) { return `<option value="">${esc(none)}</option>` + items.map(([v, t]) => `<option value="${v}"${v === cur ? ' selected' : ''}>${esc(t)}</option>`).join(''); }
function renderMe() {
  fixMe();
  const races = f => RACES.filter(r => r.f === f).map(r => `<option value="${r.id}"${r.id === me.race ? ' selected' : ''}>${esc(r.n)}</option>`).join('');
  $('#meRace').innerHTML = `<option value="">Non scelto</option><optgroup label="${facName('alliance')}">${races('alliance')}</optgroup><optgroup label="${facName('horde')}">${races('horde')}</optgroup>`;
  const cls = (me.race ? Object.keys(RC[me.race].can) : CLASSES.map(c => c.id)).map(id => [id, CL[id].n]);
  $('#meCls').innerHTML = optList(cls, me.cls, 'Non scelto');
  $('#meRole').innerHTML = me.cls ? roleOpts(CL[me.cls]).map(x => `<option value="${x}"${x === me.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('') : `<option value="">Prima scegli una classe</option>`;
  $('#meRole').disabled = !me.cls;
  const prim = PROFS.filter(p => p[2]);
  $('#meP1').innerHTML = optList(prim.filter(p => p[0] !== me.p2).map(p => [p[0], p[1]]), me.p1, 'Nessuna');
  $('#meP2').innerHTML = optList(prim.filter(p => p[0] !== me.p1).map(p => [p[0], p[1]]), me.p2, 'Nessuna');
  $('#meSec').innerHTML = PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${me.sec.includes(p[0])}">${esc(p[1])}</button>`).join('');
  document.querySelectorAll('.lvin').forEach(i => { if (document.activeElement !== i) i.value = me.lvl || ''; });
  const who = [me.race ? RC[me.race].n : '', me.cls ? CL[me.cls].n : ''].filter(Boolean).join(' · ');
  const sub = me.cls ? [ROLE_RU[me.role], me.race ? facName(RC[me.race].f) : ''].filter(Boolean).join(' · ') : 'Scegli razza, classe e livello qui sotto';
  const hero = $('#meHero');
  hero.style.setProperty('--cc', me.cls ? CCOL[me.cls] : '#c9a54a');
  hero.innerHTML = pic(me.cls ? `${me.cls}-600` : 'hero_campfire-960') + (me.lvl ? `<span class="lvb" aria-label="Livello ${me.lvl}">${me.lvl}</span>` : '')
    + `<span class="k">Il mio personaggio</span><b>${who ? esc(who) : 'Non ancora creato'}</b><span class="s">${esc(sub)}</span>`;
  let out = '';
  if (meSet()) {
    const b = [];
    if (me.cls) b.push(BUFF[me.cls] ? `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span><b>${esc(CL[me.cls].n)}:</b> ${esc(BUFF[me.cls])}</span></li>` : `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-dps"/></svg></span><span>${esc(CL[me.cls].n)}: nessun potenziamento di gruppo, danni puri.</span></li>`);
    [me.p1, me.p2, ...me.sec].filter(Boolean).forEach(id => { const p = PR[id]; b.push(`<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg></span><span><b>${esc(p[3])}</b> <span class="m">· ${esc(p[1])}</span><br>${esc(p[4])}</span></li>`); });
    if (!b.length) b.push('<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span>Scegli classe e professioni per vedere i tuoi potenziamenti.</span></li>');
    out += `<div><h4>Cosa porti al gruppo</h4><ul class="buffs">${b.join('')}</ul></div>`;
    if (me.lvl) {
      const ds = DUNGEONS.filter(d => nearLvl(d, me.lvl) && facOk(d, me.race && RC[me.race].f));
      out += `<div><h4>Spedizioni per il tuo livello</h4>` + (ds.length ? `<ul class="dlist">${ds.slice(0, 4).map(dLi).join('')}</ul>` : '<p class="small">Le prime spedizioni iniziano dal livello 13.</p>')
        + `<a class="more-l" href="guides/dungeons/">${ds.length > 4 ? `Altre spedizioni nella tabella: ${ds.length - 4}` : 'Tabella spedizioni'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`;
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
