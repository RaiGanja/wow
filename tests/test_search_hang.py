"""Поиск не виснет на запросах из букв без латинской формы и на пустых токенах (ь, ъ, mmm): движок и подсветка в search.js.
Запуск: python tests/test_search_hang.py"""
import json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
node = shutil.which('node')
if not node:
    print('FAIL: node not found'); sys.exit(1)
JS = r"""
const fs = require('fs'), vm = require('vm'), root = process.argv[1];
const eng = fs.readFileSync(root + '/assets/search/engine.js', 'utf8');
const win = fs.readFileSync(root + '/assets/search/search.js', 'utf8');
const m = win.match(/function mark\(text, ntext, toks\) \{[\s\S]*?\n  \}\n/);
const mark = new Function('esc', m[0] + 'return mark;')(s => s);
const bad = [];
for (const lang of ['ru', 'uk', 'en', 'de']) {
  const c = {}; vm.runInNewContext(eng, c);
  const e = c.gabellaSearchEngine(lang, JSON.parse(fs.readFileSync(`${root}/assets/search/${lang}.json`, 'utf8')));
  for (const q of ['mmm', 'mmmm', 'ьььь', 'ъъъ', 'ъь', 'ь', 'ъ', 'ьъьъ']) {
    const r = e.find(q);
    for (const it of r) mark(it.t, e.norm(it.t), e.terms(r.used).flatMap(t => t.alts.flatMap(a => a.toks)));
    if (r.length > 5 && /^[ьъ]{2,}$|^m{3,}$/.test(q)) bad.push(`${lang} ${q}: ${r.length} results`);
  }
}
process.stdout.write(JSON.stringify(bad));
"""
r = subprocess.run([node, '-e', JS, ROOT], capture_output=True, text=True, encoding='utf-8', timeout=30)
if r.returncode:
    print('FAIL', r.stderr[-500:]); sys.exit(1)
bad = json.loads(r.stdout)
print('FAIL ' + '; '.join(bad) if bad else 'OK: запросы ь/ъ/mmm — без зависания и без мусорной выдачи')
sys.exit(1 if bad else 0)
