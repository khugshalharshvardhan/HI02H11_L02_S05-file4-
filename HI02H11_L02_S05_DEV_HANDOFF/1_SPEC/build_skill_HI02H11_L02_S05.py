# -*- coding: utf-8 -*-
"""Build HI02H11_L02_S05 (अं / अः) — «मात्राओं की रेल».

Curriculum: अं, अः मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।

=======================================================================================
FORKED FROM HI02H11_L02_S02 (उ / ऊ) — same engine, same flow logic, same animation, same
chrome (painted train, gate Swifty lip-sync, celebration kit, runner game). Only the CONTENT
is this lesson's, and it is built to `1_SPEC/HI02H11_L02_S05_SME_Review.pptx` (SME review of
2026-10-08; notes verbatim in `1_SPEC/_SME_RECOMMENDATIONS.md`).
=======================================================================================

THE SHAPE, in the SME's deck order (confirmed with the user: deck order, no demo screen):
  landing · T1 intro (अं → ◌ं, अः → ◌ः) · T2 NEW names screen (अनुस्वार / विसर्ग) ·
  T3 build गोद → गों → गोंद · T4 pair अंडा, बंदर · T5 build छह → छः · T6 pair प्रातः ·
  «चलिए, साथ में करें!» · G1 tap बंदर · G2 tap प्रातः · G3 word sort · G4 sign sort ·
  P1 word build · P2 picture sort · P3 गरमी sentence · P4 चिड़िया sentence ·
  «अब आपकी बारी!» · MG1 the runner (अं words only, one level) · CEL.

WHAT IS NEW IN THE ENGINE FOR THIS LESSON (4_ENGINE/train_modules.js, all inert for S02 data):
  · ◌ं / ◌ः are DRAWN (grey dotted guide circle + red dot(s)), never typeset — typeset, the font
    joins ः to a stub of headline: the "extra horizontal stroke" the SME asked to remove.
  · matraHL() colours ं (above) and ः (right) with a pixel mask; the visarga mask drops the
    headline stub so only the two dots go red.
  · MATRA_PAIRS `names`: the names screen (label under each card, revealed by its own clip).
  · TRAIN_SORT `sign_mode`: the sign round never names a card, and its rung 2 enlarges the card
    and reddens its sign instead of reading the coach labels out with their marks.
  · MATRA_BUILD / MEET_PAIR accept a word with NO picture (छह, छः, प्रातः).

Run:  PYTHONUTF8=1 python 1_SPEC/build_skill_HI02H11_L02_S05.py   (from the handoff root)
"""
import hashlib
import os, re, sys, json, argparse
import array
import contextlib, wave        # [r8] page-1 matra cue, measured off the clip

CODE     = "HI02H11_L02_S05"
# ---------------------------------------------------------------- paths
HANDOFF  = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUNDLE   = os.path.join(HANDOFF, "3_BUILD")
ENGINE   = os.path.join(HANDOFF, "4_ENGINE", "lesson_template.html")
SPEC_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR  = os.path.join(BUNDLE, "assets", "Images")
AUD_DIR  = os.path.join(BUNDLE, "assets", "Audio")
CARD_TAG = re.compile(r'(<script type="application/json" id="cardData">)(.*?)(</script>)', re.S)
VER_RE   = re.compile(r'ENGINE_VERSION\s*=\s*["\']([^"\']+)["\']')
RSM_RE   = re.compile(r'RIGHT_SPACING_MATRAS\s*=\s*new Set\(\[([^\]]*)\]\)')

TRAIN_MODULES = ["TRAIN_TAP", "TRAIN_SORT", "MATRA_FILL", "MATRA_BUILD",
                 "MEET_PAIR", "CONTRAST_PAIR", "POEM_SEARCH", "MATRA_INTRO",
                 "WORD_BUILD", "SENTENCE_COMPLETE", "MATRA_PAIRS"]
STOCK_MODULES = ["CELEBRATION"]
# Fixed clips copied from HI02H11_L02_S02 (phase gates, SFX). Not recorded for this lesson.
COPY_AUDIO = ["vo_pt_tutorial", "vo_pt_guided", "vo_pt_practice",
              "sfx_celebrate", "sfx_correct", "sfx_wrong", "sfx_tap", "sfx_pop",
              "sfx_fb_correct", "sfx_fb_incorrect",   # [r73] Yasir's feedback sounds
              "sfx_play_button", "sfx_next_button",   # [r84] Yasir's play / next button sounds
              "sfx_train_arrive", "sfx_train_move", "sfx_whistle",
              "sfx_whoosh"]                           # [r142] the transition screen's swish

ANU, VIS = "ं", "ः"
U, UU = ANU, VIS          # the two target marks, under the names the shared helpers use

# ---------------------------------------------------------------- content
# key -> (word, emoji, sign). Every word carries exactly ONE of the two target signs.
OBJ = {
    "obj_anda":   ("अंडा",   "\U0001F95A", ANU),
    "obj_bandar": ("बंदर",   "\U0001F412", ANU),
    "obj_pankha": ("पंखा",   "\U0001FAAD", ANU),
    "obj_jhanda": ("झंडा",   "\U0001F6A9", ANU),
    "obj_gond":   ("गोंद",   "\U0001F9F4", ANU),
    "obj_jangal": ("जंगल",   "\U0001F333", ANU),   # tap coach only - no picture
    "obj_chhah":  ("छः",     "6️⃣", VIS),
    "obj_pratah": ("प्रातः", "\U0001F305", VIS),
}

# Full illustrated scenes for the two sentence screens (not keyed).
SCENE = {
    "scn_garmi":   "\U0001FAAD",
    "scn_chidiya": "\U0001F426",
}

# The bare LETTER (the coach roof labels), read on the sort screens' rung 2.
LETTER_VO  = {ANU: "vo_letter_anu", VIS: "vo_letter_vis"}
LETTER_TEXT = {"vo_letter_anu": "अं", "vo_letter_vis": "अः"}
# [S05-r3] file 3's naming: the SIGN is spoken «अं की मात्रा» (MATRA_VO), the LETTER «अं» (LETTER_VO)
MATRA_VO   = {ANU: "vo_matra_anu", VIS: "vo_matra_vis"}
# Where the scene glows during rung 2 on the sentence screens (cx, cy, rx, ry, fractions of the art)
SCENE_GLOW = {
    # [S05-r3] re-measured on the user's new scenes (2026-10-22), fractions of the cropped artwork
    "scn_garmi":   [[0.27, 0.40, 0.17, 0.22]],   # the table fan
    "scn_chidiya": [[0.75, 0.54, 0.12, 0.10]],   # the egg in the nest
}
MATRA_TEXT = {"vo_matra_anu": "अं की मात्रा", "vo_matra_vis": "अः की मात्रा"}
MATRA_TEXT.update(LETTER_TEXT)
MATRA_NAME = {ANU: "अं", VIS: "अः"}
LETTER     = {ANU: "अं", VIS: "अः"}
TAG        = {ANU: "anu", VIS: "vis"}

AUDIO_TEXT = {}
TEXT2ID    = {}
PENDING_ART = []


def vo(vid, text):
    if vid in AUDIO_TEXT and AUDIO_TEXT[vid] != text:
        raise ValueError("clip %s registered twice with different text:\n  %s\n  %s"
                         % (vid, AUDIO_TEXT[vid], text))
    AUDIO_TEXT[vid] = text
    return vid


def once(vid, text):
    """One clip per LINE, never per slide (a line used on two screens is recorded once)."""
    if text in TEXT2ID:
        return TEXT2ID[text]
    TEXT2ID[text] = vid
    return vo(vid, text)


def slug(key):
    return key.split("_", 1)[1] if "_" in key else key


def pic(key):
    """The image key if its picture is on disk, else None (the engine renders the emoji)."""
    if os.path.isfile(os.path.join(IMG_DIR, key + ".webp")):
        return key
    if key not in PENDING_ART:
        PENDING_ART.append(key)
    return None


def key_of(word):
    for k, v in OBJ.items():
        if v[0] == word:
            return k
    sys.exit("X  no OBJ entry for %r" % word)


# The MATRA_BUILD base words: the form BEFORE the sign, so they live outside OBJ.
# गोद has a picture (a child in a parent's lap); छह has none (SME: "Remove the six-object image").
BASE_OBJ = {
    "गोद": ("obj_god", "\U0001F931"),
    # [S05] user 2026-10-23: six mangoes as the example for छह / छः (page 5)
    "छह": ("obj_aam", "\U0001F96D"),
}


def key_of_opt(word):
    for k, v in OBJ.items():
        if v[0] == word:
            return k
    if word in BASE_OBJ:
        return BASE_OBJ[word][0]
    return None


def matra_of(word):
    for _k, (w, _e, m) in OBJ.items():
        if w == word:
            return m
    sys.exit("X  no sign known for %r" % word)


def name_clip(word):
    """One clip per WORD, never per slide."""
    return vo("vo_name_" + slug(key_of(word)), word)


# ---------------------------------------------------------------- timing, measured off the clips

def _clip_secs(audio_id):
    path = os.path.join(AUD_DIR, audio_id + ".ogg")
    try:
        with contextlib.closing(wave.open(path)) as w:
            return w.getnframes() / float(w.getframerate())
    except Exception:
        return None


def _matra_cue_ms(audio_id, line, phrase="इसकी"):
    """When `phrase` starts inside `line`'s recording, in ms (clip duration x text proportion)."""
    secs = _clip_secs(audio_id)
    if secs is None:
        return 1300
    i = line.find(phrase)
    if i < 0:
        return int(secs * 1000 * 0.35)
    before = len(line[:i].replace(" ", ""))
    total  = len(line.replace(" ", ""))
    return int(secs * 1000 * (before / float(total)))


def _read_pcm(audio_id):
    path = os.path.join(AUD_DIR, audio_id + ".ogg")
    try:
        with contextlib.closing(wave.open(path)) as w:
            if w.getsampwidth() != 2 or w.getnchannels() != 1:
                return None, None
            sr = float(w.getframerate())
            a = array.array("h"); a.frombytes(w.readframes(w.getnframes()))
            return sr, a
    except Exception:
        return None, None


