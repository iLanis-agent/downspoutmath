import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

def runoff_plan(roofSqM, stormMmHr, perSpoutLMin):
    if not (roofSqM > 0) or not (stormMmHr > 0) or not (perSpoutLMin > 0):
        return {"error": "the roof, the storm and the labeled capacity must be positive"}
    flow = round1(roofSqM * stormMmHr / 60)
    spouts = math.ceil(flow / perSpoutLMin)
    headroom = round1(spouts * perSpoutLMin - flow)
    if spouts == 1: verdict = "a single quiet drop"
    elif spouts <= 3: verdict = "a working gutter line"
    else: verdict = "a serious storm system"
    return {"flow": flow, "spouts": spouts, "headroom": headroom, "verdict": verdict}

def drop_plan(wallCm, bracketCm):
    if not (wallCm > 0) or not (bracketCm > 0):
        return {"error": "the wall and the labeled bracket spacing must be positive"}
    if wallCm < bracketCm:
        return {"error": "the wall is shorter than one labeled bracket spacing"}
    brackets = math.floor(wallCm / bracketCm) + 1
    spare = round1(wallCm - (brackets - 1) * bracketCm)
    if wallCm < 300: verdict = "a bungalow drop"
    elif wallCm <= 600: verdict = "a two-storey drop"
    else: verdict = "a tall-wall drop"
    return {"brackets": brackets, "spare": spare, "verdict": verdict}

def spread_plan(distanceCm, sectionCm):
    if not (distanceCm > 0) or not (sectionCm > 0):
        return {"error": "the target distance and the labeled section must be positive"}
    sections = math.ceil(distanceCm / sectionCm)
    reach = round1(sections * sectionCm)
    overshoot = round1(reach - distanceCm)
    if distanceCm <= 120: verdict = "a doorstep splash"
    elif distanceCm <= 300: verdict = "a garden-edge discharge"
    else: verdict = "a far-fence discharge"
    return {"sections": sections, "reach": reach, "overshoot": overshoot, "verdict": verdict}

def render_runoff(r, roofSqM, stormMmHr, perSpoutLMin):
    return ("A roof " + fmt(roofSqM) + " sq m in a labeled " + fmt(stormMmHr) + " mm/hr storm sheds "
            + plural(r["flow"], "liter") + " a minute - " + plural(r["spouts"], "downspout")
            + " at a labeled " + fmt(perSpoutLMin) + " L/min" + ("" if r["spouts"] == 1 else " each") + ", with " + fmt(r["headroom"]) + " L/min of headroom - " + r["verdict"] + ".")

def render_drop(r, wallCm, bracketCm):
    return ("A drop " + fmt(wallCm) + " cm is one straight pipe; at a labeled " + fmt(bracketCm) + " cm bracket spacing it takes "
            + plural(r["brackets"], "bracket") + ", both ends included, with " + fmt(r["spare"]) + " cm of extra spacing - " + r["verdict"] + ".")

def render_spread(r, distanceCm, sectionCm):
    return ("A target " + fmt(distanceCm) + " cm from the foundation at a labeled " + fmt(sectionCm) + " cm section takes "
            + plural(r["sections"], "extension section") + ", reaching " + fmt(r["reach"]) + " cm with " + fmt(r["overshoot"]) + " cm to spare - " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[120,50,90],[60,50,90],[300,80,90],[45,25,90],[0,50,90],[120,0,90],[120,50,0],[33.3,50,90],[540,60,90],[90,90,90]]:
    add("runoffPlan", runoff_plan, render_runoff, a)
for a in [[540,150],[280,150],[700,150],[150,150],[0,150],[540,0],[120,150],[333.5,150],[610,150],[450,180]]:
    add("dropPlan", drop_plan, render_drop, a)
for a in [[300,120],[120,120],[450,120],[240,120],[0,120],[300,0],[100,120],[301,120],[55.5,120],[600,150]]:
    add("spreadPlan", spread_plan, render_spread, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
