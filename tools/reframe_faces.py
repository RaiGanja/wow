"""Re-cut the 18 class faces (<class>-<race>-face.webp) from the 1344 px portraits in assets/art by the standard of
make_images.FACE_FIT. The masters are not needed: the portrait files have the same frame."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_images as M

for name in M.FACE_FIT:
    M.face(os.path.join(M.OUT, f'{name}-1344.webp'), name)
    print(name, 'ok')