def _runs(audio_id, quiet_s):
    sr, a = _read_pcm(audio_id)
    if not a:
        return []
    hop  = max(1, int(sr * 0.01))
    peak = max(1, max(abs(v) for v in a))
    loud = [max(abs(v) for v in a[i:i + hop]) > peak * 0.10
            for i in range(0, len(a) - hop, hop)]
    runs, i, minq = [], 0, int(quiet_s / 0.01)
    while i < len(loud):
        if loud[i]:
            j, q = i, 0
            while j < len(loud) and q < minq:
                j += 1
                q = 0 if (j < len(loud) and loud[j]) else q + 1
            runs.append(int(i * 10))
            i = j
        else:
            i += 1
    return runs


def _sound_cues_ms(audio_id, n):
    """Where each of the `n` sounds starts inside «गो। गों। गोंद।», in ms; None if it does not
    resolve into exactly n runs."""
    if not audio_id:
        return None
    r = _runs(audio_id, 0.18)
    return r if len(r) == n else None


def _voice_runs_ms(audio_id, quiet_s=0.30):
    """Where each spoken PHRASE in a clip starts, in ms (runs of sound between pauses)."""
    return _runs(audio_id, quiet_s)


# ---------------------------------------------------------------- screens

def s_intro(sid):
    """T1 · «अं → ◌ं», then «अः → ◌ः», one pair at a time. [S05-r3] file 3's page 1, line for line:
    no heading, no opening line of its own (it is on the cover, vo_landing), and S02's script shape
    «यह है अं। इसकी मात्रा है।» - the letter lands on «अं», the sign on «इसकी मात्रा है»."""
    def _pair(letter, m, aid, line):
        vo(aid, line)
        r = _voice_runs_ms(aid)
        cue = _matra_cue_ms(aid, line)
        ok = len(r) >= 3
        # [S05 2026-10-28] user: «यह है अं» -> ONLY अं shows; «इसकी मात्रा है» -> the arrow AND the sign
        # come together; then the sign's own VO. The clip is three phrases - «यह है» · «अं» ·
        # «इसकी मात्रा है» - so the letter lands on run 1 and arrow + sign on run 2 (S02's `r[-2]` put
        # the arrow on «अं», i.e. with the letter).
        return {"letter": letter, "matra": m, "audio": aid, "cue_ms": cue,
                "letter_ms": r[1] if ok else 900,
                "arrow_ms": r[2] if ok else cue,
                "matra_ms": r[2] if ok else cue,
                "matra_audio": MATRA_VO[m]}
    pairs = [_pair("अं", ANU, "vo_pair_anu", "यह है अं। इसकी मात्रा है।"),
             _pair("अः", VIS, "vo_pair_vis", "यह है अः। इसकी मात्रा है।")]
    return {"id": sid, "phase": "tutorial", "eis": "enactive", "type": "MATRA_PAIRS",
            "prompt_hi": "",
            "audio": {},
            # [S05 2026-10-28] no next button on page 1: it moves on to page 2 by itself
            "data": {"pairs": pairs, "phonemes": dict(MATRA_VO), "auto": True, "no_heading": True,
                     # [S05 2026-11-09] "add a 1 second stop in that screen then jump to the second screen"
                     "auto_next": True, "auto_next_hold_ms": 1000}}


def s_names(sid):
    """T2 · the signs' names (this lesson's own screen - file 3 has none). No heading, no labels on
    screen (user 2026-10-22); the names are spoken."""
    def _p(letter, m, tag, l1, name, l2):
        return {"letter": letter, "matra": m, "name": name,
                "audio": vo("vo_sign_%s_1" % tag, l1),
                "name_audio": vo("vo_sign_%s_2" % tag, l2)}
    pairs = [_p("अं", ANU, "anu", "अं में एक बिंदी है।", "अनुस्वार", "इस बिंदी को अनुस्वार कहते हैं।"),
             _p("अः", VIS, "vis", "अः में दो बिंदियाँ हैं।", "विसर्ग", "इसे विसर्ग कहते हैं।")]
    return {"id": sid, "phase": "tutorial", "eis": "iconic", "type": "MATRA_PAIRS",
            "prompt_hi": "",
            "audio": {"prompt": vo("vo_t2_prompt", "आइए, इन अक्षरों और इनके चिह्नों के नाम जानें।")},
            "data": {"pairs": pairs, "names": True, "hide_name_labels": True, "no_heading": True}}


def s_build(sid, base_word, consonant, matra, syllable, result_word, lines, sounds=None,
            base_pic=True, result_pic=True, result_key=None):
    """The transformation teach - file 3's MATRA_BUILD (no heading, word built piece by piece)."""
    g = sid.lower()
    a = {
        "prompt": vo("vo_%s_prompt" % g, lines["prompt"]),
        "base":   vo("vo_%s_base" % g, lines["base"]),
        "matra_name": MATRA_VO[matra],
        "onset":  vo("vo_%s_onset" % g, lines["onset"]),
        "result": vo("vo_%s_result" % g, lines["result"]),
    }
    if sounds:
        a["sounds"] = vo("vo_%s_sounds" % g, sounds)
    # `result_key` lets the result word show a picture other than its own OBJ one (page 5: छः shows
    # the same six mangoes as छह, because the two spellings mean the same thing)
    rk = (result_key or key_of(result_word)) if result_pic else None
    bk = key_of_opt(base_word) if base_pic else None
    ONSET_LINE, RESULT_LINE = lines["onset"], lines["result"]
    ON_RUNS, RE_RUNS = _voice_runs_ms(a["onset"]), _voice_runs_ms(a["result"])
    tail = result_word[len(syllable):] if result_word.startswith(syllable) else ""
    return {"id": sid, "phase": "tutorial", "eis": "symbolic", "type": "MATRA_BUILD",
            "prompt_hi": "", "audio": a,
            "data": {"base_word": base_word, "consonant": consonant, "matra": matra,
                     "syllable": syllable, "result_word": result_word,
                     "result_img": pic(rk) if rk else None,
                     "result_emoji": ((OBJ[rk][1] if rk in OBJ else
                                       next((v[1] for v in BASE_OBJ.values() if v[0] == rk), None))
                                      if rk else None),
                     "no_result_pic": not result_pic,
                     "travel": "down" if matra == ANU else "left",
                     "syl_ms":  _matra_cue_ms(a["onset"],  ONSET_LINE, "बनता"),
                     "join_ms": _matra_cue_ms(a["result"], RESULT_LINE, "जुड़ने"),
                     "sound_ms": _sound_cues_ms(a.get("sounds"), 3),
                     # file 3 / S02: the sign lands on the onset line's last phrase, the picture on
                     # the result line's last phrase, the tail on «X जुड़ने» - measured off the clips
                     "drop_ms": (ON_RUNS[-1] if len(ON_RUNS) >= 2
                                 else _matra_cue_ms(a["onset"], ONSET_LINE, syllable)),
                     "pic_ms": (RE_RUNS[-1] if len(RE_RUNS) >= 2
                                else _matra_cue_ms(a["result"], RESULT_LINE, result_word)),
                     "tail_ms": ((RE_RUNS[1] if len(RE_RUNS) >= 3
                                  else _matra_cue_ms(a["result"], RESULT_LINE, "%s जुड़ने" % tail))
                                 if tail else 0),
                     "base_img": (pic(bk) if bk else None),
                     "base_emoji": (BASE_OBJ[base_word][1] if bk and base_word in BASE_OBJ else None),
                     "no_base_pic": not base_pic,
                     "cap_base": None, "cap_mid": None, "cap_result": None,
                     "no_heading": True}}


def s_pair(sid, words, lead, lines, pictures=True):
    """Example words one at a time - file 3's MEET_PAIR (no heading; S02's line shape «शब्द, इसमें …
    की मात्रा लगी है। बोलकर देखिए।»: the picture comes with «इसमें», the sign lights on «अं / अः»)."""
    ex = []
    for w, line in zip(words, lines):
        k = key_of(w)
        vid = "vo_meet_" + slug(k)
        vo(vid, line)
        ex.append({"word": w, "matra": matra_of(w),
                   "img": pic(k) if pictures else None,
                   "emoji": OBJ[k][1] if pictures else None,
                   "no_pic": not pictures,
                   "audio_line": vid,
                   "pic_ms": ((_voice_runs_ms(vid) + [0, 0])[1] or _matra_cue_ms(vid, line, "इसमें")),
                   "matra_ms": _matra_cue_ms(vid, line, MATRA_NAME[matra_of(w)]),
                   "matra_audio": None})
    return {"id": sid, "phase": "tutorial", "eis": "iconic", "type": "MEET_PAIR",
            "prompt_hi": "",
            "audio": {"prompt": vo("vo_%s_prompt" % sid.lower(), lead)},
            "data": {"examples": ex, "no_heading": True,
                     "mic_nudge_audio": once("vo_mic_nudge", "इस बटन पर टैप करिए।"),
                     # [S05 2026-10-23] file 3's logic: the hand + «इस बटन पर टैप करिए» come at once only after
                     # page 4's FIRST word (अंडा, the child's first mic); बंदर and page 6 wait for 7 s of inactivity
                     "mic_nudge_now": sid == "T4"}}


def s_tap(sid, words, target, matra, correct_line):
    """Tap the coach whose word carries the sign - file 3's TRAIN_TAP lines, with अं / अः."""
    n = MATRA_NAME[matra]
    tag = TAG[matra]
    return {"id": sid, "phase": "guided", "eis": "symbolic", "type": "TRAIN_TAP",
            "prompt_hi": "“%s” की मात्रा वाले शब्द पर टैप कीजिए।" % LETTER[matra],
            "audio": {
                "prompt": once("vo_tap_prompt_" + tag,
                               "जिस डिब्बे में %s की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।" % n),
                "hint1": once("vo_tap_h1_" + tag,
                              "फिर से पढ़िए। %s की मात्रा वाले शब्द पर टैप कीजिए।" % n),
                "hint2": once("vo_tap_h2_" + tag, "%s की मात्रा वाले शब्द पर टैप कीजिए।" % n),
                "hint3": vo("vo_%s_h3" % sid.lower(),
                            "%s शब्द में %s की मात्रा है। %s पर टैप कीजिए।" % (target, n, target)),
                "correct": vo("vo_%s_correct" % sid.lower(), correct_line)},
            "data": {"target": target, "matra": matra,
                     "coaches": [{"word": w, "correct": (w == target),
                                  "audio": name_clip(w), "matra": matra_of(w)} for w in words]}}


