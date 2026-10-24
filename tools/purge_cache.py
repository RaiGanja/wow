"""Сброс кэша Cloudflare после выкатки: Cloudflare держит HTML гида (Cache Rule на /wow/), поэтому изменённые
адреса надо выбросить из кэша, как только GitHub Pages собрал новый коммит. Зовёт .github/workflows/purge.yml.
  python tools/purge_cache.py <база> <старый коммит> <новый коммит>   — адреса файлов, изменённых между коммитами
  python tools/purge_cache.py <база> --all                            — весь сайт (Purge Everything зоны)
  --dry — показать адреса, ничего не трогать.
<база> — https://gabella.site/wow/. Нужны переменные CF_API_TOKEN (права Zone → Cache Purge) и CF_ZONE_ID;
без них — пропуск (выкатка не должна падать из-за кэша).
После сброса скрипт сверяет главные страницы на живом с файлами коммита: GitHub Pages сам кэширует ответы
(max-age=600), и первый запрос после сброса может унести в Cloudflare старую страницу. Тогда — пауза и новый сброс."""
import hashlib, json, os, subprocess, sys, time, urllib.request

API = 'https://api.cloudflare.com/client/v4/zones/{zone}/purge_cache'
BATCH = 30                 # адресов в одном запросе: столько принимает любой тариф
CHECK = 5                  # сколько изменённых страниц сверять с коммитом
TRIES, PAUSE = 8, 75       # до ~10 минут: столько GitHub Pages держит свою копию
UA = 'Mozilla/5.0 (gabella-purge)'   # без User-Agent Cloudflare отвечает 403


def changed(old, new):
    out = subprocess.run(['git', 'diff', '--name-only', old, new], capture_output=True, text=True, check=True).stdout
    return [p for p in out.split() if not p.startswith(('.github/', 'tools/', 'tests/', 'content/', 'i18n/'))
            and not p.endswith(('.py', '.src.html', '.src.css', '.src.js', '.md'))]


def url(base, path):
    return base + (path[:-len('index.html')] if path == 'index.html' or path.endswith('/index.html') else path)


def call(body):
    req = urllib.request.Request(API.format(zone=os.environ['CF_ZONE_ID']), data=json.dumps(body).encode(), method='POST',
                                 headers={'Authorization': 'Bearer ' + os.environ['CF_API_TOKEN'],
                                          'Content-Type': 'application/json', 'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        ok = json.load(r).get('success')
    if not ok:
        raise SystemExit('purge: Cloudflare ответил ошибкой')


def purge(urls):
    for i in range(0, len(urls), BATCH):
        call({'files': urls[i:i + BATCH]})
    print(f'purge: сброшено {len(urls)} адресов')


def live(u):
    req = urllib.request.Request(u, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return hashlib.sha256(r.read()).hexdigest()


def committed(rev, path):
    return hashlib.sha256(subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, check=True).stdout).hexdigest()


def main(argv):
    dry = '--dry' in argv
    args = [a for a in argv if a != '--dry']
    base = args[0]
    if not dry and not (os.environ.get('CF_API_TOKEN') and os.environ.get('CF_ZONE_ID')):
        print('purge: нет CF_API_TOKEN / CF_ZONE_ID — пропуск')
        return 0
    if args[1:] == ['--all']:
        print('purge: весь сайт')
        if not dry:
            call({'purge_everything': True})
        return 0
    old, new = args[1], args[2]
    if subprocess.run(['git', 'cat-file', '-e', old + '^{commit}']).returncode:
        print(f'purge: нет коммита {old} — сбрасываю весь сайт')
        if not dry:
            call({'purge_everything': True})
        return 0
    paths = changed(old, new)
    urls = [url(base, p) for p in paths]
    print(f'purge: {len(urls)} адресов')
    for u in urls:
        print(' ', u)
    if not urls or dry:
        return 0
    exists = lambda p: not subprocess.run(['git', 'cat-file', '-e', f'{new}:{p}'], capture_output=True).returncode
    pages = [p for p in paths if p.endswith('.html') and exists(p)][:CHECK]
    for attempt in range(TRIES):
        purge(urls)
        time.sleep(5)
        stale = [p for p in pages if live(url(base, p)) != committed(new, p)]
        if not stale:
            print('purge: на живом новые страницы')
            return 0
        print(f'purge: ещё старые ({attempt + 1}/{TRIES}):', ' '.join(stale))
        time.sleep(PAUSE)
    print('purge: страницы так и не обновились — проверить вручную (Cloudflare → Caching → Purge Everything)')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
