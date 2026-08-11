"""Render src/template.html + src/cards.json -> index.html (the file GitHub Pages serves).

Fast path: no PDF parsing, no network, no dependencies outside the standard library.
Run extract.py instead if the source PDF itself changed.

    python build.py
"""
import base64, json, mimetypes, pathlib, sys, time

ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "index.html"

def main():
    t0 = time.perf_counter()
    cards = json.loads((SRC / "cards.json").read_text(encoding="utf-8"))
    tags = json.loads((SRC / "tags.json").read_text(encoding="utf-8"))
    topics = json.loads((SRC / "topics.json").read_text(encoding="utf-8"))

    # attach the two filter dimensions -- t = licence category, p = subject --
    # and inline every sign image as a data URI so the page stays a single portable file
    for c in cards:
        c["t"] = tags.get(str(c["n"]), ["general"])
        c["p"] = topics.get(str(c["n"]), [])
        if "img" in c:
            p = SRC / "signs" / c["img"]
            mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
            c["img"] = f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

    # the speed chart is a reading of the question bank, so every mark must be traceable:
    # the question has to exist and its own answer has to contain that number
    speeds = json.loads((SRC / "speeds.json").read_text(encoding="utf-8"))
    answers = {c["n"]: c["o"][c["a"]] for c in cards}
    for row in speeds["rows"]:
        for m in row["marks"]:
            ans = answers.get(m["q"])
            if ans is None:
                sys.exit(f"build failed: speeds.json cites Q{m['q']}, which does not exist")
            if str(m["kmh"]) not in ans:
                sys.exit(f"build failed: Q{m['q']} answers {ans!r}, not {m['kmh']} km/h")

    # same rule for the numbers sheet: a cited question must exist, and where a
    # figure is claimed the question or its answer has to actually contain it
    numbers = json.loads((SRC / "numbers.json").read_text(encoding="utf-8"))
    text = {c["n"]: c["q"] + " " + " ".join(c["o"]) for c in cards}
    facts = ([d for s in numbers["scenes"] for d in s["dims"]] + numbers["time"]["marks"]
             + [i for g in numbers["lists"] for i in g["items"]])
    for f in facts:
        for q in [f["q"]] + f.get("also", []):
            if q not in text:
                sys.exit(f"build failed: numbers.json cites Q{q}, which does not exist")
        # only the primary citation has to state the figure in digits -- the "also"
        # questions may put the same limit in words ("one meter" in Q421)
        if f.get("n") and f["n"] not in text[f["q"]]:
            sys.exit(f"build failed: Q{f['q']} never mentions {f['n']} ({f['v']})")

    data = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    html = (SRC / "template.html").read_text(encoding="utf-8")
    for token, value in (("__DATA__", data), ("__COUNT__", str(len(cards))),
                         ("__SPEEDS__", json.dumps(speeds, ensure_ascii=False, separators=(",", ":"))),
                         ("__NUMBERS__", json.dumps(numbers, ensure_ascii=False, separators=(",", ":")))):
        if token not in html:
            sys.exit(f"build failed: {token} missing from template.html")
        html = html.replace(token, value)

    OUT.write_text(html, encoding="utf-8", newline="\n")
    imgs = sum(1 for c in cards if "img" in c)
    print(f"index.html  {len(html)/1024:6.0f} KB  {len(cards)} cards  {imgs} images"
          f"  {(time.perf_counter()-t0)*1000:.0f} ms")

if __name__ == "__main__":
    main()
