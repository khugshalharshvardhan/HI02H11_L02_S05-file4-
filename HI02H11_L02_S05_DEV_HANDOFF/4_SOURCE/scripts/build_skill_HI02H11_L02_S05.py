# -*- coding: utf-8 -*-
"""Build HI02H11_L02_S05 (अं / अः) — «मात्राओं की रेल».

CONTENT ONLY. The flow, ladder, VO templates, phases and guards are the SME's 2026-09-30 review of
S03, in matra_train_lib.py.

REVIEWED BY THE SME on 2026-10-08 (HI02H11_L02_S05_SME_Review.pptx, notes in the speaker notes).
What that review changed, all of it built here:

  shape   a NEW tutorial screen after the intro — the signs' names (अनुस्वार, विसर्ग); the third
          tap (old p.9) and the third sentence (old p.16, छः गुब्बारे) deleted; the गरमी sentence
          moved in front of the चिड़िया one. 16 screens: tutorial 6 · guided 8 · independent 1.
  names   the marks are SIGNS here: «अं वाले शब्द», «बंदर शब्द में अं की बिंदी है», «यह अं का
          चिह्न है», «गो के ऊपर अनुस्वार लगाने पर…» (terms=). Where the SME kept «अं की मात्रा»
          (the build prompts, the word and picture sorts) it is kept.
  drawn   no ring round the dot (mark_ring off — "Remove the red outline/glow rings"), and the
          ◌ं / ◌ः glyphs are drawn, not typeset, so the visarga loses the font's headline stub and
          the guide circle stays grey (train_modules.js signHTML).
  p.2     «आज हम अं और अः वाले शब्द पढ़ेंगे।», «यह है अं। इसका चिह्न देखिए।»; the old instruction
          line moved, reworded, to the names screen.
  p.3     heading «गोद में अनुस्वार लगाने पर गोंद बनता है।», no gloss, no captions, no
          «अं की मात्रा» clip.
  p.4     अंडा, बंदर — «… इसमें अ के ऊपर बिंदी लगी है।»; label «इस शब्द का चिह्न».
  p.5     छह → छः with no heading, no picture, no captions.
  p.6     ONE example, प्रातः, no picture, no label, no heading — «इसमें त के आगे अः की मात्रा».
  p.7/8   बंदर · छः · प्रातः → बंदर;  जंगल · पंखा · प्रातः → प्रातः
  p.10    बंदर · छः · अंडा · प्रातः
  p.12    बंदर · पंखा · झंडा from बं छः पं दुः झं — "Use glow and lock without a hand"
  p.13    झंडा · प्रातः · पंखा (three pictures)
  gate    "VO and Text Synching required here" — the «चलिए, शुरू करें!» gate now SAYS only that.
  CEL     the SME's «बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया!» with आपने: the lesson speaks आप
          throughout (guard_register), and तुमने would be its one तुम form. Flagged.

Run:  PYTHONUTF8=1 py -3.13 build_skill_HI02H11_L02_S05.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from matra_train_lib import Lesson   # noqa: E402

ANU, VIS = "ं", "ः"

OBJ = {
    "obj_anda":   ("अंडा",   "\U0001F95A", ANU),
    "obj_bandar": ("बंदर",   "\U0001F412", ANU),
    "obj_pankha": ("पंखा",   "\U0001FAAD", ANU),
    "obj_jhanda": ("झंडा",   "\U0001F6A9", ANU),
    "obj_gond":   ("गोंद",   "\U0001F9F4", ANU),
    "obj_chhah":  ("छः",     "6️⃣", VIS),
    "obj_pratah": ("प्रातः", "\U0001F305", VIS),
    "obj_god":    ("गोद",    "\U0001F931", None),
}
SCENE = {
    "scn_garmi":   "\U0001FAAD",
    "scn_chidiya": "\U0001F426",
}

L = Lesson(
    code="HI02H11_L02_S05", m1=ANU, m2=VIS, names={ANU: "अं", VIS: "अः"},
    obj=OBJ, scene=SCENE, sibling="HI02H11_L02_S04",
    title_en="Matra train — anusvara and visarga",
    skill_hi="अं, अः मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।",
    recap="बहुत बढ़िया, दोस्त! आपने कमाल कर दिया!",
    after_marks={VIS}, cite_shabd=False,
    tap_words={"जंगल": ANU},
    pair_line_override={
        "अंडा": "अंडा — बोलकर देखिए। इसमें अ के ऊपर बिंदी लगी है।",
        "बंदर": "बंदर — बोलकर देखिए। इसमें ब के ऊपर बिंदी लगी है।",
        "प्रातः": "प्रातः — बोलकर देखिए। इसमें त के आगे अः की मात्रा लगी है।",
    },
    terms={"tap_group": "sign",
           "tap_has": {ANU: "अं की बिंदी है", VIS: "अः की दो बिंदियाँ हैं"},
           "mark_noun": "चिह्न",
           "mark_of": {ANU: "अं का चिह्न", VIS: "अः का चिह्न"}},
    gate_vo={"tutorial": "चलिए, शुरू करें!"},
)

slides = [
    L.intro("T1", prompt="आज हम अं और अः वाले शब्द पढ़ेंगे।",
            pair_lines={ANU: "यह है अं। इसका चिह्न देखिए।", VIS: "यह है अः। इसका चिह्न देखिए।"}),
    L.names_slide("T2", "आइए, इन अक्षरों और इनके चिह्नों के नाम जानें।", [
        (ANU, "अं में एक बिंदी है।", "अनुस्वार", "इस बिंदी को अनुस्वार कहते हैं।"),
        (VIS, "अः में दो बिंदियाँ हैं।", "विसर्ग", "इसे विसर्ग कहते हैं।")]),
    L.build("T3", "गोद", "गो", ANU, "गों", "गोंद", "द",
            heading="गोद में अनुस्वार लगाने पर गोंद बनता है।",
            onset="गो के ऊपर अनुस्वार लगाने पर, गों बनता है।",
            matra_name=False, captions=False),
    L.pair("T4", ["अंडा", "बंदर"], ANU, prompt="आइए, अं वाले कुछ शब्द देखें।",
           heading="अं वाले शब्द पढ़िए।", mark_label="इस शब्द का चिह्न", matra_audio=False),
    L.build("T5", "छह", "छ", VIS, "छः", "छः", "", base_pic=False, heading="",
            prompt="आइए, देखें कि अः की मात्रा के शब्द को और कैसे लिख सकते हैं।",
            explain="छह को छः भी लिखते हैं। दोनों का मतलब एक ही है।",
            matra_name=False, captions=False, result_pic=False),
    L.pair("T6", ["प्रातः"], VIS, prompt="आइए, अः की मात्रा वाला एक शब्द देखें।",
           heading="", mark_label="", matra_audio=False, pictures=False),
    L.tap("G1", ["बंदर", "छः", "प्रातः"], "बंदर"),
    L.tap("G2", ["जंगल", "पंखा", "प्रातः"], "प्रातः"),
    L.sort_words("G3", ["बंदर", "छः", "अंडा", "प्रातः"]),
    L.sort_marks("G4"),
    L.word_build("G5", [("बंदर", "दर", "बं"), ("पंखा", "खा", "पं"), ("झंडा", "डा", "झं")],
                 ["बं", "छः", "पं", "दुः", "झं"]),
    L.sort_pictures("G6", ["झंडा", "प्रातः", "पंखा"]),
    L.sentence("G7", "गरमी में ", " चलता है।", "पंखा", "scn_garmi", ["पंखा", "झंडा", "प्रातः"],
               hint3="चित्र में पंखा चल रहा है। पंखा शब्द को खाली जगह में डालिए।"),
    L.sentence("G8", "चिड़िया ने एक ", " दिया।", "अंडा", "scn_chidiya", ["अंडा", "बंदर", "छः"],
               hint3="चित्र में चिड़िया ने एक अंडा दिया है। अंडा शब्द को खाली जगह में डालिए।"),
    L.celebration(),
]

if __name__ == "__main__":
    L.emit(slides)