def s_sort(sid, phase, kind, bins, cards, heading, prompt, hint1, hint2, single=False,
           hint3_fallback=None):
    return {"id": sid, "phase": phase, "eis": "enactive", "type": "TRAIN_SORT",
            "prompt_hi": heading,
            "audio": dict([("prompt", vo("vo_%s_prompt" % sid.lower(), prompt)),
                           ("hint1", hint1)]
                          + ([("hint2", hint2)] if hint2 else [])
                          + ([("hint3", hint3_fallback)] if hint3_fallback else [])),
            "data": {"kind": kind, "bins": bins, "cards": cards, "single": single}}


def s_word_build(sid):
    """P1 - file 3's WORD_BUILD lines: _दर · _खा · _डा from बं · छः · पं · दुः · झं."""
    slots, opts = [], []
    for word, head, tail in [("बंदर", "बं", "दर"), ("पंखा", "पं", "खा"), ("झंडा", "झं", "डा")]:
        k = key_of(word)
        slots.append({"word": word, "head": head, "tail": tail, "matra": matra_of(word),
                      "img": pic(k), "emoji": OBJ[k][1],
                      "name_audio": name_clip(word),
                      # file 3 / S02 rung 3, sounding the word out: «पु को पुल वाले डिब्बे में डालिए। पु, ल… पुल।»
                      "hint3_audio": vo("vo_p1_h3_" + slug(k),
                                        "%s को %s वाले डिब्बे में डालिए। %s, %s… %s।"
                                        % (head, word, head, tail, word)),
                      "correct_audio": vo("vo_wb_" + slug(k), "शाबाश! %s बन गया।" % word)})
    for ak, aid in [("बं", "vo_ak_ban"), ("छः", "vo_ak_chhah"), ("पं", "vo_ak_pan"),
                    ("दुः", "vo_ak_duh"), ("झं", "vo_ak_jhan")]:
        opts.append({"akshar": ak, "audio": vo(aid, ak)})
    ask = "चित्र देखकर सही अक्षर से शब्द पूरा कीजिए।"
    return {"id": sid, "phase": "practice", "eis": "enactive", "type": "WORD_BUILD",
            "prompt_hi": ask,
            "audio": {
                "prompt": vo("vo_%s_prompt" % sid.lower(), ask),
                # file 3 / S02 page-12 lines
                "hint1": vo("vo_%s_h1" % sid.lower(),
                            "फिर से देखिए। चित्र का नाम सोचिए और देखिए शब्द पूरा करने के लिए "
                            "कौन-सा अक्षर लगेगा।"),
                "hint2": vo("vo_%s_h2" % sid.lower(),
                            "नाम ध्यान से सुनिए। जिस शब्द की शुरुआत इस अक्षर से होती है, उसी "
                            "डिब्बे में इसे डालिए।"),
                "hint3": vo("vo_%s_h3_any" % sid.lower(),
                            "जो अक्षर चमक रहा है, उसे उसी डिब्बे में डालिए।")},
            "data": {"slots": slots, "options": opts}}


SC_HEADING = "सही शब्द चुनकर वाक्य पूरा कीजिए।"


def _full(pre, word, post):
    """the sentence with `word` in its blank - the exact text its `_try_` clip was recorded from"""
    return (pre + word + post).replace("  ", " ").strip()


def s_sentence(sid, scene, pre, post, answer, options, correct_line, ask, text_only=False):
    """P3 / P4 - file 3's sentence ladder: per-screen question on rung 1, «जो वाक्य सही लग रहा है,
    वही शब्द चुनिए।» on rung 2, «<sentence> <word> चुनिए।» on rung 3."""
    o = []
    for w in options:
        k = key_of(w)
        o.append({"word": w, "img": pic(k), "emoji": OBJ[k][1], "audio": name_clip(w),
                  "sentence_audio": vo("vo_%s_try_%s" % (sid.lower(), slug(k)), _full(pre, w, post))})
    return {"id": sid, "phase": "practice", "eis": "symbolic", "type": "SENTENCE_COMPLETE",
            "prompt_hi": SC_HEADING,
            "audio": {
                "prompt": once("vo_sc_prompt", "चित्र देखकर सही शब्द चुनकर वाक्य पूरा कीजिए।"),
                "hint1": vo("vo_%s_h1" % sid.lower(),
                            "फिर से पढ़िए। चित्र देखिए, %s? सही शब्द चुनकर वाक्य पूरा कीजिए।" % ask),
                "hint2": once("vo_sc_h2", "जो वाक्य सही लग रहा है, वही शब्द चुनिए।"),
                "hint3": vo("vo_%s_h3" % sid.lower(), "%s %s चुनिए।" % (_full(pre, answer, post), answer)),
                "correct": vo("vo_%s_correct" % sid.lower(), correct_line)},
            "data": {"scene_img": pic(scene), "scene_emoji": SCENE[scene],
                     "sentence_pre": pre, "sentence_post": post,
                     "answer": answer, "options": o,
                     "opts_text_only": bool(text_only),
                     "sentence_on_correct": (
                         None if _full(pre, answer, post).rstrip("।") in correct_line
                         else vo("vo_%s_try_%s" % (sid.lower(), slug(key_of(answer))),
                                 _full(pre, answer, post))),
                     "sentence_full": _full(pre, answer, post),
                     "scene_glow": SCENE_GLOW.get(scene, [])}}


def sort_card(word, correct_audio):
    k = key_of(word)
    return {"bin": matra_of(word), "word": word, "img": pic(k), "emoji": OBJ[k][1],
            "audio": name_clip(word), "correct_audio": correct_audio}


def build_slides():
    """[S05-r3] file 3's lesson, screen for screen, with this lesson's words. File 3's order:
    T pairs · names (this lesson's own) · builds/pairs · G5D demo · G5 sign sort · G1 · G2 taps ·
    G4 word sort · P1 word build · P2 picture sort · P3/P4 sentences · MG1 · CEL."""
    S = []
    # ---- TUTORIAL -----------------------------------------------------------------------------
    S.append(s_intro("T1"))
    S.append(s_names("T2"))
    S.append(s_build("T3", "गोद", "गो", ANU, "गों", "गोंद",
                     {"prompt": "आइए, देखें कि अं की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है।",
                      "base": "यह शब्द देखिए, गोद।",
                      "onset": "गो के साथ अं की मात्रा लगाने पर गों बनता है।",
                      "result": "अब द जुड़ने पर गोंद बनता है।"},
                     sounds="गो। गों। गोंद।"))
    S.append(s_pair("T4", ["अंडा", "बंदर"], "आइए, अं की मात्रा वाले कुछ शब्द देखें।",
                    ["अंडा, इसमें अ पर अं की मात्रा लगी है। बोलकर देखिए।",
                     "बंदर, इसमें ब पर अं की मात्रा लगी है। बोलकर देखिए।"]))
    # छह -> छः is a second way of WRITING the same word, not a new sound - the deck's own lines
    S.append(s_build("T5", "छह", "छ", VIS, "छः", "छः",
                     {"prompt": "आइए, देखें कि अः की मात्रा के शब्द को और कैसे लिख सकते हैं।",
                      "base": "यह शब्द देखिए, छह।",
                      "onset": "छ के साथ अः की मात्रा लगाने पर छः बनता है।",
                      "result": "छह को छः भी लिखते हैं। दोनों का मतलब एक ही है।"},
                     result_key="obj_aam"))      # [S05] user: the six-mango picture under छह and छः
    S.append(s_pair("T6", ["प्रातः"], "आइए, अः की मात्रा वाला एक शब्द देखें।",
                    ["प्रातः, इसमें त के आगे अः की मात्रा लगी है। बोलकर देखिए।"]))   # [S05] user: the sunrise picture

    # ---- GUIDED -------------------------------------------------------------------------------
    S.append(s_tap("G1", ["बंदर", "छः", "प्रातः"], "बंदर", ANU,
                   "शाबाश! बंदर शब्द में अं की मात्रा है।"))
    S.append(s_tap("G2", ["जंगल", "पंखा", "प्रातः"], "प्रातः", VIS,
                   "शाबाश! प्रातः शब्द में अः की मात्रा है।"))

    g4_h1 = vo("vo_g4_h1", "फिर से पढ़िए। शब्द में कौन-सी मात्रा है, देखिए और उसे उसी मात्रा वाले डिब्बे में डालिए।")
    p2_h1 = vo("vo_p2_h1", "फिर से सुनिए। चित्र का नाम ध्यान से सुनिए और देखिए उसमें कौन-सी मात्रा है।")
    bins = [{"key": m, "label": LETTER[m], "audio": LETTER_VO[m], "matra": m} for m in (ANU, VIS)]
    # file 3's G5 demo: the letters carried onto the sign coaches, watch-only, handing its train to G5
    S.append({"id": "G5D", "phase": "guided", "eis": "iconic", "type": "TRAIN_SORT",
              "prompt_hi": "देखिए, अक्षर को उसकी मात्रा वाले डिब्बे में कैसे डालते हैं।",
              "audio": {"prompt": vo("vo_g5d_prompt",
                                     "देखिए, अक्षर को उसकी मात्रा वाले डिब्बे में कैसे डालते हैं।"),
                        "outro": vo("vo_g4d_end", "अब आप भी ऐसे ही करके देखिए।")},
              "data": {"kind": "matra", "single": True, "demo": True, "keep_train_next": True,
                       "bins": [{"key": m, "label": m, "audio": MATRA_VO[m], "matra": m}
                                for m in (ANU, VIS)],
                       "cards": [{"bin": m, "word": LETTER[m], "audio": LETTER_VO[m],
                                  "correct_audio": vo("vo_g5d_%s" % TAG[m],
                                                      "%s की मात्रा इस डिब्बे पर है, इसलिए %s इस डिब्बे में गया।"
                                                      % (LETTER[m], LETTER[m]))}
                                 for m in (ANU, VIS)]}})
    # the word round
    g4_cards = []
    for w in ["बंदर", "छः", "अंडा", "प्रातः"]:
        m = matra_of(w)
        c = sort_card(w, vo("vo_ok_%s" % slug(key_of(w)),
                            "शाबाश! %s शब्द में %s की मात्रा है।" % (w, LETTER[m])))
        c["hint2_audio"] = vo("vo_g4_h2_%s" % slug(key_of(w)), "%s में %s की मात्रा है।" % (w, LETTER[m]))
        c["hint3_audio"] = vo("vo_g4_h3_%s" % slug(key_of(w)),
                              "%s शब्द में %s की मात्रा है। इसे %s वाले डिब्बे में डालिए।"
                              % (w, LETTER[m], LETTER[m]))
        g4_cards.append(c)
    S.append(s_sort("G4", "guided", "word", bins, g4_cards,
                    "हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
                    "हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
                    g4_h1, None))
    # the sign round: ◌ं / ◌ः into the अं / अः coaches (file 3's G5)
    S.append(s_sort("G5", "guided", "matra", bins,
                    [{"bin": m, "word": m, "audio": MATRA_VO[m],
                      "hint3_audio": vo("vo_g5_h3_%s" % TAG[m],
                                        "यह %s की मात्रा है। इसे %s वाले डिब्बे में डालिए।"
                                        % (LETTER[m], LETTER[m])),
                      "correct_audio": vo("vo_ok_matra_%s" % TAG[m],
                                          "शाबाश! यह %s की मात्रा है।" % LETTER[m])}
                     for m in (ANU, VIS)],
                    "सही मात्रा को सही डिब्बे में डालिए।",
                    "सही मात्रा को सही डिब्बे में डालिए।",
                    vo("vo_g5_h1", "फिर से देखिए। सही मात्रा को सही डिब्बे में डालिए।"),
                    vo("vo_g5_h2", "मात्रा का आकार ध्यान से देखिए। इसे सही डिब्बे में डालिए।"),
                    single=True))

    # ---- PRACTICE -----------------------------------------------------------------------------
    S.append(s_word_build("P1"))
    p2_cards = []
    for w in ["झंडा", "प्रातः", "पंखा"]:
        m = matra_of(w)
        c = sort_card(w, vo("vo_okp_%s" % slug(key_of(w)), "शाबाश! %s में %s की मात्रा है।" % (w, LETTER[m])))
        c["hint2_audio"] = vo("vo_p2_h2_%s" % slug(key_of(w)),
                              "%s में %s की मात्रा है। अब इसे सही मात्रा वाली बोगी में डालिए।" % (w, LETTER[m]))
        c["hint3_audio"] = vo("vo_p2_h3_%s" % slug(key_of(w)),
                              "%s को %s की मात्रा वाली बोगी में डालिए।" % (w, LETTER[m]))
        p2_cards.append(c)
    S.append(s_sort("P2", "practice", "picture", bins, p2_cards,
                    "चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए।",
                    "चित्र का नाम सुनिए और उसे सही मात्रा वाले डिब्बे में डालिए।",
                    p2_h1, None))
    S.append(s_sentence("P3", "scn_garmi", "गरमी में ", " चलता है।", "पंखा",
                        ["पंखा", "झंडा", "प्रातः"], "शाबाश! गरमी में पंखा चलता है।",
                        "गरमी में क्या चलता है"))
    S.append(s_sentence("P4", "scn_chidiya", "चिड़िया ने एक ", " दिया।", "अंडा",
                        ["अंडा", "बंदर", "छः"], "शाबाश! चिड़िया ने एक अंडा दिया।",
                        "चिड़िया ने क्या दिया"))

    # file 3's / S02's sequence: the G5 demo and G5 open the guided block, then the taps, then G4
    SEQ = ["G5D", "G5", "G1", "G2", "G4", "P1", "P2", "P3", "P4"]
    _by = {x["id"]: x for x in S}
    assert set(SEQ) <= set(_by), "sequence names a screen that does not exist"
    S[:] = [x for x in S if x["id"] not in SEQ] + [_by[i] for i in SEQ]

    # ---- the मात्रा रनर: अं only, one level (the S05 SME) ---------------------------------------
    mg_prompt = "अब एक खेल! ऊपर दी गई मात्रा वाले शब्द पकड़िए।"
    S.append({"id": "MG1", "phase": "practice", "eis": "enactive", "type": "MINI_GAME",
              "prompt_hi": mg_prompt,
              "audio": {"prompt": vo("vo_mg_prompt", mg_prompt)},
              "data": {"src": "matra-runner/index.html", "title": "मात्रा रनर"}})

    recap = CEL_LINE
    S.append({"id": "CEL", "phase": "practice", "eis": "iconic", "type": "CELEBRATION",
              "prompt_hi": recap,
              "audio": {"prompt": vo("vo_cel_prompt", recap)}, "data": {}})
    return S


