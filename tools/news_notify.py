"""Notice to the owner: Discord webhook of the closed 📝notes channel (secret SITE_WEBHOOK_NOTES), fallback e-mail via Resend
(secret RESEND_API_KEY, variables NOTIFY_TO and NOTIFY_FROM). No Russian services. Secret values are never printed:
the log says only which channel was used and the HTTP status.

    python tools/news_notify.py --title "…" --text "…" [--url https://…]      (reads the secrets from the environment)"""
import argparse, json, os, sys, urllib.request

UA = {'User-Agent': 'gabella-wow-guide (+https://gabella.site/wow/)', 'Content-Type': 'application/json'}


def post(url, body, headers=None):
    req = urllib.request.Request(url, method='POST', data=json.dumps(body).encode('utf-8'), headers={**UA, **(headers or {})})
    try:
        return urllib.request.urlopen(req, timeout=20).status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:          # noqa: BLE001  (no network: the status says it, the text of the error may hold the address)
        return 0


def discord_body(title, text, url=None):
    return {'username': 'Gabella news', 'allowed_mentions': {'parse': []},
            'embeds': [{'title': title[:250], 'description': text[:3900], **({'url': url} if url else {}), 'color': 0xC9A54A}]}


def notify(title, text, url=None, env=None):
    env = env if env is not None else os.environ
    hook = env.get('SITE_WEBHOOK_NOTES')
    if hook:
        st = post(hook + ('&' if '?' in hook else '?') + 'wait=true', discord_body(title, text, url))
        print(f'discord: {st}')
        if 200 <= st < 300:
            return 'discord'
    key, to = env.get('RESEND_API_KEY'), env.get('NOTIFY_TO')
    if key and to:
        st = post('https://api.resend.com/emails', {'from': env.get('NOTIFY_FROM') or 'Gabella <news@gabella.site>', 'to': [to],
                                                    'subject': title[:150], 'text': text + (f'\n\n{url}' if url else '')},
                  {'Authorization': f'Bearer {key}'})
        print(f'resend: {st}')
        if 200 <= st < 300:
            return 'resend'
    print('notice not sent: no channel (SITE_WEBHOOK_NOTES or RESEND_API_KEY + NOTIFY_TO)')
    return None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--title', required=True)
    ap.add_argument('--text', default='')
    ap.add_argument('--text-file')
    ap.add_argument('--url')
    a = ap.parse_args(argv)
    text = open(a.text_file, encoding='utf-8').read() if a.text_file else a.text
    notify(a.title, text, a.url)
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
