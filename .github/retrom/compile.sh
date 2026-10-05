#!/usr/bin/env bash
set -euo pipefail
cd /work
export SOURCE_DATE_EPOCH=1779944524
emmake make -C src/burner/libretro platform=emscripten CC=emcc CXX=em++ AR=emar -j8
emcc -O3 -c .github/retrom/content-load.c -o .cache/content-load.o
cp src/burner/libretro/fbneo_libretro_emscripten.bc .cache/retroarch/libretro_emscripten.bc
emmake make -C .cache/retroarch -f Makefile.emulatorjs -f /work/.github/retrom/link.mk LIBRETRO=fbneo HAVE_THREADS=0 HAVE_CHD=0 HAVE_OPENGLES3=0 HAVE_AL=1 HAVE_RWEBAUDIO=0 ASYNC=1 GIT_VERSION=6dd4353937ef48b6ec0bfbdbb15d1c5992d86927 -j8
