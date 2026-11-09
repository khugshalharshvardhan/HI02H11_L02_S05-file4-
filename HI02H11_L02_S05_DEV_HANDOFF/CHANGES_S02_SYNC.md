# HI02H11_L02_S05 — S02's 7 QA-pass commits applied (2026-10-22)

S05 was forked from HI02H11_L02_S02 at `992e684` (measured: every other S02 commit is further from
S05's engine). S02 has since QA-passed 7 more commits (`fb835c9 … 27cea22`): bugs 1-8 + 2 more rounds,
the new transition screen (`phaseBlurTransition`, Swifty `peeking_talk_up.webp`, `sfx_whoosh`), background
music to 30%, and a proper 7 s inactivity nudge. The same commits were applied to S03 (file 3).

**S05's own screens and their deck order are unchanged** (user's choice). Everything S05 added on top of
S02 is kept: drawn ◌ं / ◌ः signs, the names screen, `sign_mode`, picture-less words, the सुनाई-lock fix
for the cover greeting, the practice hand switched off.

| File | How |
|---|---|
| `4_ENGINE/train_modules.js` | 3-way merge (S02 992e684 → 27cea22 onto S05): clean |
| `4_ENGINE/train_styles.css` | 3-way merge: one overlap at the end of the file — both blocks kept (S05's ◌ं/◌ः rules + S02's QA rules) |
| `4_ENGINE/lesson_template.html` | 3-way merge with the injected blocks set aside: clean (S05's sound-lock fix kept), then modules re-injected |
| `1_SPEC/build_skill_HI02H11_L02_S05.py` | 3-way merge: two overlaps — S02's whoosh + new gate taken, S05's no-practice-hand note kept; the old gate lip-sync step removed as in S02 |
| new assets | `3_BUILD/assets/Audio/sfx_whoosh.ogg`, `3_BUILD/assets/UI/peeking_talk_up.webp` |

**Checks:** all 374 lines S02 added in the 7 commits are present in S05's engine; the build passes every
guard (16 fixed clips incl. the whoosh); all 16 screens mount with 0 console errors; the three transitions
match S02's; page 1's ◌ं / ◌ः sit inside their cards.

**Git:** `3_BUILD/.env` and `_v1_factory_build/3_BUILD/.env` (the Gemini key) are untracked (staged, local
copies kept; `.gitignore` already ignores them). The key is still in the pushed `first commit`, so rotate it.

Pre-merge copies of every replaced file: `../_backup_pre_s02_7commits_2026-10-22/`.

## 2026-11-09 — S03 QA fixes ported (BUG_02, 03, 04, 05)

Same engine as S03, same bugs; ported from file 3.
- **BUG_02 (P3, P4 sentence screens):** `4_ENGINE/train_modules.js` — during the rung-3 hand nudge the speaker plays the page's rung-3 line (`vo_p3_h3` / `vo_p4_h3`) instead of the prompt. Before the nudge it is unchanged (prompt + sentence).
- **BUG_03 (cover):** `4_ENGINE/lesson_template.html` — the सुनो speaker ignores taps until the train has arrived, so the greeting no longer plays twice. Look unchanged.
- **BUG_04 (G5D, G5, G4, P2 coach sorts):** `_zoneAt()` skips drop zones inside a greyed-out coach (`.is-off`): after the 3rd wrong drop the wrong coach does not light up or take the card; the card glides back (no shake, not counted).
- **BUG_05 (P3, P4):** new per-slide hook `state.idleReplay`; during the rung-3 hand nudge the 7 s reminder re-shows the hand with no voice line.
- Rebuilt with `_rebuild.sh`. Verified muted: targeted tests on every affected screen + full mechanics playthrough (exit 0, 0 console errors).
