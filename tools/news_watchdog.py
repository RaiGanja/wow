"""Watchdog of the news automation: if the last run of news-auto is older than 25 minutes, open ONE issue
with label alert; when runs are back, close it with a comment. Run by the workflow news-watchdog (GITHUB_TOKEN,
no secrets). Pure logic: decide(). Test: python tests/test_news_watchdog.py"""
import json, os, urllib.request
from datetime import datetime, timezone

REPO = os.environ.get('GITHUB_REPOSITORY', 'gabella-wow/wow')
LIMIT_MIN = 25
TITLE = 'Автомат новостей молчит'
LABEL = 'alert'


def decide(now, last_run, open_issue):
    """now, last_run: aware datetimes (last_run None = no runs at all); open_issue: bool.
    Returns (action, minutes): action in 'open' | 'close' | 'none'."""
    mins = 10 ** 6 if last_run is None else int((now - last_run).total_seconds() // 60)
    if mins > LIMIT_MIN:
        return ('none' if open_issue else 'open'), mins
    return ('close' if open_issue else 'none'), mins


def api(path, method='GET', body=None):
    req = urllib.request.Request('https://api.github.com/repos/%s/%s' % (REPO, path), method=method,
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={'Authorization': 'Bearer ' + os.environ['GITHUB_TOKEN'],
                                          'Accept': 'application/vnd.github+json', 'User-Agent': 'gabella-news-watchdog'})
    with urllib.request.urlopen(req, timeout=30) as r:
        t = r.read()
        return json.loads(t) if t else None


def parse(ts):
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


def main():
    runs = api('actions/workflows/news-auto.yml/runs?per_page=1')['workflow_runs']
    last = parse(runs[0]['created_at']) if runs else None
    issues = api('issues?state=open&labels=%s&per_page=30' % LABEL)
    mine = [i for i in issues if i['title'].startswith(TITLE) and 'pull_request' not in i]
    action, mins = decide(datetime.now(timezone.utc), last, bool(mine))
    print('last run', last, 'minutes', mins, 'open issue', bool(mine), '->', action)
    if action == 'open':
        try:
            api('labels', 'POST', {'name': LABEL, 'color': 'b60205'})
        except Exception:
            pass                                    # label exists
        api('issues', 'POST', {'title': TITLE, 'labels': [LABEL],
                               'body': 'Автомат новостей молчит %d минут: последний запуск news-auto %s UTC. '
                                       'Проверить Worker gabella-news-alarm и токен.' % (mins, last)})
    elif action == 'close':
        n = mine[0]['number']
        api('issues/%d/comments' % n, 'POST', {'body': 'Запуски news-auto вернулись (последний %s UTC).' % last})
        api('issues/%d' % n, 'PATCH', {'state': 'closed', 'state_reason': 'completed'})


if __name__ == '__main__':
    main()