def build_card(slides):
    for vid, text in MATRA_TEXT.items():
        vo(vid, text)
    # [S05-r3] file 3's cover line (S02 r134: page 1's opening line moved onto the cover)
    vo("vo_landing", "नमस्ते दोस्त! मैं हूँ स्विफ्टी। आज हम अं और अः की मात्रा वाले शब्द पढ़ेंगे।")
    vo("vo_try_again", "एक बार फिर सुनिए।")

    counts = {}
    for s in slides:
        counts[s["phase"]] = counts.get(s["phase"], 0) + 1
    audio = {v: "assets/Audio/%s.ogg" % v for v in sorted(AUDIO_TEXT)}
    for v in COPY_AUDIO:
        audio.setdefault(v, "assets/Audio/%s.ogg" % v)
    image = {k: "assets/Images/%s.webp" % k for k in sorted(used_images(slides))}

    return {
        "version": "0.1", "skill_code": CODE, "lo_code": "HI02H11_L02",
        "grade": "02", "attribute": "H11", "skill_type": "CORE",
        "part_label": "", "medium": "hi",
        "title": {"hi": "मात्राओं की रेल", "en": "Matra train — anusvara and visarga"},
        "subtitle_hi": "",
        "theme": "toybox",
        "skill_description_hi": ("अं, अः मात्रा वाले शब्द पढ़ता है। "
                                 "शब्दों में आने वाली मात्रा पहचानता है।"),
        "landing_audio": "vo_landing",
        # SME: the existing two-bogie train, 1st अं (◌ं), 2nd अः (◌ः), dotted circles as guides
        "landing_hero": {"kind": "matra_train", "matras": [ANU, VIS], "letters": ["अं", "अः"]},
        "phase_transition_audio": {"tutorial": "vo_pt_tutorial", "guided": "vo_pt_guided",
                                   "practice": "vo_pt_practice"},
        "phase_transition_title": {"tutorial": "चलिए, रेल चलाएँ!", "guided": "साथ में करें।",
                                   "practice": "अब आपकी बारी।"},
        "phase_distribution": counts,
        "ui_sfx": {"play": "sfx_play_button", "next": "sfx_next_button"},
        # [r106] Yasir: "first she should seek from the bottom, then start speaking - the VO should start
        # when she starts speaking": back to her first speaking frame (r105 had made it 0)
        # [r142] the transition screen is Hindi-game-gender-identify's (engine phaseBlurTransition):
        # its Swifty (assets/UI/peeking_talk_up.webp) and animation replace the seeking bird and her
        # lip-sync, so `img`, `talk_at_ms`, `title_dur_ms` and the lip-sync sheet step are gone.
        "gate": {
                 # [r83] Yasir: the third transition «अब आपकी बारी!» after page 17, i.e. just before
                 # the runner game - not in front of the first practice page (engine: CARD.gate.at)
                 "at": {"round3": "MG1"},
                 # [r103] where each transition's on-screen phrase starts inside its clip, so the text
                 # appears when Swiftee says it: «चलिए, शुरू करें!» / «चलिए, साथ में करें!» /
                 # «अब आपकी बारी!» - measured (silencedetect -35 dB) on the shared kit clips
                 # [r109] re-measured on the recorded transition lines (25 ms envelope, the phrase
                 # after the last long pause): «चलिए, शुरू करें!» 3075-4225 ms of 4.32 s, «चलिए, साथ
                 # में करें!» 3575-4900 of 5.01 s, «अब आपकी बारी।» 925-1775 of 1.87 s
                 # [S05 2026-10-23] re-measured on the user's own transition recordings (phrase runs):
                 # «चलिए, शुरू करें!» 3370 ms of 4.74 s · «चलिए, साथ में करें!» 3520 of 4.84 · «अब आपकी बारी।» 940 of 1.86
                 "title_cue_ms": {"tutorial": 3370, "guided": 3520, "practice": 940}},
        # S05: the hand on rung 3 only on the guided taps and sorts — "Use glow and lock without a
        # hand" on word build, picture sort and both sentences (practice). So the practice hand
        # S02 switched on is OFF here; ruling [28f] keeps the hand out of practice.
        "scaffold_rules": {"nudge_timeout_ms": {"guided": 6000, "practice": 8000},
                           "max_attempts": 3, "hint_levels": 3, "hand_on_attempt": 3,
                           "hand_on_hint3": True, "lock_after_hint3": True,
                           "reveal_on_attempt": None, "silent_on_late_correct": True},
        "signals_expected": ["slide_entered", "slide_completed", "intro_letter_tap",
                             "train_tap_first_try", "matra_sort_item", "matra_sort_first_try",
                             "word_build_item", "word_build_first_try",
                             "sentence_complete_first_try",
                             "answer_wrong", "hint_shown",
                             "phase_transition", "mastery_score", "lesson_completed"],
        "_emoji_fallback": dict(list({k: v[1] for k, v in OBJ.items()}.items())
                                + [(v[0], v[1]) for v in BASE_OBJ.values()]
                                + list(SCENE.items())),
        "assets": {"audio": audio, "audio_text": AUDIO_TEXT, "image": image,
                   "audio_ext": "ogg", "img_ext": "webp"},
        "slides": slides,
    }



# ---------------------------------------------------------------- guards
def used_images(slides):
    """Every image key a slide actually renders. `pic()` returns None for art that is not on disk
    yet, so a pending picture never reaches this set and never lands in assets.image."""
    used = set()
    for s in slides:
        d = s.get("data", {}) or {}
        for k in ("result_img", "base_img", "scene_img"):
            if d.get(k):
                used.add(d[k])
        for group in ("examples", "cards", "slots", "options"):
            for it in d.get(group, []) or []:
                if isinstance(it, dict) and it.get("img"):
                    used.add(it["img"])
    return used


