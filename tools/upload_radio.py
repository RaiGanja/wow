"""Upload the radio tracks (.m4a made by tools/make_radio.py) to the Cloudflare R2 bucket that serves MEDIA (media.gabella.site).
Only files not uploaded yet (or changed since) are sent; the list of uploaded files is kept as uploaded.json in the tracks folder.
Needs a logged-in wrangler (npx wrangler login).
Run: python tools/upload_radio.py <tracks folder>"""
import concurrent.futures, json, os, subprocess, sys

BUCKET = 'gabella-media'
PREFIX = 'radio/'
CACHE = 'public, max-age=2592000'
NPX = 'npx.cmd' if os.name == 'nt' else 'npx'


def put(folder, name):
    r = subprocess.run([NPX, 'wrangler', 'r2', 'object', 'put', f'{BUCKET}/{PREFIX}{name}', '--file', os.path.join(folder, name),
                        '--content-type', 'audio/mp4', '--cache-control', CACHE, '--remote'], capture_output=True, text=True)
    return name, r.returncode, (r.stderr or r.stdout).strip().splitlines()[-1:] if r.returncode else []


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
    log = os.path.join(folder, 'uploaded.json')
    done = json.load(open(log, encoding='utf-8')) if os.path.exists(log) else {}
    files = sorted(f for f in os.listdir(folder) if f.endswith('.m4a'))
    todo = [f for f in files if done.get(f) != os.path.getsize(os.path.join(folder, f))]
    print(f'{len(files)} tracks, {len(todo)} to upload')
    failed = []
    with concurrent.futures.ThreadPoolExecutor(6) as ex:
        for i, (name, code, err) in enumerate(ex.map(lambda f: put(folder, f), todo), 1):
            if code:
                failed.append(name)
                print('FAIL', name, *err)
            else:
                done[name] = os.path.getsize(os.path.join(folder, name))
                print(f'{i}/{len(todo)} {name}')
            if i % 20 == 0:
                json.dump(done, open(log, 'w', encoding='utf-8'), indent=0)
    json.dump(done, open(log, 'w', encoding='utf-8'), indent=0)
    sys.exit(f'{len(failed)} failed' if failed else 0)


if __name__ == '__main__':
    main()
