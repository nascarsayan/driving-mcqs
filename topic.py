"""Bootstrap src/topics.json — what each question is *about*.

Companion to tag.py. That file answers "which licence does this apply to";
this one answers "which subject is this", so a candidate can drill road
markings, speed limits or Act sections on their own.

src/topics.json is the source of truth and is meant to be hand-edited; this
script only writes it if it is missing (pass --force to regenerate).

The PDF has no subject metadata, so ASSIGN below is a hand reading of all 431
questions. Rules applied while classifying:

  * Every question gets at least one topic; most get one or two. Piling on
    loosely-related topics makes a filter useless, so a topic is only added
    when someone revising that subject would want the question.
  * Signals are split three ways because they are three things to learn:
    `sign` is a sign posted by the road, `tsig` is the light at the junction,
    and `hand` is a signal a driver gives with an arm or an indicator -- which
    is what the seven "The signal represents.." pictures show. This bank has no
    traffic-police hand-signal questions; a policeman only ever appears as
    somebody who may or may not be directing an intersection (Q141, 212, 377).
  * A picture-of-a-sign question is `sign` first. A second topic is added only
    when the sign itself is the subject matter — the horn signs, the parking
    signs, the level-crossing signs, the hazard signs — not for every
    directional arrow.
  * `defn` (defensive driving) is the home for hazard awareness: weather,
    skids, gradients, following distance, fatigue, blind bends.
"""
import collections, json, pathlib, sys

SRC = pathlib.Path(__file__).parent / "src"

# id -> label, in the order they appear in the UI. Roughly: what you see on the
# road, then who and what you share it with, then the machine, then the paperwork.
LABELS = {
    "sign": "Road signs",
    "tsig": "Traffic lights",
    "hand": "Hand & turn signals",
    "mark": "Road markings",
    "lane": "Lanes & position",
    "junc": "Junctions & turns",
    "ovtk": "Overtaking",
    "park": "Parking",
    "spd":  "Speed limits",
    "ped":  "Pedestrians & animals",
    "rail": "Railway crossings",
    "horn": "Horn & noise",
    "lite": "Lights & visibility",
    "defn": "Defensive driving",
    "acc":  "Accidents & first aid",
    "veh":  "Vehicle & controls",
    "safe": "Safety gear",
    "load": "Loads & passengers",
    "poll": "Pollution & fuel",
    "doc":  "Documents & RC",
    "lic":  "Licence rules",
    "off":  "Offences & penalties",
    "law":  "MV Act sections",
}

