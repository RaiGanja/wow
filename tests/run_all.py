"""Все проверки одной командой (после python build.py): python tests/run_all.py [--live]"""
import glob, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, PYTHONUTF8='1')
runs = [[f] for f in sorted(glob.glob(os.path.join(HERE, 'test_*.py')))] + [[os.path.join(HERE, 'check_site.py')] + sys.argv[1:]]
failed = []
for args in runs:
    r = subprocess.run([sys.executable] + args, env=env, capture_output=True, text=True, encoding='utf-8')
    out = (r.stdout + r.stderr).strip().splitlines()
    print(f'{"OK  " if r.returncode == 0 else "FAIL"} {os.path.basename(args[0])}: {out[-1] if out else ""}')
    if r.returncode:
        failed.append(args[0])
        print('\n'.join(out[-15:]))
sys.exit(1 if failed else 0)
