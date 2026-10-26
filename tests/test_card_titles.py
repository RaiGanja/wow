"""Названия классов и рас не обрезаны и не шире карточки: на главной (вкладки «Классы» и «Расы») в 9 языках, на 6 ширинах,
у каждой раскрытой карточки, плюс вертикальные подписи закрытых. Нужен собранный сайт (python build.py) и Chrome.
Проверяет tests/clip_probe.mjs: headless Chrome по CDP открывает страницы и сверяет рамки каждого текстового узла с
ближайшим предком, который режет содержимое. Нет Chrome — тест пропускается (CHROME=путь указывает браузер).
Запуск: python tests/test_card_titles.py [--themes light,dark] [--widths 375,1380]"""
import functools, http.server, os, shutil, subprocess, sys, threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMES = [os.environ.get('CHROME', ''), r'C:\Program Files\Google\Chrome\Application\chrome.exe',
           r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser']
if not any(c and os.path.exists(c) for c in CHROMES) or not shutil.which('node'):
    print('SKIP: нужны Chrome и node')
    sys.exit(0)


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{srv.server_port}'
cmd = ['node', os.path.join(ROOT, 'tests', 'clip_probe.mjs'), '--base', base, '--fast',
       '--pages', 'home', '--widths', arg('--widths', '375,768,1024,1380,1920,3440'), '--themes', arg('--themes', 'light')]
r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
srv.shutdown()
out = (r.stdout + r.stderr).strip()
assert r.returncode == 0, 'названия карточек обрезаны или вылезают:\n' + '\n'.join(out.splitlines()[-40:])
print('OK', out.splitlines()[-1])
