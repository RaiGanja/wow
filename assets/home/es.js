const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Guerrero', s:'Guerrero', roles:['tank','dps'],
    specs:[['Armas','Daño cuerpo a cuerpo (arma de dos manos)',['dps']],['Furia','Daño cuerpo a cuerpo (dos armas)',['dps']],['Protección','Tanque',['tank']]],
    lvl:'La subida más lenta, un 12% más larga que la media',
    lp:12,
    raid:'Grito de guerra afecta a toda la banda',
    forever:'Más ira, mejor amenaza contra grupos de objetivos, el talento Weapon Master. Furia y Sed de sangre se han debilitado.' },
  { id:'paladin', n:'Paladín', roles:['tank','heal','dps'],
    specs:[['Sagrado','Sanador',['heal']],['Protección','Tanque',['tank']],['Reprensión','Daño cuerpo a cuerpo',['dps']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Bendición de los Reyes ahora es básica. Según las listas de la beta, Protección está entre los tanques más fuertes, y Reprensión bajó tras el parche del 15 de octubre.',
    forever:'Holy Strike desde el nivel 6, Sentencia no consume el sello. Los no-muertos ya pueden ser paladines, así que la clase llega a la Horda.' },
  { id:'hunter', n:'Cazador', roles:['dps'],
    specs:[['Bestias','Daño a distancia, mucho daño de la mascota',['dps']],['Puntería','Daño a distancia',['dps']],['Supervivencia','Cuerpo a cuerpo y a distancia, trampas',['dps']]],
    lvl:'La subida más rápida, un 8% más rápida que la media',
    lp:-8,
    raid:'Aura de disparo certero afecta a toda la banda',
    forever:'Puedes jugar sin mascota, las trampas funcionan en combate y llegan los zorros como familia de mascotas. Supervivencia puede ir cuerpo a cuerpo.' },
  { id:'rogue', n:'Pícaro', roles:['dps'],
    specs:[['Asesinato','Daño con venenos',['dps']],['Combate','Ataques rápidos con arma',['dps']],['Sutileza','Emboscadas, sangrados',['dps']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Daño cuerpo a cuerpo puro sin beneficios para la banda',
    forever:'Ya puede usar hachas de una mano. Asesinato se basa en venenos, Sutileza en sangrados y sigilo.' },
  { id:'priest', n:'Sacerdote', roles:['heal','dps'],
    specs:[['Disciplina','Sanador, escudos y absorción',['heal']],['Sagrado','Sanador',['heal']],['Sombras','Daño a distancia',['dps']]],
    lvl:'Un 5% más lenta que la media',
    lp:5,
    raid:'Espíritu divino ahora es básico. El daño de Sombras y Peste devoradora (24 s de reutilización) se mejoraron con el parche del 15 de octubre.',
    forever:'Custodia de miedo y Peste devoradora están disponibles desde el nivel 20 para cualquier raza. Cada raza tiene dos hechizos de sacerdote propios.' },
  { id:'shaman', n:'Chamán', roles:['heal','dps','tank?'],
    specs:[['Elemental','Daño a distancia',['dps']],['Mejora','Daño cuerpo a cuerpo. Su capacidad de tanque aún está en duda',['dps','tank?']],['Restauración','Sanador',['heal']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Los tótems Fuerza de la tierra, Viento Furioso, Lengua de Fuego y Gracia del aire mejoran a su grupo',
    forever:'Los enanos ya pueden ser chamanes, así que la clase llega a la Alianza. Ráfaga de lava se mejoró y Elemental subió en las clasificaciones de daño.' },
  { id:'mage', n:'Mago', roles:['dps'],
    specs:[['Arcano','Ráfagas, mucho maná',['dps']],['Fuego','Críticos e igniciones',['dps']],['Escarcha','Daño y control',['dps']]],
    lvl:'La subida más rápida, un 8% más rápida que la media (unas 12 horas de ahorro)',
    lp:-8,
    raid:'Portales y comida y agua para todo el grupo',
    forever:'Fuego recibió Buena racha, Arcano Explosión Arcana, Escarcha Lanza de hielo. Descarga de Pirofrío está disponible desde el nivel 40.' },
  { id:'warlock', n:'Brujo', roles:['dps'],
    specs:[['Aflicción','Daño con maldiciones y corrupción',['dps']],['Demonología','Daño a través de demonios',['dps']],['Destrucción','Daño directo de fuego y sombras',['dps']]],
    lvl:'Ritmo de subida medio',
    lp:0,
    raid:'Maestría de las Sombras ahora da un 2–10% de daño de sombras (antes 1–5%)',
    forever:'Aflicción tiene un nuevo hechizo canalizado, el demonio se queda con Sacrificio demoníaco, Destrucción gana Incinerar y daño en área.' },
  { id:'druid', n:'Druida', roles:['tank','heal','dps'],
    specs:[['Equilibrio','Daño a distancia',['dps']],['Combate feral','Tanque (oso) y daño cuerpo a cuerpo (gato)',['tank','dps']],['Restauración','Sanador, mucha sanación en el tiempo',['heal']]],
    lvl:'Un 5% más lenta que la media',
    lp:5,
    raid:'Líder de la manada y Aura de lechúcico lunar afectan a toda la banda y se acumulan',
    forever:'Cada especialización tiene un rol claro, las formas funcionan con pociones y encantamientos de arma. Puedes ser tanque, sanador y luchador en un solo personaje.' }
];
const ROLE_RU = { tank:'Tanque', heal:'Sanador', dps:'Daño', 'tank?':'Tanque (dudoso)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Grito de guerra', paladin:'Bendición de los Reyes', hunter:'Aura de disparo certero', priest:'Palabra de poder: entereza, Espíritu divino', shaman:'Tótems (Fuerza de la tierra, Viento Furioso, Lengua de Fuego, Gracia del aire)', mage:'Intelecto Arcano, portales, comida y agua', druid:'Marca de lo salvaje, Líder de la manada, Aura de lechúcico lunar' };

const RACES = [
  { id:'human', n:'Humano', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Will to Survive','Elimina el aturdimiento'],['a','Percepción','Revela enemigos invisibles durante 20 s'],['p','Ruthless','+2% de probabilidad de crítico'],['p','El espíritu humano','+5% de espíritu']],
    tip:'El espíritu se convierte en sanación para un Sacerdote Sagrado, así que un sacerdote humano es bueno para sanar.' },
  { id:'dwarf', n:'Enano', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Petraforma','Inmunidad a sangrados, venenos y enfermedades durante 8 s y menos daño físico'],['a','Buscar tesoro','Muestra cofres cercanos'],['p','Earth Fury','+2% de daño crítico y poder de sanación'],['p','Big Game Hunter','+5% de daño contra bestias']],
    tip:'Petraforma es útil para tanques y en JcJ.' },
  { id:'nightelf', n:'Elfo de la noche', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Elune’s Light','+10% de probabilidad de crítico durante 15 s'],['a','Fusión de las Sombras','Invisibilidad en el sitio'],['p','Prontitud','+1% de esquiva y +2% de velocidad de carrera'],['p','Espíritu de fuego fatuo','+75% de velocidad de carrera como espíritu']],
    tip:'La única raza de la Alianza con druida, salvo que elijas Skyborne.' },
  { id:'gnome', n:'Gnomo', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Artista del escape','Breve inmunidad a ralentizaciones e inmovilizaciones'],['a','Eureka!','Las próximas 3 habilidades cuestan menos y son un 10% más fuertes'],['p','Mente expansiva','+5% de maná, ira o energía máximos'],['p','Especialización de ingeniería','Los artefactos de ingeniería funcionan de forma más fiable']],
    tip:'Mente expansiva ayuda sobre todo a las clases de energía.' },
  { id:'skyA', n:'Skyborne (Alianza)', f:'alliance', paid:true, name:'Skyborne High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Planea hacia abajo durante 10 s, sin daño por caída'],['a','Read Ley Line','+100% de regeneración de salud y maná'],['p','Wind Blessed','+3% de velocidad de ataque y de hechizos'],['p','Elemental Insight','+5% de daño contra elementales']],
    tip:'Raza de pago: Heroic Pack desde 29,99 $. Empieza en Zephras Isle (niveles 1–12).' },
  { id:'orc', n:'Orco', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Furia sangrienta','+10% de poder de ataque y poder con hechizos durante 15 s'],['a','Shatter Curse','Elimina maldiciones y corrupción, −5% de daño mágico recibido durante 8 s'],['p','Savage','+1% de probabilidad de crítico'],['p','Firmeza','Los aturdimientos duran un 20% menos']],
    tip:'Furia sangrienta da una potente ventana de daño.' },
  { id:'undead', n:'No-muerto', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Voluntad de los Renegados','Elimina hechizos, miedo y sueño'],['a','Canibalizar','Restaura un 35% de salud y maná con el tiempo'],['p','Respiración subacuática','Respira bajo el agua más tiempo'],['p','Touch of the Grave','Probabilidad de drenar salud al atacar']],
    tip:'Combinación nueva: un paladín para la Horda, donde esta clase no existía antes.' },
  { id:'tauren', n:'Tauren', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Pisotón de guerra','Aturde a los enemigos cercanos durante 2 s'],['a','Cultivo','Cultiva hierbas que se pueden recoger sin Herboristería'],['p','Plainsrunning','La velocidad aumenta mientras corres'],['p','Robustez','+5% de salud y +2% de daño crítico']],
    tip:'La única raza de la Horda con druida, salvo que elijas Skyborne.' },
  { id:'troll', n:'Trol', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Iracundia','+10% de velocidad de ataque y de hechizos durante 10 s'],['a','Rapid Regeneration','Restaura salud con el tiempo'],['p','Matanza de bestias','+5% de daño contra bestias'],['p','Regeneración','La salud se regenera también en combate']],
    tip:'Más opciones de clase de la Horda: siete.' },
  { id:'skyH', n:'Skyborne (Horda)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Planea hacia abajo durante 10 s, sin daño por caída'],['a','Skysight','+10% de velocidad de carrera'],['p','Wind Blessed','+3% de velocidad de ataque y de hechizos'],['p','Elemental Insight','+5% de daño contra elementales']],
    tip:'Raza de pago: Heroic Pack desde 29,99 $. Solo la Horda puede tener chamán, solo la Alianza mago.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "La raza más numerosa de la Alianza. Versátil y fuerte en JcJ gracias a Will to Survive.", "dwarf": "Robustos mineros y fusileros de Forjaz. Por primera vez en Classic la Alianza tiene chamanes, y son enanos.", "nightelf": "Un pueblo antiguo de los bosques. Escurridizos: su propia forma de esconderse, esquiva y carrera rápida.", "gnome": "Los inventores de Gnomeregan. Pequeños, astutos y con la mejor habilidad de escape del juego.", "skyA": "Una raza nueva en Forever. Los High Order: elfos del viento que buscan la magia arcana perdida de sus ancestros.", "orc": "El corazón de la Horda. Los guerreros más fuertes y maestros del JcJ gracias a Furia sangrienta y Firmeza.", "undead": "Los Renegados: antiguos humanos que se liberaron del Rey Exánime. Inmunes al miedo y al sueño cuando importa.", "tauren": "Gigantes pacíficos de las llanuras. La mayor salud y su propio aturdimiento en área.", "troll": "La tribu Lanza Negra. Más clases que nadie en la Horda y una potente Iracundia para el daño.", "skyH": "Una raza nueva en Forever. Los Windshaper: líderes espirituales de los Skyborne, cercanos a los elementos."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Armas':'Arms','Furia':'Fury','Protección':'Protection','Sagrado':'Holy','Reprensión':'Retribution',
  'Bestias':'Beast Mastery','Puntería':'Marksmanship','Supervivencia':'Survival',
  'Asesinato':'Assassination','Combate':'Combat','Sutileza':'Subtlety',
  'Disciplina':'Discipline','Sombras':'Shadow','Elemental':'Elemental','Mejora':'Enhancement','Restauración':'Restoration',
  'Arcano':'Arcane','Fuego':'Fire','Escarcha':'Frost','Aflicción':'Affliction','Demonología':'Demonology','Destrucción':'Destruction',
  'Equilibrio':'Balance','Combate feral':'Feral',
  'Will to Survive':'Will to Survive','Percepción':'Perception','Ruthless':'Ruthless','El espíritu humano':'The Human Spirit',
  'Petraforma':'Stoneform','Buscar tesoro':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Elune’s Light':"Elune’s Light",'Fusión de las Sombras':'Shadowmeld','Prontitud':'Quickness','Espíritu de fuego fatuo':'Wisp Spirit',
  'Artista del escape':'Escape Artist','Eureka!':'Eureka!','Mente expansiva':'Expansive Mind','Especialización de ingeniería':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Furia sangrienta':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Firmeza':'Hardiness',
  'Voluntad de los Renegados':'Will of the Forsaken','Canibalizar':'Cannibalize','Respiración subacuática':'Underwater Breathing','Touch of the Grave':'Touch of the Grave',
  'Pisotón de guerra':'War Stomp','Cultivo':'Cultivation','Plainsrunning':'Plainsrunning','Robustez':'Endurance',
  'Iracundia':'Berserking','Rapid Regeneration':'Rapid Regeneration','Matanza de bestias':'Beast Slaying','Regeneración':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Consejo</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Alianza' : 'Horda'; }
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Más rápido en ${-p}%` : p > 0 ? `Más lento en ${p}%` : 'Ritmo medio';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>más rápido</span><span>más lento</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Clase</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Subida de nivel</span><span>En bandas</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Roles: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Raza</span><span>Clases</span><span class="abl">Habilidades <span class="abt">activa</span><span class="abt p">pasiva</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">de pago</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Clases: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nuevo' : v ? '' : ', no disponible')); }).join('')}</span>
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
  let h = '<thead><tr><th scope="col">Raza</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">de pago</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: no permitido"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', combinación nueva' : ''}`;
        const mark = v === 'new' && !sel ? '<span class="nw">nuevo</span>' : '<i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>';
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
    return `<button type="button" data-pc="${c.id}" class="${v ? '' : 'na'}" aria-pressed="${c.id === state.cls}">${esc(c.n)}${v === 'new' ? ' · nuevo' : ''}</button>`;
  }).join('');
  $('#pickm').innerHTML = `<div><div class="lbl">1. Raza</div><div class="chiprow">${races}</div></div>
    <div><div class="lbl">2. Clase (discontinua: no disponible para esta raza, toca para cambiar de raza)</div><div class="chiprow">${cls}</div></div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Activa' : 'Pasiva'}</span><b>${bi(x[1])}</b><span>${esc(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', requiere el pack Skyborne' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><img src="../assets/art/${c.id}-600.webp" width="600" height="804" alt="" loading="lazy" decoding="async"></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}${face(c.id, CCOL[c.id])}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Combinación nueva</span>' : ''}${r.paid ? '<span class="tag paid">Raza de pago</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Especializaciones</h4><div class="cards">${specs}</div></div>
        <div><h4>Habilidades raciales</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Subida de nivel</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>En bandas</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Novedades</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Mi elección">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copiar mi elección</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copiado');
  $('#qPick').textContent = `Ahora: ${r.n} · ${c.n}`;
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
  warrior: 'Placas, ira y primera línea. Aguanta los golpes como tanque o arrasa con un arma de dos manos.',
  paladin: 'Un guerrero sagrado con placas: sana, tanquea y golpea con el martillo. Ahora también en la Horda.',
  hunter: 'Arco, trampas y una bestia leal a tu lado. Una de las clases que más rápido suben.',
  rogue: 'Venenos, hojas y sombras. Daño puro desde la emboscada y control de masas.',
  priest: 'Luz y Sombra en unas mismas manos. El sanador principal del grupo o un lanzador oscuro.',
  shaman: 'Tótems y elementos: sana, golpea con rayos o con armas. Ahora también en la Alianza.',
  mage: 'Magia de fuego, escarcha y arcana. Portales, comida y agua para todo el grupo.',
  warlock: 'Maldiciones, demonios y fuego. Daño en el tiempo y un demonio propio que te ayuda.',
  druid: 'Oso, gato, lechúcico o sanador: los tres roles en un solo personaje.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Más sobre la clase</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">de pago</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">Más sobre la raza</span></span>
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
  $('#szNote').textContent = n ? `${parties} grupos de 5${n % PARTY ? ', el último está incompleto' : ''}` : '';
  const races = RACES.filter(r => r.f === team.f);
  let html = '';
  for (let g = 0; g < parties; g++) {
    const part = team.list.slice(g * PARTY, g * PARTY + PARTY), c = countRoles(part);
    const need = [];
    if (!c.tank) need.push('sin tanque'); if (!c.heal) need.push('sin sanador'); if (part.length < PARTY) need.push(`faltan ${PARTY - part.length}`);
    const status = need.length ? `<span class="miss">${need.join(', ')}</span>` : '<span class="ok">grupo completo</span>';
    html += `<div class="party"><div class="party-h"><h4>Grupo ${g + 1}</h4><span class="pc"><span>${ri('tank')}${c.tank}</span><span>${ri('heal')}${c.heal}</span><span>${ri('dps')}${c.dps}</span>${status}</span></div>`;
    part.forEach((s, k) => {
      const i = g * PARTY + k, r = RC[s.race], ro = roleOpts(CL[s.cls]);
      html += `<div class="slot" style="--cc:${CCOL[s.cls]}" data-i="${i}"><span class="no av"><img src="${ROOT}assets/art/${s.cls}-face.webp" width="160" height="160" alt="" loading="lazy" decoding="async"><b>${i + 1}</b></span>
      <select class="srace" aria-label="Raza del jugador ${i + 1}">${races.map(x => `<option value="${x.id}"${x.id === s.race ? ' selected' : ''}>${esc(x.n)}${x.paid ? ' (de pago)' : ''}</option>`).join('')}</select>
      <select class="scls" aria-label="Clase del jugador ${i + 1}">${Object.keys(r.can).map(c2 => `<option value="${c2}"${c2 === s.cls ? ' selected' : ''}>${esc(CL[c2].n)}</option>`).join('')}</select>
      <select class="srole" aria-label="Rol del jugador ${i + 1}">${ro.map(x => `<option value="${x}"${x === s.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('')}</select>
      <button class="del" aria-label="Quitar jugador ${i + 1}"><svg class="ico" aria-hidden="true"><use href="#i-x"/></svg></button></div>`;
    });
    html += '</div>';
  }
  $('#slots').innerHTML = html;
  $('#bAdd').disabled = n >= MAXT;
  const cnt = countRoles(team.list);
  $('#roleSum').innerHTML = RR.map(x => `<div class="rs ${cnt[x] ? 'ok' : 'zero'}"><b>${cnt[x]}</b><span>${ri(x)}${ROLE_RU[x]}</span></div>`).join('');
  const v = [];
  if (!n) v.push(['', 'Toca un tamaño de grupo o añade un jugador.']);
  else {
    const full = Array.from({ length: parties }, (_, g) => team.list.slice(g * PARTY, g * PARTY + PARTY)).filter(p => p.length === PARTY && p.some(s => s.role === 'tank') && p.some(s => s.role === 'heal')).length;
    if (full) v.push(['good', `Grupos listos para mazmorra: ${full} de ${parties}. Cada uno tiene tanque y sanador.`]);
    if (full < parties) v.push(['warn', 'A algunos grupos les falta tanque, sanador o jugadores. Están resaltados en la lista.']);
    RAIDS.forEach(([size, name]) => v.push([n >= size ? 'good' : '', n >= size ? `Banda de ${size} (${name}): jugadores suficientes.` : `Banda de ${size} (${name}): faltan ${size - n}.`]));
    const byCls = {}; team.list.forEach(s => byCls[s.cls] = (byCls[s.cls] || 0) + 1);
    const dup = Object.keys(byCls).filter(c => byCls[c] > 1 && BUFF[c]);
    if (dup.length && n <= 10) v.push(['', `Clases repetidas (${dup.map(c => CL[c].n).join(', ')}): sus beneficios se solapan, la segunda aporta menos.`]);
    const sky = team.list.filter(s => RC[s.race].paid).length;
    if (sky) v.push(['', `Skyborne es una raza de pago: el Heroic Pack desde 29,99 $ lo necesitan ${sky} de ${n} jugadores.`]);
  }
  $('#verdict').innerHTML = v.map(x => `<li class="${x[0]}">${esc(x[1])}</li>`).join('');
  const have = [...new Set(team.list.map(s => s.cls))];
  const withB = have.filter(c => BUFF[c]), noB = have.filter(c => !BUFF[c]);
  $('#buffs').innerHTML = (withB.length ? withB.map(c => `<li class="good"><span class="cdot" style="--cc:${CCOL[c]}"></span><b>${esc(CL[c].n)}:</b> ${esc(BUFF[c])}</li>`).join('') : '<li>Aún no hay clases con beneficios de grupo.</li>')
    + (noB.length ? `<li>Sin beneficio de grupo: ${noB.map(c => CL[c].n).join(', ')}. Hacen daño puro.</li>` : '');
  $('#teamText').value = n ? Array.from({ length: parties }, (_, g) => (parties > 1 ? `Grupo ${g + 1}: ` : '') + team.list.slice(g * PARTY, g * PARTY + PARTY).map(s => `${raceName(RC[s.race])} ${CL[s.cls].n} (${ROLE_RU[s.role]})`).join(', ')).join('; ') + ` — ${facName(team.f)}` : '';
  $('#qTeam').textContent = n ? `${facName(team.f)}, jugadores: ${n}, tanques ${cnt.tank}, sanadores ${cnt.heal}` : 'De uno a cuarenta jugadores';
  if (teamTouched) { try { history.replaceState(null, '', n ? teamLink() : location.pathname); } catch (e) {} }
}
function touch() { teamTouched = true; renderTeam(); }
async function copyTo(text, msgEl, ok) {
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'No se pudo copiar, selecciona el texto y pulsa Ctrl+C'; }
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
$('#copyTeam').onclick = () => copyTo($('#teamText').value, $('#teamMsg'), 'Grupo copiado');
$('#copyLink').onclick = () => copyTo(teamLink(), $('#teamMsg'), 'Enlace copiado');
if (!fromLink) team.list = autoTeam(5, team.f);
renderTeam();
if (fromLink) setTimeout(() => document.getElementById('builder').scrollIntoView(), 0);

