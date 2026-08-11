"""Bootstrap src/tags.json — which licence categories each question is relevant to.

src/tags.json is the source of truth and is meant to be hand-edited; this script only
writes it if it is missing (pass --force to regenerate and lose manual edits).

The PDF ships no category metadata, so these lists are a reading of all 431 questions.
The guiding rule is **when in doubt, general**: a question wrongly left in costs a
candidate a few seconds, a question wrongly filtered out costs them a mark. So only
questions that are unmistakably about one class of vehicle are narrowed. Everything
about signs, signals, documents, first aid, road discipline and vehicle control
(gears, brakes, mirrors, tyres — a motorcycle has those too) stays general.
"""
import json, pathlib, sys

SRC = pathlib.Path(__file__).parent / "src"

# Order here is the order the categories appear in the UI.
LABELS = {
    "general":    "General",
    "two-wheeler":"Two-wheeler",
    "car":        "Car / LMV",
    "auto":       "Auto-rickshaw",
    "transport":  "Transport / heavy",
    "tractor":    "Tractor",
}

# motorcycle-only: rider age, pillion, helmet, bike speed limits, bike handling
TWO_WHEELER = [73, 77, 95, 129, 162, 174, 178, 184, 188, 189, 195, 205, 217, 314, 323,
               342, 343, 357, 358]
# motor car / light motor vehicle: car speed limits, seat belts, car tax, car handling
CAR = [83, 170, 175, 176, 187, 193, 194, 197, 322, 370, 371, 391, 414, 416]
# three-wheeler autorickshaw
AUTO = [192, 196, 207, 343, 410]
# goods carriage, heavy vehicles, trucks, public service and transport vehicles
TRANSPORT = [13, 87, 101, 131, 135, 137, 177, 179, 181, 182, 190, 191, 200, 202, 203,
             204, 208, 210, 306, 320, 405, 421]
TRACTOR = [149, 427]

GROUPS = [("two-wheeler", TWO_WHEELER), ("car", CAR), ("auto", AUTO),
          ("transport", TRANSPORT), ("tractor", TRACTOR)]


def main():
    out = SRC / "tags.json"
    if out.exists() and "--force" not in sys.argv:
        sys.exit(f"{out} already exists; it is hand-maintained. Pass --force to regenerate.")

    cards = json.loads((SRC / "cards.json").read_text(encoding="utf-8"))
    known = {c["n"] for c in cards}
    for name, nums in GROUPS:                       # catch a typo'd question number early
        missing = sorted(set(nums) - known)
        assert not missing, f"{name} lists questions that do not exist: {missing}"

    tags = {}
    for c in cards:
        t = [name for name, nums in GROUPS if c["n"] in nums]
        tags[str(c["n"])] = t or ["general"]        # anything not narrowed applies to everyone

    out.write_text(json.dumps(tags, indent=0, sort_keys=False), encoding="utf-8", newline="\n")

    tally = {k: sum(1 for v in tags.values() if k in v) for k in LABELS}
    print(f"wrote {out} for {len(tags)} questions")
    for k, n in tally.items():
        print(f"  {LABELS[k]:20s} {n:3d}")

if __name__ == "__main__":
    main()
