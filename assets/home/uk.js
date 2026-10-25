const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Воїн', s:'Воїн', roles:['tank','dps'],
    specs:[['Зброя','Шкода в ближньому бою (дворучна зброя)',['dps']],['Лють','Шкода в ближньому бою (дві зброї)',['dps']],['Захист','Танк',['tank']]],
    lvl:'Найповільніше прокачування, приблизно на 12% довше за середнє',
    lp:12,
    raid:'Бойовий клич діє на весь рейд',
    forever:'Більше Люті, краща загроза по групі цілей, талант Майстер зброї. Лють і Жага крові послаблені.' },
  { id:'paladin', n:'Паладин', roles:['tank','heal','dps'],
    specs:[['Світло','Цілитель',['heal']],['Захист','Танк',['tank']],['Відплата','Шкода в ближньому бою',['dps']]],
    lvl:'Середній темп прокачування',
    lp:0,
    raid:'Благословення королів тепер базове. За бета-списками Захист серед найсильніших танків, Відплата просіла після патча 15 жовтня.',
    forever:'Священний удар з 6 рівня, Правосуддя не витрачає печатку. Нежить тепер може бути паладином, отже клас з’явився в Орді.' },
  { id:'hunter', n:'Мисливець', roles:['dps'],
    specs:[['Володіння звірами','Шкода здалеку, багато шкоди від улюбленця',['dps']],['Стрільба','Шкода здалеку',['dps']],['Виживання','Ближній і дальній бій, пастки',['dps']]],
    lvl:'Найшвидше прокачування, приблизно на 8% швидше за середнє',
    lp:-8,
    raid:'Аура влучного стрільця діє на весь рейд',
    forever:'Можна грати без улюбленця, пастки працюють у бою, з’явилися лисиці як родина улюбленців. Виживання може йти в ближній бій.' },
  { id:'rogue', n:'Розбійник', roles:['dps'],
    specs:[['Ліквідація','Шкода отрутами',['dps']],['Бій','Швидкі атаки зброєю',['dps']],['Непомітність','Засідки, кровотечі',['dps']]],
    lvl:'Середній темп прокачування',
    lp:0,
    raid:'Чиста шкода в ближньому бою без баффів на весь рейд',
    forever:'Тепер можна використовувати одноручні сокири. Ліквідація будується на отрутах, Непомітність на кровотечах і невидимості.' },
  { id:'priest', n:'Жрець', roles:['heal','dps'],
    specs:[['Послух','Цілитель, щити та поглинання',['heal']],['Світло','Цілитель',['heal']],['Темрява','Шкода здалеку',['dps']]],
    lvl:'Приблизно на 5% повільніше за середнє',
    lp:5,
    raid:'Божественний дух став базовим. Шкоду Темряви та «Пожираючу чуму» (відновлення 24 сек) підсилено патчем 15 жовтня.',
    forever:'Захист від страху та «Пожираюча чума» доступні з 20 рівня будь-якій расі. У кожної раси по два своїх закляття жерця.' },
  { id:'shaman', n:'Шаман', roles:['heal','dps','tank?'],
    specs:[['Стихії','Шкода здалеку',['dps']],['Вдосконалення','Шкода в ближньому бою. Можливість танкувати поки під питанням',['dps','tank?']],['Зцілення','Цілитель',['heal']]],
    lvl:'Середній темп прокачування',
    lp:0,
    raid:'Тотеми сили землі, несамовитості вітру, язиків полум’я та грації повітря підсилюють свою групу',
    forever:'Дворфи тепер можуть бути шаманами, отже клас з’явився в Альянсі. Сплеск лави підсилено, Стихії піднялися в списках шкоди.' },
  { id:'mage', n:'Маг', roles:['dps'],
    specs:[['Тайна магія','Бурст, багато мани',['dps']],['Вогонь','Криті та підпали',['dps']],['Лід','Шкода і контроль',['dps']]],
    lvl:'Найшвидше прокачування, приблизно на 8% швидше за середнє (близько 12 годин економії)',
    lp:-8,
    raid:'Портали та їжа з водою для всієї компанії',
    forever:'Вогонь отримав Hotstreak, Тайна магія — Arcane Blast, Лід — Крижаний спис. Вогняно-крижана стріла доступна з 40 рівня.' },
  { id:'warlock', n:'Чорнокнижник', roles:['dps'],
    specs:[['Прокляття','Шкода від прокляттів і псування',['dps']],['Демонологія','Шкода через демонів',['dps']],['Руйнування','Пряма шкода вогнем і темрявою',['dps']]],
    lvl:'Середній темп прокачування',
    lp:0,
    raid:'Майстерність темряви тепер дає 2–10% шкоди від темряви (було 1–5%)',
    forever:'У Прокляття нове закляття з наведенням, демон лишається при Жертві демона, у Руйнування з’явилися Спалення та AoE.' },
  { id:'druid', n:'Друїд', roles:['tank','heal','dps'],
    specs:[['Баланс','Шкода здалеку',['dps']],['Сила звіра','Танк (ведмідь) і шкода в ближньому бою (кішка)',['tank','dps']],['Зцілення','Цілитель, багато лікування з часом',['heal']]],
    lvl:'Приблизно на 5% повільніше за середнє',
    lp:5,
    raid:'Ватажок зграї та аура місячного совиця діють на весь рейд і складаються',
    forever:'Кожна спеціалізація отримала чітку роль, форми працюють із зіллями та чарами на зброї. Можна бути танком, цілителем і бійцем на одному персонажі.' }
];
const ROLE_RU = { tank:'Танк', heal:'Цілитель', dps:'Шкода', 'tank?':'Танк (під питанням)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Бойовий клич', paladin:'Благословення королів', hunter:'Аура влучного стрільця', priest:'Power Word: Fortitude, Божественний дух', shaman:'Тотеми (сила землі, несамовитість вітру, язики полум’я, грація повітря)', mage:'Arcane Intellect, портали, їжа та вода', druid:'Mark of the Wild, Ватажок зграї, аура місячного совиця' };

