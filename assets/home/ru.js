const HOME = '';   // language home, the classes/ and races/ pages set their own
/* ref:start — shared with the classes/ and races/ pages (build_guides.ref_js); no $ or esc here, every page defines its own */
const CLASSES = [
  { id:'warrior', n:'Воин', s:'Воин', roles:['tank','dps'],
    specs:[['Оружие','Урон в ближнем бою (двуручное оружие)',['dps']],['Неистовство','Урон в ближнем бою (два оружия)',['dps']],['Защита','Танк',['tank']]],
    lvl:'Самая медленная прокачка, примерно на 12% дольше среднего',
    lp:12,
    raid:'Боевой крик действует на весь рейд',
    forever:'Больше Ярости, лучше угроза по группе целей, талант Мастер оружия. Неистовство и Кровожадность ослаблены.' },
  { id:'paladin', n:'Паладин', roles:['tank','heal','dps'],
    specs:[['Свет','Лекарь',['heal']],['Защита','Танк',['tank']],['Воздаяние','Урон в ближнем бою',['dps']]],
    lvl:'Средний темп прокачки',
    lp:0,
    raid:'Благословение королей теперь базовое. По бета-спискам Защита среди сильнейших танков, Воздаяние просело после патча 15 октября.',
    forever:'Священный удар с 6 уровня, Правосудие не тратит печать. Нежить теперь может быть паладином, значит класс появился у Орды.' },
  { id:'hunter', n:'Охотник', roles:['dps'],
    specs:[['Повелитель зверей','Урон дальнего боя, много урона от питомца',['dps']],['Стрельба','Урон дальнего боя',['dps']],['Выживание','Ближний и дальний бой, ловушки',['dps']]],
    lvl:'Самая быстрая прокачка, примерно на 8% быстрее среднего',
    lp:-8,
    raid:'Аура меткого выстрела действует на весь рейд',
    forever:'Можно играть без питомца, ловушки работают в бою, появились лисы как семейство питомцев. Выживание может идти в ближний бой.' },
  { id:'rogue', n:'Разбойник', roles:['dps'],
    specs:[['Ликвидация','Урон ядами',['dps']],['Бой','Быстрые атаки оружием',['dps']],['Скрытность','Засады, кровотечения',['dps']]],
    lvl:'Средний темп прокачки',
    lp:0,
    raid:'Чистый урон в ближнем бою без баффов на весь рейд',
    forever:'Теперь можно использовать одноручные топоры. Ликвидация строится на ядах, Скрытность на кровотечениях и невидимости.' },
  { id:'priest', n:'Жрец', roles:['heal','dps'],
    specs:[['Послушание','Лекарь, щиты и поглощение',['heal']],['Свет','Лекарь',['heal']],['Темная магия','Урон дальнего боя',['dps']]],
    lvl:'Примерно на 5% медленнее среднего',
    lp:5,
    raid:'Божественный дух стал базовым. Урон Тьмы и «Всепожирающая чума» (откат 24 сек) усилены патчем 15 октября.',
    forever:'Защита от страха и «Всепожирающая чума» доступны с 20 уровня любой расе. У каждой расы по два своих заклинания жреца.' },
  { id:'shaman', n:'Шаман', roles:['heal','dps','tank?'],
    specs:[['Стихии','Урон дальнего боя',['dps']],['Совершенствование','Урон в ближнем бою. Возможность танковать пока под вопросом',['dps','tank?']],['Исцеление','Лекарь',['heal']]],
    lvl:'Средний темп прокачки',
    lp:0,
    raid:'Тотемы силы земли, неистовства ветра, языков пламени и грации воздуха усиливают свою группу',
    forever:'Дворфы теперь могут быть шаманами, значит класс появился у Альянса. Выброс лавы усилен, Стихии поднялись в списках урона.' },
  { id:'mage', n:'Маг', roles:['dps'],
    specs:[['Тайная магия','Бурст, много маны',['dps']],['Огонь','Криты и поджоги',['dps']],['Лёд','Урон и контроль',['dps']]],
    lvl:'Самая быстрая прокачка, примерно на 8% быстрее среднего (около 12 часов экономии)',
    lp:-8,
    raid:'Порталы и еда с водой для всей компании',
    forever:'Огонь получил Путь огня, Тайная магия — Чародейскую вспышку, Лёд — Ледяное копьё. Огненно-ледяная стрела доступна с 40 уровня.' },
  { id:'warlock', n:'Чернокнижник', roles:['dps'],
    specs:[['Колдовство','Урон от проклятий и порчи',['dps']],['Демонология','Урон через демонов',['dps']],['Разрушение','Прямой урон огнём и тьмой',['dps']]],
    lvl:'Средний темп прокачки',
    lp:0,
    raid:'Мастерство тьмы теперь даёт 2–10% урона от тьмы (было 1–5%)',
    forever:'У Колдовства новое направляемое заклинание, демон остаётся при Жертве демона, у Разрушения появились Испепеление и урон по площади.' },
  { id:'druid', n:'Друид', roles:['tank','heal','dps'],
    specs:[['Баланс','Урон дальнего боя',['dps']],['Сила зверя','Танк (медведь) и урон в ближнем бою (кошка)',['tank','dps']],['Исцеление','Лекарь, много лечения по времени',['heal']]],
    lvl:'Примерно на 5% медленнее среднего',
    lp:5,
    raid:'Вожак стаи и аура лунного совуха действуют на весь рейд и складываются',
    forever:'Каждая специализация получила чёткую роль, формы работают с зельями и чарами на оружии. Можно быть танком, лекарем и бойцом на одном персонаже.' }
];
const ROLE_RU = { tank:'Танк', heal:'Лекарь', dps:'Урон', 'tank?':'Танк (под вопросом)' };
const ri = r => `<svg class="ri" aria-hidden="true"><use href="#i-${r.replace('?','')}"/></svg>`;
const CCOL = { warrior:'#c79c6e', paladin:'#f58cba', hunter:'#abd473', rogue:'#fff569', priest:'#e8e8e8', shaman:'#2f8cf0', mage:'#40c7eb', warlock:'#8788ee', druid:'#ff7d0a' };
const BUFF = { warrior:'Боевой крик', paladin:'Благословение королей', hunter:'Аура меткого выстрела', priest:'Слово силы: Стойкость, Божественный дух', shaman:'Тотемы (сила земли, неистовство ветра, языки пламени, грация воздуха)', mage:'Чародейский интеллект, порталы, еда и вода', druid:'Знак дикой природы, Вожак стаи, аура лунного совуха' };