# question number -> space-separated topic ids
ASSIGN = {
    1: "ped",        2: "sign",       3: "defn",       4: "sign",
    5: "acc",        6: "sign junc",  7: "lane",       8: "sign lane",
    9: "ovtk",      10: "sign junc", 11: "rail",      12: "sign ped",
   13: "doc",       14: "sign park", 15: "lic",       16: "sign junc",
   17: "ped",       18: "sign horn", 19: "acc",       20: "sign defn",
   21: "lane",      22: "sign",      23: "ovtk",      24: "sign",
   25: "lane",      26: "sign",      27: "park lite", 28: "sign spd",
   29: "lite",      30: "sign defn", 31: "mark ped",  32: "sign rail",
   33: "acc",       34: "sign ovtk", 35: "tsig",      36: "sign junc",
   37: "park",      38: "sign",      39: "defn sign", 40: "sign junc",
   41: "ovtk",      42: "sign horn", 43: "ovtk",      44: "sign junc",
   45: "off",       46: "sign park", 47: "horn",      48: "sign lane",
   49: "veh",       50: "sign",      51: "load",      52: "sign",
   53: "park",      54: "sign",      55: "veh",       56: "sign ped",
   57: "off",       58: "sign junc", 59: "ovtk",      60: "sign spd",
   61: "ped",       62: "sign load", 63: "doc",       64: "sign load",
   65: "junc hand", 66: "sign park", 67: "doc poll",  68: "sign junc",
   69: "lite",      70: "sign junc", 71: "hand",      72: "sign lane",
   73: "lic",       74: "sign defn", 75: "ped sign",  76: "sign defn",
   77: "hand",      78: "sign defn", 79: "hand junc", 80: "sign defn",
   81: "junc",      82: "sign defn", 83: "doc",       84: "sign defn",
   85: "ovtk",      86: "sign load", 87: "load",      88: "sign junc",
   89: "ovtk",      90: "sign junc", 91: "park",      92: "sign junc",
   93: "veh park",  94: "sign defn", 95: "off load",  96: "sign rail",
   97: "horn ovtk", 98: "sign junc", 99: "doc off",  100: "sign junc",
  101: "lic",      102: "sign junc",103: "ovtk defn",104: "sign junc",
  105: "ped",      106: "sign defn",107: "park",     108: "sign defn",
  109: "spd off",  110: "sign ped", 111: "ped",      112: "sign ped",
  113: "ped",      114: "sign ped", 115: "acc",      116: "sign ped",
  117: "acc",      118: "sign defn",119: "ovtk",     120: "sign",
  121: "ovtk",     122: "sign defn",123: "ovtk",     124: "sign defn",
  125: "park",     126: "sign",     127: "park",     128: "sign mark",
  129: "safe",     130: "sign defn",131: "off lic",  132: "sign rail",
  133: "off lic",  134: "sign junc",135: "off lic",  136: "sign",
  137: "load off", 138: "sign park",139: "off lic",  140: "sign park",
  141: "junc",     142: "sign park",143: "tsig junc",144: "sign park",
  145: "mark ovtk",146: "hand",     147: "defn",     148: "hand",
  149: "load",     150: "hand",     151: "junc",     152: "hand",
  153: "ovtk",     154: "hand",     155: "defn",     156: "hand",
  157: "doc off",  158: "hand",     159: "horn",     160: "lane",
  161: "off",      162: "lic",      163: "tsig",     164: "doc",
  165: "defn",     166: "doc load", 167: "ovtk mark",168: "mark lane",
  169: "tsig",     170: "spd",      171: "defn",     172: "mark",
  173: "veh",      174: "spd",      175: "spd",      176: "spd",
  177: "spd",      178: "spd",      179: "load",     180: "load",
  181: "load",     182: "spd",      183: "load",     184: "spd",
  185: "ovtk lane",186: "spd load", 187: "spd",      188: "spd",
  189: "spd",      190: "load",     191: "load off", 192: "spd",
  193: "spd",      194: "spd",      195: "spd",      196: "spd",
  197: "spd",      198: "spd",      199: "law spd",  200: "law load",
  201: "spd ped",  202: "load",     203: "spd",      204: "spd",
  205: "law safe", 206: "spd",      207: "spd",      208: "spd",
  209: "spd",      210: "spd",      211: "spd",      212: "junc tsig",
  213: "defn",     214: "veh defn", 215: "lic",      216: "junc",
  217: "safe",     218: "horn",     219: "ped ovtk", 220: "ovtk lite",
  221: "lane",     222: "tsig",     223: "ped mark", 224: "park",
  225: "lite defn",226: "lite defn",227: "lane junc",228: "ovtk lite",
  229: "lite",     230: "defn",     231: "veh",      232: "defn",
  233: "junc hand",234: "junc defn",235: "lite park",236: "lite",
  237: "veh",      238: "lite",     239: "ovtk ped", 240: "spd defn",
  241: "defn",     242: "mark ovtk",243: "mark spd", 244: "defn ovtk",
  245: "defn",     246: "junc defn",247: "junc defn",248: "lane",
  249: "defn",     250: "ovtk defn",251: "lane",     252: "lane",
  253: "mark",     254: "sign",     255: "mark ovtk",256: "mark ovtk",
  257: "junc hand",258: "junc mark",259: "park veh", 260: "defn",
  261: "junc lane",262: "lane junc",263: "junc hand",264: "lane",
  265: "lane",     266: "lane tsig",267: "veh",      268: "poll horn",
  269: "poll",     270: "horn poll off",            271: "veh",
  272: "veh defn", 273: "lite defn",274: "veh",      275: "spd defn",
  276: "law off",  277: "law off",  279: "acc",      280: "acc",
  281: "off defn", 282: "tsig",     283: "defn",     284: "defn",
  285: "defn",     286: "veh",      287: "veh",      288: "veh defn",
  289: "veh",      290: "defn",     291: "veh defn", 292: "veh",
  293: "veh",      294: "veh defn", 295: "veh",      296: "veh defn",
  297: "lite park",298: "veh safe", 299: "acc",      300: "acc",
  301: "veh defn", 302: "safe",     303: "park safe",304: "load",
  305: "load",     306: "load",     307: "junc veh", 308: "lane hand",
  309: "junc ped", 310: "veh",      311: "veh defn", 312: "defn",
  313: "veh",      314: "spd sign", 315: "veh",      316: "veh ovtk",
  317: "safe acc", 318: "defn",     319: "sign",     320: "load",
  321: "horn",     322: "safe",     323: "safe",     324: "ped",
  325: "veh",      326: "lane",     327: "park lite",328: "poll doc",
  329: "poll",     330: "lane hand",331: "load",     332: "lite",
  333: "lane hand",334: "ovtk lane",335: "park hand",336: "junc",
  337: "junc lane",338: "acc ped",  339: "ovtk",     340: "lane",
  341: "defn",     342: "defn lane",343: "hand",     344: "park",
  345: "doc off",  346: "acc law",  347: "off",      348: "park veh",
  349: "lic",      350: "lic",      351: "lic off",  352: "lite off",
  353: "poll off", 354: "veh defn", 355: "veh off",  356: "spd ped",
  357: "veh defn", 358: "lane defn",359: "defn",     360: "poll veh",
  361: "poll",     362: "poll doc off",             363: "poll",
  364: "veh defn", 365: "doc",      366: "spd off",  367: "veh",
  368: "acc",      369: "park safe",370: "park",     371: "veh defn",
  372: "horn off", 373: "tsig",     374: "tsig",     375: "tsig",
  376: "junc",     377: "junc defn",378: "acc",      379: "horn",
  380: "doc lite", 381: "sign",     382: "sign",     383: "sign",
  384: "ped",      385: "junc veh", 386: "veh hand", 387: "veh",
  388: "veh defn", 389: "lite defn park",           390: "ped defn",
  391: "doc",      392: "veh",      393: "veh",      394: "veh",
  395: "acc",      396: "park veh", 397: "hand junc",398: "lane sign",
  399: "defn",     401: "off law",  402: "law off",  403: "law rail",
  404: "spd",      405: "doc",      406: "ovtk defn",407: "park",
  408: "ped mark", 409: "off law",  410: "load",     411: "defn",
  412: "off",      413: "junc",     414: "safe",     415: "load off",
  416: "safe off", 417: "off",      418: "load",     419: "veh",
  420: "sign junc",421: "load",     422: "veh",      424: "lic off",
  426: "mark park",427: "load",     428: "lite defn",429: "mark lane",
  430: "mark ovtk",431: "mark",     432: "tsig",     434: "mark lane",
  435: "defn",     436: "veh",
}


