# CHANGES: HI02H11_L02_S05 «मात्राओं की रेल» (अं / अः)

**What this build is.** HI02H11_L02_S02 (उ / ऊ, the completed lesson) forked to अं / अः. It uses
S02's engine, layout, buttons, colours, typography, painted train, gate Swifty lip-sync,
celebration kit, hint ladders and the मात्रा रनर game. The **content** follows the SME deck
`1_SPEC/HI02H11_L02_S05_SME_Review.pptx` (notes verbatim in `1_SPEC/_SME_RECOMMENDATIONS.md`).

**Decisions confirmed with the user (2026-10-16):** the deck's screen order with no demo screen;
the runner pairs one अं word against one अः word; all new VO is Gemini TTS, voice **Leda**.

Status: ✅ DONE · ⚑ FLAGGED (built, with a stated difference) · N/C (no change asked)

## Checklist, deck position by position

| # | deck | change asked | status | proof |
|---|---|---|---|---|
| 1 | 2 landing | title «मात्राओं की रेल», the existing two-bogie train: अं (◌ं), अः (◌ः), dotted guide circles | ✅ | `01_landing.png` (S02's painted train: the bogies are yellow/green, not pink/green) |
| 2 | 2 landing | train enters right→left; signs pop in one by one after it parks; whistle + sparkle SFX | ✅ | S02 engine, unchanged |
| 3 | 2 landing | VO «हेलो दोस्त! मैं हूँ स्विफ्टी। आज हम मात्राओं के बारे में जानेंगे।» | ✅ | `vo_landing` |
| 4 | 3 gate | "VO and Text Synching required here" | ⚑ | S02's gate: the title is typed **while Swifty says it** (voiced-segment sync). The gate clip is S02's shared clip, which says more than the title before the title phrase |
| 5 | 4 intro | heading and VO «आज हम अं और अः वाले शब्द पढ़ेंगे।» (no «की मात्रा») | ✅ | `02_MATRA_PAIRS.png` |
| 6 | 4 intro | «यह है अं। इसका चिह्न देखिए।» / «यह है अः…»; letter first, then the sign; one pair at a time; the first pair dims | ✅ | MATRA_PAIRS + new `mq-dim` |
| 7 | 4 intro | ◌ः without the extra horizontal stroke; dotted circle grey; only the dots coloured | ✅ | drawn signs (`signHTML`) |
| 8 | 5 NEW | names screen: no heading; «आइए, इन अक्षरों और इनके चिह्नों के नाम जानें।» → card 1 + dot lit «अं में एक बिंदी है।» → «इस बिंदी को अनुस्वार कहते हैं।» + label → card 1 dims → card 2 … «इसे विसर्ग कहते हैं।»; both shown at the end; आगे after both | ✅ | `03_MATRA_PAIRS.png`, MATRA_PAIRS `names` mode |
| 9 | 6 build | heading «गोद में अनुस्वार लगाने पर गोंद बनता है।»; गोद + lap picture → the dot comes down onto गो → द joins → गोंद + glue; only the dot coloured; «गो। गों। गोंद।» sound contrast | ✅ | `04_MATRA_BUILD.png` |
| 10 | 6 build | centre equation «गो + ◌ं = गों» | ⚑ | S02 removed the equation panel (Yasir r121). Kept S02's layout: गोद → गोंद with the dot flying in |
| 11 | 7 pair | heading «अं वाले शब्द पढ़िए।»; अंडा, then बंदर, one at a time; «अंडा, बोलकर देखिए। इसमें अ के ऊपर बिंदी लगी है।»; dot lit on «बिंदी» | ✅ | `05_MEET_PAIR.png` (+ S02's mic turn) |
| 12 | 8 build | no heading, no picture: छह → छः; «छ के साथ अः की मात्रा लगाने पर, छः बनता है।» → «छह को छः भी लिखते हैं। दोनों का मतलब एक ही है।» | ✅ | `06_MATRA_BUILD.png` |
| 13 | 9 pair | प्रातः only, no picture, no label, no heading; «… इसमें त के आगे अः की मात्रा लगी है।» | ✅ | `07_MEET_PAIR.png` |
| 14 | 11 tap | बंदर · छः · प्रातः → बंदर; heading «“अं” वाले शब्द पर टैप कीजिए।»; the deck's prompt, praise, H1, H2 and H3 lines | ✅ | driven: miss1 → H1, miss2 → the three words read with signs lit → H2 line, win |
| 15 | 12 tap | जंगल · पंखा · प्रातः → प्रातः; «… अः की दो बिंदियाँ हैं।» | ✅ | driven |
| 16 | 13 word sort | बंदर · छः · अंडा · प्रातः into अं / अः; per-card praise and H3 | ✅ | driven, 4/4 placed |
| 17 | 14 sign sort | ◌ः · ◌ं into अं / अः; **no sign name is ever spoken**; H2 enlarges the card and colours its sign; H3 «यह अं का चिह्न है। इसे अं वाले डिब्बे में डालिए।» | ✅ | driven: miss2 plays only `vo_g4_h2`, no names |
| 18 | 15 word build | बं+दर · पं+खा · झं+डा from बं छः पं दुः झं; «शाबाश! बंदर बन गया।»; H3 «बं लगाने से बंदर बनता है…»; glow and lock, **no hand** | ✅ | driven, 3/3 built; `hand_on_hint3: false` |
| 19 | 16 picture sort | झंडा · प्रातः · पंखा; H1 «फिर से सुनिए। झंडा। चित्र को…» (per card); H3 per card; no hand | ✅ | driven, 3/3 |
| 20 | 17 sentence | «गरमी में ___ चलता है।», options पंखा · झंडा · प्रातः; sentence read with the blank; H3 «चित्र में पंखा चल रहा है…» | ✅ | driven |
| 21 | 18 sentence | «चिड़िया ने एक ___ दिया।», options अंडा · बंदर · छः | ✅ | driven |
| 22 | 16 / 9 | deleted: the third tap (old p.9) and the छः-balloons sentence (old p.16); गरमी moved before चिड़िया | ✅ | `guard_flow` |
| 23 | 20 runner | "find अं Matra only not अः, 1 level game only": the 10 अं words (अंग … लंबा) to catch, with प्रातः · पुनः · अतः · छः as the wrong word in each pair | ✅ | driven: pairs बंदर/प्रातः, लंबा/अतः; `16b_MINI_GAME_playing.png` |
| 24 | 19 gate | «अब आपकी बारी!» before the runner | ✅ | S02 `gate.at.round3 = MG1` |
| 25 | 21 celebration | «बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया!» | ✅ | S02's lip-synced celebration kit, re-synced to this clip |

## Deliberate differences from the deck (S02 kept, as instructed)

* **Highlight colour** is S02's orange (`--matra-hi #FF8A00`), not the deck's "red".
* **Hint ladders are S02's.** Rung 2 on the word sort reads every remaining card, and on word
  build it reads the three picture names (the deck reads only the dropped item). The deck's VO
  lines sit inside S02's ladder. The one exception is the sign sort, where S02's rung 2
  (labels read out with their marks) would have given the answer away.
* **Cards and options are shuffled** each visit (S02's r29), so the deck's fixed option orders
  are not kept.
* S02 removed headings from its teach screens. The deck asks for headings on T1, T3 and T4, so
  those three keep a slimmer band (`.s05-head`).

## Assets

* **VO:** 104 lesson clips + 15 runner clips, Gemini TTS, voice Leda. Phase-gate VO, SFX, music
  and the mic-nudge clip are copied from S02. `_verify_assets.py`: **0 FAIL 0 WARN**, no
  truncated clips.
* **EAR-CHECK** (these needed a style wrapper or a danda to generate; same voice, but listen to
  them): `vo_meet_anda`, `vo_meet_pratah`, `vo_t4_prompt`, `vo_t6_prompt`, `vo_name_pratah`,
  `vo_name_bandar`, `vo_g3_h3_pratah`, `vo_p1_h3_pankha`, `vo_g3_h3_chhah`, `vo_ak_pan`,
  `vo_letter_vis`, `vo_ak_jhan`, `vo_ak_duh`; runner: `ang`, `patang`, `sang`, `rang`.
* **Images:** the S05 factory set (8 cut-outs + 2 scenes), reused. No new art was needed.

## Observations (noticed, not changed)

* At sort-card size the प्रातः sunrise (`obj_pratah`) reads as a mound. Consider redrawing it.
* `3_BUILD` is 48 MB (raw-WAV audio + runner video), the same situation as S02. Optimise
  a copy before shipping (Opus audio, prune unused `assets/UI`).
* `3_BUILD/`, `4_SOURCE/`, `5_SCREENSHOTS/` at the root are the old factory build. They are
  duplicated in `_v1_factory_build/` and can be deleted (they were locked by the editor).

## Fix after review: cover had no VO / SFX / play button (2026-10-16)

Chrome blocks all sound until the page has been touched. The greeting's `play()` then **hung**
(never ended), so the play button, which waits for the greeting, stayed hidden for up to 25 s,
and the first-tap fallback took the hung clip for a playing one and never retried. S02 has the
same weakness: it only works there if the cover is tapped during the train's arrival.
`4_ENGINE/lesson_template.html` (`_soundLocked` / `_deferGreeting`, tagged `[S05]`): while sound
is locked the greeting is not started. The play button shows as soon as the arrival ends, and
the first touch of the cover (not ▶) unlocks sound and plays the greeting. Verified headless
without the autoplay flag: button at ~10 s, tap → greeting plays (button greyed) → button back.

## Round 2: user asks of 2026-10-22 (on-screen text removed, VO unchanged)

| # | page | ask | status |
|---|---|---|---|
| R2-1 | 1 intro | remove the heading «आज हम अं और अः वाले शब्द पढ़ेंगे।» | ✅ `no_heading`; the line is still the opening VO; S02's page-1 layout (centred) applies |
| R2-2 | 2 names | remove the text अनुस्वार and विसर्ग | ✅ `hide_name_labels`; both names are still spoken |
| R2-3 | 3 गोद build | remove «गोद में अनुस्वार लगाने पर गोंद बनता है।» | ✅ no heading; S02's build layout |
| R2-4 | 4 अंडा/बंदर | remove «अं वाले शब्द पढ़िए।» | ✅ no heading; S02's pair layout |

No teach screen has a heading now, so the `.s05-head` layout no longer applies anywhere (left in the
CSS, inert). S02's commits up to 6f621ea (r139–r145: bug fixes, transition screen, whoosh, BGM
volume, 7 s idle nudge) were already present in this engine when this round started.

## Round 3 (2026-10-22): made the same as file 3 (HI02H11_L02_S03)

User: "my file 3, 4 are same … only elements (images, texts) and learning will change, everything
else exactly same … extract same logic, same hint and everything". Decisions confirmed with the user:
file 3's screen order + demo · S02 human takes + Gemini **Kore** (file 3's voice) · file 3's line
shapes with अं / अः · runner stays 1 level, अं only (the S05 SME).

| area | now |
|---|---|
| engine | 3-way merge (base S02 @ 6f621ea → file 3) onto this engine: file 3's QA fixes (hint-3 speaker replay after the 3rd wrong tap, ink-centred page-1 cards, above-line highlight), S02 r139–r150 incl. the 7 s repeating idle reminder (r150 was missing here), plus this lesson's drawn ◌ं/◌ः, dot masks, names screen, cover sound fix |
| order | T1 pairs · T2 names · T3 गोद · T4 अंडा/बंदर · T5 छह→छः · T6 प्रातः · **G5D demo · G5 sign sort** · G1 बंदर · G2 प्रातः · G4 word sort · P1 word build · P2 picture sort · P3 गरमी · P4 चिड़िया · MG1 · CEL |
| lines | file 3's shapes: cover «नमस्ते दोस्त! … आज हम अं और अः की मात्रा वाले शब्द पढ़ेंगे।» · page 1 «यह है अं। इसकी मात्रा है।» (no own prompt) · «… की मात्रा वाले शब्द पर टैप कीजिए।» ladders · S02 sort/word-build/sentence hint lines · «अब एक खेल! ऊपर दी गई मात्रा वाले शब्द पकड़िए।» |
| hand | `hand_on_hint3: true` (file 3) |
| sign sort | file 3's logic: cards named on reveal («अं की मात्रा»), rung 2 reads the coach labels with their signs |
| pictures | the user's 10 new pictures (added 17:54–17:56) replace the old ones: cut-outs cropped to their ink, scenes cropped inside their white frame, scene glows re-measured. Old ones: `_v1_factory_build/replaced_images_2026-10-22/` |
| voice | 16 lines = S02's recordings (same text); 96 lesson + 15 runner lines Gemini Kore at -16 LUFS (file 3's `_tools/tts_lines.py`; single words via gen_tts's wrapper ladder, all Kore). Leda takes kept in `_v1_factory_build/leda_vo_2026-10-22/` |

Verified: build guards pass; `_verify_assets.py` 1 FAIL «slides with no spoken prompt: T1», the
same result file 3's verifier gives (page 1 speaks only its pair lines, by S02's design);
0 truncated clips; all 18 screens captured; the mechanics driver completes every activity
screen; console sweep: only `favicon.ico` 404 (local server; Vercel rewrites it).
EAR-CHECK (wrapper-generated): vo_meet_pratah, vo_t3_base, vo_matra_vis, vo_letter_anu,
vo_letter_vis, vo_ak_duh, vo_ak_jhan; runner sang.

