# Art brief — HI02H11_L02_S05 · अं / अः

> **Updated for the SME's review of 2026-10-08.** No new art was needed: every picture the review
> asks for already matched its requirement (egg, monkey, table fan, flag, sunrise, glue bottle,
> parent's lap, the fan scene, the bird-and-nest scene). `obj_dukh` and `scn_gubbare` are no longer
> used (the दुःख example and the छः गुब्बारे sentence were removed) and sit in
> `_quarantine/unused_images/`. **10 images** in use: 8 cut-outs + 2 scenes.


**12 images: 9 cut-out objects + 3 illustrated scenes. Generated, looked at, and committed.**
All nine objects and all three scenes were right on the first pass — unusual, and not to be
assumed next time. The rules, and the failures that produced them, are in
[`_ART_RULES.md`](_ART_RULES.md).

## Objects — `gen_objects.py` (magenta key, transparent PNG)

| key | word | mark | what it is |
|---|---|---|---|
| `obj_anda` | अंडा | ं | a cream egg — specified cream, never white, or it keys out with the background |
| `obj_bandar` | बंदर | ं | friendly brown monkey, sitting |
| `obj_pankha` | पंखा | ं | blue table fan |
| `obj_jhanda` | झंडा | ं | the Indian tricolour on a pole |
| `obj_chhah` | छः | ः | **exactly six** orange balls, touching, in two rows of three |
| `obj_dukh` | दुःख | ः | a sad child's face with one tear — gentle, not distressing |
| `obj_pratah` | प्रातः | ः | sunrise behind two green hills |
| `obj_god` | गोद | — | a mother with her child in her lap · **base word**, screen 2 |
| `obj_gond` | गोंद | ं | a bottle of school glue · **result**, screen 2 |

## Scenes — `gen_art.py --no-key` (background kept, 1024×1024)

| key | sentence | shows |
|---|---|---|
| `scn_chidiya` | चिड़िया ने एक ___ दिया। | a bird on her nest with one egg clearly visible |
| `scn_garmi` | गरमी में ___ चलता है। | a table fan turning, a child enjoying the breeze |
| `scn_gubbare` | मेरे पास ___ गुब्बारे हैं। | a child holding **exactly six** balloons |

`scn_gubbare` was magnified and counted by hand: red, orange, yellow, blue, green, purple. Six.
The whole sentence depends on that count, so check it again if it is ever re-rolled.

## Why only three अः words

Hindi's visarga vocabulary is tatsama and mostly abstract — दुःख, अतः, पुनः, प्रातः, छः, निःशब्द,
क्रमशः. Exactly **three** of those can be drawn for a seven-year-old, against a dozen easy अं
nouns. So अः never gets a fourth card anywhere in this lesson. That is a property of the language,
not a shortcut, and it is the one content decision in this lesson worth the SME's attention.

## The mark is a DOT, which is an ART problem as much as an engine one

The anusvara is 17×16px of ink at a 100px font, and the engine renders a sort-card label at 21px.
matraHL now draws a ring around every mark in the lesson so the child can find it. Nothing in the
art has to compensate — but if a future word is chosen whose picture is busy, remember that the
thing the child is hunting for is three pixels wide.


---

## Voice-over — 107 clips, generated and checked

Kore throughout except where the model refused and the ladder recovered elsewhere. **Ear-check
these**, the timbre differs: `vo_rev_sort_bandar` and `vo_rev_sort_chhah` (Aoede), `vo_akshara_2`
and `vo_rev_sort_jhanda` (wrapped Despina), `vo_meet_dukh` and `vo_matra_vis` (wrapped Kore),
`vo_akshara_4` (danda).

### Two clips came back truncated, and only the peer-length check found them

`vo_meet_bandar` at 0.97s and `vo_meet_dukh` at 0.77s, against a 1.99s median across four peers of
the same length. Both files existed, played, and were correctly named.

Regenerating is a lottery, not a fix for the text — `vo_meet_bandar` took three tries
(0.93s · 1.21s · **3.05s**) with the same voice and the same words, which matches what the sibling
lesson recorded. `vo_meet_dukh` came back right on the first retry.

**Never ship a TTS run without the peer-length check**, and re-run the check after every retry.
A stub clip is indistinguishable from a good one by existence, by file size, and by ear if you
happen to spot-check a different clip.