/* Dungeons: [name, min, max, entrance zone, new, other sites' ranges where they differ] */
const DUNGEONS = [
  ['Sima Ígnea', 13, 18, 'Orgrimmar', 0, [], 'horde'],
  ['Hall of Thanes', 13, 18, 'Forjaz', 1, [['Icy Veins', '13–20']]],
  ['Ruinas de Lordaeron', 15, 20, 'Claros de Tirisfal', 1, [['Icy Veins', '15–22']]],
  ['Las Minas de la Muerte', 15, 22, 'Páramos de Poniente', 0, [['Icy Veins', '17–26']]],
  ['Cuevas de los Lamentos', 17, 24, 'Los Baldíos', 0, [['Icy Veins', '15–24']]],
  ['Castillo de Colmillo Oscuro', 20, 26, 'Bosque de Argénteos', 0, [['Icy Veins', '20–30']]],
  ['Cavernas de Brazanegra', 22, 28, 'Vallefresno', 0, [['Sportskeeda', '22–26'], ['Icy Veins', '24–32']]],
  ['Excavation Site: Wetlands', 24, 29, 'Los Humedales', 1, [['ClassicWoW.gg', '26–31'], ['Icy Veins', '26–33']]],
  ['Las Mazmorras', 25, 29, 'Ciudad de Ventormenta', 0, [['Icy Veins', '24–32']], 'alliance'],
  ['City of Dalaran', 28, 33, 'Montañas de Alterac', 1, [['Icy Veins', '28–35']]],
  ['Gnomeregan', 29, 38, 'Dun Morogh', 0],
  ['Horado Rajacieno', 29, 38, 'Los Baldíos', 0],
  ['Monasterio Escarlata: Cementerio', 30, 38, 'Claros de Tirisfal', 0],
  ['Monasterio Escarlata: Biblioteca', 33, 41, 'Claros de Tirisfal', 0],
  ['The Drowned City', 35, 40, 'Vega de Tuercespina', 1],
  ['Monasterio Escarlata: Armería', 36, 44, 'Claros de Tirisfal', 0],
  ['Uldaman', 36, 45, 'Tierras Inhóspitas', 0, [['Icy Veins', '41–51']]],
  ['Zahúrda Rojocieno', 37, 46, 'Los Baldíos', 0],
  ['Monasterio Escarlata: Catedral', 38, 46, 'Claros de Tirisfal', 0],
  ["Zul’Farrak", 40, 47, 'Tanaris', 0, [['Icy Veins', '44–54']]],
  ["Krol’dok Stronghold", 40, 45, 'Riverglades', 1],
  ['Maraudon', 45, 51, 'Desolace', 0, [['Icy Veins', '46–55']]],
  ['Alcaz Island Prison', 48, 53, 'Marjal Revolcafango', 1],
  ["El Templo de Atal’Hakkar", 50, 55, 'Pantano de las Penas', 0, [['Icy Veins', '50–60']]],
  ['Profundidades de Roca Negra', 52, 60, 'Montaña Roca Negra', 0],
  ['Blackmaw Hold', 55, 60, 'Azshara', 1],
  ['Cumbre de Roca Negra Inferior', 57, 60, 'Montaña Roca Negra', 0, [['Icy Veins', '55–60']]],
  ['La Masacre: Este', 58, 60, 'Feralas', 0, [['Icy Veins', '54–60']]],
  ["Shaper’s Terrace", 58, 60, "Cráter de Un’Goro", 1],
  ['Stratholme: vivos', 58, 60, 'Tierras de la Peste del Este', 0],
  ['Stratholme: no-muertos', 58, 60, 'Tierras de la Peste del Este', 0],
  ['Scholomance', 58, 60, 'Tierras de la Peste del Oeste', 0],
  ['Cumbre de Roca Negra Superior', 60, 60, 'Montaña Roca Negra', 0, [['Icy Veins', '59–60']]],
  ['La Masacre: Oeste', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]],
  ['La Masacre: Norte', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]]
];
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
const facOk = (d, f) => !f || !d[6] || d[6] === f;   // Ragefire Chasm and The Stockade open from a capital