const RACES = [
  { id:'human', n:'Человек', f:'alliance',
    cls:['warrior','paladin','hunter*','rogue','priest','mage','warlock'],
    rac:[['a','Воля к жизни','Снимает оглушение'],['a','Внимательность','Показывает невидимых врагов на 20 сек'],['p','Беспощадность','+2% шанс крита'],['p','Человеческий дух','+5% к духу']],
    tip:'Дух идёт в лечение Жрецу Света, так что Человек-жрец хорош для лекаря.' },
  { id:'dwarf', n:'Дворф', f:'alliance',
    cls:['warrior','paladin','hunter','rogue','priest','shaman*'],
    rac:[['a','Каменная форма','Иммунитет к кровотечениям, ядам и болезням на 8 сек и снижение физического урона'],['a','Поиск сокровища','Показывает сундуки рядом'],['p','Ярость земли','+2% к урону крита и силе лечения'],['p','Охотник на крупную дичь','+5% урона по зверям']],
    tip:'Каменная форма полезна танку и в PvP.' },
  { id:'nightelf', n:'Ночной эльф', f:'alliance',
    cls:['warrior','hunter','rogue','priest','druid'],
    rac:[['a','Свет Элуны','+10% к шансу крита на 15 сек'],['a','Слиться с тенью','Невидимость на месте'],['p','Расторопность','+1% к уклонению и +2% к скорости бега'],['p','Дух огонька','+75% к скорости бега в виде духа']],
    tip:'Единственная раса Альянса с друидом, если не брать Скайборн.' },
  { id:'gnome', n:'Гном', f:'alliance',
    cls:['warrior','rogue','mage','warlock','priest*'],
    rac:[['a','Мастер побега','Короткий иммунитет к замедлению и корням'],['a','Эврика!','Следующие 3 способности дешевле и на 10% сильнее'],['p','Пытливый ум','+5% к максимуму маны, ярости или энергии'],['p','Инженерное дело, специализация','Инженерные устройства срабатывают надёжнее']],
    tip:'Пытливый ум особенно выручает классам на энергии.' },
  { id:'skyA', n:'Скайборн (Альянс)', f:'alliance', paid:true, name:'Высший скайборн',
    cls:['warrior','hunter','rogue','mage','druid'],
    rac:[['a','Хождение по воздуху','Планирование вниз 10 сек, нет урона от падения'],['a','Чтение лей-линий','+100% к восстановлению здоровья и маны'],['p','Благословение ветра','+3% к скорости атаки и заклинаний'],['p','Прозрение стихий','+5% урона по элементалям']],
    tip:'Платная раса: набор Heroic Pack от $29.99. Старт в локации Zephras Isle (1–12 уровни).' },
  { id:'orc', n:'Орк', f:'horde',
    cls:['warrior','hunter','rogue','shaman','warlock','mage*'],
    rac:[['a','Кровавое неистовство','+10% к силе атаки и заклинаний на 15 сек'],['a','Разрушение проклятий','Снимает проклятия и порчи, магический урон по вам −5% на 8 сек'],['p','Дикость','+1% шанс крита'],['p','Твердость','Оглушения короче на 20%']],
    tip:'Кровавое неистовство даёт мощное окно урона.' },
  { id:'undead', n:'Нежить', f:'horde',
    cls:['warrior','rogue','mage','priest','warlock','paladin*'],
    rac:[['a','Воля Отрекшихся','Снимает очарование, страх и сон'],['a','Каннибализм','Восстанавливает 35% здоровья и маны со временем'],['p','Подводное дыхание','Дыхание под водой дольше'],['p','Могильное касание','Шанс высосать здоровье при атаке']],
    tip:'Новая комбинация: паладин у Орды, где раньше этого класса не было.' },
  { id:'tauren', n:'Таурен', f:'horde',
    cls:['warrior','hunter','shaman','druid'],
    rac:[['a','Громовая поступь','Оглушает врагов рядом на 2 сек'],['a','Проращивание','Выращивает травы, которые можно собрать без травничества'],['p','Бег по равнинам','Скорость растёт, пока вы бежите'],['p','Закалка','+5% здоровья и +2% к урону крита']],
    tip:'Единственная раса Орды с друидом, если не брать Скайборн.' },
  { id:'troll', n:'Тролль', f:'horde',
    cls:['warrior','hunter','rogue','priest','shaman','mage','warlock*'],
    rac:[['a','Боевое исступление','+10% к скорости атаки и заклинаний на 10 сек'],['a','Быстрая регенерация','Восстанавливает здоровье со временем'],['p','Убийство животных','+5% урона по зверям'],['p','Регенерация','Здоровье восстанавливается и в бою']],
    tip:'Больше всего вариантов классов в Орде: семь.' },
  { id:'skyH', n:'Скайборн (Орда)', f:'horde', paid:true, name:'Скайборн-ветрорез',
    cls:['warrior','hunter','rogue','shaman','druid'],
    rac:[['a','Хождение по воздуху','Планирование вниз 10 сек, нет урона от падения'],['a','Взгляд в небо','+10% к скорости бега'],['p','Благословение ветра','+3% к скорости атаки и заклинаний'],['p','Прозрение стихий','+5% урона по элементалям']],
    tip:'Платная раса: набор Heroic Pack от $29.99. Из скайборнов шаманом может быть только ветрорез (Орда), магом — только Высший орден (Альянс).' }
];
RACES.forEach(r => { r.can = {}; r.cls.forEach(c => { const isNew = c.endsWith('*'); r.can[isNew ? c.slice(0,-1) : c] = isNew ? 'new' : 'ok'; }); });
const CL = Object.fromEntries(CLASSES.map(c => [c.id, c]));
const RC = Object.fromEntries(RACES.map(r => [r.id, r]));
const RLEAD = {"human": "Самая многочисленная раса Альянса. Универсальна и сильна в PvP благодаря Воле к жизни.", "dwarf": "Крепкие горняки и стрелки Стальгорна. Впервые в Classic у Альянса есть шаманы, и это дворфы.", "nightelf": "Древний народ лесов. Неуловимы: свой способ скрыться, уклонение и быстрый бег.", "gnome": "Изобретатели Гномрегана. Маленькие, хитрые и с лучшей способностью побега в игре.", "skyA": "Новая раса Forever. Высший орден: эльфы ветра, которые ищут утраченную тайную магию предков.", "orc": "Сердце Орды. Сильнейшие воины и мастера PvP благодаря Кровавому неистовству и Твердости.", "undead": "Отрекшиеся: бывшие люди, вырвавшиеся из-под власти Короля-лича. Не боятся страха и сна.", "tauren": "Мирные великаны равнин. Больше всех здоровья и свой массовый оглушающий удар.", "troll": "Племя Чёрного Копья. Больше всех классов в Орде и сильное Боевое исступление для урона.", "skyH": "Новая раса Forever. Ветрорезы: духовные лидеры скайборнов, близкие к стихиям."}; // race page leads and URL slugs, filled in by build.py
const RSLUG = {"human": "human", "dwarf": "dwarf", "nightelf": "night-elf", "gnome": "gnome", "skyA": "skyborne-alliance", "orc": "orc", "undead": "undead", "tauren": "tauren", "troll": "troll", "skyH": "skyborne-horde"};