def guard_engine(src):
    m = VER_RE.search(src)
    if not m:
        sys.exit("X  no ENGINE_VERSION in 4_ENGINE/lesson_template.html")
    ver = m.group(1)
    for name in TRAIN_MODULES:
        if ("SlideModules." + name + " = {") not in src:
            sys.exit("X  the engine copy is missing the module %s. Re-run the injector "
                     "(4_ENGINE/inject_train.py); do NOT hand-edit the monolith." % name)
    for name in STOCK_MODULES:
        if not (re.search(r'^\s{2}"?' + name + r'"?\s*[:(]', src, re.M)
                or re.search(r'SlideModules\.' + name + r'\s*=', src)):
            sys.exit("X  the engine copy is missing the stock module %s" % name)
    if "TRAIN STYLES :: BEGIN" not in src:
        sys.exit("X  the train CSS block is missing — the coaches would render unstyled")
    if 'case "letter":' not in src:
        sys.exit("X  conceptTileHTML has no `letter` case — the landing strip would be empty")
    if "dressLandingTrain" not in src:
        sys.exit("X  the landing-train dressing is missing — the landing bogies would not render")
    if 'kind !== "matra_train"' not in src:
        sys.exit("X  the landing train is still the drawn version — re-run inject_train.py")
    if "TrainChrome" not in src or "TRAIN_ART" not in src:
        sys.exit("X  TrainChrome is missing — the activity screens would draw a SECOND, "
                 "different locomotive beside the painted cover. "
                 "Re-run 4_ENGINE/inject_train.py.")
    print("  OK  engine: %s  (4_ENGINE, pinned)" % ver)
    print("      modules present: %s" % ", ".join(TRAIN_MODULES))
    print("      train styles present")
    return ver


def guard_flow(slides):
    """The flow must match the deck screen for screen, plus the mini-game: landing + 18."""
    # [S05-r3] file 3's / S02's order, with this lesson's names screen, two taps and two sentences
    want = ["MATRA_PAIRS", "MATRA_PAIRS", "MATRA_BUILD", "MEET_PAIR", "MATRA_BUILD", "MEET_PAIR",
            "TRAIN_SORT",         # G5D - the watch-only demo
            "TRAIN_SORT",         # G5 - the sign round
            "TRAIN_TAP", "TRAIN_TAP",
            "TRAIN_SORT",         # G4 - the word round
            "WORD_BUILD", "TRAIN_SORT",
            "SENTENCE_COMPLETE", "SENTENCE_COMPLETE",
            "MINI_GAME", "CELEBRATION"]
    got = [s["type"] for s in slides]
    if got != want:
        sys.exit("X  flow does not match the SME's S05 deck.\n     want: %s\n     got:  %s"
                 % (want, got))
    print("  OK  flow guard: landing + %d slides, in file 3's (S02's) order" % len(slides))


def guard_single_matra():
    bad = []
    for w, m in [(v[0], v[2]) for v in OBJ.values()]:
        found = set(c for c in w if c in (U, UU))
        if found != set([m]):
            bad.append("%s carries %s, declared %r" % (w, sorted(found) or "none", m))
    if bad:
        sys.exit("X  single-matra rule broken:\n     " + "\n     ".join(bad))
    print("  OK  single-matra rule: all %d words carry exactly one target matra" % len(OBJ))


def guard_sentences(slides):
    """Every sentence screen must be answerable and must not give itself away.

    Two ways a sentence screen can be quietly broken, both invisible to an existence check: the
    answer is not among the options (unanswerable), or the answer is already printed in the
    sentence (free). Whether a distractor ALSO reads correctly cannot be decided mechanically —
    that one is a human read, and it is on the verification list.
    """
    bad = []
    for s in slides:
        if s["type"] != "SENTENCE_COMPLETE":
            continue
        d = s["data"]
        words = [o["word"] for o in d["options"]]
        if d["answer"] not in words:
            bad.append("%s: answer %r is not one of the options %s" % (s["id"], d["answer"], words))
        if len(set(words)) != len(words):
            bad.append("%s: duplicate option %s" % (s["id"], words))
        shown = (d["sentence_pre"] or "") + (d["sentence_post"] or "")
        if d["answer"] in shown:
            bad.append("%s: the answer %r is already printed in the sentence"
                       % (s["id"], d["answer"]))
    if bad:
        sys.exit("X  sentence audit:\n     " + "\n     ".join(bad))
    n = len([s for s in slides if s["type"] == "SENTENCE_COMPLETE"])
    print("  OK  sentence audit: %d screens, answer present as an option and never pre-printed" % n)


def guard_word_build(slides):
    """A WORD_BUILD option must complete EXACTLY ONE coach, and every coach must be completable.

    The module judges a drop by reconstructing the word (`akshar + tail == word`), so an option
    that completed two coaches would make one of them accept the wrong tile, and a distractor that
    accidentally completed a coach would mark a wrong answer right. Both are silent at runtime.
    """
    for s in slides:
        if s["type"] != "WORD_BUILD":
            continue
        d = s["data"]
        for sl in d["slots"]:
            hits = [o["akshar"] for o in d["options"] if o["akshar"] + sl["tail"] == sl["word"]]
            if len(hits) != 1:
                sys.exit("X  word-build: %r is completed by %s — must be exactly one option"
                         % (sl["word"], hits or "nothing"))
        dis = [o["akshar"] for o in d["options"]
               if not any(o["akshar"] + sl["tail"] == sl["word"] for sl in d["slots"])]
        if not dis:
            sys.exit("X  word-build: the SME asks for 1-2 distractors; there are none")
        if "मी" in [o["akshar"] for o in d["options"]]:
            sys.exit("X  word-build: मी is still an option — the SME asked for it to be removed")
        print("  OK  word-build audit: %d coaches, exactly 1 option each, distractors %s"
              % (len(d["slots"]), dis))


GESTURE = {"TRAIN_TAP": "pick", "TRAIN_SORT": "drag", "MATRA_FILL": "drag",
           "WORD_BUILD": "drag", "SENTENCE_COMPLETE": "pick", "POEM_SEARCH": "search"}


def guard_prompts(slides):
    """EVERY slide must carry on-screen heading text.

    THE DEFECT THIS EXISTS TO PREVENT (SME review round 2, 2026-09-21):
    «ऊपर स्विफ्टी वाले बॉक्स की हेडिंग मिसिंग है». The first build shipped prompt_hi: "" on 14 of
    16 slides and then hid the heading band with CSS, because the SME's per-screen note says
    "No instruction text on screen. Only VO should play." That reading was wrong — their own
    mockups draw the band, with text in it, on both test and teach screens, and the round-3
    mockups draw it again on all four sentence screens and on the word-build screen. The note
    means no EXTRA explanatory copy in the PLAY AREA; the heading band beside the mascot is house
    chrome on every screen of every shipped lesson.

    Failing the build is the right response because the symptom was invisible to every other
    check: the page scored 0 FAIL / 0 WARN, all assets served and no JS errored — it simply had a
    mascot sitting next to nothing.
    """
    bad = [sl["id"] for sl in slides
           if not (sl.get("prompt_hi") or "").strip()
           and not (sl.get("data") or {}).get("no_heading")]
    if bad:
        sys.exit("X  guard_prompts: empty prompt_hi on %s — the heading band would render "
                 "blank beside the mascot" % ", ".join(bad))
    short = [(sl["id"], sl["prompt_hi"]) for sl in slides
             if not (sl.get("data") or {}).get("no_heading")
             and len(sl["prompt_hi"].strip()) < 8]
    if short:
        sys.exit("X  guard_prompts: heading too short to read: %s" % short)
    opted = [sl["id"] for sl in slides if (sl.get("data") or {}).get("no_heading")]
    print("   guard_prompts ....... %d/%d slides carry heading text%s"
          % (len(slides) - len(opted), len(slides),
             ("; %s opted out on the SME's instruction" % ", ".join(opted)) if opted else ""))


BAD_REGISTER = ["करो", "सोचो", "देखो", "डालो", "सुनो", "चुनो", "पढ़ो", "बोलो", "ढूँढो",
                "घुमाओ", "मिलाओ", "लगाओ", "बनाओ", "तुम"]
# [r105] the one line allowed a तुम form: the standard Swiftee end-screen dialogue Yasir chose
CEL_LINE = "बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया!"
REGISTER_ALLOW = {CEL_LINE}


def guard_register(slides, card):
    """No तुम-form imperative may survive the round-3 flip.

    The SME says it twice — "Use respectful language throughout: सुनिए, पहचानिए, डालिए" and
    "Maintain respectful language: सोचिए, देखिए, चुनिए instead of सोचो, देखो, चुनो". Round 2 was
    entirely तुम, so this touches almost every clip and every heading, and a single missed line
    reads as sloppiness rather than as a bug — which is exactly the kind of thing no other check
    would catch. So it is checked mechanically.
    """
    hits = []
    targets = [("%s (clip)" % v, t) for v, t in AUDIO_TEXT.items()]
    targets += [("%s heading" % s["id"], s.get("prompt_hi") or "") for s in slides]
    targets += [("phase title %s" % k, v) for k, v in card["phase_transition_title"].items()]
    for where, text in targets:
        if text in REGISTER_ALLOW:
            continue
        for b in BAD_REGISTER:
            if b in text:
                hits.append("%s: %s" % (where, text))
                break
    if hits:
        sys.exit("X  register guard: तुम-form survives the round-3 flip in %d place(s):\n     %s"
                 % (len(hits), "\n     ".join(hits)))
    print("  OK  register guard: आप throughout — no तुम form in any clip, heading or phase title")


def guard_mechanics(slides):
    # [r36] MINI_GAME is excluded with CELEBRATION: the drag/pick ratio is about how the lesson
    # ASKS its questions, and a runner asks none - counting it would skew a balance the deck set.
    tests = [s for s in slides
             if s["phase"] != "tutorial" and s["type"] not in ("CELEBRATION", "MINI_GAME")]
    fams = {}
    for s in tests:
        f = GESTURE.get(s["type"])
        if not f:
            sys.exit("X  %s: %s unclassified in GESTURE" % (s["id"], s["type"]))
        fams[f] = fams.get(f, 0) + 1
    n = len(tests)
    if len(fams) < 2:
        sys.exit("X  mechanic gate: one family only")
    if "drag" not in fams:
        sys.exit("X  mechanic gate: no produce mechanic")
    # ROUND 3 RAISES THE CEILING FROM 60% TO 70%, AND THAT IS A REAL LOOSENING — so it says so out
    # loud rather than being quietly widened. The SME's round-3 flow is three tap screens plus
    # four sentence screens against four drag screens: 7 pick / 4 drag = 64% pick. The gate exists
    # to stop a lesson being one gesture end to end, and 64/36 across two families with a real
    # produce mechanic is not that. The deck is authoritative on the flow, so the guard moves
    # rather than the lesson — and the move is reported in the scorecard.
    for f, c in sorted(fams.items()):
        if 100.0 * c / n > 70.0:
            sys.exit("X  mechanic gate: %s is %.0f%% of %d test slides" % (f, 100.0 * c / n, n))
    mix = ", ".join("%s %d (%.0f%%)" % (f, c, 100.0 * c / n) for f, c in sorted(fams.items()))
    print("  OK  mechanic gate: %d test slides — %s" % (n, mix))
    if max(100.0 * c / n for c in fams.values()) > 60.0:
        print("  !!  NOTE: above the round-2 ceiling of 60%. The SME's round-3 flow is pick-heavy "
              "by design (3 tap + 4 sentence screens); ceiling raised to 70% for this deck.")


