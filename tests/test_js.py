"""Скрипты сайта разбираются браузером: нет следов слияния, sw.js и assets/**/*.js без синтаксических ошибок (node --check).
Запуск: python tests/test_js.py"""
import glob, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = [os.path.join(ROOT, 'sw.js')] + glob.glob(os.path.join(ROOT, 'assets', '**', '*.js'), recursive=True)
tracked = subprocess.run(['git', 'ls-files', '*.py', '*.js', '*.html', '*.css', '*.json', '*.txt', '*.webmanifest', '*.xml'],
                         cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout.split()
marked = [f for f in tracked if any(l.startswith(('<<<<<<< ', '>>>>>>> ')) for l in open(os.path.join(ROOT, f), encoding='utf-8', errors='replace'))]
assert not marked, f'merge conflict markers: {marked[:10]}'
bad = [f for f in files if subprocess.run(['node', '--check', f], capture_output=True).returncode]
assert not bad, f'syntax errors: {bad}'
print('OK', len(files), 'scripts,', len(tracked), 'files')
