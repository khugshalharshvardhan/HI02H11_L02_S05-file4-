# HI02H11_L02_S05 · अं / अः — implementation status against the SME's 2026-10-08 review

Every line of the SME's speaker notes has been read against the built game. **✅ built and
verified by driving it in the browser · ◐ built, with a stated difference · ➜ the developer's.**
Nothing is marked ✅ on the strength of reading code alone.

The flow and the hint ladder are the S03 review of 2026-09-30. This review changed the lesson's
SHAPE (a new screen, two screens deleted, one moved), its vocabulary (अनुस्वार / विसर्ग / चिह्न),
and how the two signs are drawn.

## The shape of the lesson

| | |
|---|---|
| ✅ **16 screens** in the SME's deck order: landing · intro · **names (new)** · build · pair · build · pair · 2 taps · word sort · sign sort · word build · picture sort · **गरमी sentence, then चिड़िया sentence** · celebration | page 9 (third tap) and page 16 (छः गुब्बारे) deleted; `guard_flow` checks the shape |
| ✅ tutorial 6 · guided 8 · independent 1; «चलिए, शुरू करें!» before the intro, «चलिए, साथ में करें!» between the प्रातः pair and G1 | |
| ✅ **«चलिए, शुरू करें!» gate — "VO and Text Synching required here"**: the gate's VO was the shared clip «ध्यान से देखिए और मेरे साथ जानिए। चलिए, शुरू करें!» under a title reading only «चलिए, शुरू करें!». This lesson now has its own clip saying exactly the title | verified: title and VO match |
| ✅ **Hint-3 hand**: on the taps and both sorts; "Use glow and lock without a hand" on word build, picture sort and both sentences, as the notes now say outright | verified: hand on G1 and G4 |
| ➜ **the independent round** (deck position 20, after «अब आपकी बारी!»): the word-catch game; "In this game we will ask child to find अं Matra only not अः — 1 level game only". **The developer builds it**; the words are below | |

**The independent round's words** (the SME's, verbatim; the round asks for अं only):

* अं (ं) वाले शब्द: अंग, रंग, संग, बंदर, जंगल, पतंग, संतरा, चंदा, घंटा, लंबा
* अः (ः) वाले सरल शब्द: प्रातः, पुनः, अतः, छः

## The two signs, drawn

| | |
|---|---|
| ✅ "Correct the second card's symbol to ◌ः. Remove the extra horizontal stroke above the two dots" | typeset, this font joins ः to a stub of headline. ◌ं and ◌ः are now DRAWN: a grey dotted guide circle, one solid dot above / two dots to the right — the SME's own mockup — on the landing, intro, names screen, build equation, pair callout and sign-sort cards |
| ✅ "Keep the dotted circles neutral grey and the actual signs red" | the guide circle no longer turns red with the mark |
| ✅ "Remove the red outline/glow rings around the dot" | the ring drawn round every anusvara/visarga (`mark_ring`) is off |
| ✅ inside words («छः», «प्रातः») only the two dots go red | the highlight had also reddened the headline stub — fixed in the mask (`_markMask`) |

## Page by page