def guard_pictures(slides, card):
    used = used_images(slides)
    declared = set(card["assets"]["image"])
    if used - declared:
        sys.exit("X  images used but not declared: %s" % sorted(used - declared))
    if declared - used:
        sys.exit("X  images declared but never shown: %s" % sorted(declared - used))
    missing = [k for k, p in card["assets"]["image"].items()
               if not os.path.isfile(os.path.join(BUNDLE, p))]
    if missing:
        sys.exit("X  declared images missing from disk: %s" % sorted(missing))
    print("  OK  picture guard: %d images, all declared, all used, all on disk" % len(used))


def guard_audio(slides, card):
    """Every audio id a slide names must be declared, and every test slide must carry the whole
    3-rung ladder — a missing rung is a silent beat exactly when the child is stuck.

    ROUND 3: the `correct` rung may be satisfied PER ITEM instead of per slide. The SME moved the
    praise line onto each card («शाबाश! 'सुई' शब्द में उ की मात्रा है।») and asked for no completion
    line, so a sort or build screen whose every item carries `correct_audio` has a complete ladder
    without a slide-level clip — and demanding one would mean recording a line nothing ever plays.
    """
    declared = set(card["assets"]["audio"])
    miss, ladders = [], []
    for s in slides:
        d = s.get("data", {}) or {}
        for k, v in (s.get("audio") or {}).items():
            if v and v not in declared:
                miss.append("%s.%s -> %s" % (s["id"], k, v))
        items = (d.get("cards") or []) + (d.get("slots") or [])
        for group in ("cards", "slots", "options", "examples", "pairs", "bins", "coaches"):
            for it in d.get(group, []) or []:
                if not isinstance(it, dict):
                    continue
                for k in ("audio", "correct_audio", "audio_line", "matra_audio", "name_audio",
                          "hint1_audio", "hint2_audio", "hint3_audio", "sentence_audio"):
                    if it.get(k) and it[k] not in declared:
                        miss.append("%s %s.%s -> %s" % (s["id"], group, k, it[k]))
        # [r83] a watch-only demonstration asks the child nothing, so it has no ladder to check
        if s["type"] in GESTURE and not d.get("demo"):
            per_item = bool(items) and all(c.get("correct_audio") for c in items)
            # REVIEW-1: rungs 2 and 3 may be satisfied PER ITEM as well. On the word and picture
            # rounds both lines name the card («'सूरज' में बड़ी 'ऊ' की मात्रा है»), so a
            # screen-level recording would be a line nothing ever plays.
            per_h2 = bool(items) and all(c.get("hint2_audio") for c in items)
            per_h3 = bool(items) and all(c.get("hint3_audio") for c in items)
            for rung in ("prompt", "hint1", "hint2", "hint3", "correct"):
                if (s.get("audio") or {}).get(rung):
                    continue
                if rung == "correct" and per_item:
                    continue
                if rung == "hint2" and per_h2:
                    continue
                if rung == "hint3" and per_h3:
                    continue
                ladders.append("%s missing %s" % (s["id"], rung))
    if miss:
        sys.exit("X  undeclared audio ids:\n     " + "\n     ".join(miss))
    if ladders:
        sys.exit("X  incomplete 3-attempt ladder:\n     " + "\n     ".join(ladders))
    print("  OK  audio guard: every id declared; every test slide has a complete ladder")


# ---------------------------------------------------------------- stale-asset pruning
def prune_stale(card):
    """Delete exactly the clips round 3 invalidated — nothing more.

    THIS IS THE DEFECT IT PREVENTS, and it has already happened on this lesson once: a clip's TEXT
    changed in the builder while its ID stayed the same, the old .ogg stayed on disk, and
    `gen_tts.py` — which skips ids that already have a file — never re-recorded it. The game then
    shipped round-2 audio under round-3 text. It is invisible to an existence check and to a
    file-size check.

    The previous build's `card.json` still holds the previous `audio_text`, so the comparison is
    exact: a clip is STALE if its text changed and ORPHANED if its id is gone. Deleting exactly
    those leaves gen_tts a minimal, correct work list — which is also the rule about regenerating
    only what changed, since re-running an UNCHANGED clip returns a different take.
    """
    old_path = os.path.join(BUNDLE, "card.json")
    if not os.path.isfile(old_path):
        return [], [], []
    try:
        old = json.load(open(old_path, encoding="utf-8"))
    except Exception:
        return [], [], []
    old_text = (old.get("assets") or {}).get("audio_text") or {}
    new_text = card["assets"]["audio_text"]
    stale, orphan = [], []
    for vid, text in sorted(old_text.items()):
        if vid not in new_text:
            orphan.append(vid)
        elif new_text[vid] != text:
            stale.append(vid)
    for vid in stale + orphan:
        f = os.path.join(AUD_DIR, vid + ".ogg")
        if os.path.isfile(f):
            os.remove(f)
    old_img = set((old.get("assets") or {}).get("image") or {})
    img_orphan = sorted(old_img - set(card["assets"]["image"]))
    return stale, orphan, img_orphan


def write_vo_list():
    """The recording list, with the two traps this lesson keeps hitting called out by name."""
    risky = sorted(v for v, t in AUDIO_TEXT.items() if "—" in t or t.count("।") >= 3)
    with open(os.path.join(SPEC_DIR, "VO_RECORDING_LIST.md"), "w", encoding="utf-8") as f:
        f.write("# %s (भाग 1 — उ / ऊ) · «मात्राओं की रेल» — VO recording list (ROUND 3)\n\n" % CODE)
        f.write("%d clips. Shown text == spoken text; record exactly this.\n\n" % len(AUDIO_TEXT))
        f.write("**Register is आप** — the SME asked for it twice, in as many words. Round 2 was "
                "तुम, so most of this list is a re-record, not a new line. `guard_register` in the "
                "builder fails the build if a तुम form survives anywhere.\n\n")
        f.write("**Only re-record what changed.** The builder deletes exactly the clips whose text "
                "moved this round, so `gen_tts.py` (which skips ids that already have a file) "
                "regenerates precisely those and leaves every unchanged take alone. Never "
                "`--force` the whole card: generated audio is non-deterministic, so re-running an "
                "unchanged clip returns a different take — a change the SME never asked for.\n\n")
        f.write("## ⚠️ EAR-CHECK — %d clips a human must listen to before delivery\n\n" % len(risky))
        f.write("The TTS model truncates a clip when an **em-dash precedes a short final word** "
                "(measured on this lesson: em-dash 0.73–1.05 s vs comma 1.53–2.21 s for the same "
                "words), and it does the same to a line built from several short danda-separated "
                "pieces. The SME's round-3 MEET_PAIR lines and the new sound-differentiation clips "
                "are written in exactly those shapes. Their wording ships as written — rewriting a "
                "reviewer's Hindi to dodge a synthesis bug is the worse failure — so the clips are "
                "flagged instead. **Truncation is invisible to an existence check and to a "
                "file-size check.** `_verify_assets.py` compares each clip against peers of "
                "similar text length and is the only thing that catches it. Run it, then listen to "
                "every id below.\n\n")
        for v in risky:
            f.write("- `%s` — %s\n" % (v, AUDIO_TEXT[v]))
        f.write("\n## All clips\n\n| clip id | spoken text |\n|---|---|\n")
        for v in sorted(AUDIO_TEXT):
            f.write("| `%s` | %s |\n" % (v, AUDIO_TEXT[v]))
        f.write("\n## Copied, do NOT record\n\n")
        for v in COPY_AUDIO:
            f.write("- `%s`\n" % v)
    return risky


ART_BRIEFS = {}   # every S05 picture exists (generated for the factory build)


def write_art_manifest(slides):
    """`_art_manifest.json` keeps the prompt for every picture in the lesson; the pending ones are
    split out so an art run can be pointed straight at a work list, and the scenes are named
    separately because they must NOT go through the chroma-key pipeline."""
    path = os.path.join(SPEC_DIR, "_art_manifest.json")
    existing = json.load(open(path, encoding="utf-8")) if os.path.isfile(path) else {}
    if isinstance(existing, dict) and "all" in existing:
        existing = existing["all"]
    allm = dict(existing)
    allm.update(ART_BRIEFS)
    # anything this card no longer shows is dropped, so nothing is regenerated for a deleted screen
    live = set(used_images(slides)) | set(PENDING_ART)
    allm = dict((k, v) for k, v in allm.items() if k in live)
    out = {"all": allm,
           "pending": dict((k, allm[k]) for k in sorted(PENDING_ART) if k in allm),
           "scenes_do_not_key": sorted(SCENE)}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return out


def check_chrome():
    """The shared UI chrome and the fixed clips (phase gates + SFX) already live in the bundle.

    The factory build copied them from a reference bundle under
    `<factory>/KG and G1 refernce ready HTML's`, which is OUTSIDE this self-contained handoff.
    Nothing here reaches out to it: the files are checked in place and a missing one is reported
    rather than silently re-copied from a path that does not exist.
    """
    ui = os.path.join(BUNDLE, "assets", "UI")
    n = len(os.listdir(ui)) if os.path.isdir(ui) else 0
    missing = [v for v in COPY_AUDIO if not os.path.isfile(os.path.join(AUD_DIR, v + ".ogg"))]
    print("  OK  chrome in place: %d UI files, %d/%d fixed clips"
          % (n, len(COPY_AUDIO) - len(missing), len(COPY_AUDIO)))
    if missing:
        print("  !!  fixed clips MISSING from the bundle: %s" % missing)