const EN = {
  'Оружие':'Arms','Неистовство':'Fury','Защита':'Protection','Свет':'Holy','Воздаяние':'Retribution',
  'Повелитель зверей':'Beast Mastery','Стрельба':'Marksmanship','Выживание':'Survival',
  'Ликвидация':'Assassination','Бой':'Combat','Скрытность':'Subtlety',
  'Послушание':'Discipline','Темная магия':'Shadow','Стихии':'Elemental','Совершенствование':'Enhancement','Исцеление':'Restoration',
  'Тайная магия':'Arcane','Огонь':'Fire','Лёд':'Frost','Колдовство':'Affliction','Демонология':'Demonology','Разрушение':'Destruction',
  'Баланс':'Balance','Сила зверя':'Feral',
  'Воля к жизни':'Will to Survive','Внимательность':'Perception','Беспощадность':'Ruthless','Человеческий дух':'The Human Spirit',
  'Каменная форма':'Stoneform','Поиск сокровища':'Find Treasure','Ярость земли':'Earth Fury','Охотник на крупную дичь':'Big Game Hunter',
  'Свет Элуны':"Elune’s Light",'Слиться с тенью':'Shadowmeld','Расторопность':'Quickness','Дух огонька':'Wisp Spirit',
  'Мастер побега':'Escape Artist','Эврика!':'Eureka!','Пытливый ум':'Expansive Mind','Инженерное дело, специализация':'Engineering Specialization',
  'Хождение по воздуху':'Walk on Air','Чтение лей-линий':'Read Ley Line','Благословение ветра':'Wind Blessed','Прозрение стихий':'Elemental Insight','Взгляд в небо':'Skysight',
  'Кровавое неистовство':'Blood Fury','Разрушение проклятий':'Shatter Curse','Дикость':'Savage','Твердость':'Hardiness',
  'Воля Отрекшихся':'Will of the Forsaken','Каннибализм':'Cannibalize','Подводное дыхание':'Underwater Breathing','Могильное касание':'Touch of the Grave',
  'Громовая поступь':'War Stomp','Проращивание':'Cultivation','Бег по равнинам':'Plainsrunning','Закалка':'Endurance',
  'Боевое исступление':'Berserking','Быстрая регенерация':'Rapid Regeneration','Убийство животных':'Beast Slaying','Регенерация':'Regeneration'
};
RC.skyA.en = 'High Order Skyborne'; RC.skyH.en = 'Windshaper Skyborne';
const tipBox = h => `<div class="tipbox"><svg class="ico fi" aria-hidden="true"><use href="#i-fire"/></svg><p><span class="tl">Совет</span>${h}</p></div>`;
function bi(ru) { return EN[ru] && EN[ru] !== ru ? `${esc(ru)} <span class="en">(${esc(EN[ru])})</span>` : esc(ru); }
function raceEn(r) { return r.en ? ` <span class="en">/ ${esc(r.en)}</span>` : ''; }
function facName(f) { return f === 'alliance' ? 'Альянс' : 'Орда'; }
/* Round face avatar: assets/art/<id>-face.webp, ring colour cc */
function face(id, cc, cls = '', title = '') { return `<span class="av ${cls}" style="--cc:${cc}"${title ? ` title="${esc(title)}"` : ''}><img src="./assets/art/${id}-face.webp" width="160" height="160" alt="" loading="lazy" decoding="async"></span>`; }
function lvlMeter(c) {
  const p = c.lp || 0, w = Math.min(Math.abs(p) / 12 * 46, 46);
  const label = p < 0 ? `Быстрее на ${-p}%` : p > 0 ? `Медленнее на ${p}%` : 'Средний темп';
  const bar = p ? `<i class="${p > 0 ? 'slow' : ''}" style="${p < 0 ? 'right' : 'left'}:50%;width:${w}%"></i>` : '';
  return `<span class="lvl"><span>${label}</span><span class="bar" role="img" aria-label="${label}">${bar}</span><span class="scale" aria-hidden="true"><span>быстрее</span><span>медленнее</span></span></span>`;
}
function renderClassRef() {
  const roles = ['tank', 'heal', 'dps'];
  const head = `<div class="cmp-h" aria-hidden="true"><span>Класс</span><span class="rdots">${roles.map(x => `<span title="${ROLE_RU[x]}">${ri(x)}</span>`).join('')}</span><span>Прокачка</span><span>В рейде</span><span></span></div>`;
  $('#classRef').innerHTML = head + CLASSES.map(c => `<a class="cmp-row" href="${HOME}classes/${c.id}/" style="--cc:${CCOL[c.id]};--art:url('./assets/art/${c.id}-360.webp')">
    <span class="cmp-id">${face(c.id, CCOL[c.id])}<span><b>${esc(c.n)}</b><small>${c.specs.map(s => esc(s[0])).join(' · ')}</small></span></span>
    <span class="rdots" role="img" aria-label="Роли: ${c.roles.map(x => ROLE_RU[x]).join(', ')}">${roles.map(x => { const on = c.roles.includes(x), q = c.roles.includes(x + '?'); return `<span class="rdot${on ? ' on' : q ? ' q' : ''}" title="${ROLE_RU[q ? x + '?' : x]}">${ri(x)}</span>`; }).join('')}</span>
    ${lvlMeter(c)}
    <span class="cmp-txt">${esc(c.raid)}</span>
    <span class="go" aria-hidden="true"><svg class="ico"><use href="#i-arrow"/></svg></span>
  </a>`).join('');
}

