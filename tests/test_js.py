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
import re, tempfile
for page in ('tools', 'roster'):   # inline scripts of the pages built from *.src.html (their template strings are not in assets/)
    html = open(os.path.join(ROOT, page, 'index.html'), encoding='utf-8').read()
    for k, body in enumerate(re.findall(r'<script(?![^>]*src=)(?![^>]*type="(?:application/ld\+json|importmap)")[^>]*>(.*?)</script>', html, re.S)):
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(body)
        ok = subprocess.run(['node', '--check', f.name], capture_output=True).returncode == 0
        os.unlink(f.name)
        assert ok, f'syntax error in an inline script of {page}/index.html (#{k})'
print('OK', len(files), 'scripts,', len(tracked), 'files')