LETTER_GLOW_CSS = """
<style id="bundleLetterGlow">
/* Landing letter-strip glow. concept_strip returns before the engine adds show/hint-glow, so
   every such landing in the fleet misses it; raised as a dev ask. Base rule, not keyframes-only:
   capture_pages.py kills animation, and a glow that lives only in @keyframes vanishes from the
   review deck. Amber, because blue disappears against the pale-blue landing card.
   ROUND 3: scoped OFF the train landing — there the bogie is the frame, so the pill and its
   pulse would fight it. See `.lt-train .sg-ex-letter` in the train styles. */
.sg-ex-letter{
  box-shadow:0 0 0 6px rgba(255,206,46,.65),0 0 18px 4px rgba(252,188,24,.50),
             0 12px 28px rgba(11,61,140,.16);
  animation:sgLetterGlow 2.2s ease-in-out infinite;
}
.sg-acell:nth-child(1) .sg-ex-letter{animation-delay:.95s;}
.sg-acell:nth-child(2) .sg-ex-letter{animation-delay:1.40s;}
@keyframes sgLetterGlow{
  0%,100%{box-shadow:0 0 0 6px rgba(255,206,46,.65),0 0 18px 4px rgba(252,188,24,.50),
                     0 12px 28px rgba(11,61,140,.16);}
  50%    {box-shadow:0 0 0 10px rgba(255,206,46,.92),0 0 28px 8px rgba(252,188,24,.70),
                     0 14px 32px rgba(11,61,140,.22);}
}
@media (prefers-reduced-motion:reduce){ .sg-ex-letter{animation:none;} }
</style>
"""


# ---------------------------------------------------------------- [r85] celebration Swiftie
# The lip-synced celebration from celebration_kit/ (see its README): she jumps on «शाबाश!», talks
# with her beak opening on each syllable of THIS lesson's celebration line, then idles mouth shut.
#   · the kit's three sheets are copied UNCHANGED into assets/UI/celebration/ on every build
#   · the lip-sync track is measured from the celebration VO on every build, so a re-recorded clip
#     re-syncs by itself - make_lipsync.py is the kit's own measurer, run as it ships
#   · meta + track ride on the card as CARD.end_anim; the kit's player and the README's wrapper of
#     SlideModules.CELEBRATION.mount are injected after the engine script - the engine is not edited
KIT = os.path.join(HANDOFF, "celebration_kit")
CEL_DIR = os.path.join(BUNDLE, "assets", "UI", "celebration")


def celebration_anim(slides):
    import shutil, filecmp, tempfile, subprocess
    cel = [x for x in slides if x["type"] == "CELEBRATION"]
    vo_id = cel and (cel[0].get("audio") or {}).get("prompt")
    vo_path = vo_id and os.path.join(AUD_DIR, vo_id + ".ogg")
    if not (os.path.isdir(KIT) and vo_path and os.path.isfile(vo_path)):
        print("  !!  celebration Swiftie skipped (kit or %s missing) - the stock mascot stays" % vo_id)
        return None
    meta = json.load(open(os.path.join(KIT, "sheets", "cel_meta.json"), encoding="utf-8"))
    os.makedirs(CEL_DIR, exist_ok=True)
    for sheet in (meta["shabaash"]["src"], meta["talk"]["src"], meta["idle"]["src"]):
        a, b = os.path.join(KIT, "sheets", sheet), os.path.join(CEL_DIR, sheet)
        if not (os.path.isfile(b) and filecmp.cmp(a, b, shallow=False)):
            shutil.copy2(a, b)
    out = os.path.join(tempfile.gettempdir(), "cel_track_%s.json" % CODE)
    subprocess.run([sys.executable, os.path.join(KIT, "make_lipsync.py"), vo_path, "--json", out],
                   check=True, capture_output=True)
    track = json.load(open(out, encoding="utf-8"))
    if "1" not in track["bits"]:
        sys.exit("X  the celebration VO measured silent - no lip-sync track")
    print("  OK  celebration Swiftie: 3 kit sheets in assets/UI/celebration/, lip-sync track from %s "
          "(%d ms, %d steps)" % (vo_id, track["ms"], len(track["bits"])))
    return {"base": "assets/UI/celebration/", "vo": vo_id, "meta": meta, "track": track}


CEL_WRAP = r"""
/* [r85] THE CELEBRATION SWIFTIE - the kit's README wrapper, verbatim in intent. The engine's
   CELEBRATION module is wrapped, not edited: it still does everything it did (sfx, sunburst, stars,
   the arrow), then the stock .end-mascot is hidden and a 300x358 host takes its place - the mascot's
   own 358 px layout height, so the arrow below it keeps its exact size and position.
   The clock is the clip's own - see THE CLOCK below. */
(function(){
  if(typeof SlideModules === "undefined" || !SlideModules.CELEBRATION || typeof CARD === "undefined"
     || !CARD.end_anim || typeof SwiftieCelebration === "undefined") return;
  const EA = CARD.end_anim;
  /* the three sheets (~2 MB) are fetched quietly 12 s after the lesson loads, so on a first visit
     they are in the cache long before the last page: the kit only starts loading them when the
     celebration mounts, and on a slow connection the jump (350 ms in) would play before its sheet
     had arrived. Kept referenced so the cached copies are not dropped. */
  const _warm = [];
  const warm = ()=> [EA.meta.shabaash, EA.meta.talk, EA.meta.idle].forEach(s => {
    const i = new Image(); i.decoding = "async"; i.src = EA.base + s.src; _warm.push(i); });
  const arm = ()=> setTimeout(warm, 12000);
  if(document.readyState === "complete") arm(); else window.addEventListener("load", arm);
  /* THE CLOCK. The kit takes `audio` - anything with paused / ended / currentTime - and anchors
     itself as  t0 = now - currentTime  the first time it sees the clip sounding. Measured here: the
     celebration mounts in a burst of work (sunburst, stars, sound), the page's main thread stalls
     150-330 ms right as the clip starts, and a yes/no "sounding" signal is only noticed on the first
     frame AFTER the stall - which put the whole lip-sync 170-1470 ms late when opened as a file.
     So the clock below reports how long the clip has really been audible, from the moment it
     became so, however late the next frame runs:
       · Web Audio (served): when the engine started the source, + the context's output latency
       · <audio> (opened as a file): the element's own "playing" event timestamp */
  const _st = AudioBufferSourceNode.prototype.start;
  AudioBufferSourceNode.prototype.start = function(when){
    try{ const c = this.context;
      this.__swcAt = performance.now() + ((when && when > c.currentTime) ? (when - c.currentTime) * 1000 : 0)
                     + ((c.baseLatency || 0) + (c.outputLatency || 0)) * 1000; }catch(e){}
    return _st.apply(this, arguments);
  };
  const heardAt = ()=>{
    const a = currentAudio;
    if(a){
      if(!a.__swc){ a.__swc = true;
        a.addEventListener("playing", (e)=>{ a.__swcAt = e.timeStamp - a.currentTime * 1000; }); }
      return a.paused ? null : (a.__swcAt != null ? a.__swcAt
                               : (a.currentTime > 0 ? performance.now() - a.currentTime * 1000 : null));
    }
    return currentVoiceSource && currentVoiceSource.__swcAt != null ? currentVoiceSource.__swcAt : null;
  };
  const clock = {
    get paused(){ return !isPlaying || heardAt() == null; },
    get ended(){ return !isPlaying; },
    get currentTime(){ const t = heardAt(); return t == null ? 0 : Math.max(0, performance.now() - t) / 1000; }
  };
  const _cel = SlideModules.CELEBRATION.mount;
  SlideModules.CELEBRATION.mount = function(host, slide){
    const r = _cel.apply(this, arguments);
    const img = document.querySelector("#endScreen .end-mascot");
    let box = document.getElementById("celBox");
    if(!box && img){ box = document.createElement("div"); box.id = "celBox";
      /* the stock mascot's OWN layout height, measured before it is hidden: 330 px wide at its
         516x476 art is 357.72 px, not the kit's 358 - and 0.28 px is a whole screen pixel of arrow
         movement at 1920x1080. Falls back to the kit's 358 if the stock art never loaded. */
      const h = (img.naturalWidth && img.offsetWidth) ? img.offsetWidth * img.naturalHeight / img.naturalWidth : 358;
      box.style.cssText = "width:300px;height:" + h + "px;position:relative;z-index:2";
      img.parentNode.insertBefore(box, img); }
    if(!box) return r;
    if(img) img.style.display = "none";
    box.innerHTML = "";
    /* [r106] SHE JUMPS AND CELEBRATES FIRST, THEN SPEAKS. Yasir: "in the last celebration screen Swifty
       jumps and celebrates, then starts speaking - the VO should only play when she starts speaking".
       So the line is NOT played by the page on arrival (ownsAudio): the jump - the kit's own शाबाश
       sheet, its standing frames and its jump frames - plays first, silent but for the celebration
       sound; then the line starts and the kit's player takes over, with a track arranged so that it
       finishes the landing over the clip's lead-in and then lip-syncs the WHOLE line on the talk
       sheet (a 25 ms stand-in "first word" stops the kit spending the real first words on a jump). */
    state.ownsAudio = true;
    const M = EA.meta, S = M.shabaash, COLS = M.cols || 6;
    const sp = document.createElement("div"); sp.className = "swc-sprite";
    sp.innerHTML = '<div class="swc-art"></div>'; box.appendChild(sp);
    const art = sp.firstChild; art.style.aspectRatio = M.fw + " / " + M.fh;
    art.style.backgroundImage = 'url("' + EA.base + S.src + '")';
    const showF = (i)=>{ const c = i % COLS, rr = Math.floor(i / COLS);
      art.style.backgroundPosition = (c * 100 / (COLS - 1)) + "% " + (rr * 100 / (COLS - 1)) + "%";
      sp.dataset.sheet = "shabaash"; sp.dataset.f = i; };
    const frames = S.pre.concat(S.word), FMS = 45;          /* ~22 fps: 30 frames, 1.35 s */
    showF(frames[0]);
    const bits = EA.track.bits, lead = Math.max(0, bits.indexOf("1"));
    const step = EA.track.step_ms || 25;
    const bits2 = "1" + "00000000" + bits.slice(lead);      /* stand-in word, 200 ms gap, the line */
    const shift = (9 - lead) * step / 1000;                 /* keeps the line on the clip's clock */
    const clock2 = {
      get paused(){ return clock.paused; }, get ended(){ return clock.ended; },
      get currentTime(){ const t = clock.currentTime; return t > 0 ? Math.max(0.001, t + shift) : 0; }
    };
    const t0 = performance.now();
    (function jump(){
      if(!sp.isConnected || CARD.slides[state.idx] !== slide) return;
      const k = Math.floor((performance.now() - t0) / FMS);
      if(k < frames.length){ showF(frames[k]); requestAnimationFrame(jump); return; }
      /* the jump is over: the line starts, and the kit takes over the moment it is sounding */
      const src = (typeof audioFor === "function") ? audioFor(slide, "prompt") : null;
      if(src) play(src, ()=>{});
      const h = SwiftieCelebration.play({ host: box, meta: M, base: EA.base, bits: bits2, step_ms: step, audio: clock2 });
      h.el.style.animation = "none"; h.el.style.position = "absolute"; h.el.style.inset = "0";
      h.el.style.visibility = "hidden";
      (function swap(){
        if(!h.el.isConnected) return;
        if(h.el.dataset.t !== undefined || h.el.dataset.sheet === "idle"){ h.el.style.visibility = ""; sp.remove(); return; }
        requestAnimationFrame(swap);
      })();
    })();
    return r;
  };
})();
"""


