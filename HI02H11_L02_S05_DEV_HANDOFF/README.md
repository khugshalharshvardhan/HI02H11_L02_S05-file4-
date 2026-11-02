# HI02H11_L02_S05: «मात्राओं की रेल» (अं / अः)

The S02 (उ / ऊ) lesson forked to अं / अः. Engine, layout, animation, train, gate Swifty,
celebration and runner game are S02's. The content follows the SME deck in `1_SPEC/`.
**Read `CHANGES.md` first:** every deck ask, with its status.

## Run

```bash
cd 3_BUILD && python -m http.server 8905
# open http://127.0.0.1:8905/HI02H11_L02_S05.html (over http, not as a file)
```

## Rebuild

```bash
./_rebuild.sh        # runner embed -> 4_ENGINE/inject_train.py -> 1_SPEC/build_skill_HI02H11_L02_S05.py
```

Content lives in `1_SPEC/build_skill_HI02H11_L02_S05.py`. The runner's words are in
`1_SPEC/matra_runner_src/index.html` (`POOL_U` = अं targets, `POOL_UU` = अः distractors). Engine
changes go in `4_ENGINE/train_modules.js` / `train_styles.css`; S05 additions are tagged `[S05]`.
Never hand-edit the built HTML.

## Voice-over

```bash
cd 3_BUILD && export $(grep -v '^#' .env | grep -v '^$' | xargs)
python <swiftpal-game-revise>/scripts/build/gen_tts.py card.json --voice Leda --ext ogg
cd .. && ./_rebuild.sh       # re-measures every timing cue from the new clips
```

The builder deletes the clips whose text changed, so gen_tts re-records only those. Runner clips:
put WAVs in `1_SPEC/game_art_src/runner_voice/source_wav/<id>.wav`, then run
`python 1_SPEC/prepare_runner_voice.py <ids>`.

## Folders

| | |
|---|---|
| `1_SPEC/` | SME deck + verbatim notes, the builder, runner source, helper scripts |
| `3_BUILD/` | the lesson (HTML + card.json + assets) |
| `4_ENGINE/` | the pinned engine copy and train modules (S02's, plus `[S05]` additions) |
| `celebration_kit/` | the lip-synced celebration Swifty (from S02) |
| `5_CURRENT_BUILD_SCREENSHOTS/` | every screen of this build |
| `_v1_factory_build/` | the original factory draft, kept for reference |
