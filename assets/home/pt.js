const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Guerreiro', s:'Guerreiro', roles:['tank','dps'],
    specs:[['Armas','Dano corpo a corpo (arma de duas mãos)',['dps']],['Fúria','Dano corpo a corpo (duas armas)',['dps']],['Proteção','Tanque',['tank']]],
    lvl:'A evolução mais lenta, cerca de 12% mais longa que a média',
    lp:12,
    raid:'Brado de Batalha afeta a raide toda',
    forever:'Mais Raiva, melhor ameaça em grupos de alvos, o talento Weapon Master. Fúria e Sede de Sangue foram enfraquecidos.' },
  { id:'paladin', n:'Paladino', roles:['tank','heal','dps'],
    specs:[['Sagrado','Curador',['heal']],['Proteção','Tanque',['tank']],['Retribuição','Dano corpo a corpo',['dps']]],
    lvl:'Ritmo de evolução médio',
    lp:0,
    raid:'Bênção dos Reis agora é básica. Pelas listas do beta, Proteção está entre os tanques mais fortes, e Retribuição caiu depois do patch de 15 de outubro.',
    forever:'Golpe Sagrado a partir do nível 6, Julgamento não consome o selo. Mortos-vivos agora podem ser paladinos, então a classe chegou à Horda.' },
  { id:'hunter', n:'Caçador', roles:['dps'],
    specs:[['Domínio das Feras','Dano à distância, muito dano vindo do mascote',['dps']],['Precisão','Dano à distância',['dps']],['Sobrevivência','Corpo a corpo e à distância, armadilhas',['dps']]],
    lvl:'A evolução mais rápida, cerca de 8% mais rápida que a média',
    lp:-8,
    raid:'Aura de Tiro Certeiro afeta a raide toda',
    forever:'Dá para jogar sem mascote, armadilhas funcionam em combate, raposas surgiram como família de mascotes. Sobrevivência pode ir para o corpo a corpo.' },
  { id:'rogue', n:'Ladino', roles:['dps'],
    specs:[['Assassinato','Dano de venenos',['dps']],['Combate','Ataques rápidos com armas',['dps']],['Subterfúgio','Emboscadas, sangramentos',['dps']]],
    lvl:'Ritmo de evolução médio',
    lp:0,
    raid:'Dano corpo a corpo puro, sem bônus para a raide toda',
    forever:'Agora dá para usar machados de uma mão. Assassinato é construído em venenos, Subterfúgio em sangramentos e furtividade.' },
  { id:'priest', n:'Sacerdote', roles:['heal','dps'],
    specs:[['Disciplina','Curador, escudos e absorção',['heal']],['Sagrado','Curador',['heal']],['Sombra','Dano à distância',['dps']]],
    lvl:'Cerca de 5% mais lenta que a média',
    lp:5,
    raid:'Espírito Divino agora é básico. O dano de Sombra e Peste Devoradora (recarga de 24 s) foram fortalecidos pelo patch de 15 de outubro.',
    forever:'Proteção contra Medo e Peste Devoradora ficam disponíveis a partir do nível 20 para qualquer raça. Cada raça tem dois feitiços de sacerdote próprios.' },
  { id:'shaman', n:'Xamã', roles:['heal','dps','tank?'],
    specs:[['Elemental','Dano à distância',['dps']],['Aperfeiçoamento','Dano corpo a corpo. A capacidade de tanquear ainda é incerta',['dps','tank?']],['Restauração','Curador',['heal']]],
    lvl:'Ritmo de evolução médio',
    lp:0,
    raid:'Os totens Força da Terra, Fúria dos Ventos, Labaredas e Graça do Ar dão bônus ao próprio grupo',
    forever:'Anões agora podem ser xamãs, então a classe chegou à Aliança. Estouro de Lava foi fortalecida, Elemental subiu no ranking de dano.' },
  { id:'mage', n:'Mago', roles:['dps'],
    specs:[['Arcano','Explosão de dano, muita mana',['dps']],['Fogo','Críticos e ignições',['dps']],['Gélido','Dano e controle',['dps']]],
    lvl:'A evolução mais rápida, cerca de 8% mais rápida que a média (cerca de 12 horas a menos)',
    lp:-8,
    raid:'Portais, comida e água para o grupo todo',
    forever:'Fogo ganhou Embalo de Fogo, Arcano ganhou Impacto Arcano, Gélido ganhou Lança de Gelo. Seta de Fogofrio fica disponível a partir do nível 40.' },
  { id:'warlock', n:'Bruxo', roles:['dps'],
    specs:[['Suplício','Dano de maldições e corrupção',['dps']],['Demonologia','Dano por meio de demônios',['dps']],['Destruição','Dano direto de fogo e de sombra',['dps']]],
    lvl:'Ritmo de evolução médio',
    lp:0,
    raid:'Maestria em Sombras agora dá 2–10% de dano de sombra (antes 1–5%)',
    forever:'Suplício tem um novo feitiço canalizado, o demônio fica com Sacrifício Demoníaco, Destruição ganhou Incinerar e dano em área.' },
  { id:'druid', n:'Druida', roles:['tank','heal','dps'],
    specs:[['Equilíbrio','Dano à distância',['dps']],['Combate Feral','Tanque (urso) e dano corpo a corpo (gato)',['tank','dps']],['Restauração','Curador, muita cura ao longo do tempo',['heal']]],
    lvl:'Cerca de 5% mais lenta que a média',
    lp:5,
    raid:'Líder do Bando e Aura de Luniscante afetam a raide toda e se acumulam',
    forever:'Cada especialização ganhou uma função clara, as formas funcionam com poções e encantamentos de arma. Você pode ser tanque, curador e lutador num só personagem.' }
];
const ROLE_RU = { tank:'Tanque', heal:'Curador', dps:'Dano', 'tank?':'Tanque (incerto)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Brado de Batalha', paladin:'Bênção dos Reis', hunter:'Aura de Tiro Certeiro', priest:'Palavra de Poder: Fortitude, Espírito Divino', shaman:'Totens (Força da Terra, Fúria dos Ventos, Labaredas, Graça do Ar)', mage:'Inteligência Arcana, portais, comida e água', druid:'Marca do Indomado, Líder do Bando, Aura de Luniscante' };

