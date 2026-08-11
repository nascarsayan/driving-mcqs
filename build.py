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

    # attach licence-category tags, and inline every sign image as a data URI
    # so the page stays a single portable file
    for c in cards:
        c["t"] = tags.get(str(c["n"]), ["general"])
        if "img" in c:
            p = SRC / "signs" / c["img"]
            mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
            c["img"] = f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

    data = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    html = (SRC / "template.html").read_text(encoding="utf-8")
    for token, value in (("__DATA__", data), ("__COUNT__", str(len(cards)))):
        if token not in html:
            sys.exit(f"build failed: {token} missing from template.html")
        html = html.replace(token, value)

    OUT.write_text(html, encoding="utf-8", newline="\n")
    imgs = sum(1 for c in cards if "img" in c)
    print(f"index.html  {len(html)/1024:6.0f} KB  {len(cards)} cards  {imgs} images"
          f"  {(time.perf_counter()-t0)*1000:.0f} ms")

if __name__ == "__main__":
    main()