| page | status | notes |
|---|---|---|
| 1 landing | ✅ | the drawn signs in the two bogies; train enters, signs pop one by one |
| | ◐ | no per-bogie SFX (the browser blocks sound before the first tap), as in S03/S04 |
| 2 intro | ✅ | heading «आज हम अं और अः वाले शब्द पढ़ेंगे।» (no «की मात्रा»); «यह है अं। इसका चिह्न देखिए।»; one pair lit at a time; the old dot-count instruction line removed (it moved, reworded, to the names screen) |
| 3 **names (new)** | ✅ | no heading; «आइए, इन अक्षरों और इनके चिह्नों के नाम जानें।» → card 1 «अं में एक बिंदी है।» (dot lit) → «इस बिंदी को अनुस्वार कहते हैं।» (label appears) → card 1 dims → card 2 «अः में दो बिंदियाँ हैं।» → «इसे विसर्ग कहते हैं।»; both visible at the end; आगे after both. Verified in sequence |
| | ◐ | the notes give the last line twice: «इसे विसर्ग कहते हैं।» (VO block) and «इस चिह्न को विसर्ग कहते हैं।» (sequence). Built with the VO block's |
| 4 build | ✅ | heading «गोद में अनुस्वार लगाने पर गोंद बनता है।»; «यह शब्द देखिए, गोद।» → «गो के ऊपर अनुस्वार लगाने पर, गों बनता है।» → «अब द जुड़ने पर, गोंद बनता है।»; parent's-lap and glue pictures; **no captions**; the «अं की मात्रा» clip between the steps removed (not in the SME's sequence) |
| 5 pair | ✅ | अंडा, बंदर — «… इसमें अ के ऊपर बिंदी लगी है।»; label «इस शब्द का चिह्न — ◌ं»; heading «अं वाले शब्द पढ़िए।»; the trailing «अं की मात्रा» clip removed |
| 6 build | ✅ | **no heading, no picture, no captions**; «आइए, देखें कि अः की मात्रा के शब्द को और कैसे लिख सकते हैं।» → «यह शब्द देखिए, छह।» → «छ के साथ अः की मात्रा लगाने पर, छः बनता है।» → «छह को छः भी लिखते हैं। दोनों का मतलब एक ही है।» |
| 7 pair | ✅ | ONE example, **प्रातः**, no picture, no label, no heading; «इसमें त के आगे अः की मात्रा लगी है।» |
| 8 tap | ✅ | **बंदर · छः · प्रातः** → बंदर; «“अं” वाले शब्द पर टैप कीजिए।»; «शाबाश! बंदर शब्द में अं की बिंदी है।»; Hint 3 «बंदर शब्द में अं की बिंदी है। बंदर पर टैप कीजिए।» + hand. Verified rung by rung, silent after the reveal |
| 9 tap | ✅ | **जंगल · पंखा · प्रातः** → प्रातः; «… अः की दो बिंदियाँ हैं।» |
| 10 word sort | ✅ | **बंदर · छः · अंडा · प्रातः**, picture-and-word cards, each read before the tray unlocks |
| 11 sign sort | ✅ | «सही चिह्न को सही डिब्बे में डालिए।»; ◌ः · ◌ं drawn; **no name is spoken** — not as the cards appear, not on a tap (the tray used to read «अः की मात्रा», «अं की मात्रा» aloud); Hint 2 «चिह्न का आकार ध्यान से देखिए…» with the dots red; Hint 3 «यह अः का चिह्न है…» + hand, the other card frozen; «शाबाश! यह अं का चिह्न है।». Verified |
| 12 word build | ✅ | बं+दर · पं+खा · झं+डा; options बं, छः, पं, दुः, झं in that order; «शाबाश! पंखा बन गया।»; no hand |
| 13 picture sort | ✅ | **झंडा · प्रातः · पंखा** (three); Hint 1 «फिर से सुनिए।» → name → «चित्र को…»; no hand |
| 14 sentence | ✅ | «गरमी में ___ चलता है।» — पंखा, झंडा, प्रातः; Hint 3 «… पंखा शब्द को खाली जगह में डालिए।» |
| 15 sentence | ✅ | «चिड़िया ने एक ___ दिया।» — अंडा, बंदर, छः; Hint 3 «… अंडा शब्द को खाली जगह में डालिए।» |
| | ◐ | Hint 2 "Highlight the fan / the egg in the nest" — the whole scene is ringed, as in S03/S04 |
| 16 celebration | ◐ | the SME wrote «बहुत बढ़िया, दोस्त! **तुमने** कमाल कर दिया!». Built as «… **आपने** कमाल कर दिया!»: every other line of the lesson is आप, and the build's register guard forbids तुम forms. One word to flip if तुमने was intended |

## Assets

| | |
|---|---|
| voice-over | **110 clips, `_verify_assets.py` 0 FAIL / 0 WARN.** 70 new |
| ear-check | fallback voice/wrapper: `vo_t4_prompt` (Kore), `vo_rev_word_pratah`, `vo_t6_prompt`, `vo_akshara_3` (पं), `vo_ok_mark_vis`, `vo_akshara_4` (झं) |
| images | **10** (8 cut-outs + 2 scenes), unchanged; दुःख and the balloons scene retired to quarantine |
| JS errors | none — all 15 slides mounted; every audio file and image resolves |
