"""Re-extract the question bank from the official PDF into src/cards.json + src/signs/.

Only needed if source/STALL_QB_ENGLISH_NEW.pdf is replaced with a newer edition;
day-to-day edits just need `python build.py`.

    pip install pymupdf
    python extract.py

The PDF is a 27-page table. Rather than guessing structure from text layout, this reads
the table's own ruling lines to get row bands and uses fixed x-ranges for the columns, so
each cell -- and each embedded sign image -- lands on the question it belongs to.
"""
import collections, json, pathlib, re, sys

try:
    import pymupdf
except ImportError:
    sys.exit("needs pymupdf:  pip install pymupdf")

ROOT = pathlib.Path(__file__).parent
PDF = ROOT / "source" / "STALL_QB_ENGLISH_NEW.pdf"
SRC = ROOT / "src"

# x-ranges of the table's columns, in PDF points
COLS = [("qno", 20, 77), ("q", 77, 183), ("o1", 183, 246.5),
        ("o2", 246.5, 342), ("o3", 342, 434), ("ans", 434, 472)]
# the PDF's own text runs these together
FIX = {"causinginjury": "causing injury", "nearestpolice": "nearest police"}


def hlines(page):
    """y of every horizontal rule wide enough to be a table row separator."""
    ys = {round((d["rect"].y0 + d["rect"].y1) / 2, 1)
          for d in page.get_drawings() if d["rect"].width > 200 and d["rect"].height < 3}
    return sorted(ys)


def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    for k, v in FIX.items():
        s = s.replace(k, v)
    return s


def rows_of(doc):
    for page in doc:
        ys = hlines(page)
        if len(ys) < 2:
            continue
        bands = list(zip(ys[:-1], ys[1:]))
        cells = [collections.defaultdict(list) for _ in bands]
        imgs = [[] for _ in bands]

        def band_of(y):
            for i, (a, b) in enumerate(bands):
                if a - 0.5 <= y < b + 0.5:
                    return i
            return None

        for x0, y0, x1, y1, text, *_ in page.get_text("words"):
            i = band_of((y0 + y1) / 2)
            if i is None:
                continue
            for name, a, b in COLS:
                if a <= x0 < b:
                    cells[i][name].append((round(y0, 1), round(x0, 1), text))
                    break
        for im in page.get_image_info(xrefs=True):
            i = band_of((im["bbox"][1] + im["bbox"][3]) / 2)
            if i is not None and im["xref"] > 0:
                imgs[i].append(im["xref"])

        for i, cell in enumerate(cells):
            if not cell and not imgs[i]:
                continue
            row = {name: " ".join(w[2] for w in sorted(cell.get(name, [])))
                   for name, _, _ in COLS}
            row["imgs"] = imgs[i]
            yield row


def main():
    if not PDF.exists():
        sys.exit(f"missing {PDF}")
    doc = pymupdf.open(PDF)

    merged = []
    for row in rows_of(doc):
        if row["qno"] == "Q_NUMBER":                      # repeated header
            continue
        if re.fullmatch(r"\d+", row["qno"].strip()):
            row["qno"] = int(row["qno"])
            merged.append(row)
        elif merged:                                      # a cell that wrapped onto a new band
            prev = merged[-1]
            for k in ("q", "o1", "o2", "o3", "ans"):
                if row[k]:
                    prev[k] = (prev[k] + " " + row[k]).strip()
            prev["imgs"] += row["imgs"]

    merged.sort(key=lambda r: r["qno"])

    # the extraction is only trustworthy if every one of these holds
    nums = [r["qno"] for r in merged]
    dupes = [n for n, c in collections.Counter(nums).items() if c > 1]
    assert not dupes, f"duplicate question numbers: {dupes}"
    assert all(r["ans"] in ("1", "2", "3") for r in merged), "answer outside 1-3"
    assert all(r["o1"] and r["o2"] and r["o3"] for r in merged), "a question is missing an option"
    assert all(len(r["imgs"]) <= 1 for r in merged), "a row claimed more than one image"

    (SRC / "signs").mkdir(parents=True, exist_ok=True)
    for old in (SRC / "signs").glob("*.jpeg"):
        old.unlink()

    cards = []
    for r in merged:
        card = {"n": r["qno"], "q": clean(r["q"]),
                "o": [clean(r["o1"]), clean(r["o2"]), clean(r["o3"])],
                "a": int(r["ans"]) - 1}
        if r["imgs"]:
            img = doc.extract_image(r["imgs"][0])
            name = f"{r['qno']}.{img['ext']}"
            (SRC / "signs" / name).write_bytes(img["image"])
            card["img"] = name
        cards.append(card)

    (SRC / "cards.json").write_text(
        json.dumps(cards, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

    missing = sorted(set(range(nums[0], nums[-1] + 1)) - set(nums))
    print(f"{len(cards)} cards, {sum(1 for c in cards if 'img' in c)} images -> src/")
    print(f"numbers {nums[0]}-{nums[-1]}; absent from the PDF: {missing}")

if __name__ == "__main__":
    main()
