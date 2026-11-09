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


## 2026-11-09 — S03 QA BUG_01 ported: start-screen speaker and play button

- **Speaker colour unchanged (reverted):** the start-screen speaker still greys out while a voice line plays, as before (Yasir r73). A first version kept it blue; the user asked to keep the grey, so that CSS was removed. Only the play-button change below remains.
- **Play button stays on replay:** `4_ENGINE/lesson_template.html` `_speakLanding` — the play button is held back for the first greeting only. Once it has appeared, replaying the greeting from the speaker leaves it on screen and pressable (pressing it stops the greeting and starts the lesson). Also when sound is locked and the button was shown at once, the first-tap greeting no longer hides it.
- Verified muted, plus BUG_03 regression and full mechanics playthrough.

- **BUG_04 follow-up (card can no longer be carried over the greyed coach):** `4_ENGINE/lesson_template.html` `makeDraggable` - after the 3rd wrong drop, the locked card (`data-only`) meets the greyed coaches as a wall: it stops at their edge (slides along it) and cannot be dragged into them at all. It can still go home or to its own coach. Other cards drag as before. Verified muted on all four sort screens (overlap with the greyed coach = 0) + full playthrough.
- **BUG_04 follow-up (greyed coach lit up under the cursor):** `4_ENGINE/train_styles.css` - the gold hover glow on coaches outranked the grey of a coach greyed out by rung 3 (`.is-off`), so on pages 6/7/11/13 the dead coach lit up when the cursor was over it and went grey again when it left. Both hover-glow rules (and the tap pages hover lift) now skip `.is-off` coaches; a greyed coach stays grey at rest, under the cursor, while a card is dragged at it, and after release. Verified muted on all four sort screens.

## 2026-11-09 — remaining S03 (file 3) fixes ported

Checked every S03 change log entry against S05. Already here: centred coach words, bigger coach labels / matra
cards, the matra-coach pulse (page 7), the pages 8-10 rung-3 speaker, the 7 s idle repeat (r150), the mic hand
(r151), the 260 px pictures, and all QA BUG_01-05 fixes. Ported now:
- **Sentence scenes (pages 14 / 15):** `4_ENGINE/train_styles.css` `.sc-scene` takes the scenes' own ~1:1 shape
  (`aspect-ratio:800/792`, was a fixed 366x288), so `object-fit:cover` no longer cuts off the top and bottom.
- **Word level with the mic (pages 4 / 6):** `4_ENGINE/train_modules.js` - the word is moved so the letters' body
  (शिरोरेखा to baseline) is centred on the mic (was ~15 px high); the word row sits 16 px lower, word + mic together.
- **Runner heart:** `3_BUILD/assets/MatraRunner/heart_full.webp` replaced with S03's cleaned heart (the grey halo
  outside its outline removed); art stamp moved so devices refetch. Old file: `../_backup_pre_s03_port_2026-11-09/`.
Not ported (S03-only content): े / ै glyph rules, S03's words / pictures / VO, the page 2/4 syllable glow timed to
S03's own recordings, the page 1 matra-name beat (S03's own matra-name clips).
