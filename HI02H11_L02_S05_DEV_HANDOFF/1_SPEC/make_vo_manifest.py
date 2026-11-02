# -*- coding: utf-8 -*-
"""The lesson's VO recording list, in the structure of the user's "Sample Manifest.xlsx".

One sheet "Recording list": S.No · Audio ID · Hindi script (spoken exactly) · Plays on · Duration (s).
Every clip once, in the order the child first hears it (start screen, transitions, pages, game,
celebration); "Plays on" lists every page that uses it; duration is measured from the file.
The sample itself is the template, so its fonts, fills, borders, widths and filter carry over.

Run:  PYTHONUTF8=1 python 1_SPEC/make_vo_manifest.py "<Sample Manifest.xlsx>" "<out.xlsx>"
"""
import json, os, re, subprocess, sys, copy
import openpyxl

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(HERE, "3_BUILD")
RUNNER_SRC = os.path.join(HERE, "1_SPEC", "matra_runner_src", "index.html")
SAMPLE, OUT = sys.argv[1], sys.argv[2]

card = json.load(open(os.path.join(BUILD, "card.json"), encoding="utf-8"))
TEXT = card["assets"]["audio_text"]
PATH = card["assets"]["audio"]
slides = card["slides"]

# ---------------------------------------------------------------- the order each page speaks in
def ids_for(s):
    a, d, out = s.get("audio") or {}, s.get("data") or {}, []
    add = lambda *v: out.extend(x for x in v if x)
    t = s["type"]
    if t == "MATRA_PAIRS":
        add(a.get("prompt"))
        for p in d.get("pairs", []): add(p.get("audio"), p.get("name_audio"))
    elif t == "MATRA_BUILD":
        add(a.get("prompt"), a.get("base"), a.get("onset"), a.get("result"), a.get("sounds"))
    elif t == "MEET_PAIR":
        add(a.get("prompt"))
        for e in d.get("examples", []): add(e.get("audio_line"), d.get("mic_nudge_audio"))
    elif t == "TRAIN_TAP":
        add(a.get("prompt"))
        for c in d.get("coaches", []): add(c.get("audio"))
        add(a.get("hint1"), a.get("hint2"), a.get("hint3"), a.get("correct"))
    elif t == "TRAIN_SORT":
        add(a.get("prompt"))
        if d.get("demo"):
            for c in d.get("cards", []): add(c.get("audio"), c.get("correct_audio"))
            add(a.get("outro"))
        else:
            for c in d.get("cards", []): add(c.get("audio"))
            add(a.get("hint1"))
            for b in d.get("bins", []): add(b.get("audio"))
            add(a.get("hint2"))
            for c in d.get("cards", []): add(c.get("hint1_audio"), c.get("hint2_audio"), c.get("hint3_audio"), c.get("correct_audio"))
            add(a.get("hint3"))
    elif t == "WORD_BUILD":
        add(a.get("prompt"))
        for o in d.get("options", []): add(o.get("audio"))
        for sl in d.get("slots", []): add(sl.get("name_audio"))
        add(a.get("hint1"), a.get("hint2"))
        for sl in d.get("slots", []): add(sl.get("hint3_audio"), sl.get("correct_audio"))
        add(a.get("hint3"))
    elif t == "SENTENCE_COMPLETE":
        add(a.get("prompt"), a.get("sentence"))
        for o in d.get("options", []): add(o.get("audio"))
        add(a.get("hint1"))
        for o in d.get("options", []): add(o.get("sentence_audio"))
        add(a.get("hint2"), a.get("hint3"), d.get("sentence_on_correct"), a.get("correct"))
    else:
        add(*[v for v in a.values()])
    return out

# page numbers as the user counts them: slide index + 1; transitions sit before a page
PT = card.get("phase_transition_audio", {})
gate_at = (card.get("gate") or {}).get("at", {})
rows = []                     # [id, text, [places]]
pos = {}
def put(i, text, where):
    if not i: return
    if i in pos:
        if where not in rows[pos[i]][2]: rows[pos[i]][2].append(where)
        return
    pos[i] = len(rows); rows.append([i, text, [where]])

PT_TEXT = {"vo_pt_tutorial": "ध्यान से देखिए और मेरे साथ जानिए। चलिए, शुरू करें!",
           "vo_pt_guided": "बहुत बढ़िया! अब हम साथ मिलकर शुरू करते हैं। चलिए, साथ में करें!",
           "vo_pt_practice": "वाह! अब आपकी बारी।"}

put("vo_landing", TEXT["vo_landing"], "Start screen")
prev_phase, n_trans = None, 0
for k, s in enumerate(slides):
    page = "Page %d" % (k + 1)
    ph = s["phase"]
    trans = None
    if ph != prev_phase and ph in PT and ph != "practice": trans = PT[ph]
    if s["id"] == gate_at.get("round3"): trans = PT.get("practice")
    if trans:
        n_trans += 1
        put(trans, PT_TEXT.get(trans, TEXT.get(trans, "")), "Transition %d (before page %d)" % (n_trans, k + 1))
    prev_phase = ph
    for i in ids_for(s):
        put(i, TEXT.get(i, ""), page)
    if s["type"] == "MINI_GAME":
        # the runner's own voice (assets/MatraRunner/voice/<id>.ogg), in the order the game speaks it
        src = open(RUNNER_SRC, encoding="utf-8").read()
        lines = dict(re.findall(r'^\s*(\w+)\s*:\s*"([^"]*)"', src[src.index("const LINES = {"):src.index("};", src.index("const LINES = {"))], re.M))
        pool = re.findall(r'\["([^"]+)","(\w+)"\]', src[src.index("const POOL_U"):src.index("const NO_PAIRS")])
        order = ["goal_u", "tut_lane", "tut_jump", "tut_slide", "tut_go"] + [w[1] for w in pool] + ["right", "wrong", "hit", "retry", "win"]
        words = {w[1]: w[0] for w in pool}
        for i in order:
            f = os.path.join(BUILD, "assets", "MatraRunner", "voice", i + ".ogg")
            if os.path.isfile(f):
                put("runner/" + i, lines.get(i) or words.get(i, ""), page)

def dur(i):
    if i.startswith("runner/"):
        f = os.path.join(BUILD, "assets", "MatraRunner", "voice", i[7:] + ".ogg")
    else:
        f = os.path.join(BUILD, PATH.get(i, "assets/Audio/%s.ogg" % i))
    if not os.path.isfile(f): return None
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                       capture_output=True, text=True)
    try: return round(float(r.stdout.strip()), 2)
    except ValueError: return None

# ---------------------------------------------------------------- write, on the sample's own styles
wb = openpyxl.load_workbook(SAMPLE)
ws = wb["Recording list"]
tpl = [copy.copy(ws.cell(2, c)._style) for c in range(1, 6)]
h_body = ws.row_dimensions[4].height      # the sample's body-row height (17.5)
if ws.max_row > 1: ws.delete_rows(2, ws.max_row)
for n, (i, text, where) in enumerate(rows, start=1):
    r = n + 1
    vals = [n, i, text, ", ".join(where), dur(i)]
    for c, v in enumerate(vals, start=1):
        cell = ws.cell(r, c, v); cell._style = copy.copy(tpl[c - 1])
    ws.row_dimensions[r].height = h_body
ws.auto_filter.ref = "A1:E%d" % (len(rows) + 1)
ws.freeze_panes = "A2"
wb.save(OUT)
missing = [r[0] for r in rows if not r[1]]
print("rows:", len(rows), "| no text:", missing, "| no duration:", [r[0] for r in rows if dur(r[0]) is None])