function renderRaceRef() {
  const head = `<div class="cmp-h" aria-hidden="true"><span>Раса</span><span>Классы</span><span class="abl">Способности <span class="abt">активная</span><span class="abt p">пассивная</span></span><span></span></div>`;
  $('#raceRef').innerHTML = ['alliance', 'horde'].map(f => `<div class="rgroup ${f}"><h3>${facName(f)}</h3>${head}` + RACES.filter(r => r.f === f).map(r => `<a class="cmp-row" href="${HOME}races/${RSLUG[r.id]}/" style="--cc:var(--${f});--art:url('./assets/art/${RSLUG[r.id]}-360.webp')">
    <span class="cmp-id">${face(RSLUG[r.id], `var(--${f})`)}<span><b>${esc(r.n)}${r.paid ? '<span class="paid">платная</span>' : ''}</b>${r.en ? `<small>${esc(r.en)}</small>` : ''}</span></span>
    <span class="ccl" role="img" aria-label="Классы: ${Object.keys(r.can).map(id => CL[id].n).join(', ')}">${CLASSES.map(c => { const v = r.can[c.id]; return face(c.id, CCOL[c.id], v ? (v === 'new' ? 'nw' : '') : 'off', c.n + (v === 'new' ? ', новое' : v ? '' : ', нельзя')); }).join('')}</span>
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
      h += `<tr class="${r.id === state.race ? 'rowsel' : ''}"><th scope="row"><span class="rn">${face(RSLUG[r.id], `var(--${r.f})`)}${esc(r.n)}${r.paid ? '<span class="paid">платная</span>' : ''}</span></th>`;
      CLASSES.forEach(c => {
        const v = r.can[c.id];
        const dim = roleMatch(c, state.r) ? '' : ' dim';
        if (!v) { h += `<td><span class="cell no${dim}" role="img" aria-label="${esc(r.n)} ${esc(c.n)}: нельзя"></span></td>`; return; }
        const sel = (r.id === state.race && c.id === state.cls) ? ' sel' : '';
        const label = `${r.n} ${c.n}${v === 'new' ? ', новая комбинация' : ''}`;
        const mark = v === 'new' && !sel ? '<span class="nw">новое</span>' : '<i><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i>';
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
    return `<button type="button" data-pc="${c.id}" class="${v ? '' : 'na'}" aria-pressed="${c.id === state.cls}">${esc(c.n)}${v === 'new' ? ' · новое' : ''}</button>`;
  }).join('');
  $('#pickm').innerHTML = `<div><div class="lbl">1. Раса</div><div class="chiprow">${races}</div></div>
    <div><div class="lbl">2. Класс · пунктир — не для этой расы, нажмите, чтобы сменить расу</div><div class="chiprow">${cls}</div></div>`;
}

function renderDetail() {
  const r = RC[state.race], c = CL[state.cls], isNew = r.can[c.id] === 'new';
  const specs = c.specs.map(s => {
    const hit = state.r !== 'all' && s[2].includes(state.r) ? ' on' : '';
    return `<div class="card${hit}" style="--cc:${CCOL[c.id]}"><span class="rc">${ri(s[2][0])}</span><b>${bi(s[0])}</b><span>${esc(s[1])}</span></div>`;
  }).join('');
  const rac = r.rac.map(x => `<div class="card ab"><span class="abt${x[0] === 'a' ? '' : ' p'}">${x[0] === 'a' ? 'Активная' : 'Пассивная'}</span><b>${bi(x[1])}</b><span>${esc(x[2])}</span></div>`).join('');
  const text = `${r.name || r.n} ${c.n} (${facName(r.f)})${r.paid ? ', нужен набор Скайборн' : ''}`;
  $('#detail').innerHTML = `
    <div class="d-head">
      <div class="d-art" aria-hidden="true"><img src="./assets/art/${c.id}-600.webp" width="600" height="804" alt="" loading="lazy" decoding="async"></div>
      <div class="d-avs">${face(RSLUG[r.id], `var(--${r.f})`)}${face(c.id, CCOL[c.id])}</div>
      <div class="d-title"><h3>${esc(r.n)}${raceEn(r)} · ${esc(c.n)}</h3>
        <div class="chips"><span class="tag ${r.f}">${facName(r.f)}</span>${isNew ? '<span class="tag new">Новая комбинация</span>' : ''}${r.paid ? '<span class="tag paid">Платная раса</span>' : ''}${roleChips(c)}</div></div>
    </div>
    <div class="d-body">
      <div class="d-cols">
        <div><h4>Специализации</h4><div class="cards">${specs}</div></div>
        <div><h4>Способности расы</h4><div class="cards two">${rac}</div></div>
      </div>
      <div class="facts3">
        <div class="fact"><h4>Прокачка</h4>${lvlMeter(c)}</div>
        <div class="fact"><h4>В рейде</h4><span>${esc(c.raid)}.</span></div>
        <div class="fact"><h4>Что нового</h4><span>${esc(c.forever)}</span></div>
      </div>
      ${tipBox(esc(r.tip))}
      <div class="copyrow">
        <input id="pickText" readonly value="${esc(text)}" aria-label="Мой выбор">
        <button class="btn" id="copyBtn"><svg class="ico" aria-hidden="true"><use href="#i-copy"/></svg>Скопировать мой выбор</button>
        <span class="small" id="copyMsg" role="status"></span>
      </div>
    </div>`;
  $('#copyBtn').onclick = () => copyTo($('#pickText').value, $('#copyMsg'), 'Скопировано');
  $('#qPick').textContent = `Сейчас: ${r.n} · ${c.n}`;
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
const ROOT = './';
const DESC = {
  warrior: 'Латы, ярость и первый ряд. Держит удар как танк или рубит двуручным оружием.',
  paladin: 'Святой воин в латах: лечит, танкует и бьёт молотом. Теперь есть и у Орды.',
  hunter: 'Лук, ловушки и верный зверь рядом. Один из самых быстрых классов в прокачке.',
  rogue: 'Яды, клинки и тень. Чистый урон из засады и контроль врагов.',
  priest: 'Свет и Тьма в одних руках. Главный лекарь группы или тёмный заклинатель.',
  shaman: 'Тотемы и стихии: лечит, бьёт молнией или оружием. Теперь есть и у Альянса.',
  mage: 'Огонь, лёд и тайная магия. Порталы, еда и вода для всей компании.',
  warlock: 'Проклятия, демоны и огонь. Урон со временем и свой демон в помощь.',
  druid: 'Медведь, кошка, сова или лекарь: все три роли на одном персонаже.'
};
const artSet = (id, ext) => [360, 600, 896].map(w => `${ROOT}assets/art/${id}-${w}.${ext} ${w}w`).join(', ');
const ART_SIZES = '(max-width: 719px) 78vw, 440px';
function renderRoster() {
  $('#roster').innerHTML = CLASSES.map((c, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="classes/${c.id}/" style="--cc:${CCOL[c.id]}">
    <picture><source type="image/avif" srcset="${artSet(c.id, 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(c.id, 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${c.id}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(c.n)}</span>
    <span class="info"><b>${esc(c.n)}</b><span class="roles">${c.roles.filter(r => !r.endsWith('?')).map(r => `<span>${ri(r)}${ROLE_RU[r]}</span>`).join('')}</span><span class="d">${esc(DESC[c.id])}</span><span class="more">Подробнее о классе</span></span>
  </a>`).join('');
}
renderRoster();
/* Race roster: one row of portraits per faction, links to the race pages */
function renderPeoples() {
  [['alliance', '#rosterA'], ['horde', '#rosterH']].forEach(([f, sel]) => {
    $(sel).innerHTML = RACES.filter(r => r.f === f).map((r, i) => `<a class="hc${i === 0 ? ' on' : ''}" href="races/${RSLUG[r.id]}/" style="--cc:var(--${f})">
    <picture><source type="image/avif" srcset="${artSet(RSLUG[r.id], 'avif')}" sizes="${ART_SIZES}"><source type="image/webp" srcset="${artSet(RSLUG[r.id], 'webp')}" sizes="${ART_SIZES}"><img src="${ROOT}assets/art/${RSLUG[r.id]}-600.webp" width="896" height="1200" alt="" loading="lazy" decoding="async"></picture>
    <span class="vn" aria-hidden="true">${esc(raceName(r))}</span>
    <span class="info"><b>${esc(raceName(r))}</b>${r.paid ? '<span class="tag paid">платная</span>' : ''}<span class="d">${esc(RLEAD[r.id])}</span><span class="more">Подробнее о расе</span></span>
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
  try { await navigator.clipboard.writeText(text); msgEl.textContent = ok; } catch (e) { msgEl.textContent = 'Не удалось скопировать, выделите и нажмите Ctrl+C'; }
}

/* Dungeons: [name, min, max, entrance zone, new, other sites' ranges where they differ] */
const DUNGEONS = [
  ['Огненная пропасть (Ragefire Chasm)', 13, 18, 'Оргриммар', 0, [], 'horde'],
  ['Hall of Thanes', 13, 18, 'Стальгорн', 1, [['Icy Veins', '13–20']]],
  ['Руины Лордерона (Ruins of Lordaeron)', 15, 20, 'Тирисфальские леса', 1, [['Icy Veins', '15–22']]],
  ['Мертвые копи (The Deadmines)', 15, 22, 'Западный Край', 0, [['Icy Veins', '17–26']]],
  ['Пещеры Стенаний (Wailing Caverns)', 17, 24, 'Степи', 0, [['Icy Veins', '15–24']]],
  ['Крепость Темного Клыка (Shadowfang Keep)', 20, 26, 'Серебряный бор', 0, [['Icy Veins', '20–30']]],
  ['Непроглядная Пучина (Blackfathom Deeps)', 22, 28, 'Ясеневый лес', 0, [['Sportskeeda', '22–26'], ['Icy Veins', '24–32']]],
  ['Excavation Site: Wetlands', 24, 29, 'Болотина', 1, [['ClassicWoW.gg', '26–31'], ['Icy Veins', '26–33']]],
  ['Тюрьма (The Stockade)', 25, 29, 'Штормград', 0, [['Icy Veins', '24–32']], 'alliance'],
  ['City of Dalaran', 28, 33, 'Альтеракские горы', 1, [['Icy Veins', '28–35']]],
  ['Гномреган (Gnomeregan)', 29, 38, 'Дун Морог', 0],
  ['Лабиринты Иглошкурых (Razorfen Kraul)', 29, 38, 'Степи', 0],
  ['Монастырь Алого ордена: кладбище (Scarlet Monastery: Graveyard)', 30, 38, 'Тирисфальские леса', 0],
  ['Монастырь Алого ордена: библиотека (Scarlet Monastery: Library)', 33, 41, 'Тирисфальские леса', 0],
  ['The Drowned City', 35, 40, 'Тернистая долина', 1],
  ['Монастырь Алого ордена: оружейная (Scarlet Monastery: Armory)', 36, 44, 'Тирисфальские леса', 0],
  ['Ульдаман (Uldaman)', 36, 45, 'Бесплодные земли', 0, [['Icy Veins', '41–51']]],
  ['Курганы Иглошкурых (Razorfen Downs)', 37, 46, 'Степи', 0],
  ['Монастырь Алого ордена: собор (Scarlet Monastery: Cathedral)', 38, 46, 'Тирисфальские леса', 0],
  ["Zul'Farrak", 40, 47, 'Tanaris', 0, [['Icy Veins', '44–54']]],
  ["Krol'dok Stronghold", 40, 45, 'Riverglades', 1],
  ['Мародон (Maraudon)', 45, 51, 'Пустоши', 0, [['Icy Veins', '46–55']]],
  ['Alcaz Island Prison', 48, 53, 'Пылевые топи', 1],
  ["Temple of Atal'Hakkar", 50, 55, 'Swamp of Sorrows', 0, [['Icy Veins', '50–60']]],
  ['Глубины Черной горы (Blackrock Depths)', 52, 60, 'Черная гора', 0],
  ['Blackmaw Hold', 55, 60, 'Азшара', 1],
  ['Нижняя часть Вершины Черной горы (Lower Blackrock Spire)', 57, 60, 'Черная гора', 0, [['Icy Veins', '55–60']]],
  ['Забытый Город: восток (Dire Maul: East)', 58, 60, 'Фералас', 0, [['Icy Veins', '54–60']]],
  ["Shaper's Terrace", 58, 60, "Un'Goro Crater", 1],
  ['Стратхольм: живые (Stratholme: Living)', 58, 60, 'Восточные Чумные земли', 0],
  ['Стратхольм: нежить (Stratholme: Undead)', 58, 60, 'Восточные Чумные земли', 0],
  ['Некроситет (Scholomance)', 58, 60, 'Западные Чумные земли', 0],
  ['Верхняя часть Вершины Черной горы (Upper Blackrock Spire)', 60, 60, 'Черная гора', 0, [['Icy Veins', '59–60']]],
  ['Забытый Город: запад (Dire Maul: West)', 60, 60, 'Фералас', 0, [['Icy Veins', '56–60']]],
  ['Забытый Город: север (Dire Maul: North)', 60, 60, 'Фералас', 0, [['Icy Veins', '56–60']]]
];
const lvRange = d => d[1] === d[2] ? String(d[1]) : `${d[1]}–${d[2]}`;
const nearLvl = (d, lv) => lv >= d[1] - 3 && lv <= d[2] + 3;
const facOk = (d, f) => !f || !d[6] || d[6] === f;   // Ragefire Chasm and The Stockade open from a capital

/* Professions: camp object (tier 1) and the class buff it stands in for */
const PROFS = [
  ['alchemy', 'Алхимия', 1, 'Mana Well', 'как Благословение мудрости'],
  ['blacksmithing', 'Кузнечное дело', 1, 'Sharpening Wheel', 'как Тотем силы земли'],
  ['enchanting', 'Наложение чар', 1, 'Enchanted Lute', 'как Знак дикой природы'],
  ['engineering', 'Инженерное дело', 1, 'Reagent Bot', 'торговец реагентами, на 2 уровне ремонт'],
  ['herbalism', 'Травничество', 1, 'Incense Candle', 'как Чародейский интеллект'],
  ['leatherworking', 'Кожевничество', 1, 'Camp Tent', 'больше опыта от отдыха'],
  ['mining', 'Горное дело', 1, 'Lodestone', 'как Благословение могущества'],
  ['skinning', 'Снятие шкур', 1, 'Camp Chair', 'как аура лунного совуха'],
  ['tailoring', 'Портняжное дело', 1, 'Faction Banner', 'как Божественный дух'],
  ['cooking', 'Кулинария', 0, 'Basic Campfire', 'больше мест для объектов в лагере'],
  ['firstaid', 'Первая помощь', 0, 'First Aid Kit', 'как Слово силы: Стойкость'],
  ['fishing', 'Рыбалка', 0, 'Fish Bowl', 'как Благословение королей']
];
const PR = Object.fromEntries(PROFS.map(p => [p[0], p]));

/* Game stages: f = fact from the sources, t = our tip */
const SRC = {
  names: ['Icy Veins: резерв имён', 'https://www.icy-veins.com/wow-forever/name-reservation'],
  names2: ['Team Overpowered: имена и фамилии', 'https://teamoverpowered.com/forever/guides/name-reservation/'],
  prof: ['Warcraft Tavern: профессии', 'https://www.warcrafttavern.com/forever/guides/professions/'],
  camp: ['Warcraft Tavern: лагерь', 'https://www.warcrafttavern.com/forever/guides/camping/'],
  legacy: ['Blizzard: Legacy', 'https://news.blizzard.com/en-gb/article/24307383'],
  dung: ['Warcraft Tavern: подземелья', 'https://www.warcrafttavern.com/forever/guides/dungeons/'],
  ride: ['Warcraft Tavern: верховая езда', 'https://www.warcrafttavern.com/forever/guides/riding/'],
  cwg: ['ClassicWoW.gg: даты и рейды', 'https://classicwow.gg/forever']
};
const STAGES = [
  { id: 'pre', n: 'До старта', sub: 'до 04.11', lo: 0, hi: 0,
    todo: [['f', 'Ранняя резервация имён 27.10 – 03.11 для владельцев наборов Heroic, Epic и Collection. Кто первым пришёл, тот и занял.'],
      ['f', 'Можно занять до трёх персонажей на аккаунт. У персонажа имя и фамилия, уникальным должно быть их сочетание в пределах региона.'],
      ['f', 'С 04.11 для игры нужна подписка или игровое время.'],
      ['t', 'Придумайте по три имени с фамилией и запасные варианты до 27.10.']],
    dnote: 'Первые подземелья доступны с 13 уровня.',
    prof: [['f', 'На персонажа две основные профессии и все три вспомогательные: Кулинария, Первая помощь и Рыбалка.'],
      ['f', 'Каждая профессия ставит в лагерь свой объект с баффом, похожим на бафф класса.'],
      ['t', 'Распределите профессии заранее: один берёт Кулинарию ради костра, у остальных разные, чтобы баффы лагеря не повторялись.']],
    legacy: [['f', 'Legacy открывается с первым очком: 25 уровень, 150 в профессии (не сбор) или исследование всей карты.'],
      ['f', 'На старте на персонажа можно потратить не больше 16 очков, лишние идут в трек наград.']],
    group: [['t', 'Договоритесь об одной фракции и одном режиме: группироваться можно только внутри режима, а в PvP на аккаунте одна фракция.'],
      ['t', 'Соберите состав в конструкторе: танк, лекарь и разные классы ради баффов.']],
    src: ['names', 'names2', 'prof', 'legacy'] },
  { id: 'first', n: 'Первые дни', sub: 'уровни 1–15', lo: 1, hi: 15,
    todo: [['f', 'Скайборн начинают на Zephras Isle, это уровни 1–12.'],
      ['f', 'Таланты открываются с 10 уровня, с перком Legacy Talented с 9.'],
      ['f', 'Большая часть готовой еды даёт бонус к опыту. Он складывается с лагерем и «Уютным спальным мешком».'],
      ['t', 'Копите отдых: выходите из игры в трактире или у лагеря с палаткой.']],
    prof: [['f', 'Базовый костёр доступен без Кулинарии и вмещает 3 объекта. Горит около 10 минут, поставить новый можно через 5.'],
      ['f', 'Чтобы получить баффы лагеря, сядьте рядом (/sit) хотя бы на минуту.'],
      ['t', 'Берите сбор с первых уровней: травы, руда и шкуры понадобятся ремеслу, а 150 в ремесле открывает Legacy.']],
    legacy: [['f', 'Перков пока нет: первое очко даст 25 уровень или 150 в профессии.'],
      ['t', 'Когда откроется Legacy, первыми берите перки опыта и лагеря: Well Rested, Field Guide, Permanence. Talented пригодится твинкам.']],
    group: [['t', 'Качайтесь в одной зоне и ставьте лагерь на привале: пять минут на костёр окупаются баффами на всю группу.'],
      ['t', 'Собирайтесь в первую пятёрку к 13–15 уровню.']],
    src: ['camp', 'legacy', 'dung'] },
  { id: 'dung', n: 'Подземелья', sub: 'уровни 15–40', lo: 15, hi: 40,
    todo: [['f', 'Основной опыт за подземелье дают его цепочки заданий. Повторные заходы после них приносят заметно меньше опыта, чем задания в мире.'],
      ['f', 'Любая выпавшая вещь открывает свой облик для трансмогрификации всем, кто может её надеть, даже если вещь досталась другому.'],
      ['f', 'На 25 уровне открывается Legacy.'],
      ['t', 'Соберите задания подземелья всей группой заранее и идите, когда они есть у каждого.']],
    prof: [['f', 'Кулинария 140 даёт 5 мест в лагере, 220 даёт 10.'],
      ['f', 'Каждая профессия делает три объекта лагеря, по одному на уровень. Навык для 2 и 3 уровня у источников расходится.'],
      ['t', 'Если до 25 уровня далеко, доведите ремесло до 150: Legacy откроется раньше.']],
    legacy: [['f', 'Каждое испытание даёт 1 очко. Всего их 65: классы 27, профессии 18, PvP 12, подземелья 3, рейды 3, приключения 2.'],
      ['t', 'Ценны Reagent Economy (без покупных реагентов для способностей) и Field Guide (короче откат объектов лагеря).']],
    group: [['f', 'Подземелье рассчитано на 5 игроков: танк, лекарь и трое с уроном.'],
      ['f', 'Масштабирования уровней нет, поэтому сильно отставшему другу в подземелье будет тяжело.'],
      ['t', 'Держите уровни близко: отставшие догоняют на заданиях, подземелья проходите вместе.']],
    src: ['dung', 'camp', 'legacy'] },
  { id: 'path', n: 'Путь к 60', sub: 'уровни 40–60', lo: 40, hi: 60,
    todo: [['f', 'Скакун с 40 уровня (скорость 60%), быстрый с 60 (100%). Учиться у тренера своей расы.'],
      ['f', 'Паладин и чернокнижник получают скакуна заданиями класса.'],
      ['f', 'Почёт у своей фракции даёт скидку 10% на обучение езде и скакунов. По Warcraft Tavern: 100 + 20 золотых на 40 уровне, 1000 + 200 на 60.'],
      ['t', 'Отложите золото к 40 уровню: езда будет самой крупной тратой на пути к 60.']],
    prof: [['f', 'Объекты лагеря 2 и 3 уровня у каждой профессии свои. У Инженерного дела второй объект Ремонтный робот чинит экипировку.'],
      ['t', 'Держите в группе Кулинарию 220 ради лагеря на 10 объектов: к рейду места хватит всем.']],
    legacy: [['f', 'На персонажа не больше 16 очков, лишние идут в трек наград: игрушка за 15, питомец за 25, табард за 40, скакун за 55.']],
    group: [['f', 'Рейды откроются 09.12: Barrow Deeps на 10 игроков, Вершина Хиджала на 20, Логово Ониксии на 40.'],
      ['t', 'Для 10-местного рейда нужно 10 игроков: если вас меньше, найдите недостающих в гильдии заранее.']],
    src: ['ride', 'prof', 'legacy', 'cwg'] },
  { id: 'raid', n: '60 и рейды', sub: 'с 09.12', lo: 60, hi: 60,
    todo: [['f', '09.12 открываются Barrow Deeps (10 игроков), Вершина Хиджала (20) и Логово Ониксии (40, Пылевые топи).'],
      ['f', 'За прохождение каждого из трёх рейдов даётся очко Legacy.'],
      ['f', 'Новое поле боя 15 на 15: Darkspear Islands у побережья Пылевых топей.'],
      ['t', 'Пока набираете людей на рейд, проходите подземелья 60 уровня за экипировкой.']],
    prof: [['f', 'Баффы лагеря немного слабее классовых и не складываются с ними: Благословение королей даёт 10% ко всем характеристикам, лагерь 8%.'],
      ['t', 'Ставьте лагерь у входа в рейд: его баффы закроют то, чего нет у ваших классов.']],
    legacy: [['f', 'Испытания для 60 уровня: подземелья 3, рейды 3, PvP 12. В PvP звания с недельным лимитом и улучшение экипировки за Честь.']],
    group: [['f', 'Одинаковые баффы двух игроков одного класса перекрываются, разные классы складываются.'],
      ['t', 'Соберите рейдовый состав в конструкторе и пошлите ссылку в чат.']],
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
  if (now < D_REL) return ['pre', 'Выбрано по дате: до релиза 04.11.'];
  if (me.lvl) return [me.lvl < 15 ? 'first' : me.lvl < 40 ? 'dung' : me.lvl < 60 ? 'path' : 'raid', 'Выбрано по уровню вашего персонажа.'];
  if (now >= D_RAID) return ['raid', 'Выбрано по дате: рейды открыты.'];
  return [now < new Date('2026-11-11T00:00:00') ? 'first' : 'dung', 'Выбрано по дате. Укажите уровень персонажа, и этап подстроится.'];
}
const START = { pre: 'hero_dawn-960', first: 'hero_campfire-960', dung: 'warlock-360', path: 'hunter-360', raid: 'paladin-360' };
const ARTV = /*ARTV*/{"hero_campfire-960.avif":"?v=2654726f","hero_campfire-960.webp":"?v=d73f1e16","hero_dawn-960.avif":"?v=72b3acf6","hero_dawn-960.webp":"?v=4eae2c5c"};   // ?v= of the scene arts, filled in by build.art_version (same names, redrawn pictures)
const pic = f => `<picture><source type="image/avif" srcset="${ROOT}assets/art/${f}.avif${ARTV[f + '.avif'] || ''}"><img src="${ROOT}assets/art/${f}.webp${ARTV[f + '.webp'] || ''}" alt="" loading="lazy" decoding="async"></picture>`;
const tipL = () => '<span class="tl">Совет</span>';
function liC(x) { return x[0] === 't' ? `<li class="tip">${tipL()}${esc(x[1])}</li>` : `<li>${esc(x[1])}</li>`; }
function dLi(d) {
  const mine = me.lvl && nearLvl(d, me.lvl);
  return `<li class="${mine ? 'mine' : ''}"><b>${esc(d[0])}</b><span class="lvl${mine ? ' gold' : ''}">${lvRange(d)}</span><span class="z">${esc(d[3])}${d[4] ? ' · <i>новое</i>' : ''}${mine ? '<span class="sr"> · под ваш уровень</span>' : ''}</span></li>`;
}
function renderStage() {
  const [auto, why] = autoStage();
  if (stageAuto) stageSel = auto;
  const s = ST[stageSel];
  $('#stageBar').innerHTML = STAGES.map(x => `<button type="button" class="stile" role="tab" id="tab-${x.id}" data-st="${x.id}" aria-controls="stagePanel" aria-selected="${x.id === stageSel}" tabindex="${x.id === stageSel ? 0 : -1}">${pic(START[x.id])}<b>${esc(x.n)}</b><span class="lv">${esc(x.sub)}${x.id === auto ? ' · <span class="now">сейчас</span>' : ''}</span></button>`).join('');
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
  $('#stagePanel').innerHTML = `<div class="st-head"><div class="t"><h3>${esc(s.n)}</h3><span class="when">${esc(s.sub)}</span></div><p class="why">${stageAuto ? esc(why) : 'Этап выбран вручную.'}</p></div>
    <ol class="steps-c">${steps}</ol>
    <div class="st-cols">
      <div><h4>Подземелья под уровень</h4>${s.dnote ? `<p class="small" style="margin:-4px 0 10px">${esc(s.dnote)}</p>` : ''}<ul class="dlist">${ds.slice(0, MAXD).map(dLi).join('')}</ul>
        <a class="more-l" href="guides/dungeons/">${extra > 0 ? `Ещё подземелий в таблице: ${extra}` : 'Все 35 подземелий'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>
      <div style="display:grid;gap:24px;align-content:start"><div><h4>Профессии и лагерь</h4><ul class="clean">${s.prof.map(liC).join('')}</ul></div>
        <div><h4>Перки Legacy</h4><ul class="clean">${s.legacy.map(liC).join('')}</ul></div></div>
    </div>
    <div class="gtip"><h4 style="margin:0 0 10px;font-size:var(--fs-16)">Советы группе</h4><ul class="clean">${s.group.map(liC).join('')}</ul></div>
    <p class="st-src"><span>Источники:</span>${s.src.map(k2 => `<a href="${SRC[k2][1]}" target="_blank" rel="noopener">${esc(SRC[k2][0])}</a>`).join('')}</p>`;
}
function optList(items, cur, none) { return `<option value="">${esc(none)}</option>` + items.map(([v, t]) => `<option value="${v}"${v === cur ? ' selected' : ''}>${esc(t)}</option>`).join(''); }
function renderMe() {
  fixMe();
  const races = f => RACES.filter(r => r.f === f).map(r => `<option value="${r.id}"${r.id === me.race ? ' selected' : ''}>${esc(r.n)}</option>`).join('');
  $('#meRace').innerHTML = `<option value="">Не выбрана</option><optgroup label="${facName('alliance')}">${races('alliance')}</optgroup><optgroup label="${facName('horde')}">${races('horde')}</optgroup>`;
  const cls = (me.race ? Object.keys(RC[me.race].can) : CLASSES.map(c => c.id)).map(id => [id, CL[id].n]);
  $('#meCls').innerHTML = optList(cls, me.cls, 'Не выбран');
  $('#meRole').innerHTML = me.cls ? roleOpts(CL[me.cls]).map(x => `<option value="${x}"${x === me.role ? ' selected' : ''}>${ROLE_RU[x]}</option>`).join('') : `<option value="">Сначала класс</option>`;
  $('#meRole').disabled = !me.cls;
  const prim = PROFS.filter(p => p[2]);
  $('#meP1').innerHTML = optList(prim.filter(p => p[0] !== me.p2).map(p => [p[0], p[1]]), me.p1, 'Нет');
  $('#meP2').innerHTML = optList(prim.filter(p => p[0] !== me.p1).map(p => [p[0], p[1]]), me.p2, 'Нет');
  $('#meSec').innerHTML = PROFS.filter(p => !p[2]).map(p => `<button type="button" data-sec="${p[0]}" aria-pressed="${me.sec.includes(p[0])}">${esc(p[1])}</button>`).join('');
  document.querySelectorAll('.lvin').forEach(i => { if (document.activeElement !== i) i.value = me.lvl || ''; });
  const who = [me.race ? RC[me.race].n : '', me.cls ? CL[me.cls].n : ''].filter(Boolean).join(' · ');
  const sub = me.cls ? [ROLE_RU[me.role], me.race ? facName(RC[me.race].f) : ''].filter(Boolean).join(' · ') : 'Выберите расу, класс и уровень ниже';
  const hero = $('#meHero');
  hero.style.setProperty('--cc', me.cls ? CCOL[me.cls] : '#c9a54a');
  hero.innerHTML = pic(me.cls ? `${me.cls}-600` : 'hero_campfire-960') + (me.lvl ? `<span class="lvb" aria-label="Уровень ${me.lvl}">${me.lvl}</span>` : '')
    + `<span class="k">Мой персонаж</span><b>${who ? esc(who) : 'Ещё не создан'}</b><span class="s">${esc(sub)}</span>`;
  let out = '';
  if (meSet()) {
    const b = [];
    if (me.cls) b.push(BUFF[me.cls] ? `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span><b>${esc(CL[me.cls].n)}:</b> ${esc(BUFF[me.cls])}</span></li>` : `<li><span class="bi" style="--cc:${CCOL[me.cls]}"><svg class="ico" aria-hidden="true"><use href="#i-dps"/></svg></span><span>${esc(CL[me.cls].n)}: без группового баффа, чистый урон.</span></li>`);
    [me.p1, me.p2, ...me.sec].filter(Boolean).forEach(id => { const p = PR[id]; b.push(`<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-fire"/></svg></span><span><b>${esc(p[3])}</b> <span class="m">· ${esc(p[1])}</span><br>${esc(p[4])}</span></li>`); });
    if (!b.length) b.push('<li><span class="bi"><svg class="ico" aria-hidden="true"><use href="#i-sun"/></svg></span><span>Выберите класс и профессии, чтобы увидеть баффы.</span></li>');
    out += `<div><h4>Что вы приносите группе</h4><ul class="buffs">${b.join('')}</ul></div>`;
    if (me.lvl) {
      const ds = DUNGEONS.filter(d => nearLvl(d, me.lvl) && facOk(d, me.race && RC[me.race].f));
      out += `<div><h4>Подземелья под ваш уровень</h4>` + (ds.length ? `<ul class="dlist">${ds.slice(0, 4).map(dLi).join('')}</ul>` : '<p class="small">Первые подземелья с 13 уровня.</p>')
        + `<a class="more-l" href="guides/dungeons/">${ds.length > 4 ? `Ещё подземелий в таблице: ${ds.length - 4}` : 'Таблица подземелий'}<svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg></a></div>`;
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
