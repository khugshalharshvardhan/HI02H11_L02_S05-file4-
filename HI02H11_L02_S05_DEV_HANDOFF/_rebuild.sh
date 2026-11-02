#!/bin/bash
# one command: runner embed -> engine inject -> lesson build
cd "$(dirname "$0")"
export PYTHONUTF8=1
python 1_SPEC/embed_matra_runner.py >/dev/null || exit 1
python 4_ENGINE/inject_train.py | tail -1 || exit 1
python 1_SPEC/build_skill_HI02H11_L02_S05.py 2>&1 | grep -v "^  ->" | grep -E "X |!!|html:" 