/* Professions: camp object (tier 1) and the class buff it stands in for */
const PROFS = [
  ['alchemy', 'Alquimia', 1, 'Mana Well', 'como Bendición de Sabiduría'],
  ['blacksmithing', 'Herrería', 1, 'Sharpening Wheel', 'como Fuerza de tótem de la Tierra'],
  ['enchanting', 'Encantamiento', 1, 'Enchanted Lute', 'como Marca de lo salvaje'],
  ['engineering', 'Ingeniería', 1, 'Reagent Bot', 'vendedor de componentes, reparaciones en nivel 2'],
  ['herbalism', 'Herboristería', 1, 'Incense Candle', 'como Intelecto Arcano'],
  ['leatherworking', 'Peletería', 1, 'Camp Tent', 'más experiencia por descanso'],
  ['mining', 'Minería', 1, 'Lodestone', 'como Bendición del poderío'],
  ['skinning', 'Desollando', 1, 'Camp Chair', 'como Aura de lechúcico lunar'],
  ['tailoring', 'Sastrería', 1, 'Faction Banner', 'como Espíritu divino'],
  ['cooking', 'Cocina', 0, 'Basic Campfire', 'más huecos para objetos en el campamento'],
  ['firstaid', 'Primeros auxilios', 0, 'First Aid Kit', 'como Palabra de poder: entereza'],
  ['fishing', 'Pesca', 0, 'Fish Bowl', 'como Bendición de los Reyes']
];
const PR = Object.fromEntries(PROFS.map(p => [p[0], p]));

