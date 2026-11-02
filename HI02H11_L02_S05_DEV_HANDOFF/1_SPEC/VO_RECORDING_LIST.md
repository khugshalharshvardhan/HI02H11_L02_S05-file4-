# HI02H11_L02_S05 (भाग 1 — उ / ऊ) · «मात्राओं की रेल» — VO recording list (ROUND 3)

112 clips. Shown text == spoken text; record exactly this.

**Register is आप** — the SME asked for it twice, in as many words. Round 2 was तुम, so most of this list is a re-record, not a new line. `guard_register` in the builder fails the build if a तुम form survives anywhere.

**Only re-record what changed.** The builder deletes exactly the clips whose text moved this round, so `gen_tts.py` (which skips ids that already have a file) regenerates precisely those and leaves every unchanged take alone. Never `--force` the whole card: generated audio is non-deterministic, so re-running an unchanged clip returns a different take — a change the SME never asked for.

## ⚠️ EAR-CHECK — 1 clips a human must listen to before delivery

The TTS model truncates a clip when an **em-dash precedes a short final word** (measured on this lesson: em-dash 0.73–1.05 s vs comma 1.53–2.21 s for the same words), and it does the same to a line built from several short danda-separated pieces. The SME's round-3 MEET_PAIR lines and the new sound-differentiation clips are written in exactly those shapes. Their wording ships as written — rewriting a reviewer's Hindi to dodge a synthesis bug is the worse failure — so the clips are flagged instead. **Truncation is invisible to an existence check and to a file-size check.** `_verify_assets.py` compares each clip against peers of similar text length and is the only thing that catches it. Run it, then listen to every id below.

- `vo_t3_sounds` — गो। गों। गोंद।

## All clips

