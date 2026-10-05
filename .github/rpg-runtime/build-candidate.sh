#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
output=${1:?output required}
cd "$root"
test ! -L "$output"
mkdir -p "$output"
output=$(realpath "$output")
python3 .github/rpg-runtime/candidate_descriptor.py prepare "$output"
python3 .github/retrom/prepare.py
cc -std=c11 -Wall -Wextra -Werror .github/retrom/content-load-test.c .github/retrom/content-load.c -o .cache/content-load-test
.cache/content-load-test
docker run --rm --user "$(id -u):$(id -g)" \
  -e EM_CACHE=/work/.cache/emscripten -v "$root:/work" -w /work \
  emscripten/emsdk@sha256:90b757eb11fa9a0e3ce4d2d9f76d932a56018e4accc37b5a28b2783751e60eb7 \
  bash .github/retrom/compile.sh
python3 .github/rpg-runtime/package.py "$output"
