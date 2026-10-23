#!/usr/bin/env bash
# Upload the radio tracks (.m4a made by tools/make_radio.py) to the Cloudflare R2 bucket behind MEDIA (media.gabella.site).
# Only files not uploaded yet (or changed since) are sent; uploaded.txt in the tracks folder lists "name size" of each.
# Needs a logged-in wrangler (npx wrangler login). Run from bash (Git Bash on Windows): tools/upload_radio.sh <tracks folder>
set -u
dir=${1:?usage: tools/upload_radio.sh <tracks folder>}
log="$dir/uploaded.txt"; touch "$log"
put() {
  local f=$1 name size
  name=$(basename "$f"); size=$(stat -c %s "$f")
  grep -qx "$name $size" "$log" && return 0
  if npx wrangler r2 object put "gabella-media/radio/$name" --file "$f" --content-type audio/mp4 \
       --cache-control 'public, max-age=2592000' --remote > /dev/null 2>&1; then
    echo "$name $size" >> "$log"; echo "ok $name"
  else
    echo "FAIL $name"
  fi
}
export -f put; export log
ls "$dir"/*.m4a | xargs -P 6 -I{} bash -c 'put "$@"' _ {}
echo "uploaded: $(sort -u "$log" | wc -l) of $(ls "$dir"/*.m4a | wc -l)"