def main():
    out = SRC / "topics.json"
    if out.exists() and "--force" not in sys.argv:
        sys.exit(f"{out} already exists; it is hand-maintained. Pass --force to regenerate.")

    cards = json.loads((SRC / "cards.json").read_text(encoding="utf-8"))
    known = {c["n"] for c in cards}

    # every question classified, nothing classified that does not exist, no typo'd topic id
    assert not (set(ASSIGN) - known), f"unknown question numbers: {sorted(set(ASSIGN) - known)}"
    assert not (known - set(ASSIGN)), f"unclassified questions: {sorted(known - set(ASSIGN))}"
    for n, ids in ASSIGN.items():
        bad = [t for t in ids.split() if t not in LABELS]
        assert not bad, f"Q{n} uses unknown topic ids {bad}"

    topics = {str(c["n"]): ASSIGN[c["n"]].split() for c in cards}
    out.write_text(json.dumps(topics, indent=0, sort_keys=False), encoding="utf-8", newline="\n")

    tally = collections.Counter(t for v in topics.values() for t in v)
    print(f"wrote {out} for {len(topics)} questions, "
          f"{sum(tally.values())/len(topics):.2f} topics each")
    for k, label in LABELS.items():
        print(f"  {label:24s} {tally[k]:3d}")

if __name__ == "__main__":
    main()