const RACES = [
  { id:'human', n:'Humano', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Desejo de Sobreviver','Remove atordoamento'],['a','Percepção','Revela inimigos invisíveis por 20 s'],['p','Ruthless','+2% de chance de crítico'],['p','O Espírito Humano','+5% de espírito']],
    tip:'O espírito vira cura para um Sacerdote Sagrado, então um sacerdote humano é bom para curar.' },
  { id:'dwarf', n:'Anão', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Forma de Pedra','Imunidade a sangramentos, venenos e doenças por 8 s e dano físico reduzido'],['a','Localizar Tesouros','Mostra baús por perto'],['p','Earth Fury','+2% de dano crítico e de poder de cura'],['p','Big Game Hunter','+5% de dano contra feras']],
    tip:'Forma de Pedra é útil para tanques e no PvP.' },
  { id:'nightelf', n:'Elfo Noturno', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Luz de Eluna','+10% de chance de crítico por 15 s'],['a','Fusão Sombria','Invisibilidade sem sair do lugar'],['p','Rapidez','+1% de esquiva e +2% de velocidade de corrida'],['p','Espírito de Fogo-fátuo','+75% de velocidade de corrida como espírito']],
    tip:'A única raça da Aliança com druida, a menos que você pegue Skyborne.' },
  { id:'gnome', n:'Gnomo', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Artista da Fuga','Breve imunidade a lentidão e enraizamento'],['a','Eureca!','As próximas 3 habilidades custam menos e ficam 10% mais fortes'],['p','Mente Expansiva','+5% de mana, raiva ou energia máxima'],['p','Especialização em Engenharia','Dispositivos de engenharia funcionam com mais confiabilidade']],
    tip:'Mente Expansiva ajuda especialmente as classes de energia.' },
  { id:'skyA', n:'Skyborne (Aliança)', f:'alliance', paid:true, name:'Skyborne da High Order',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Walk on Air','Plana para baixo por 10 s, sem dano de queda'],['a','Read Ley Line','+100% de regeneração de vida e mana'],['p','Wind Blessed','+3% de velocidade de ataque e de feitiços'],['p','Elemental Insight','+5% de dano contra elementais']],
    tip:'Raça paga: Heroic Pack a partir de $29.99. Começa na região de Zephras Isle (níveis 1–12).' },
  { id:'orc', n:'Orc', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Fúria Sangrenta','+10% de poder de ataque e poder mágico por 15 s'],['a','Shatter Curse','Remove maldições e corrupção, −5% de dano mágico recebido por 8 s'],['p','Savage','+1% de chance de crítico'],['p','Robustez','Atordoamentos duram 20% menos']],
    tip:'Fúria Sangrenta dá uma janela de dano poderosa.' },
  { id:'undead', n:'Morto-vivo', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Determinação dos Renegados','Remove enfeitiçamento, medo e sono'],['a','Canibalizar','Restaura 35% de vida e mana ao longo do tempo'],['p','Respiração Subaquática','Respira debaixo d’água por mais tempo'],['p','Toque do Túmulo','Chance de drenar vida ao atacar']],
    tip:'Nova combinação: um paladino para a Horda, onde essa classe não existia antes.' },
  { id:'tauren', n:'Taureno', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Pisada de Guerra','Atordoa inimigos próximos por 2 s'],['a','Cultivo','Faz crescer ervas que podem ser colhidas sem Herborismo'],['p','Vencer Planícies','A velocidade aumenta enquanto você corre'],['p','Resistência','+5% de vida e +2% de dano crítico']],
    tip:'A única raça da Horda com druida, a menos que você pegue Skyborne.' },
  { id:'troll', n:'Troll', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Berserk','+10% de velocidade de ataque e de feitiços por 10 s'],['a','Regeneração Rápida','Restaura vida ao longo do tempo'],['p','Matança de Feras','+5% de dano contra feras'],['p','Regeneração','A vida se regenera também em combate']],
    tip:'O maior número de classes na Horda: sete.' },
  { id:'skyH', n:'Skyborne (Horda)', f:'horde', paid:true, name:'Skyborne Windshaper',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Walk on Air','Plana para baixo por 10 s, sem dano de queda'],['a','Skysight','+10% de velocidade'],['p','Wind Blessed','+3% de velocidade de ataque e de feitiços'],['p','Elemental Insight','+5% de dano contra elementais']],
    tip:'Raça paga: Heroic Pack a partir de $29.99. Só a Horda pode ter xamã, só a Aliança, mago.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "A raça mais numerosa da Aliança. Versátil e forte no PvP graças a Desejo de Sobreviver.", "dwarf": "Mineradores e fuzileiros robustos de Altaforja. Pela primeira vez no Classic a Aliança tem xamãs, e eles são anões.", "nightelf": "Um povo antigo das florestas. Esquivos: seu próprio jeito de se esconder, esquivar e correr rápido.", "gnome": "Os inventores de Gnomeregan. Pequenos, astutos e com a melhor habilidade de fuga do jogo.", "skyA": "Uma nova raça no Forever. A High Order: elfos do vento em busca da magia arcana perdida dos seus ancestrais.", "orc": "O coração da Horda. Os guerreiros mais fortes e mestres do PvP graças a Fúria Sangrenta e Robustez.", "undead": "Os Renegados: ex-humanos que se libertaram do Lich Rei. Imunes a medo e sono quando importa.", "tauren": "Gigantes pacíficos das planícies. A maior vida e seu próprio atordoamento em área.", "troll": "A tribo Lançanegra. O maior número de classes na Horda e um Berserk forte para dano.", "skyH": "Uma nova raça no Forever. Os Windshapers: líderes espirituais dos Skyborne, próximos aos elementos."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Armas':'Arms','Fúria':'Fury','Proteção':'Protection','Sagrado':'Holy','Retribuição':'Retribution',
  'Domínio das Feras':'Beast Mastery','Precisão':'Marksmanship','Sobrevivência':'Survival',
  'Assassinato':'Assassination','Combate':'Combat','Subterfúgio':'Subtlety',
  'Disciplina':'Discipline','Sombra':'Shadow','Elemental':'Elemental','Aperfeiçoamento':'Enhancement','Restauração':'Restoration',
  'Arcano':'Arcane','Fogo':'Fire','Gélido':'Frost','Suplício':'Affliction','Demonologia':'Demonology','Destruição':'Destruction',
  'Equilíbrio':'Balance','Combate Feral':'Feral',
  'Desejo de Sobreviver':'Will to Survive','Percepção':'Perception','Ruthless':'Ruthless','O Espírito Humano':'The Human Spirit',
  'Forma de Pedra':'Stoneform','Localizar Tesouros':'Find Treasure','Earth Fury':'Earth Fury','Big Game Hunter':'Big Game Hunter',
  'Luz de Eluna':"Elune’s Light",'Fusão Sombria':'Shadowmeld','Rapidez':'Quickness','Espírito de Fogo-fátuo':'Wisp Spirit',
  'Artista da Fuga':'Escape Artist','Eureca!':'Eureka!','Mente Expansiva':'Expansive Mind','Especialização em Engenharia':'Engineering Specialization',
  'Walk on Air':'Walk on Air','Read Ley Line':'Read Ley Line','Wind Blessed':'Wind Blessed','Elemental Insight':'Elemental Insight','Skysight':'Skysight',
  'Fúria Sangrenta':'Blood Fury','Shatter Curse':'Shatter Curse','Savage':'Savage','Robustez':'Hardiness',
  'Determinação dos Renegados':'Will of the Forsaken','Canibalizar':'Cannibalize','Respiração Subaquática':'Underwater Breathing','Toque do Túmulo':'Touch of the Grave',
  'Pisada de Guerra':'War Stomp','Cultivo':'Cultivation','Vencer Planícies':'Plainsrunning','Resistência':'Endurance',
  'Berserk':'Berserking','Regeneração Rápida':'Rapid Regeneration','Matança de Feras':'Beast Slaying','Regeneração':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Dica</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Aliança' : 'Horda'; }
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Mais rápido em ${-p}%` : p > 0 ? `Mais lento em ${p}%` : 'Ritmo médio';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>mais rápido</span><span>mais lento</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Classe</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Evolução</span><span>Em raides</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Funções: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Raça</span><span>Classes</span><span class="abl">Habilidades <span class="abt">ativa</span><span class="abt p">passiva</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">paga</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Classes: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', nova' : v ? '' : ', indisponível')); }).join('')}</span>
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
  let h = '<thead><tr><th scope="col">Raça</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">paga</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: não permitido"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', nova combinação' : ''}`;
        const mark = v === 'new' && !sel ? '<span class="nw">novo</span>' : '<i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>';
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
    return `<button type="button" data-pc="${c.id}" class="${v ? '' : 'na'}" aria-pressed="${c.id === state.cls}">${esc(c.n)}${v === 'new' ? ' · nova' : ''}</button>`;
  }).join('');
  $('#pickm').innerHTML = `<div><div class="lbl">1. Raça</div><div class="chiprow">${races}</div></div>
    <div><div class="lbl">2. Classe (tracejada: indisponível para esta raça, toque para trocar a raça)</div><div class="chiprow">${cls}</div></div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Ativa' : 'Passiva'}</span><b>${bi(x[1])}</b><span>${esc(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', requer o pacote Skyborne' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><img src="../assets/art/${c.id}-600.webp" width="600" height="804" alt="" loading="lazy" decoding="async"></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}${face(c.id, CCOL[c.id])}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Nova combinação</span>' : ''}${r.paid ? '<span class="tag paid">Raça paga</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Especializações</h4><div class="cards">${specs}</div></div>
        <div><h4>Habilidades raciais</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Evolução</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>Em raides</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Novidades</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Minha escolha">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Copiar minha escolha</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Copiado');
  $('#qPick').textContent = `Agora: ${r.n} · ${c.n}`;
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
  warrior: 'Placas, raiva e a linha de frente. Aguenta os golpes como tanque ou varre tudo com uma arma de duas mãos.',
  paladin: 'Um guerreiro sagrado de placas: cura, tanqueia e brande um martelo. Agora também na Horda.',
  hunter: 'Arco, armadilhas e uma fera leal ao seu lado. Uma das classes que evolui mais rápido.',
  rogue: 'Venenos, lâminas e sombras. Dano puro de emboscada e controle de grupo.',
  priest: 'Luz e Sombra num só par de mãos. O principal curador do grupo ou um conjurador sombrio.',
  shaman: 'Totens e elementos: cura, ataca com raios ou armas. Agora também na Aliança.',
  mage: 'Magia de fogo, gelo e arcana. Portais, comida e água para a turma toda.',
  warlock: 'Maldições, demônios e fogo. Dano ao longo do tempo e um demônio só seu para ajudar.',
  druid: 'Urso, gato, coruja ou curador: as três funções num só personagem.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Mais sobre a classe</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">paga</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">Mais sobre a raça</span></span>
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
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Não foi possível copiar, selecione o texto e pressione Ctrl+C'; }
}

/* Dungeons: [name, min, max, entrance zone, new, other sites' ranges where they differ] */
const DUNGEONS = [
  ['Cavernas Ígneas', 13, 18, 'Orgrimmar', 0, [], 'horde'],
  ['Hall of Thanes', 13, 18, 'Altaforja', 1, [['Icy Veins', '13–20']]],
  ['Ruínas de Lordaeron', 15, 20, 'Clareiras de Tirisfal', 1, [['Icy Veins', '15–22']]],
  ['Minas Mortas', 15, 22, 'Cerro Oeste', 0, [['Icy Veins', '17–26']]],
  ['Caverna Ululante', 17, 24, 'Sertões', 0, [['Icy Veins', '15–24']]],
  ['Bastilha da Presa Negra', 20, 26, 'Floresta de Pinhaprata', 0, [['Icy Veins', '20–30']]],
  ['Profundezas Negras', 22, 28, 'Vale Gris', 0, [['Sportskeeda', '22–26'], ['Icy Veins', '24–32']]],
  ['Excavation Site: Wetlands', 24, 29, 'Pantanal', 1, [['ClassicWoW.gg', '26–31'], ['Icy Veins', '26–33']]],
  ['O Cárcere', 25, 29, 'Ventobravo', 0, [['Icy Veins', '24–32']], 'alliance'],
  ['City of Dalaran', 28, 33, 'Montanhas de Alterac', 1, [['Icy Veins', '28–35']]],
  ['Gnomeregan', 29, 38, 'Dun Morogh', 0],
  ['Urzal dos Tuscos', 29, 38, 'Sertões', 0],
  ['Monastério Escarlate: Cemitério', 30, 38, 'Clareiras de Tirisfal', 0],
  ['Monastério Escarlate: Biblioteca', 33, 41, 'Clareiras de Tirisfal', 0],
  ['The Drowned City', 35, 40, 'Selva do Espinhaço', 1],
  ['Monastério Escarlate: Arsenal', 36, 44, 'Clareiras de Tirisfal', 0],
  ['Uldaman', 36, 45, 'Ermos', 0, [['Icy Veins', '41–51']]],
  ['Urzal dos Mortos', 37, 46, 'Sertões', 0],
  ['Monastério Escarlate: Catedral', 38, 46, 'Clareiras de Tirisfal', 0],
  ["Zul’Farrak", 40, 47, 'Tanaris', 0, [['Icy Veins', '44–54']]],
  ["Krol’dok Stronghold", 40, 45, 'Riverglades', 1],
  ['Maraudon', 45, 51, 'Desolação', 0, [['Icy Veins', '46–55']]],
  ['Alcaz Island Prison', 48, 53, 'Pântano Vadeoso', 1],
  ["Templo de Atal’Hakkar", 50, 55, 'Pântano das Mágoas', 0, [['Icy Veins', '50–60']]],
  ['Abismo Rocha Negra', 52, 60, 'Montanha Rocha Negra', 0],
  ['Blackmaw Hold', 55, 60, 'Azshara', 1],
  ['Pico da Rocha Negra Inferior', 57, 60, 'Montanha Rocha Negra', 0, [['Icy Veins', '55–60']]],
  ['Gládio Cruel: Leste', 58, 60, 'Feralas', 0, [['Icy Veins', '54–60']]],
  ["Shaper’s Terrace", 58, 60, "Cratera Un’Goro", 1],
  ['Stratholme: vivos', 58, 60, 'Terras Pestilentas Orientais', 0],
  ['Stratholme: mortos-vivos', 58, 60, 'Terras Pestilentas Orientais', 0],
  ['Scolomântia', 58, 60, 'Terras Pestilentas Ocidentais', 0],
  ['Pico da Rocha Negra Superior', 60, 60, 'Montanha Rocha Negra', 0, [['Icy Veins', '59–60']]],
  ['Gládio Cruel: Oeste', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]],
  ['Gládio Cruel: Norte', 60, 60, 'Feralas', 0, [['Icy Veins', '56–60']]]
];
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
const facOk = (d, f) => !f || !d[6] || d[6] === f;   // Ragefire Chasm and The Stockade open from a capital

/* Professions: camp object (tier 1) and the class buff it stands in for */
const PROFS = [
  ['alchemy', 'Alquimia', 1, 'Mana Well', 'como Bênção de Sabedoria'],
  ['blacksmithing', 'Ferraria', 1, 'Sharpening Wheel', 'como Totem da Força da Terra'],
  ['enchanting', 'Encantamento', 1, 'Enchanted Lute', 'como Marca do Indomado'],
  ['engineering', 'Engenharia', 1, 'Reagent Bot', 'vendedor de reagentes, reparos no nível 2'],
  ['herbalism', 'Herborismo', 1, 'Incense Candle', 'como Inteligência Arcana'],
  ['leatherworking', 'Couraria', 1, 'Camp Tent', 'mais experiência de descanso'],
  ['mining', 'Mineração', 1, 'Lodestone', 'como Bênção do Poder'],
  ['skinning', 'Esfolamento', 1, 'Camp Chair', 'como Aura de Luniscante'],
  ['tailoring', 'Alfaiataria', 1, 'Faction Banner', 'como Espírito Divino'],
  ['cooking', 'Culinária', 0, 'Basic Campfire', 'mais espaços de objetos no acampamento'],
  ['firstaid', 'Primeiros Socorros', 0, 'First Aid Kit', 'como Palavra de Poder: Fortitude'],
  ['fishing', 'Pesca', 0, 'Fish Bowl', 'como Bênção dos Reis']
];
const PR = Object.fromEntries(PROFS.map(p => [p[0], p]));

/* Game stages: f = fact from the sources, t = our tip */
const SRC = {
  names: ['Icy Veins: reserva de nomes', 'https://www.icy-veins.com/wow-forever/name-reservation'],
  names2: ['Team Overpowered: nomes e sobrenomes', 'https://teamoverpowered.com/forever/guides/name-reservation/'],
  prof: ['Warcraft Tavern: profissões', 'https://www.warcrafttavern.com/forever/guides/professions/'],
  camp: ['Warcraft Tavern: acampamento', 'https://www.warcrafttavern.com/forever/guides/camping/'],
  legacy: ['Blizzard: Legacy', 'https://news.blizzard.com/en-gb/article/24307383'],
  dung: ['Warcraft Tavern: masmorras', 'https://www.warcrafttavern.com/forever/guides/dungeons/'],
  ride: ['Warcraft Tavern: montaria', 'https://www.warcrafttavern.com/forever/guides/riding/'],
  cwg: ['ClassicWoW.gg: datas e raides', 'https://classicwow.gg/forever']
};
const STAGES = [
  { id: 'pre', n: 'Antes do lançamento', sub: 'até 04.11', lo: 0, hi: 0,
    todo: [['f', 'Reserva antecipada de nomes de 27.10 a 03.11 para donos dos pacotes Heroic, Epic e Collection. Quem chegar primeiro leva.'],
      ['f', 'Você pode reservar até três personagens por conta. O personagem tem nome e sobrenome, e o par precisa ser único na região.'],
      ['f', 'A partir de 04.11 é preciso assinatura ou tempo de jogo para jogar.'],
      ['t', 'Escolha três nomes com sobrenomes, mais reservas, antes de 27.10.']],
    dnote: 'As primeiras masmorras abrem no nível 13.',
    prof: [['f', 'Cada personagem tem duas profissões primárias e todas as três secundárias: Culinária, Primeiros Socorros e Pesca.'],
      ['f', 'Cada profissão coloca seu próprio objeto de acampamento com um bônus parecido com um bônus de classe.'],
      ['t', 'Dividam as profissões com antecedência: um de vocês pega Culinária para a fogueira, os outros escolhem profissões diferentes para os bônus do acampamento não se repetirem.']],
    legacy: [['f', 'O Legacy abre com o seu primeiro ponto: nível 25, 150 numa profissão (não de coleta) ou explorar o mapa inteiro.'],
      ['f', 'No lançamento um personagem pode gastar no máximo 16 pontos, o resto vai para a trilha de recompensas.']],
    group: [['t', 'Combinem uma facção e um modo: só dá para formar grupo dentro do mesmo modo, e no PvP a conta tem uma facção.'],
      ['t', 'Monte sua escalação no montador de grupo: um tanque, um curador e classes diferentes para os bônus.']],
    src: ['names', 'names2', 'prof', 'legacy'] },
  { id: 'first', n: 'Primeiros dias', sub: 'níveis 1–15', lo: 1, hi: 15,
    todo: [['f', 'Os Skyborne começam em Zephras Isle, níveis 1–12.'],
      ['f', 'Os talentos abrem no nível 10, ou no 9 com a vantagem de Legacy Talented.'],
      ['f', 'A maioria das comidas preparadas dá bônus de experiência. Acumula com o acampamento e com o Saco de Dormir Aconchegante.'],
      ['t', 'Acumule descanso: deslogue numa estalagem ou num acampamento com barraca.']],
    prof: [['f', 'A fogueira básica não precisa de Culinária e comporta 3 objetos. Ela queima por cerca de 10 minutos, e você pode colocar uma nova depois de 5.'],
      ['f', 'Para receber os bônus do acampamento, sente-se perto (/sit) por pelo menos um minuto.'],
      ['t', 'Pegue uma profissão de coleta desde os primeiros níveis: ervas, minério e couro alimentam a produção, e 150 numa profissão de produção abre o Legacy.']],
    legacy: [['f', 'Ainda sem vantagens: o primeiro ponto vem no nível 25 ou com 150 numa profissão.'],
      ['t', 'Quando o Legacy abrir, pegue primeiro as vantagens de experiência e de acampamento: Well Rested, Field Guide, Permanence. Talented serve para alts.']],
    group: [['t', 'Evoluam na mesma zona e montem acampamento a cada parada: cinco minutos numa fogueira se pagam com bônus para o grupo todo.'],
      ['t', 'Formem seu primeiro grupo de cinco até o nível 13–15.']],
    src: ['camp', 'legacy', 'dung'] },
  { id: 'dung', n: 'Masmorras', sub: 'níveis 15–40', lo: 15, hi: 40,
    todo: [['f', 'A maior parte da experiência de uma masmorra vem das suas cadeias de missões. Repetir depois delas dá bem menos experiência do que fazer missões pelo mundo.'],
      ['f', 'Cada item que cai desbloqueia a aparência de transmog para todos que podem usá-lo, mesmo que outra pessoa tenha ficado com o item.'],
      ['f', 'O Legacy abre no nível 25.'],
      ['t', 'Peguem primeiro as missões da masmorra em grupo e entrem quando todos as tiverem.']],
    prof: [['f', 'Culinária 140 dá 5 espaços no acampamento, 220 dá 10.'],
      ['f', 'Cada profissão faz três objetos de acampamento, um por nível. As fontes divergem sobre a perícia necessária para os níveis 2 e 3.'],
      ['t', 'Se o nível 25 ainda está longe, leve uma profissão de produção a 150: o Legacy abre antes.']],
    legacy: [['f', 'Cada desafio dá 1 ponto. São 65: classes 27, profissões 18, PvP 12, masmorras 3, raides 3, aventura 2.'],
      ['t', 'Reagent Economy (sem reagentes comprados para habilidades) e Field Guide (recarga menor dos objetos de acampamento) valem a pena.']],
    group: [['f', 'Uma masmorra é feita para 5 jogadores: um tanque, um curador e três de dano.'],
      ['f', 'Não há ajuste de nível, então um amigo muito atrás vai sofrer na masmorra.'],
      ['t', 'Mantenham os níveis próximos: quem ficar para trás recupera com missões, e vocês fazem masmorras juntos.']],
    src: ['dung', 'camp', 'legacy'] },
  { id: 'path', n: 'Rumo ao 60', sub: 'níveis 40–60', lo: 40, hi: 60,
    todo: [['f', 'Montaria no nível 40 (60% de velocidade), uma rápida no 60 (100%). Treine com o instrutor da sua raça.'],
      ['f', 'Paladinos e bruxos conseguem a montaria por missões de classe.'],
      ['f', 'Honrado com a sua própria facção dá 10% de desconto no treino de montaria e nas montarias. Segundo a Warcraft Tavern: 100 + 20 de ouro no nível 40, 1.000 + 200 no 60.'],
      ['t', 'Guarde ouro para o nível 40: a montaria será seu maior gasto no caminho até o 60.']],
    prof: [['f', 'Cada profissão tem seus próprios objetos de acampamento de nível 2 e 3. O segundo objeto da Engenharia, Robô de Conserto, conserta o equipamento.'],
      ['t', 'Mantenham Culinária 220 no grupo para um acampamento de 10 objetos: na hora das raides haverá espaço para todos.']],
    legacy: [['f', 'No máximo 16 pontos por personagem, o resto vai para a trilha de recompensas: um brinquedo com 15, um mascote com 25, um tabardo com 40, uma montaria com 55.']],
    group: [['f', 'As raides abrem em 09.12: Barrow Deeps para 10 jogadores, Pico Hyjal para 20, Covil da Onyxia para 40.'],
      ['t', 'A raide de 10 jogadores precisa de 10 jogadores: se vocês forem menos, encontrem o resto na guilda com antecedência.']],
    src: ['ride', 'prof', 'legacy', 'cwg'] },
  { id: 'raid', n: '60 e raides', sub: 'a partir de 09.12', lo: 60, hi: 60,
    todo: [['f', 'Em 09.12 abrem Barrow Deeps (10 jogadores), Pico Hyjal (20) e Covil da Onyxia (40, Pântano Vadeoso).'],
      ['f', 'Concluir cada uma das três raides dá um ponto de Legacy.'],
      ['f', 'Novo campo de batalha 15x15: Darkspear Islands, na costa do Pântano Vadeoso.'],
      ['t', 'Enquanto juntam gente para a raide, façam masmorras de nível 60 para equipamento.']],
    prof: [['f', 'Os bônus do acampamento são um pouco mais fracos que os de classe e não se acumulam com eles: Bênção dos Reis dá 10% a todos os atributos, o acampamento dá 8%.'],
      ['t', 'Montem acampamento na entrada da raide: os bônus cobrem o que falta nas suas classes.']],
    legacy: [['f', 'Desafios para o nível 60: masmorras 3, raides 3, PvP 12. O PvP tem patentes com limite semanal e melhorias de equipamento por Honra.']],
    group: [['f', 'Os mesmos bônus de dois jogadores da mesma classe se sobrepõem, classes diferentes se acumulam.'],
      ['t', 'Monte a escalação da raide no montador de grupo e poste o link no chat.']],
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
  if (now < D_REL) return ['pre', 'Escolhida pela data: antes do lançamento de 04.11.'];
  if (me.lvl) return [me.lvl < 15 ? 'first' : me.lvl < 40 ? 'dung' : me.lvl < 60 ? 'path' : 'raid', 'Escolhida pelo nível do seu personagem.'];
  if (now >= D_RAID) return ['raid', 'Escolhida pela data: as raides estão abertas.'];
  return [now < new Date('2026-11-11T00:00:00') ? 'first' : 'dung', 'Escolhida pela data. Adicione o nível do seu personagem e a etapa vai acompanhá-lo.'];
}
const START = { pre: 'hero_dawn-960', first: 'hero_campfire-960', dung: 'warlock-360', path: 'hunter-360', raid: 'paladin-360' };
const ARTV = /*ARTV*/{"hero_campfire-960.avif":"?v=2654726f","hero_campfire-960.webp":"?v=d73f1e16","hero_dawn-960.avif":"?v=72b3acf6","hero_dawn-960.webp":"?v=4eae2c5c"};   // ?v= of the scene arts, filled in by build.art_version (same names, redrawn pictures)
const pic = f => `<picture><source type="image/avif" srcset="${ROOT}assets/art/${f}.avif${ARTV[f + '.avif'] || ''}"><img src="${ROOT}assets/art/${f}.webp${ARTV[f + '.webp'] || ''}" alt="" loading="lazy" decoding="async"></picture>`;
const tipL = () => '<span class="tl">Dica</span>';
function liC(x) { return x[0] === 't' ? `<li class="tip">${tipL()}${esc(x[1])}</li>` : `<li>${esc(x[1])}</li>`; }
function dLi(d) {
  const mine = me.lvl && nearLvl(d, me.lvl);
  return `<li class="${mine ? 'mine' : ''}"><b>${esc(d[0])}</b><span class="lvl${mine ? ' gold' : ''}">${lvRange(d)}</span><span class="z">${esc(d[3])}${d[4] ? ' · <i>novo</i>' : ''}${mine ? '<span class="sr"> · para o seu nível</span>' : ''}</span></li>`;
}
function renderStage() {
  const [auto, why] = autoStage();
  if (stageAuto) stageSel = auto;
  const s = ST[stageSel];
  $('#stageBar').innerHTML = STAGES.map(x => `<button type="button" class="stile" role="tab" id="tab-${x.id}" data-st="${x.id}" aria-controls="stagePanel" aria-selected="${x.id === stageSel}" tabindex="${x.id === stageSel ? 0 : -1}">${pic(START[x.id])}<b>${esc(x.n)}</b><span class="lv">${esc(x.sub)}${x.id === auto ? ' · <span class="now">agora</span>' : ''}</span></button>`).join('');
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
  $('#stagePanel').innerHTML = `<div class="st-head"><div class="t"><h3>${esc(s.n)}</h3><span class="when">${esc(s.sub)}</span></div><p class="why">${stageAuto ? esc(why) : 'Etapa escolhida manualmente.'}</p></div>
    <ol class="steps-c">${steps}</ol>
    <div class="st-cols">
      <div><h4>Masmorras para este nível</h4>${s.dnote ? `<p class="small" style="margin:-4px 0 10px">${esc(s.dnote)}</p>` : ''}<ul class="dlist">${ds.slice(0, MAXD).map(dLi).join('')}</ul>
        <a class="more-l" href="guides/dungeons/">${extra > 0 ? `Mais masmorras na tabela: ${extra}` : 'Todas as 35 masmorras'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
      <div style="display:grid;gap:24px;align-content:start"><div><h4>Profissões e acampamento</h4><ul class="clean">${s.prof.map(liC).join('')}</ul></div>
        <div><h4>Vantagens de Legacy</h4><ul class="clean">${s.legacy.map(liC).join('')}</ul></div></div>
    </div>
    <div class="gtip"><h4 style="margin:0 0 10px;font-size:1.02rem">Dicas para o grupo</h4><ul class="clean">${s.group.map(liC).join('')}</ul></div>
    <p class="st-src"><span>Fontes:</span>${s.src.map(k2 => `<a href="${SRC[k2][1]}" target="_blank" rel="noopener">${esc(SRC[k2][0])}</a>`).join('')}</p>`;
}
function optList(items, cur, none) { return `<option value="">${esc(none)}</option>` + items.map(([v, t]) => `<option value="${v}"${v === cur ? ' selected' : ''}>${esc(t)}</option>`).join(''); }
function renderMe() {
  fixMe();
  const races = f => RACES.filter(r => r.f === f).map(r => `<option value="${r.id}"${r.id === me.race ? ' selected' : ''}>${esc(r.n)}</option>`).join('');
  $('#meRace').innerHTML = `<option value="">Não escolhido</option><optgroup label="${facName('alliance')}">${races('alliance')}</optgroup><optgroup label="${facName('horde')}">${races('horde')}</optgroup>`;
  const cls = (me.race ? Object.keys(RC[me.race].can) : CLASSES.map(c => c.id)).map(id => [id, CL[id].n]);
  $('#meCls').innerHTML = optList(cls, me.cls, 'Não escolhido');
  $('#meRole').innerHTML = me.cls ? roleOpts(CL[me.cls]).map(x => `<option value="${x}"${x === me.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('') : `<option value="">Escolha uma classe primeiro</option>`;
  $('#meRole').disabled = !me.cls;
  const prim = PROFS.filter(p => p[2]);
  $('#meP1').innerHTML = optList(prim.filter(p => p[0] !== me.p2).map(p => [p[0], p[1]]), me.p1, 'Nenhum');
  $('#meP2').innerHTML = optList(prim.filter(p => p[0] !== me.p1).map(p => [p[0], p[1]]), me.p2, 'Nenhum');
  $('#meSec').innerHTML = PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${me.sec.includes(p[0])}">${esc(p[1])}</button>`).join('');
  document.querySelectorAll('.lvin').forEach(i => { if (document.activeElement !== i) i.value = me.lvl || ''; });
  const who = [me.race ? RC[me.race].n : '', me.cls ? CL[me.cls].n : ''].filter(Boolean).join(' · ');
  const sub = me.cls ? [ROLE_RU[me.role], me.race ? facName(RC[me.race].f) : ''].filter(Boolean).join(' · ') : 'Escolha raça, classe e nível abaixo';
  const hero = $('#meHero');
  hero.style.setProperty('--cc', me.cls ? CCOL[me.cls] : '#c9a54a');
  hero.innerHTML = pic(me.cls ? `${me.cls}-600` : 'hero_campfire-960') + (me.lvl ? `<span class="lvb" aria-label="Nível ${me.lvl}">${me.lvl}</span>` : '')
    + `<span class="k">Meu personagem</span><b>${who ? esc(who) : 'Ainda não criado'}</b><span class="s">${esc(sub)}</span>`;
  let out = '';
  if (meSet()) {
    const b = [];
    if (me.cls) b.push(BUFF[me.cls] ? `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span><b>${esc(CL[me.cls].n)}:</b> ${esc(BUFF[me.cls])}</span></li>` : `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-dps"/></svg></span><span>${esc(CL[me.cls].n)}: sem bônus de grupo, dano puro.</span></li>`);
    [me.p1, me.p2, ...me.sec].filter(Boolean).forEach(id => { const p = PR[id]; b.push(`<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg></span><span><b>${esc(p[3])}</b> <span class="m">· ${esc(p[1])}</span><br>${esc(p[4])}</span></li>`); });
    if (!b.length) b.push('<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span>Escolha uma classe e profissões para ver seus bônus.</span></li>');
    out += `<div><h4>O que você traz para o grupo</h4><ul class="buffs">${b.join('')}</ul></div>`;
    if (me.lvl) {
      const ds = DUNGEONS.filter(d => nearLvl(d, me.lvl) && facOk(d, me.race && RC[me.race].f));
      out += `<div><h4>Masmorras para o seu nível</h4>` + (ds.length ? `<ul class="dlist">${ds.slice(0, 4).map(dLi).join('')}</ul>` : '<p class="small">As primeiras masmorras começam no nível 13.</p>')
        + `<a class="more-l" href="guides/dungeons/">${ds.length > 4 ? `Mais masmorras na tabela: ${ds.length - 4}` : 'Tabela de masmorras'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`;
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