/* Game stages: f = fact from the sources, t = our tip */
const SRC = {
  names: ['Icy Veins: reserva de nombres', 'https://www.icy-veins.com/wow-forever/name-reservation'],
  names2: ['Team Overpowered: nombres y apellidos', 'https://teamoverpowered.com/forever/guides/name-reservation/'],
  prof: ['Warcraft Tavern: profesiones', 'https://www.warcrafttavern.com/forever/guides/professions/'],
  camp: ['Warcraft Tavern: acampada', 'https://www.warcrafttavern.com/forever/guides/camping/'],
  legacy: ['Blizzard: Legacy', 'https://news.blizzard.com/en-gb/article/24307383'],
  dung: ['Warcraft Tavern: mazmorras', 'https://www.warcrafttavern.com/forever/guides/dungeons/'],
  ride: ['Warcraft Tavern: equitación', 'https://www.warcrafttavern.com/forever/guides/riding/'],
  cwg: ['ClassicWoW.gg: fechas y bandas', 'https://classicwow.gg/forever']
};
const STAGES = [
  { id: 'pre', n: 'Antes del lanzamiento', sub: 'hasta el 04.11', lo: 0, hi: 0,
    todo: [['f', 'Reserva anticipada de nombres del 27.10 al 03.11 para quienes tengan los packs Heroic, Epic y Collection. Por orden de llegada.'],
      ['f', 'Puedes reservar hasta tres personajes por cuenta. Un personaje tiene nombre y apellido, y la pareja debe ser única en la región.'],
      ['f', 'Desde el 04.11 se necesita suscripción o tiempo de juego para jugar.'],
      ['t', 'Elige tres nombres con apellido, más algunos de reserva, antes del 27.10.']],
    dnote: 'Las primeras mazmorras abren al nivel 13.',
    prof: [['f', 'Cada personaje tiene dos profesiones principales y las tres secundarias: Cocina, Primeros auxilios y Pesca.'],
      ['f', 'Cada profesión coloca su propio objeto de campamento con un beneficio parecido a uno de clase.'],
      ['t', 'Repartid las profesiones antes: uno se queda Cocina para la hoguera, los demás eligen distintas para que los beneficios del campamento no se repitan.']],
    legacy: [['f', 'Legacy se abre con tu primer punto: nivel 25, 150 en una profesión (no de recolección) o explorar todo el mapa.'],
      ['f', 'En el lanzamiento un personaje puede gastar como máximo 16 puntos, el resto va a la ruta de recompensas.']],
    group: [['t', 'Poneos de acuerdo en una facción y un modo: solo podéis agruparos dentro de un modo, y en JcJ una cuenta tiene una sola facción.'],
      ['t', 'Monta tu grupo en el creador de grupos: un tanque, un sanador y clases distintas por los beneficios.']],
    src: ['names', 'names2', 'prof', 'legacy'] },
  { id: 'first', n: 'Primeros días', sub: 'niveles 1–15', lo: 1, hi: 15,
    todo: [['f', 'Los Skyborne empiezan en Zephras Isle, niveles 1–12.'],
      ['f', 'Los talentos se abren al nivel 10, o al 9 con la ventaja de Legacy Talented.'],
      ['f', 'La mayoría de la comida cocinada da un bonus de experiencia. Se acumula con el campamento y con el Cozy Sleeping Bag.'],
      ['t', 'Acumula descanso: desconéctate en una posada o en un campamento con tienda.']],
    prof: [['f', 'La hoguera básica no necesita Cocina y admite 3 objetos. Arde unos 10 minutos, y puedes poner otra a los 5.'],
      ['f', 'Para recibir los beneficios del campamento, siéntate cerca (/sit) al menos un minuto.'],
      ['t', 'Empieza con una profesión de recolección desde los primeros niveles: hierbas, mineral y pieles alimentan la fabricación, y 150 en una profesión de fabricación abre Legacy.']],
    legacy: [['f', 'Aún no hay ventajas: el primer punto llega al nivel 25 o con 150 en una profesión.'],
      ['t', 'Cuando se abra Legacy, coge primero las ventajas de experiencia y campamento: Well Rested, Field Guide, Permanence. Talented sirve para los alters.']],
    group: [['t', 'Subid de nivel en la misma zona y montad campamento en cada parada: cinco minutos de hoguera se pagan con beneficios para todo el grupo.'],
      ['t', 'Formad vuestro primer grupo de cinco hacia el nivel 13–15.']],
    src: ['camp', 'legacy', 'dung'] },
  { id: 'dung', n: 'Mazmorras', sub: 'niveles 15–40', lo: 15, hi: 40,
    todo: [['f', 'La mayor parte de la experiencia de una mazmorra viene de sus cadenas de misiones. Repetirla después da bastante menos experiencia que hacer misiones en el mundo.'],
      ['f', 'Cada objeto que cae desbloquea su apariencia de transfiguración para todos los que puedan llevarlo, aunque se lo quede otro.'],
      ['f', 'Legacy se abre al nivel 25.'],
      ['t', 'Recoged primero las misiones de la mazmorra en grupo y entrad cuando todos las tengan.']],
    prof: [['f', 'Cocina 140 da 5 huecos de campamento, 220 da 10.'],
      ['f', 'Cada profesión fabrica tres objetos de campamento, uno por nivel. Las fuentes no coinciden en la habilidad necesaria para los niveles 2 y 3.'],
      ['t', 'Si el nivel 25 aún queda lejos, sube una profesión de fabricación a 150: Legacy se abrirá antes.']],
    legacy: [['f', 'Cada desafío da 1 punto. Hay 65: clases 27, profesiones 18, JcJ 12, mazmorras 3, bandas 3, aventura 2.'],
      ['t', 'Merecen la pena Reagent Economy (sin componentes comprados para habilidades) y Field Guide (menos reutilización de los objetos de campamento).']],
    group: [['f', 'Una mazmorra está pensada para 5 jugadores: un tanque, un sanador y tres de daño.'],
      ['f', 'No hay escalado de nivel, así que un amigo que vaya muy por detrás lo pasará mal en la mazmorra.'],
      ['t', 'Mantened los niveles parejos: quien se quede atrás se pone al día con misiones, y las mazmorras las hacéis juntos.']],
    src: ['dung', 'camp', 'legacy'] },
  { id: 'path', n: 'Camino al 60', sub: 'niveles 40–60', lo: 40, hi: 60,
    todo: [['f', 'Montura al nivel 40 (60% de velocidad), una rápida al 60 (100%). Entrena con el instructor de tu raza.'],
      ['f', 'Los paladines y los brujos consiguen su montura con misiones de clase.'],
      ['f', 'Honorable con tu propia facción da un 10% de descuento en el entrenamiento de equitación y en monturas. Según Warcraft Tavern: 100 + 20 de oro en el nivel 40, 1000 + 200 en el 60.'],
      ['t', 'Ahorra oro para el nivel 40: la equitación será tu mayor gasto camino al 60.']],
    prof: [['f', 'Cada profesión tiene sus propios objetos de campamento de nivel 2 y 3. El segundo objeto de Ingeniería, Repair Bot, repara el equipo.'],
      ['t', 'Mantened Cocina 220 en el grupo para un campamento de 10 objetos: para las bandas habrá sitio para todos.']],
    legacy: [['f', 'Como máximo 16 puntos por personaje, el resto va a la ruta de recompensas: un juguete a los 15, una mascota a los 25, un tabardo a los 40, una montura a los 55.']],
    group: [['f', 'Las bandas abren el 09.12: Barrow Deeps para 10 jugadores, la Cima Hyjal para 20, Guarida de Onyxia para 40.'],
      ['t', 'La banda de 10 necesita 10 jugadores: si sois menos, buscad al resto en vuestra hermandad con tiempo.']],
    src: ['ride', 'prof', 'legacy', 'cwg'] },
  { id: 'raid', n: '60 y bandas', sub: 'desde el 09.12', lo: 60, hi: 60,
    todo: [['f', 'El 09.12 abren Barrow Deeps (10 jugadores), la Cima Hyjal (20) y Guarida de Onyxia (40, Marjal Revolcafango).'],
      ['f', 'Completar cada una de las tres bandas da un punto de Legacy.'],
      ['f', 'Nuevo campo de batalla 15c15: Darkspear Islands, frente a la costa del Marjal Revolcafango.'],
      ['t', 'Mientras reunís gente para la banda, haced mazmorras de nivel 60 para conseguir equipo.']],
    prof: [['f', 'Los beneficios del campamento son algo más débiles que los de clase y no se acumulan con ellos: Bendición de los Reyes da un 10% a todas las estadísticas, el campamento un 8%.'],
      ['t', 'Montad el campamento en la entrada de la banda: sus beneficios cubren lo que les falta a vuestras clases.']],
    legacy: [['f', 'Desafíos para el nivel 60: mazmorras 3, bandas 3, JcJ 12. El JcJ tiene rangos con tope semanal y mejoras de equipo por Honor.']],
    group: [['f', 'Los mismos beneficios de dos jugadores de una clase se solapan; los de clases distintas se acumulan.'],
      ['t', 'Monta tu banda en el creador de grupos y publica el enlace en el chat.']],
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
  if (now < D_REL) return ['pre', 'Según la fecha: antes del lanzamiento del 04.11.'];
  if (me.lvl) return [me.lvl < 15 ? 'first' : me.lvl < 40 ? 'dung' : me.lvl < 60 ? 'path' : 'raid', 'Según el nivel de tu personaje.'];
  if (now >= D_RAID) return ['raid', 'Según la fecha: las bandas están abiertas.'];
  return [now < new Date('2026-11-11T00:00:00') ? 'first' : 'dung', 'Según la fecha. Añade el nivel de tu personaje y la etapa lo seguirá.'];
}
const START = { pre: 'hero_dawn-960', first: 'hero_campfire-960', dung: 'warlock-360', path: 'hunter-360', raid: 'paladin-360' };
const ARTV = /*ARTV*/{"hero_campfire-960.avif":"?v=2654726f","hero_campfire-960.webp":"?v=d73f1e16","hero_dawn-960.avif":"?v=72b3acf6","hero_dawn-960.webp":"?v=4eae2c5c"};   // ?v= of the scene arts, filled in by build.art_version (same names, redrawn pictures)
const pic = f => `<picture><source type="image/avif" srcset="${ROOT}assets/art/${f}.avif${ARTV[f + '.avif'] || ''}"><img src="${ROOT}assets/art/${f}.webp${ARTV[f + '.webp'] || ''}" alt="" loading="lazy" decoding="async"></picture>`;
const tipL = () => '<span class="tl">Consejo</span>';
function liC(x) { return x[0] === 't' ? `<li class="tip">${tipL()}${esc(x[1])}</li>` : `<li>${esc(x[1])}</li>`; }
function dLi(d) {
  const mine = me.lvl && nearLvl(d, me.lvl);
  return `<li class="${mine ? 'mine' : ''}"><b>${esc(d[0])}</b><span class="pill${mine ? ' gold' : ''}">${lvRange(d)}</span><span class="z">${esc(d[3])}${d[4] ? ' · <i>nuevo</i>' : ''}${mine ? '<span class="sr"> · para tu nivel</span>' : ''}</span></li>`;
}
function renderStage() {
  const [auto, why] = autoStage();
  if (stageAuto) stageSel = auto;
  const s = ST[stageSel];
  $('#stageBar').innerHTML = STAGES.map(x => `<button type="button" class="stile" role="tab" id="tab-${x.id}" data-st="${x.id}" aria-controls="stagePanel" aria-selected="${x.id === stageSel}" tabindex="${x.id === stageSel ? 0 : -1}">${pic(START[x.id])}${x.id === auto ? '<span class="now">ahora</span>' : ''}<b>${esc(x.n)}</b><span class="lv">${esc(x.sub)}</span></button>`).join('');
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
  $('#stagePanel').innerHTML = `<div class="st-head"><div class="t"><h3>${esc(s.n)}</h3><span class="pill gold">${esc(s.sub)}</span></div><p class="why">${stageAuto ? esc(why) : 'Etapa elegida a mano.'}</p></div>
    <ol class="steps-c">${steps}</ol>
    <div class="st-cols">
      <div><h4>Mazmorras para este nivel</h4>${s.dnote ? `<p class="small" style="margin:-4px 0 10px">${esc(s.dnote)}</p>` : ''}<ul class="dlist">${ds.slice(0, MAXD).map(dLi).join('')}</ul>
        <a class="more-l" href="guides/dungeons/">${extra > 0 ? `Más mazmorras en la tabla: ${extra}` : 'Las 35 mazmorras'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
      <div style="display:grid;gap:24px;align-content:start"><div><h4>Profesiones y campamento</h4><ul class="clean">${s.prof.map(liC).join('')}</ul></div>
        <div><h4>Ventajas de Legacy</h4><ul class="clean">${s.legacy.map(liC).join('')}</ul></div></div>
    </div>
    <div class="gtip"><h4 style="margin:0 0 10px;font-size:1.02rem">Consejos para el grupo</h4><ul class="clean">${s.group.map(liC).join('')}</ul></div>
    <p class="st-src"><span>Fuentes:</span>${s.src.map(k2 => `<a href="${SRC[k2][1]}" target="_blank" rel="noopener">${esc(SRC[k2][0])}</a>`).join('')}</p>`;
}
function optList(items, cur, none) { return `<option value="">${esc(none)}</option>` + items.map(([v, t]) => `<option value="${v}"${v === cur ? ' selected' : ''}>${esc(t)}</option>`).join(''); }
function renderMe() {
  fixMe();
  const races = f => RACES.filter(r => r.f === f).map(r => `<option value="${r.id}"${r.id === me.race ? ' selected' : ''}>${esc(r.n)}</option>`).join('');
  $('#meRace').innerHTML = `<option value="">Sin elegir</option><optgroup label="${facName('alliance')}">${races('alliance')}</optgroup><optgroup label="${facName('horde')}">${races('horde')}</optgroup>`;
  const cls = (me.race ? Object.keys(RC[me.race].can) : CLASSES.map(c => c.id)).map(id => [id, CL[id].n]);
  $('#meCls').innerHTML = optList(cls, me.cls, 'Sin elegir');
  $('#meRole').innerHTML = me.cls ? roleOpts(CL[me.cls]).map(x => `<option value="${x}"${x === me.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('') : `<option value="">Elige primero una clase</option>`;
  $('#meRole').disabled = !me.cls;
  const prim = PROFS.filter(p => p[2]);
  $('#meP1').innerHTML = optList(prim.filter(p => p[0] !== me.p2).map(p => [p[0], p[1]]), me.p1, 'Ninguno');
  $('#meP2').innerHTML = optList(prim.filter(p => p[0] !== me.p1).map(p => [p[0], p[1]]), me.p2, 'Ninguno');
  $('#meSec').innerHTML = PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${me.sec.includes(p[0])}">${esc(p[1])}</button>`).join('');
  document.querySelectorAll('.lvin').forEach(i => { if (document.activeElement !== i) i.value = me.lvl || ''; });
  const who = [me.race ? RC[me.race].n : '', me.cls ? CL[me.cls].n : ''].filter(Boolean).join(' · ');
  const sub = me.cls ? [ROLE_RU[me.role], me.race ? facName(RC[me.race].f) : ''].filter(Boolean).join(' · ') : 'Elige raza, clase y nivel abajo';
  const hero = $('#meHero');
  hero.style.setProperty('--cc', me.cls ? CCOL[me.cls] : '#c9a54a');
  hero.innerHTML = pic(me.cls ? `${me.cls}-600` : 'hero_campfire-960') + (me.lvl ? `<span class="lvb" aria-label="Nivel ${me.lvl}">${me.lvl}</span>` : '')
    + `<span class="k">Mi personaje</span><b>${who ? esc(who) : 'Aún no creado'}</b><span class="s">${esc(sub)}</span>`;
  let out = '';
  if (meSet()) {
    const b = [];
    if (me.cls) b.push(BUFF[me.cls] ? `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span><b>${esc(CL[me.cls].n)}:</b> ${esc(BUFF[me.cls])}</span></li>` : `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-dps"/></svg></span><span>${esc(CL[me.cls].n)}: sin beneficio de grupo, daño puro.</span></li>`);
    [me.p1, me.p2, ...me.sec].filter(Boolean).forEach(id => { const p = PR[id]; b.push(`<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg></span><span><b>${esc(p[3])}</b> <span class="m">· ${esc(p[1])}</span><br>${esc(p[4])}</span></li>`); });
    if (!b.length) b.push('<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span>Elige una clase y profesiones para ver tus beneficios.</span></li>');
    out += `<div><h4>Qué aportas al grupo</h4><ul class="buffs">${b.join('')}</ul></div>`;
    if (me.lvl) {
      const ds = DUNGEONS.filter(d => nearLvl(d, me.lvl) && facOk(d, me.race && RC[me.race].f));
      out += `<div><h4>Mazmorras para tu nivel</h4>` + (ds.length ? `<ul class="dlist">${ds.slice(0, 4).map(dLi).join('')}</ul>` : '<p class="small">Las primeras mazmorras empiezan al nivel 13.</p>')
        + `<a class="more-l" href="guides/dungeons/">${ds.length > 4 ? `Más mazmorras en la tabla: ${ds.length - 4}` : 'Tabla de mazmorras'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`;
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