const RACES = [
  { id:'human', n:'Людина', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Воля до життя','Знімає приголомшення'],['a','Уважність','Показує невидимих ворогів на 20 сек'],['p','Безжальність','+2% шанс крита'],['p','Людський дух','+5% до духу']],
    tip:'Дух іде в лікування Жрецю Світла, тож Людина-жрець добра для цілителя.' },
  { id:'dwarf', n:'Дворф', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Кам’яна форма','Імунітет до кровотеч, отрут і хвороб на 8 сек і зниження фізичної шкоди'],['a','Пошук скарбів','Показує скрині поруч'],['p','Лють землі','+2% до шкоди крита та сили лікування'],['p','Мисливець на велику дичину','+5% шкоди по звірах']],
    tip:'Кам’яна форма корисна танку й у PvP.' },
  { id:'nightelf', n:'Нічний ельф', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Світло Елуни','+10% до шансу крита на 15 сек'],['a','Злиття з тінню','Невидимість на місці'],['p','Спритність','+1% до ухилення та +2% до швидкості бігу'],['p','Дух-вогник','+75% до швидкості бігу у вигляді духу']],
    tip:'Єдина раса Альянсу з друїдом, якщо не брати Скайборн.' },
  { id:'gnome', n:'Гном', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Майстер втечі','Короткий імунітет до уповільнення та коренів'],['a','Еврика!','Наступні 3 здібності дешевші й на 10% сильніші'],['p','Допитливий розум','+5% до максимуму мани, люті або енергії'],['p','Спеціалізація: інженерія','Інженерні пристрої спрацьовують надійніше']],
    tip:'Допитливий розум особливо виручає класам на енергії.' },
  { id:'skyA', n:'Скайборн (Альянс)', f:'alliance', paid:true, name:'Високий скайборн',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Ходіння повітрям','Планування вниз 10 сек, немає шкоди від падіння'],['a','Читання лей-ліній','+100% до відновлення здоров’я та мани'],['p','Благословення вітру','+3% до швидкості атаки та заклять'],['p','Прозріння стихій','+5% шкоди по елементалях']],
    tip:'Платна раса: набір Heroic Pack від $29.99. Старт у локації Zephras Isle (1–12 рівні).' },
  { id:'orc', n:'Орк', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Кривава лють','+10% до сили атаки та заклять на 15 сек'],['a','Руйнування прокляттів','Знімає прокляття і псування, магічна шкода по вас −5% на 8 сек'],['p','Дикість','+1% шанс крита'],['p','Загартування','Приголомшення коротші на 20%']],
    tip:'Кривава лють дає потужне вікно шкоди.' },
  { id:'undead', n:'Нежить', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Воля Відрікшихся','Знімає зачарування, страх і сон'],['a','Канібалізм','Відновлює 35% здоров’я та мани з часом'],['p','Підводне дихання','Дихання під водою довше'],['p','Дотик могили','Шанс висмоктати здоров’я під час атаки']],
    tip:'Нова комбінація: паладин в Орді, де раніше цього класу не було.' },
  { id:'tauren', n:'Таурен', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Тупіт війни','Приголомшує ворогів поруч на 2 сек'],['a','Культивація','Вирощує трави, які можна зібрати без травництва'],['p','Біг рівнинами','Швидкість росте, поки ви біжите'],['p','Витривалість','+5% здоров’я та +2% до шкоди крита']],
    tip:'Єдина раса Орди з друїдом, якщо не брати Скайборн.' },
  { id:'troll', n:'Троль', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Берсерк','+10% до швидкості атаки та заклять на 10 сек'],['a','Швидке відновлення','Відновлює здоров’я з часом'],['p','Убивця звірів','+5% шкоди по звірах'],['p','Регенерація','Здоров’я відновлюється і в бою']],
    tip:'Найбільше варіантів класів в Орді: сім.' },
  { id:'skyH', n:'Скайборн (Орда)', f:'horde', paid:true, name:'Скайборн-вітрорізь',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Ходіння повітрям','Планування вниз 10 сек, немає шкоди від падіння'],['a','Погляд у небо','+10% до швидкості бігу'],['p','Благословення вітру','+3% до швидкості атаки та заклять'],['p','Прозріння стихій','+5% шкоди по елементалях']],
    tip:'Платна раса: набір Heroic Pack від $29.99. Шаманом може бути лише Орда, магом лише Альянс.' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "Найчисленніша раса Альянсу. Універсальна й сильна в PvP завдяки Will to Survive.", "dwarf": "Міцні гірники та стрільці Ironforge. Уперше в Classic Альянс має шаманів, і це дворфи.", "nightelf": "Давній народ лісів. Невловимі: власний спосіб сховатися, ухилення та швидкий біг.", "gnome": "Винахідники Gnomeregan. Маленькі, хитрі й з найкращою здібністю втечі в грі.", "skyA": "Нова раса Forever. Вищий орден: ельфи вітру, які шукають втрачену таємну магію предків.", "orc": "Серце Орди. Найсильніші воїни та майстри PvP завдяки Blood Fury і Hardiness.", "undead": "Відреклі: колишні люди, що вирвалися з-під влади Короля-ліча. Не бояться страху та сну.", "tauren": "Мирні велетні рівнин. Найбільше здоров’я та власний масовий оглушливий удар.", "troll": "Плем’я Darkspear. Найбільше класів в Орді та сильний Berserking для шкоди.", "skyH": "Нова раса Forever. Вітрорізи: духовні лідери скайборнів, близькі до стихій."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Зброя':'Arms','Лють':'Fury','Захист':'Protection','Світло':'Holy','Відплата':'Retribution',
  'Володіння звірами':'Beast Mastery','Стрільба':'Marksmanship','Виживання':'Survival',
  'Ліквідація':'Assassination','Бій':'Combat','Непомітність':'Subtlety',
  'Послух':'Discipline','Темрява':'Shadow','Стихії':'Elemental','Вдосконалення':'Enhancement','Зцілення':'Restoration',
  'Тайна магія':'Arcane','Вогонь':'Fire','Лід':'Frost','Прокляття':'Affliction','Демонологія':'Demonology','Руйнування':'Destruction',
  'Баланс':'Balance','Сила звіра':'Feral',
  'Воля до життя':'Will to Survive','Уважність':'Perception','Безжальність':'Ruthless','Людський дух':'The Human Spirit',
  'Кам’яна форма':'Stoneform','Пошук скарбів':'Find Treasure','Лють землі':'Earth Fury','Мисливець на велику дичину':'Big Game Hunter',
  'Світло Елуни':"Elune’s Light",'Злиття з тінню':'Shadowmeld','Спритність':'Quickness','Дух-вогник':'Wisp Spirit',
  'Майстер втечі':'Escape Artist','Еврика!':'Eureka!','Допитливий розум':'Expansive Mind','Спеціалізація: інженерія':'Engineering Specialization',
  'Ходіння повітрям':'Walk on Air','Читання лей-ліній':'Read Ley Line','Благословення вітру':'Wind Blessed','Прозріння стихій':'Elemental Insight','Погляд у небо':'Skysight',
  'Кривава лють':'Blood Fury','Руйнування прокляттів':'Shatter Curse','Дикість':'Savage','Загартування':'Hardiness',
  'Воля Відрікшихся':'Will of the Forsaken','Канібалізм':'Cannibalize','Підводне дихання':'Underwater Breathing','Дотик могили':'Touch of the Grave',
  'Тупіт війни':'War Stomp','Культивація':'Cultivation','Біг рівнинами':'Plainsrunning','Витривалість':'Endurance',
  'Берсерк':'Berserking','Швидке відновлення':'Rapid Regeneration','Убивця звірів':'Beast Slaying','Регенерація':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Порада</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Альянс' : 'Орда'; }
const PV = /*PV*/'?v=6e06af80';   // ?v= of the class and race portraits, filled in by build.art_version (redrawn under the same names)
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="../assets/art/${id}-face.webp${PV}" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Швидше на ${-p}%` : p > 0 ? `Повільніше на ${p}%` : 'Середній темп';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>швидше</span><span>повільніше</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Клас</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Прокачування</span><span>У рейді</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('../assets/art/${c.id}-360.webp${PV}')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Ролі: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Раса</span><span>Класи</span><span class="abl">Здібності <span class="abt">активна</span><span class="abt p">пасивна</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('../assets/art/${RSLUG[r.id]}-360.webp${PV}')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">платна</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Класи: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', нове' : v ? '' : ', недоступно')); }).join('')}</span>
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
  let h = '<thead><tr><th scope="col">Раса</th>';
  CLASSES.forEach(c => { h += `<th scope="col" class="${roleMatch(c, state.r) ? '' : 'dim'}${c.id === state.cls ? ' selc' : ''}">${face(c.id, CCOL[c.id])}${esc(c.n)}</th>`; });
  h += '</tr></thead><tbody>';
  ['alliance', 'horde'].forEach(f => {
    const rows = RACES.filter(r => r.f === f && raceVisible(r));
    if (!rows.length) return;
    h += `<tr class="fh ${f}"><th colspan="${CLASSES.length + 1}" scope="rowgroup"><span class="f ${f}"></span>${facName(f)}</th></tr>`;
    rows.forEach(r => {
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">платна</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: не можна"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', нова комбінація' : ''}`;
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
    return `<button type="button" data-pc="${c.id}" class="${v ? '' : 'na'}" aria-pressed="${c.id === state.cls}">${esc(c.n)}${v === 'new' ? ' · нове' : ''}</button>`;
  }).join('');
  $('#pickm').innerHTML = `<div><div class="lbl">1. Раса</div><div class="chiprow">${races}</div></div>
    <div><div class="lbl">2. Клас (пунктиром: цій расі недоступний, натисніть, щоб змінити расу)</div><div class="chiprow">${cls}</div></div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Активна' : 'Пасивна'}</span><b>${bi(x[1])}</b><span>${esc(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', потрібен набір Скайборн' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><img src="../assets/art/${RSLUG[r.id]}-600.webp${PV}" width="600" height="804" alt="" loading="lazy" decoding="async"></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}${face(c.id, CCOL[c.id])}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Нова комбінація</span>' : ''}${r.paid ? '<span class="tag paid">Платна раса</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Спеціалізації</h4><div class="cards">${specs}</div></div>
        <div><h4>Расові здібності</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Прокачування</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>У рейді</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Що нового</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Мій вибір">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Скопіювати мій вибір</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Скопійовано');
  $('#qPick').textContent = `Зараз: ${r.n} · ${c.n}`;
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
  warrior: 'Лати, лють і перший ряд. Тримає удар як танк або рубає дворучною зброєю.',
  paladin: 'Святий воїн у латах: лікує, танкує й б’є молотом. Тепер є й в Орді.',
  hunter: 'Лук, пастки й вірний звір поруч. Один із найшвидших класів у прокачці.',
  rogue: 'Отрути, клинки й тінь. Чиста шкода із засідки та контроль ворогів.',
  priest: 'Світло й Темрява в одних руках. Головний цілитель групи або темний заклинач.',
  shaman: 'Тотеми й стихії: лікує, б’є блискавкою або зброєю. Тепер є й в Альянсу.',
  mage: 'Вогонь, лід і таємна магія. Портали, їжа й вода для всієї компанії.',
  warlock: 'Прокляття, демони й вогонь. Шкода з часом і власний демон на допомогу.',
  druid: 'Ведмідь, кіт, сова або цілитель: усі три ролі на одному персонажі.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext}${PV} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Докладніше про клас</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp${PV}" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">платна</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">Детальніше про расу</span></span>
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
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Не вдалося скопіювати, виділіть і натисніть Ctrl+C'; }
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
  ['alchemy', 'Алхімія', 1, 'Mana Well', 'як Благословення мудрості'],
  ['blacksmithing', 'Ковальство', 1, 'Sharpening Wheel', 'як Тотем сили землі'],
  ['enchanting', 'Зачарування', 1, 'Enchanted Lute', 'як Знак дикої природи'],
  ['engineering', 'Інженерія', 1, 'Reagent Bot', 'торговець реагентами, на 2 рівні ремонт'],
  ['herbalism', 'Травництво', 1, 'Incense Candle', 'як Чародійський інтелект'],
  ['leatherworking', 'Шкіряництво', 1, 'Camp Tent', 'більше досвіду від відпочинку'],
  ['mining', 'Гірництво', 1, 'Lodestone', 'як Благословення могутності'],
  ['skinning', 'Знімання шкур', 1, 'Camp Chair', 'як аура місячного совуха'],
  ['tailoring', 'Кравецтво', 1, 'Faction Banner', 'як Божественний дух'],
  ['cooking', 'Кулінарія', 0, 'Basic Campfire', 'більше місць для об’єктів у таборі'],
  ['firstaid', 'Перша допомога', 0, 'First Aid Kit', 'як Слово сили: Стійкість'],
  ['fishing', 'Рибальство', 0, 'Fish Bowl', 'як Благословення королів']
];
const PR = Object.fromEntries(PROFS.map(p => [p[0], p]));

/* Game stages: f = fact from the sources, t = our tip */
const SRC = {
  names: ['Icy Veins: резерв імен', 'https://www.icy-veins.com/wow-forever/name-reservation'],
  names2: ['Team Overpowered: імена та прізвища', 'https://teamoverpowered.com/forever/guides/name-reservation/'],
  prof: ['Warcraft Tavern: професії', 'https://www.warcrafttavern.com/forever/guides/professions/'],
  camp: ['Warcraft Tavern: табір', 'https://www.warcrafttavern.com/forever/guides/camping/'],
  legacy: ['Blizzard: Legacy', 'https://news.blizzard.com/en-gb/article/24307383'],
  dung: ['Warcraft Tavern: підземелля', 'https://www.warcrafttavern.com/forever/guides/dungeons/'],
  ride: ['Warcraft Tavern: верхова їзда', 'https://www.warcrafttavern.com/forever/guides/riding/'],
  cwg: ['ClassicWoW.gg: дати та рейди', 'https://classicwow.gg/forever']
};
const STAGES = [
  { id: 'pre', n: 'До старту', sub: 'до 04.11', lo: 0, hi: 0,
    todo: [['f', 'Рання резервація імен 27.10 – 03.11 для власників наборів Heroic, Epic і Collection. Хто перший прийшов, той і зайняв.'],
      ['f', 'Можна зайняти до трьох персонажів на акаунт. Персонаж має ім’я та прізвище, унікальним має бути їхнє поєднання в межах регіону.'],
      ['f', 'З 04.11 для гри потрібна підписка або ігровий час.'],
      ['t', 'Придумайте по три імені з прізвищем і запасні варіанти до 27.10.']],
    dnote: 'Перші підземелля доступні з 13 рівня.',
    prof: [['f', 'На персонажа дві основні професії та всі три допоміжні: Кулінарія, Перша допомога і Риболовля.'],
      ['f', 'Кожна професія ставить у табір свій об’єкт із бафом, схожим на баф класу.'],
      ['t', 'Розподіліть професії заздалегідь: один бере Кулінарію заради багаття, решта різні, щоб бафи табору не повторювалися.']],
    legacy: [['f', 'Legacy відкривається з першим очком: 25 рівень, 150 у професії (не збирання) або дослідження всієї мапи.'],
      ['f', 'На старті на персонажа можна витратити не більше 16 очок, зайві йдуть у трек нагород.']],
    group: [['t', 'Домовтеся про одну фракцію та один режим: групуватися можна лише всередині режиму, а в PvP на акаунті одна фракція.'],
      ['t', 'Зберіть склад у конструкторі: танк, цілитель і різні класи заради бафів.']],
    src: ['names', 'names2', 'prof', 'legacy'] },
  { id: 'first', n: 'Перші дні', sub: 'рівні 1–15', lo: 1, hi: 15,
    todo: [['f', 'Скайборн починають на острові Zephras Isle, це рівні 1–12.'],
      ['f', 'Таланти відкриваються з 10 рівня, з перком Legacy Talented з 9 (на 5 рангах з 5).'],
      ['f', 'Більшість готової їжі дає бонус до досвіду. Він складається з табором і спальником Cozy Sleeping Bag.'],
      ['t', 'Накопичуйте відпочинок: виходьте з гри в таверні або біля табору з наметом.']],
    prof: [['f', 'Базове багаття доступне без Кулінарії і вміщає 3 об’єкти. Горить близько 10 хвилин, поставити нове можна через 5.'],
      ['f', 'Щоб отримати бафи табору, сядьте поруч (/sit) хоча б на хвилину.'],
      ['t', 'Беріть збирання з перших рівнів: трави, руда і шкури знадобляться ремеслу, а 150 у ремеслі відкриває Legacy.']],
    legacy: [['f', 'Перків поки немає: перше очко дасть 25 рівень або 150 у професії.'],
      ['t', 'Коли відкриється Legacy, першими беріть перки досвіду та табору: Well Rested, Field Guide, Permanence. Talented знадобиться твінкам.']],
    group: [['t', 'Качайтеся в одній зоні й ставте табір на привалі: п’ять хвилин на багаття окупаються бафами на всю групу.'],
      ['t', 'Збирайтеся в першу п’ятірку до 13–15 рівня.']],
    src: ['camp', 'legacy', 'dung'] },
  { id: 'dung', n: 'Підземелля', sub: 'рівні 15–40', lo: 15, hi: 40,
    todo: [['f', 'Основний досвід за підземелля дають його ланцюжки завдань. Повторні заходи після них дають помітно менше досвіду, ніж завдання у світі.'],
      ['f', 'Будь-яка річ, що випала, відкриває свій вигляд для трансмогрифікації всім, хто може її вдягнути, навіть якщо річ дісталася іншому.'],
      ['f', 'На 25 рівні відкривається Legacy.'],
      ['t', 'Зберіть завдання підземелля всією групою заздалегідь і йдіть, коли вони є в кожного.']],
    prof: [['f', 'Кулінарія 140 дає 5 місць у таборі, 220 дає 10.'],
      ['f', 'Кожна професія робить три об’єкти табору, по одному на рівень. Навичка для 2 і 3 рівня у джерел розходиться.'],
      ['t', 'Якщо до 25 рівня далеко, доведіть ремесло до 150: Legacy відкриється раніше.']],
    legacy: [['f', 'Кожне випробування дає 1 очко. Усього їх 65: класи 27, професії 18, PvP 12, підземелля 3, рейди 3, пригоди 2.'],
      ['t', 'Цінні Reagent Economy (без купованих реагентів для здібностей) і Field Guide (коротший відкат об’єктів табору).']],
    group: [['f', 'Підземелля розраховане на 5 гравців: танк, цілитель і троє зі шкодою.'],
      ['f', 'Масштабування рівнів немає, тому другові, що сильно відстав, у підземеллі буде важко.'],
      ['t', 'Тримайте рівні близько: ті, хто відстав, наздоганяють на завданнях, підземелля проходьте разом.']],
    src: ['dung', 'camp', 'legacy'] },
  { id: 'path', n: 'Шлях до 60', sub: 'рівні 40–60', lo: 40, hi: 60,
    todo: [['f', 'Скакун з 40 рівня (швидкість 60%), швидкий з 60 (100%). Навчатися в тренера своєї раси.'],
      ['f', 'Паладин і чорнокнижник отримують скакуна завданнями класу.'],
      ['f', 'Пошана у своєї фракції дає знижку 10% на навчання їзді та скакунів. За Warcraft Tavern: 100 + 20 золотих на 40 рівні, 1000 + 200 на 60.'],
      ['t', 'Відкладіть золото до 40 рівня: їзда буде найбільшою витратою на шляху до 60.']],
    prof: [['f', 'Об’єкти табору 2 і 3 рівня в кожної професії свої. В Інженерії другий об’єкт Repair Bot лагодить екіпірування.'],
      ['t', 'Тримайте в групі Кулінарію 220 заради табору на 10 об’єктів: до рейду місця вистачить усім.']],
    legacy: [['f', 'На персонажа не більше 16 очок, зайві йдуть у трек нагород: іграшка за 15, вихованець за 25, табард за 40, скакун за 55.']],
    group: [['f', 'Рейди відкриються 09.12: Barrow Deeps на 10 гравців, Hyjal Summit на 20, Onyxia’s Lair на 40.'],
      ['t', 'Для 10-місного рейду потрібно 10 гравців: якщо вас менше, знайдіть решту в гільдії заздалегідь.']],
    src: ['ride', 'prof', 'legacy', 'cwg'] },
  { id: 'raid', n: '60 і рейди', sub: 'з 09.12', lo: 60, hi: 60,
    todo: [['f', '09.12 відкриваються Barrow Deeps (10 гравців), Hyjal Summit (20) і Onyxia’s Lair (40, Dustwallow Marsh).'],
      ['f', 'За проходження кожного з трьох рейдів дається очко Legacy.'],
      ['f', 'Нове поле бою 15 на 15: Darkspear Islands біля узбережжя Dustwallow Marsh.'],
      ['t', 'Поки набираєте людей на рейд, проходьте підземелля 60 рівня за екіпіруванням.']],
    prof: [['f', 'Бафи табору трохи слабші за класові й не складаються з ними: Благословення королів дає 10% до всіх характеристик, табір 8%.'],
      ['t', 'Ставте табір біля входу в рейд: його бафи закриють те, чого немає у ваших класів.']],
    legacy: [['f', 'Випробування для 60 рівня: підземелля 3, рейди 3, PvP 12. У PvP звання з тижневим лімітом і покращення екіпірування за Честь.']],
    group: [['f', 'Однакові бафи двох гравців одного класу перекриваються, різні класи складаються.'],
      ['t', 'Зберіть рейдовий склад у конструкторі й надішліть посилання в чат.']],
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
  if (now < D_REL) return ['pre', 'Обрано за датою: до релізу 04.11.'];
  if (me.lvl) return [me.lvl < 15 ? 'first' : me.lvl < 40 ? 'dung' : me.lvl < 60 ? 'path' : 'raid', 'Обрано за рівнем вашого персонажа.'];
  if (now >= D_RAID) return ['raid', 'Обрано за датою: рейди відкрито.'];
  return [now < new Date('2026-11-11T00:00:00') ? 'first' : 'dung', 'Обрано за датою. Вкажіть рівень персонажа, і етап підлаштується.'];
}
const START = { pre: 'hero_dawn-960', first: 'hero_campfire-960', dung: 'warlock-360', path: 'hunter-360', raid: 'paladin-360' };
const ARTV = /*ARTV*/{"hero_campfire-960.avif":"?v=93981d6a","hero_campfire-960.webp":"?v=5aa0e1b2","hero_dawn-960.avif":"?v=447302fd","hero_dawn-960.webp":"?v=b2d0d95b"};   // ?v= of the scene arts, filled in by build.art_version (same names, redrawn pictures)
const pic = f => `<picture><source type="image/avif" srcset="${ROOT}assets/art/${f}.avif${ARTV[f + '.avif'] || PV}"><img src="${ROOT}assets/art/${f}.webp${ARTV[f + '.webp'] || PV}" alt="" loading="lazy" decoding="async"></picture>`;
const tipL = () => '<span class="tl">Порада</span>';
function liC(x) { return x[0] === 't' ? `<li class="tip">${tipL()}${esc(x[1])}</li>` : `<li>${esc(x[1])}</li>`; }
function dLi(d) {
  const mine = me.lvl && nearLvl(d, me.lvl);
  return `<li class="${mine ? 'mine' : ''}"><b>${esc(d[0])}</b><span class="lvl${mine ? ' gold' : ''}">${lvRange(d)}</span><span class="z">${esc(d[3])}${d[4] ? ' · <i>нове</i>' : ''}${mine ? '<span class="sr"> · під ваш рівень</span>' : ''}</span></li>`;
}
function renderStage() {
  const [auto, why] = autoStage();
  if (stageAuto) stageSel = auto;
  const s = ST[stageSel];
  $('#stageBar').innerHTML = STAGES.map(x => `<button type="button" class="stile" role="tab" id="tab-${x.id}" data-st="${x.id}" aria-controls="stagePanel" aria-selected="${x.id === stageSel}" tabindex="${x.id === stageSel ? 0 : -1}">${pic(START[x.id])}<b>${esc(x.n)}</b><span class="lv">${esc(x.sub)}${x.id === auto ? ' · <span class="now">зараз</span>' : ''}</span></button>`).join('');
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
  $('#stagePanel').innerHTML = `<div class="st-head"><div class="t"><h3>${esc(s.n)}</h3><span class="when">${esc(s.sub)}</span></div><p class="why">${stageAuto ? esc(why) : 'Етап обрано вручну.'}</p></div>
    <ol class="steps-c">${steps}</ol>
    <div class="st-cols">
      <div><h4>Підземелля під рівень</h4>${s.dnote ? `<p class="small" style="margin:-4px 0 10px">${esc(s.dnote)}</p>` : ''}<ul class="dlist">${ds.slice(0, MAXD).map(dLi).join('')}</ul>
        <a class="more-l" href="guides/dungeons/">${extra > 0 ? `Ще підземель у таблиці: ${extra}` : 'Усі 35 підземель'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
      <div style="display:grid;gap:24px;align-content:start"><div><h4>Професії і табір</h4><ul class="clean">${s.prof.map(liC).join('')}</ul></div>
        <div><h4>Перки Legacy</h4><ul class="clean">${s.legacy.map(liC).join('')}</ul></div></div>
    </div>
    <div class="gtip"><h4 style="margin:0 0 10px;font-size:var(--fs-16)">Поради групі</h4><ul class="clean">${s.group.map(liC).join('')}</ul></div>
    <p class="st-src"><span>Джерела:</span>${s.src.map(k2 => `<a href="${SRC[k2][1]}" target="_blank" rel="noopener">${esc(SRC[k2][0])}</a>`).join('')}</p>`;
}
function optList(items, cur, none) { return `<option value="">${esc(none)}</option>` + items.map(([v, t]) => `<option value="${v}"${v === cur ? ' selected' : ''}>${esc(t)}</option>`).join(''); }
function renderMe() {
  fixMe();
  const races = f => RACES.filter(r => r.f === f).map(r => `<option value="${r.id}"${r.id === me.race ? ' selected' : ''}>${esc(r.n)}</option>`).join('');
  $('#meRace').innerHTML = `<option value="">Не обрано</option><optgroup label="${facName('alliance')}">${races('alliance')}</optgroup><optgroup label="${facName('horde')}">${races('horde')}</optgroup>`;
  const cls = (me.race ? Object.keys(RC[me.race].can) : CLASSES.map(c => c.id)).map(id => [id, CL[id].n]);
  $('#meCls').innerHTML = optList(cls, me.cls, 'Не обрано');
  $('#meRole').innerHTML = me.cls ? roleOpts(CL[me.cls]).map(x => `<option value="${x}"${x === me.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('') : `<option value="">Спершу клас</option>`;
  $('#meRole').disabled = !me.cls;
  const prim = PROFS.filter(p => p[2]);
  $('#meP1').innerHTML = optList(prim.filter(p => p[0] !== me.p2).map(p => [p[0], p[1]]), me.p1, 'Немає');
  $('#meP2').innerHTML = optList(prim.filter(p => p[0] !== me.p1).map(p => [p[0], p[1]]), me.p2, 'Немає');
  $('#meSec').innerHTML = PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${me.sec.includes(p[0])}">${esc(p[1])}</button>`).join('');
  document.querySelectorAll('.lvin').forEach(i => { if (document.activeElement !== i) i.value = me.lvl || ''; });
  const who = [me.race ? RC[me.race].n : '', me.cls ? CL[me.cls].n : ''].filter(Boolean).join(' · ');
  const sub = me.cls ? [ROLE_RU[me.role], me.race ? facName(RC[me.race].f) : ''].filter(Boolean).join(' · ') : 'Оберіть расу, клас і рівень нижче';
  const hero = $('#meHero');
  hero.style.setProperty('--cc', me.cls ? CCOL[me.cls] : '#c9a54a');
  hero.innerHTML = pic(me.cls ? `${me.cls}-600` : 'hero_campfire-960') + (me.lvl ? `<span class="lvb" aria-label="Рівень ${me.lvl}">${me.lvl}</span>` : '')
    + `<span class="k">Мій персонаж</span><b>${who ? esc(who) : 'Ще не створено'}</b><span class="s">${esc(sub)}</span>`;
  let out = '';
  if (meSet()) {
    const b = [];
    if (me.cls) b.push(BUFF[me.cls] ? `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span><b>${esc(CL[me.cls].n)}:</b> ${esc(BUFF[me.cls])}</span></li>` : `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-dps"/></svg></span><span>${esc(CL[me.cls].n)}: без групового бафу, чистий урон.</span></li>`);
    [me.p1, me.p2, ...me.sec].filter(Boolean).forEach(id => { const p = PR[id]; b.push(`<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg></span><span><b>${esc(p[3])}</b> <span class="m">· ${esc(p[1])}</span><br>${esc(p[4])}</span></li>`); });
    if (!b.length) b.push('<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span>Оберіть клас і професії, щоб побачити бафи.</span></li>');
    out += `<div><h4>Що ви даєте групі</h4><ul class="buffs">${b.join('')}</ul></div>`;
    if (me.lvl) {
      const ds = DUNGEONS.filter(d => nearLvl(d, me.lvl) && facOk(d, me.race && RC[me.race].f));
      out += `<div><h4>Підземелля під ваш рівень</h4>` + (ds.length ? `<ul class="dlist">${ds.slice(0, 4).map(dLi).join('')}</ul>` : '<p class="small">Перші підземелля з 13 рівня.</p>')
        + `<a class="more-l" href="guides/dungeons/">${ds.length > 4 ? `Ще підземель у таблиці: ${ds.length - 4}` : 'Таблиця підземель'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`;
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