## 2026-10-22: picture sizes aligned with file 3

User: "in page 4 the image is looking very big, fix the image alignment in all pages, see file 3".
The tight-cropped new pictures filled their boxes edge to edge (the egg ran 260 px tall into its
word). File 3's normalisation is applied: each cut-out on an 800×800 canvas at ~42 % ink coverage,
centred on its visual weight (अंडा, बंदर, छः, झंडा, पंखा, प्रातः); the गोद / गोंद build pictures stay
tight-cropped, as file 3's build-page pictures are. Pages 4, 10, 11, 12 and the sentence options now
read at file 3's scale (captured side by side). Previous versions: `_v1_factory_build/replaced_images_2026-10-22/tight_crop_r3/`.

## 2026-10-22: page 7 sign label · picture cache

* **Page 7 (G5D demo):** the drawn ◌ं on the अं coach label had its dot above the label plate. The
  sign is lowered inside coach labels (`.coach-label .sg-sign.sg-anu`, train_styles.css), so ring and
  dot both sit inside the plate.
* **Page 15 (बंदर option):** the card already pointed at the new `obj_bandar.webp`, but pictures were
  replaced under the SAME names, so a browser kept drawing its cached old picture. Lesson pictures
  are now versioned like the audio: `?v=<hash of assets/Images>` (engine `_iv()` in
  lesson_template.html, stamped by the builder). Any future picture change gets a fresh address.