def inject_celebration(html, card):
    if not card.get("end_anim") or 'id="swcKit"' in html:
        return html
    css = open(os.path.join(KIT, "swiftie_celebration.css"), encoding="utf-8").read()
    js = open(os.path.join(KIT, "swiftie_celebration.js"), encoding="utf-8").read()
    html, n1 = re.subn(r"</head>", lambda m: '<style id="swcKitCss">\n' + css + "</style>\n</head>", html, count=1)
    i = html.rfind("</body>")
    if n1 != 1 or i < 0:
        sys.exit("X  could not inject the celebration Swiftie")
    html = html[:i] + '<script id="swcKit">\n' + js + "\n" + CEL_WRAP + "</script>\n" + html[i:]
    print("  OK  celebration Swiftie injected (kit player + CELEBRATION.mount wrapper)")
    return html


def main():
    argparse.ArgumentParser().parse_args()
    # [r126] pictures -> WebP, videos -> WebM, before anything reads the asset folders (see the script)
    import subprocess
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 "normalize_assets.py")], check=True)
    if not os.path.isfile(ENGINE):
        sys.exit("X  no engine at %s" % ENGINE)
    src = open(ENGINE, encoding="utf-8").read()
    ver = guard_engine(src)

    guard_single_matra()
    slides = build_slides()
    guard_flow(slides)
    guard_sentences(slides)
    guard_word_build(slides)
    card = build_card(slides)
    if sum(card["phase_distribution"].values()) != len(slides):
        sys.exit("X  phase_distribution does not sum to the slide count")
    guard_prompts(slides)
    guard_register(slides, card)
    guard_mechanics(slides)
    guard_pictures(slides, card)
    guard_audio(slides, card)

    for d in ("assets/Audio", "assets/Images", "assets/UI"):
        os.makedirs(os.path.join(BUNDLE, d), exist_ok=True)
    check_chrome()

    stale, orphan, img_orphan = prune_stale(card)
    if stale or orphan:
        print("  OK  cleared %d stale clip(s) (text changed) + %d orphan(s) (screen gone) — "
              "gen_tts will re-record exactly these" % (len(stale), len(orphan)))
    if img_orphan:
        print("  !!  images no longer used by the card (delete before packaging): %s" % img_orphan)

    card["end_anim"] = celebration_anim(slides)          # [r85]
    if not card["end_anim"]:
        del card["end_anim"]
    payload = json.dumps(card, ensure_ascii=False, indent=1)
    if not CARD_TAG.search(src):
        sys.exit("X  cardData tag not found")
    html = CARD_TAG.sub(lambda m: m.group(1) + payload + m.group(3), src, count=1)

    first = []
    # [r126] the head's high-priority preloads are the COVER's train pictures - the first thing the child
    # sees, and on a slow line the thing that went missing. The page-2 pictures load with the rest.
    del first
    links = "".join('<link rel="preload" as="image" fetchpriority="high" href="assets/UI/%s">' % f
                    for f in ("train_still.webp", "train_spritesheet.webp"))
    html, n_pre = re.subn(r'(?:<link rel="preload" as="image"[^>]*>)+', links, html, count=1)
    declared = set(card["assets"]["image"])
    bad = sorted(set(re.findall(r'<link rel="preload"[^>]*href="assets/Images/([^".]+)\.\w+"',
                                html)) - declared)
    if bad:
        sys.exit("X  preload points at missing art: %s" % bad)
    print("  OK  preload: the cover's train pictures (%d block rewritten)" % n_pre)

    if 'id="bundleLetterGlow"' not in html:
        html, n = re.subn(r"</head>", LETTER_GLOW_CSS + "</head>", html, count=1)
        if n != 1:
            sys.exit("X  could not inject the letter glow")
        print("  OK  letter-strip glow injected")
    html = inject_celebration(html, card)                # [r85]


    # [r17] AUDIO CACHE VERSION. Hash every clip's bytes, so the stamp moves when a recording
    # changes and stays put when it does not. Without this a re-recorded clip keeps its filename,
    # the browser serves the copy it already has, and the reviewer hears the take we just replaced
    # - which is exactly what happened with vo_t3_prompt and vo_t5_prompt.
    _h = hashlib.sha1()
    for _f in sorted(os.listdir(AUD_DIR)):
        if _f.endswith(".ogg"):
            _h.update(_f.encode("utf-8"))
            _h.update(open(os.path.join(AUD_DIR, _f), "rb").read())
    html = html.replace("__AUDIO_V_STAMP__", _h.hexdigest()[:12])
    # [S05] ...and the lesson's pictures (replaced under the same names): stamped from their content
    _ih = hashlib.sha1()
    for _f in sorted(os.listdir(IMG_DIR)):
        _ih.update(_f.encode("utf-8")); _ih.update(open(os.path.join(IMG_DIR, _f), "rb").read())
    html = html.replace("__IMG_V_STAMP__", _ih.hexdigest()[:12])
    print("  OK  picture stamp %s" % _ih.hexdigest()[:12])
    # [r80] the same for the runner game's own sounds: its voice clips, its music and the two
    # feedback sounds it plays. Hashed by content, so the stamp moves only when one changes.
    _mr = os.path.join(BUNDLE, "assets", "MatraRunner")
    _mh = hashlib.sha1()
    _mfiles = [os.path.join(_mr, "voice", f) for f in sorted(os.listdir(os.path.join(_mr, "voice")))
               if f.endswith(".ogg")]
    _mfiles += [os.path.join(_mr, "bgm_game.ogg"),
                os.path.join(AUD_DIR, "sfx_fb_correct.ogg"), os.path.join(AUD_DIR, "sfx_fb_incorrect.ogg")]
    for _f in _mfiles:
        if os.path.exists(_f):
            _mh.update(os.path.basename(_f).encode("utf-8")); _mh.update(open(_f, "rb").read())
    _n_mr = html.count("__MR_AUDIO_V_STAMP__")
    html = html.replace("__MR_AUDIO_V_STAMP__", _mh.hexdigest()[:12])
    print("  OK  runner audio stamp %s (%d)" % (_mh.hexdigest()[:12], _n_mr))
    # [r124] ...and for its pictures and video (every file directly in assets/MatraRunner/), which
    # were requested with no version at all and so stayed in a device's cache across redeploys
    _ah = hashlib.sha1()
    for _f in sorted(os.listdir(_mr)):
        _p = os.path.join(_mr, _f)
        if os.path.isfile(_p):
            _ah.update(_f.encode("utf-8")); _ah.update(open(_p, "rb").read())
    _n_art = html.count("__MR_ART_V_STAMP__")
    if not _n_art:
        sys.exit("X  the runner's art stamp placeholder is missing - re-run embed_matra_runner.py")
    html = html.replace("__MR_ART_V_STAMP__", _ah.hexdigest()[:12])
    # [r126] ...and the list of the game's pictures, for the lesson to fetch ahead (warmRunner): read
    # from the game's own art table, so it is exactly what the game will ask for
    _rs = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "matra_runner_src", "index.html"),
               encoding="utf-8").read()
    _art = sorted(set(re.findall(r'\[\s*"([\w.-]+\.webp)"\s*,\s*\d+\s*\]', _rs) +
                      re.findall(r'"--mr-ui-[\w-]+"\s*:\s*"([\w.-]+\.webp)"', _rs) + ["panel3.webp"]))
    _art = [f for f in _art if os.path.isfile(os.path.join(_mr, f))] + ["coin.svg"]
    if html.count("__MR_ART_LIST__") != 1 or len(_art) < 20:
        sys.exit("X  runner warm-up list: placeholder %d, %d files" % (html.count("__MR_ART_LIST__"), len(_art)))
    html = html.replace("__MR_ART_LIST__", ",".join(_art))
    print("  OK  runner warm-up list: %d pictures" % len(_art))
    print("  OK  runner art stamp %s (%d)" % (_ah.hexdigest()[:12], _n_art))
    open(os.path.join(BUNDLE, CODE + ".html"), "w", encoding="utf-8").write(html)
    open(os.path.join(BUNDLE, "card.json"), "w", encoding="utf-8").write(payload + "\n")

    risky = write_vo_list()
    art = write_art_manifest(slides)

    print("  OK  card:   %d slides  %s" % (len(slides), card["phase_distribution"]))
    print("  OK  audio:  %d to record + %d copied  (%d flagged EAR-CHECK)"
          % (len(AUDIO_TEXT), len(COPY_AUDIO), len(risky)))
    print("  OK  images: %d on disk" % len(card["assets"]["image"]))
    if art["pending"]:
        print("  !!  ART PENDING (%d) — rendering as the emoji fallback until generated: %s"
              % (len(art["pending"]), ", ".join(sorted(art["pending"]))))
    gap = [v for v in AUDIO_TEXT if not os.path.isfile(os.path.join(AUD_DIR, v + ".ogg"))]
    if gap:
        print("  !!  VO PENDING (%d of %d) — these fall back to a silent beat until recorded"
              % (len(gap), len(AUDIO_TEXT)))
    print("  OK  html:   %s.html  (engine %s)" % (CODE, ver))


if __name__ == "__main__":
    main()