| clip id | spoken text |
|---|---|
| `vo_ak_ban` | बं |
| `vo_ak_chhah` | छः |
| `vo_ak_duh` | दुः |
| `vo_ak_jhan` | झं |
| `vo_ak_pan` | पं |
| `vo_cel_prompt` | बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया! |
| `vo_g1_correct` | शाबाश! बंदर शब्द में अं की मात्रा है। |
| `vo_g1_h3` | बंदर शब्द में अं की मात्रा है। बंदर पर टैप कीजिए। |
| `vo_g2_correct` | शाबाश! प्रातः शब्द में अः की मात्रा है। |
| `vo_g2_h3` | प्रातः शब्द में अः की मात्रा है। प्रातः पर टैप कीजिए। |
| `vo_g4_h1` | फिर से पढ़िए। शब्द में कौन-सी मात्रा है, देखिए और उसे उसी मात्रा वाले डिब्बे में डालिए। |
| `vo_g4_h2_anda` | अंडा में अं की मात्रा है। |
| `vo_g4_h2_bandar` | बंदर में अं की मात्रा है। |
| `vo_g4_h2_chhah` | छः में अः की मात्रा है। |
| `vo_g4_h2_pratah` | प्रातः में अः की मात्रा है। |
| `vo_g4_h3_anda` | अंडा शब्द में अं की मात्रा है। इसे अं वाले डिब्बे में डालिए। |
| `vo_g4_h3_bandar` | बंदर शब्द में अं की मात्रा है। इसे अं वाले डिब्बे में डालिए। |
| `vo_g4_h3_chhah` | छः शब्द में अः की मात्रा है। इसे अः वाले डिब्बे में डालिए। |
| `vo_g4_h3_pratah` | प्रातः शब्द में अः की मात्रा है। इसे अः वाले डिब्बे में डालिए। |
| `vo_g4_prompt` | हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए। |
| `vo_g4d_end` | अब आप भी ऐसे ही करके देखिए। |
| `vo_g5_h1` | फिर से देखिए। सही मात्रा को सही डिब्बे में डालिए। |
| `vo_g5_h2` | मात्रा का आकार ध्यान से देखिए। इसे सही डिब्बे में डालिए। |
| `vo_g5_h3_anu` | यह अं की मात्रा है। इसे अं वाले डिब्बे में डालिए। |
| `vo_g5_h3_vis` | यह अः की मात्रा है। इसे अः वाले डिब्बे में डालिए। |
| `vo_g5_prompt` | सही मात्रा को सही डिब्बे में डालिए। |
| `vo_g5d_anu` | अं की मात्रा इस डिब्बे पर है, इसलिए अं इस डिब्बे में गया। |
| `vo_g5d_prompt` | देखिए, अक्षर को उसकी मात्रा वाले डिब्बे में कैसे डालते हैं। |
| `vo_g5d_vis` | अः की मात्रा इस डिब्बे पर है, इसलिए अः इस डिब्बे में गया। |
| `vo_landing` | नमस्ते दोस्त! मैं हूँ स्विफ्टी। आज हम अं और अः की मात्रा वाले शब्द पढ़ेंगे। |
| `vo_letter_anu` | अं |
| `vo_letter_vis` | अः |
| `vo_matra_anu` | अं की मात्रा |
| `vo_matra_vis` | अः की मात्रा |
| `vo_meet_anda` | अंडा, इसमें अ पर अं की मात्रा लगी है। बोलकर देखिए। |
| `vo_meet_bandar` | बंदर, इसमें ब पर अं की मात्रा लगी है। बोलकर देखिए। |
| `vo_meet_pratah` | प्रातः, इसमें त के आगे अः की मात्रा लगी है। बोलकर देखिए। |
| `vo_mg_prompt` | अब एक खेल! ऊपर दी गई मात्रा वाले शब्द पकड़िए। |
| `vo_mic_nudge` | इस बटन पर टैप करिए। |
| `vo_name_anda` | अंडा |
| `vo_name_bandar` | बंदर |
| `vo_name_chhah` | छः |
| `vo_name_jangal` | जंगल |
| `vo_name_jhanda` | झंडा |
| `vo_name_pankha` | पंखा |
| `vo_name_pratah` | प्रातः |
| `vo_ok_anda` | शाबाश! अंडा शब्द में अं की मात्रा है। |
| `vo_ok_bandar` | शाबाश! बंदर शब्द में अं की मात्रा है। |
| `vo_ok_chhah` | शाबाश! छः शब्द में अः की मात्रा है। |
| `vo_ok_matra_anu` | शाबाश! यह अं की मात्रा है। |
| `vo_ok_matra_vis` | शाबाश! यह अः की मात्रा है। |
| `vo_ok_pratah` | शाबाश! प्रातः शब्द में अः की मात्रा है। |
| `vo_okp_jhanda` | शाबाश! झंडा में अं की मात्रा है। |
| `vo_okp_pankha` | शाबाश! पंखा में अं की मात्रा है। |
| `vo_okp_pratah` | शाबाश! प्रातः में अः की मात्रा है। |
| `vo_p1_h1` | फिर से देखिए। चित्र का नाम सोचिए और देखिए शब्द पूरा करने के लिए कौन-सा अक्षर लगेगा। |
| `vo_p1_h2` | नाम ध्यान से सुनिए। जिस शब्द की शुरुआत इस अक्षर से होती है, उसी डिब्बे में इसे डालिए। |
| `vo_p1_h3_any` | जो अक्षर चमक रहा है, उसे उसी डिब्बे में डालिए। |
| `vo_p1_h3_bandar` | बं को बंदर वाले डिब्बे में डालिए। बं, दर… बंदर। |
| `vo_p1_h3_jhanda` | झं को झंडा वाले डिब्बे में डालिए। झं, डा… झंडा। |
| `vo_p1_h3_pankha` | पं को पंखा वाले डिब्बे में डालिए। पं, खा… पंखा। |
| `vo_p1_prompt` | चित्र देखकर सही अक्षर से शब्द पूरा कीजिए। |
| `vo_p2_h1` | फिर से सुनिए। चित्र का नाम ध्यान से सुनिए और देखिए उसमें कौन-सी मात्रा है। |
| `vo_p2_h2_jhanda` | झंडा में अं की मात्रा है। अब इसे सही मात्रा वाली बोगी में डालिए। |
| `vo_p2_h2_pankha` | पंखा में अं की मात्रा है। अब इसे सही मात्रा वाली बोगी में डालिए। |
| `vo_p2_h2_pratah` | प्रातः में अः की मात्रा है। अब इसे सही मात्रा वाली बोगी में डालिए। |
| `vo_p2_h3_jhanda` | झंडा को अं की मात्रा वाली बोगी में डालिए। |
| `vo_p2_h3_pankha` | पंखा को अं की मात्रा वाली बोगी में डालिए। |
| `vo_p2_h3_pratah` | प्रातः को अः की मात्रा वाली बोगी में डालिए। |
| `vo_p2_prompt` | चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए। |
| `vo_p3_correct` | शाबाश! गरमी में पंखा चलता है। |
| `vo_p3_h1` | फिर से पढ़िए। चित्र देखिए, गरमी में क्या चलता है? सही शब्द चुनकर वाक्य पूरा कीजिए। |
| `vo_p3_h3` | गरमी में पंखा चलता है। पंखा चुनिए। |
| `vo_p3_try_jhanda` | गरमी में झंडा चलता है। |
| `vo_p3_try_pankha` | गरमी में पंखा चलता है। |
| `vo_p3_try_pratah` | गरमी में प्रातः चलता है। |
| `vo_p4_correct` | शाबाश! चिड़िया ने एक अंडा दिया। |
| `vo_p4_h1` | फिर से पढ़िए। चित्र देखिए, चिड़िया ने क्या दिया? सही शब्द चुनकर वाक्य पूरा कीजिए। |
| `vo_p4_h3` | चिड़िया ने एक अंडा दिया। अंडा चुनिए। |
| `vo_p4_try_anda` | चिड़िया ने एक अंडा दिया। |
| `vo_p4_try_bandar` | चिड़िया ने एक बंदर दिया। |
| `vo_p4_try_chhah` | चिड़िया ने एक छः दिया। |
| `vo_pair_anu` | यह है अं। इसकी मात्रा है। |
| `vo_pair_vis` | यह है अः। इसकी मात्रा है। |
| `vo_sc_h2` | जो वाक्य सही लग रहा है, वही शब्द चुनिए। |
| `vo_sc_prompt` | चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए। |
| `vo_sign_anu_1` | अं में एक बिंदी है। |
| `vo_sign_anu_2` | इस बिंदी को अनुस्वार कहते हैं। |
| `vo_sign_vis_1` | अः में दो बिंदियाँ हैं। |
| `vo_sign_vis_2` | इसे विसर्ग कहते हैं। |
| `vo_t2_prompt` | आइए, इन अक्षरों और इनके चिह्नों के नाम जानें। |
| `vo_t3_base` | यह शब्द देखिए, गोद। |
| `vo_t3_onset` | गो के साथ अं की मात्रा लगाने पर गों बनता है। |
| `vo_t3_prompt` | आइए, देखें कि अं की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है। |
| `vo_t3_result` | अब द जुड़ने पर गोंद बनता है। |
| `vo_t3_sounds` | गो। गों। गोंद। |
| `vo_t4_prompt` | आइए, अं की मात्रा वाले कुछ शब्द देखें। |
| `vo_t5_base` | यह शब्द देखिए, छह। |
| `vo_t5_onset` | छ के साथ अः की मात्रा लगाने पर छः बनता है। |
| `vo_t5_prompt` | आइए, देखें कि अः की मात्रा के शब्द को और कैसे लिख सकते हैं। |
| `vo_t5_result` | छह को छः भी लिखते हैं। दोनों का मतलब एक ही है। |
| `vo_t6_prompt` | आइए, अः की मात्रा वाला एक शब्द देखें। |
| `vo_tap_h1_anu` | फिर से पढ़िए। अं की मात्रा वाले शब्द पर टैप कीजिए। |
| `vo_tap_h1_vis` | फिर से पढ़िए। अः की मात्रा वाले शब्द पर टैप कीजिए। |
| `vo_tap_h2_anu` | अं की मात्रा वाले शब्द पर टैप कीजिए। |
| `vo_tap_h2_vis` | अः की मात्रा वाले शब्द पर टैप कीजिए। |
| `vo_tap_prompt_anu` | जिस डिब्बे में अं की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए। |
| `vo_tap_prompt_vis` | जिस डिब्बे में अः की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए। |
| `vo_try_again` | एक बार फिर सुनिए। |
| `vo_wb_bandar` | शाबाश! बंदर बन गया। |
| `vo_wb_jhanda` | शाबाश! झंडा बन गया। |
| `vo_wb_pankha` | शाबाश! पंखा बन गया। |

## Copied, do NOT record

- `vo_pt_tutorial`
- `vo_pt_guided`
- `vo_pt_practice`
- `sfx_celebrate`
- `sfx_correct`
- `sfx_wrong`
- `sfx_tap`
- `sfx_pop`
- `sfx_fb_correct`
- `sfx_fb_incorrect`
- `sfx_play_button`
- `sfx_next_button`
- `sfx_train_arrive`
- `sfx_train_move`
- `sfx_whistle`
- `sfx_whoosh`