## 2026-10-23: S02 `8e8fd29` "added vo and hand nudge of mic button" (r151)

Applied: on the word pages (अंडा / बंदर, प्रातः) the hand goes to the mic and «इस बटन पर टैप करिए»
plays 0.35 s after «… बोलकर देखिए» ends, instead of only after 7 s of inactivity; it then repeats
after every 7 s of silence until the mic is tapped. `4_ENGINE/train_modules.js` micTurn is now
identical to S02's. Measured on page 4: line ends ≈7.55 s → hand + reminder 7.9 s → repeats 16.6 s,
25.2 s; no console errors.

## 2026-10-23: mic hand only with the reminder

User: "when the first time it says tap kijiye then only show the hand nudge instantly, after (that) …
show the hand nudge after 7 seconds of inactivity". On the mic pages (अंडा / बंदर, प्रातः) the hand used
to stay on the mic for good after the first reminder. Now it comes WITH «इस बटन पर टैप करिए» and
leaves when the line ends; it returns, with the line, after each 7 s of no tap (`micTurn`,
train_modules.js). Measured: hand 7.9–9.6 s, 16.5–18.2 s, 25.2–26.9 s; no console errors.

## 2026-10-23: cover train sound · pages 4, 5, 6 pictures

* **Cover train SFX.** The cover's sounds (whistle + chug at 2.3 s, pops, greeting) are identical to
  file 3's when the browser allows sound, measured on both. They go missing when the train arrives
  before the page has been tapped: Chrome blocks every sound until a gesture, in this file and in
  file 3 alike (a site Chrome has seen used a lot may be allowed sooner). Now, when the arrival was
  muted, the first tap sounds the whistle and the greeting follows when it ends (whistle 10.66 s →
  greeting 12.16 s after a tap at 10.6 s); a tap before the arrival behaves exactly as before.
  `window.__coverTrainSound` (train_modules.js) · `_deferGreeting` + the first-tap fallback (lesson_template.html).
