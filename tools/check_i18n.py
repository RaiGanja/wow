"""Проверка перевода нового языка: i18n/<lang>.json против заготовки (python build.py --missing <lang> > todo.json).
Ошибки: пропущенные или пустые строки, кавычки/скобки, которых нет в английском, кириллица, потерянные {подстановки}
и ${…}, другие пробелы по краям. Предупреждения: числа не совпадают, перевод сильно длиннее короткой строки меню,
английское название из names.json не заменено официальным.
Запуск: python tools/check_i18n.py <lang> <todo.json>"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import langs  # noqa: E402

SUBST = re.compile(r'\$\{[^}]*\}|\{\w+\}')
NUM = re.compile(r'\d+')
CYR = re.compile(r'[А-Яа-яЁёІіЇїЄєҐґ]')


def check(lang, todo, tr):
    errors, warns = [], []
    for en in todo:
        x = tr.get(en)
        if not x or not x.strip():
            errors.append(f'нет перевода: {en[:80]!r}')
            continue
        if not langs.check_chars(en, x):
            errors.append(f"символы ' \" ` < > {{ }} не из исходника: {x[:80]!r}")
        if CYR.search(x):
            errors.append(f'кириллица: {x[:80]!r}')
        if sorted(SUBST.findall(en)) != sorted(SUBST.findall(x)):
            errors.append(f'подстановки {SUBST.findall(en)} -> {SUBST.findall(x)}: {x[:80]!r}')
        if (en[:1].isspace(), en[-1:].isspace()) != (x[:1].isspace(), x[-1:].isspace()):
            errors.append(f'пробелы по краям: {en!r} -> {x!r}')
        if sorted(NUM.findall(en)) != sorted(NUM.findall(x)):
            warns.append(f'числа {NUM.findall(en)} -> {NUM.findall(x)}: {x[:80]!r}')
        if len(en) <= 25 and len(x) > max(2 * len(en), len(en) + 14):
            warns.append(f'длинно для меню: {en!r} -> {x!r}')
        if lang in langs.NAMED:
            for name, loc in langs.NAMES.items():
                off = loc.get(lang)
                if off and off != name and len(name) > 3 and re.search(r'\b' + re.escape(name) + r'\b', en) \
                        and name not in x and off not in x:
                    warns.append(f'название {name!r} -> официально {off!r}: {x[:80]!r}')
    extra = [k for k in tr if k not in todo and k not in (langs.OV.get(lang) or {})]
    return errors, warns, extra


def main():
    lang, todo_path = sys.argv[1], sys.argv[2]
    todo = json.load(open(todo_path, encoding='utf-8'))
    tr = json.load(open(os.path.join(ROOT, 'i18n', f'{lang}.json'), encoding='utf-8'))
    errors, warns, extra = check(lang, todo, tr)
    sys.stdout.reconfigure(encoding='utf-8')
    for e in errors:
        print('ERROR', e)
    for w in warns:
        print('WARN ', w)
    print(f'{lang}: {len(todo)} строк, ошибок {len(errors)}, предупреждений {len(warns)}, лишних ключей {len(extra)}')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