* **Page 4:** the user's `obj-andaa.png` is the egg (`obj_anda.webp`, file 3's 42 % canvas) — it is
  the one अंडा picture, so pages 10, 15 and the sentence options show it too.
* **Page 5:** the user's `aam.png` (six mangoes) under छह AND under छः, word above, picture below —
  the example that both spellings mean six (`obj_aam.webp`; builder `BASE_OBJ` + `result_key`).
* **Page 6:** प्रातः now shows the user's original sunrise picture (`obj_pratah.webp`). No file named
  "og-pratha" exists in the project; the original pratha picture was taken to be meant.
Originals: `_v1_factory_build/replaced_images_2026-10-22/user_originals/`.

## 2026-10-23: mic hand = file 3's logic (file 3 pages 3 / 5 → this file's pages 4 / 6)

From file 3 @ `f6fec41` ("hand nudge timing fixed"): `micTurn` (train_modules.js) copied verbatim and
the card flag `mic_nudge_now` set on T4. The hand + «इस बटन पर टैप करिए» come at once only after page 4's
FIRST word (अंडा, the child's first mic); बंदर and page 6 (प्रातः) wait for 7 s of no tap; each repeats
after every 7 s of silence until the mic is tapped. This replaces the earlier "hand only while the line
plays" variant of this file. Measured: अंडा line ends ≈7.8 s → hand 8.1 s · बंदर ends ≈19.6 s → 26.6 s ·
प्रातः ends ≈8.4 s → 15.4 s; tapping the mic removes the hand.

## 2026-10-23: the user's own VO recordings

Source: `3_BUILD/assets/Audio/VO's for अं और अः/…/voiceovers/` — 138 WAVs (24 kHz mono), exactly the
138 rows of `HI02H11_L02_S05 Manifest.xlsx` (no clip missing, none extra).
* Lesson (114 `vo_*`): S02's `prepare_lesson_voice.py` — trim, -16 LUFS, peak limit, WAV under the
  `.ogg` name (the builder reads them as WAV for the page cues). Includes the three transition lines and
  the mic reminder, which were S02's recordings before.
* Runner (24): S02's `prepare_runner_voice.py` → `assets/MatraRunner/voice/` (Ogg Vorbis, -16 LUFS).
* Transition title typing re-timed to the new clips: «चलिए, शुरू करें!» 3370 ms · «चलिए, साथ में करें!»
  3520 ms · «अब आपकी बारी।» 940 ms (were S02's 3075 / 3575 / 925). Every page cue, the celebration
  lip-sync and the audio cache stamps re-measured by the rebuild.
* `_verify_assets.py`: 0 truncated, 0 missing (the by-design T1 note only); all screens load, no errors.
* The raw folder is excluded from Vercel (`.vercelignore`). Previous Kore takes: `_v1_factory_build/kore_vo_2026-10-23/`.

## 2026-10-28: page 1 timing + auto-next · bigger labels and signs · centred signs · page 7 pulse

* **Page 1:** «यह है अं» → only अं shows; «इसकी मात्रा है» → the arrow AND ◌ं appear together; then the
  sign's own VO «अं की मात्रा» plays (the user's recording) while it glows; same for अः. The arrow was
  cued to the «अं» phrase (S02's `r[-2]`), so it arrived with the letter; now arrow + sign share the
  «इसकी मात्रा है» phrase (run 2). Measured: अं 0.9 s · arrow+◌ं 1.8 s · «अं की मात्रा» 3.0 s.
* **Page 1 has no next button** and moves on to page 2 by itself (`auto_next` card flag → the engine's
  `autoAdvances`, the hidden-button path the test pages use); page 2 shows its next button.
* **Coach labels** (अं / अः above the coaches) 38 → 54 px. **A sign dropped into a coach** 46 → 64 px.
* **Centring:** words inside the boxes were within 2–4 px; the DRAWN signs were not — ◌ं read 10 px
  high (its dot rides above the ring), ◌ः 11 px right (its dots sit beside it). They are now shifted by
  half their overhang wherever they sit in a box (coach, label, tray card): measured within 3 px.
* **Page 7 (demo):** while «… इसलिए अं इस डिब्बे में गया» plays, that coach pulses for 3 s (same for अः).
Verified muted in headless Chrome: event timelines for pages 1 and 7, ink-centre measurements, screen
captures, and a sweep of every screen (no errors).

## 2026-10-28: page 1 polish

* No dimming: the first pair stays fully clear while the second is taught (names screen keeps its dim).
* The matra card PULSES when «इसकी मात्रा है» brings it in, and again while «अं की मात्रा» plays.
* Pace: a 1.4 s beat after the page appears before «यह है अं» (it used to start at once); 0.3 s breath
  between the line and the matra's own clip; 1.1 s before the next pair. Measured: अं 1.9 s · arrow +
  ◌ं (pulse) 2.8 s · «अं की मात्रा» 4.2 s · «यह है अः» 6.4 s · … · page 2 at 13.3 s.
* Page 1 pulse slowed (user): 1.4 s per beat × 2 (was 0.6 s × 3), a gentler 1.10 swell.

## 2026-10-29: page 5 opening VO replaced

The user's new `vo_t5_prompt.wav` (added to assets/Audio) replaces page 5's opening line
(«आइए, देखें कि अः की मात्रा के शब्द को और कैसे लिख सकते हैं।»): prepared with prepare_lesson_voice.py
(trim, -16 LUFS → 4.77 s), source moved to 1_SPEC/game_art_src/lesson_voice/source_wav/, the audio
cache stamp re-made by the rebuild. Old take: `_v1_factory_build/replaced_vo_2026-10-29/`.

## 2026-10-29: page 7 = file 3's page 6

Taken from file 3 (`D:\HI02H11_L02_S03(file3)`, commit 2b7e635 "Final chnages", its page 6 = this page 7):
* **Coach pulse:** file 3's code verbatim — the coach body (`.zone`) gets `tr-demopulse`
  (`trDemoPulse`, 1 s × 3, scale 1.06 + golden glow) as «… इसलिए अं / अः इस डिब्बे में गया» plays.
  Measured: अं coach 11.2–14.2 s, अः coach 19.4–22.4 s. Replaces this file's faster 0.75 s pulse.
* **Letters centred in the coaches on their body** (file 3's `centerInkGlyph` wrapper: शिरोरेखा-to-baseline
  on the window's middle; an above-line mark rises from it). All coach screens.
* **Sizes = file 3's:** coach labels 50 px (min 128 px), matra cards 64 px, snapped matra 58 px.
* The drawn ◌ं / ◌ः on the label plates made a touch smaller so ring and dot stay inside the plate.

## 2026-11-09 — speaker stays grey for the whole VO sequence (all pages)
- Cause: a stray merge marker (`=======`) in `4_ENGINE/train_styles.css` made the browser drop the
  `body.spk-busy .audio-chip` rule, so the speaker was grey only while a clip sounded and flashed blue
  in every pause between lines (page 1 most visibly).
- Fix: marker removed; `mountSlide` also greys the speaker on the page's first frame. Now the speaker
  is grey from the moment a page opens until its last line has finished, then turns blue - same as the
  cover. Verified on pages 1–15 (muted headless sweep): no blue between lines.

## 2026-11-09 — page 1 holds 1 s before page 2
- New slide flag `auto_next_hold_ms` (engine `_autoAdvance`); page 1 sets 1000. Measured: last VO ends →
  page 2 now 2.65 s (was 1.66 s). Page 1's next button stays hidden throughout (`body.auto-next`).

## 2026-11-09 — cover: ▶ works only after the cover VO has finished
- `4_ENGINE/lesson_template.html` landing. Sound locked on a first visit: ▶ used to be pressable before
  the greeting had played, so a press during the greeting jumped to page 1. Now the first tap (even on ▶)
  plays the whistle + greeting, and ▶ is not pressable until it ends.
- Replay from the speaker: ▶ stays on screen (QA BUG_01) but ignores presses until the replay ends.
- The 12 s backstop also waits for a queued greeting; a new backstop re-enables ▶ if a clip never reports
  its end. Verified muted, sound locked and open: mid-VO presses stay on the cover, a press after the VO
  starts the lesson.
