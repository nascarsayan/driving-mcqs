# Driving MCQs — Learner's Licence Flashcards

Interactive flashcards for the Indian learner's licence (LLR) test, built from the official
Parivahan question bank. **431 questions, 95 road-sign images.**

### ▶ [Open the flashcards](https://nascarsayan.github.io/driving-mcqs/)

No install, no sign-up, no server. The whole app is a single self-contained HTML file with the
sign images embedded, so it also works offline — save the page and open it on a plane.

Three views, switched from the header:

| | |
|---|---|
| **Study** | The flashcards — spaced repetition, decks, filters |
| **Signs** | Every picture in the bank as a cheat sheet: 73 road signs, the 7 driver hand signals and 15 road-marking photos, each with what it means. Filter it by text, or tap one to go and be quizzed on it |
| **Speeds** | Every speed limit in the bank on one 0–80 km/h ray per vehicle, so you can see at a glance that a motor cycle does 25 near a school, 30 in the city at night, 40 in the city and 50 flat out. Filter by vehicle type; tap a branch for the question it came from |
| **Numbers** | Everything else you have to memorise. Load and dimension limits as scale drawings of a lorry, a tow and a restriction gantry; the four time limits on a log ray; ages, fines, the blood-alcohol limit and the eight Motor Vehicles Act sections as plain lists |

## Studying

| | |
|---|---|
| **Answer** | Click an option, or press <kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd> — you get instant feedback with the correct answer |
| **Search** | The magnifier (<kbd>/</kbd>) fuzzy-matches the question, then the correct answer, then the wrong options, in that order of weight. Whole words aren't needed — `hlmt` finds the helmet question, `ylw ln` finds the yellow line, `q42` jumps to question 42 |
| **Decks** | All · Starred · Tricky |
| **Filters** | The funnel button (<kbd>F</kbd>) opens a sheet with two tabs: **Licence**, for the class of vehicle you're sitting for, and **Topics**, for the subject. Within a tab your picks are OR'd, and the two tabs are AND'ed — "Two-wheeler + Speed limits" is the seven bike speed-limit questions |
| **Spaced repetition** | Leitner boxes: a right answer promotes a card (New → Learning → … → Mastered), a wrong one sends it back to the start |
| **Order** | Question order by default (Q1 → Q436); hit the shuffle button or <kbd>X</kbd> to randomise, weakest cards first |
| **Jump anywhere** | Drag the progress bar at the top — it's a scrubber. A bubble shows which question you'd land on, and the card only changes when you let go |
| **Reveal mode** | The ◐ button hides the multiple choice — read the question, press <kbd>R</kbd> to flip, like a paper flashcard |
| **Tricky deck** | Auto-collects every card you miss more often than you get right |
| **Themes** | Light and dark, following your system by default — the ☀/☾ button overrides it |

Everything is saved in your browser's local storage: your Leitner boxes and stars, your all-time
correct/wrong totals, and **which card you were on**. Refresh or close the tab and you come back to
the same question in the same deck, with the same totals. The ⟳ button clears it.

Other keys: <kbd>Space</kbd> / <kbd>→</kbd> next · <kbd>←</kbd> back · <kbd>S</kbd> star · <kbd>F</kbd> filters · <kbd>/</kbd> search.

### Numbers

[`src/numbers.json`](src/numbers.json) holds the figures, and the build applies the same rule as
the speed chart: a cited question must exist, and where a figure is claimed the question or its
answer has to contain it in digits. That check has already earned its keep — it caught Q421 stating
the rear-projection limit as *"one meter"* in words rather than 100 cm.

What gets a picture and what gets a list is deliberate. The load and dimension limits are drawn,
to scale at 33 px to the metre, because they are physical facts and a lorry with arrows on it says
it faster than a sentence. The four time limits share a **log** ray, because 24 hours and 15 years
cannot sit on the same linear axis. Ages, fines, the blood-alcohol threshold and the Act sections
are lists: the first three are one-off facts with nothing to compare them against, and a section
number is an identifier rather than a quantity — 185 is not "more" than 122. A chart for either
would be decoration.

The eight sections the bank names: **112** speed · **113** permitted weight · **122** leaving a
vehicle dangerously · **129** helmets · **131** unguarded level crossings · **184** dangerous
driving · **185** drink and drugs, plus **CMVR 21(25)** for using a phone at the wheel.

**There is no weight chart, because the bank contains no weight figure at all.** Every weight answer
is qualitative: the load is whatever the permit allows (Q190), the limit is posted on an axle-weight
sign (Q86), section 113 forbids exceeding it (Q200). The only number attached to weight is the
₹2000 minimum overloading fine, which lives on the money list.

### Speed limits

The Speeds view is built from [`src/speeds.json`](src/speeds.json), and every mark on it is an
answer in the bank rather than a rule looked up elsewhere — the build fails if a cited question
doesn't exist or if its own answer doesn't contain that number. Where the bank contradicts itself it
says so rather than picking a side: a motor car on a ghat road is 40 km/h by Q194, yet Q187 names
the motor car as the vehicle not permitted above 30, and passing a procession is 15 km/h by Q201 but
25 by Q356. Learn both as printed.

## Where the questions come from

Everything is extracted from the official question bank published by the Ministry of Road Transport
& Highways: [STALL_QB_ENGLISH_NEW.pdf](https://parivahan.gov.in/sites/default/files/DownloadForm/STALL_QB_ENGLISH_NEW.pdf)
(archived in [`source/`](source/) for reference).

The PDF is a 27-page table. Text and images were parsed with PyMuPDF using the table's own ruling
lines as row boundaries, which makes each cell and each image land on the right question rather than
being inferred from text layout. Checks that passed: no duplicate question numbers, every card has
exactly three options and an answer in 1–3, and each of the 95 images maps to exactly one question.
All 95 sign images were then eyeballed against their answer text — including the pairs that would
expose an off-by-one error, such as right-hand curve vs left-hand curve and the two hairpin bends.

Two notes on fidelity to the source:

- Question numbers **278, 400, 423, 425 and 433 do not exist** in the PDF, which is why the count is
  431 rather than 436. Numbering follows the original so you can cross-check against the PDF.
- Two run-together words in the PDF's own text (`causinginjury`, `nearestpolice`) were split. Nothing
  else was reworded — questions, options and answers are verbatim.

## Licence categories

The PDF ships one undifferentiated list, but not all of it is relevant to every candidate — speed
limits for goods carriages don't help someone sitting a two-wheeler test. Each question is tagged:

| Category | Questions | |
|---|---|---|
| General | 370 | Signs, signals, documents, right of way, first aid, vehicle control — everyone |
| Two-wheeler | 19 | Rider age, pillion, helmets, motorcycle speed limits and handling |
| Car / LMV | 14 | Motor-car speed limits, seat belts, car tax and handling |
| Auto-rickshaw | 5 | Three-wheeler speed limits and passenger rules |
| Transport / heavy | 22 | Goods carriages, trucks, heavy and public service vehicles |
| Tractor | 2 | Tractor-specific rules |

Selecting categories shows questions carrying **any** of them, so "General + Two-wheeler" is the
two-wheeler syllabus, while "Two-wheeler" alone is the 19 bike-specific ones for focused drilling.
The quick picks in the dialog set the common combinations.

These tags are a **reading of the questions, not official metadata** — the PDF has no category
field. The rule applied was *when in doubt, general*: a question wrongly left in costs you a few
seconds, one wrongly filtered out costs you a mark. So anything about signs, road discipline or
vehicle control (gears, brakes, mirrors, tyres — a motorcycle has those too) stays general, and only
questions unmistakably about one class of vehicle are narrowed. The real exam can still draw from
the whole bank, so treat this as prioritisation, not a guarantee.

Tags live in [`src/tags.json`](src/tags.json), keyed by question number, and are meant to be
hand-edited — if you disagree with a call, change it there and rebuild. `tag.py` holds the original
classification lists and only regenerates that file with `--force`.

## Topics

The second filter tab is the subject. Every question carries one or two topics — 1.46 on average:

| | | | | | |
|---|--:|---|--:|---|--:|
| Road signs | 82 | Traffic lights | 12 | Hand & turn signals | 21 |
| Road markings | 19 | Lanes & position | 31 | Junctions & turns | 45 |
| Overtaking | 31 | Parking | 30 | Speed limits | 39 |
| Pedestrians & animals | 25 | Railway crossings | 5 | Horn & noise | 11 |
| Lights & visibility | 19 | Defensive driving | 71 | Accidents & first aid | 15 |
| Vehicle & controls | 50 | Safety gear | 12 | Loads & passengers | 28 |
| Pollution & fuel | 11 | Documents & RC | 15 | Licence rules | 13 |
| Offences & penalties | 34 | MV Act sections | 10 | | |

Three of these are easy to conflate, so they are deliberately separate: **Road signs** is a sign
posted beside the road, **Traffic lights** is the signal at the junction, and **Hand & turn signals**
is a signal a driver gives — with an arm or an indicator. The seven `The signal represents..`
pictures are the driver's arm signals. This question bank has **no traffic-police signal questions**;
a policeman appears only as somebody who may or may not be directing an intersection (Q141, Q212,
Q377).

Like the licence categories, topics are a hand reading of all 431 questions rather than official
metadata. A topic is only attached when someone revising that subject would actually want the
question — piling on loosely related tags makes a filter useless. Sign pictures are tagged
`Road signs` and get a second topic only when the sign itself is the subject (the horn signs, the
parking signs, the level-crossing signs, the hazard signs), not for every directional arrow.
They live in [`src/topics.json`](src/topics.json) and are hand-editable the same way; `topic.py`
holds the per-question reading, asserts that every question is classified, and only regenerates with
`--force`.

## Development

`index.html` at the repo root is a **generated file** — don't hand-edit it, since the question data
is inlined into it. Edit `src/` and rebuild:

```
src/template.html   the actual app: markup, styles, logic, with __DATA__/__COUNT__ placeholders
src/cards.json      431 questions - text, options, answer index, sign filename
src/tags.json       question number -> licence categories (hand-maintained)
src/topics.json     question number -> subjects (hand-maintained)
src/speeds.json     the speed chart: vehicle, circumstance, km/h, source question
src/numbers.json    the numbers sheet: dimensions, time limits, one-off figures
src/signs/*.jpeg    95 sign images, one per question that has one
```

```sh
python build.py     # src/ -> index.html, ~0.5s, standard library only
```

The build inlines each sign as a base64 data URI, which is what keeps the site a single portable
file with no asset requests — so it loads in one round trip and works offline.

Re-extracting from the PDF is a separate, slower step, needed only if the official question bank is
republished:

```sh
pip install pymupdf
python extract.py   # source/*.pdf -> src/cards.json + src/signs/, ~2s
```

`extract.py` asserts its own output: no duplicate question numbers, every answer in 1–3, every
question with three options, and at most one image per row. If the PDF's layout changes in a way
that breaks parsing, it fails loudly rather than emitting quietly-wrong flashcards.

## Disclaimer

An unofficial study aid. The question bank is the property of the Ministry of Road Transport &
Highways, Government of India. Always confirm current rules with your local RTO — road rules and the
official question set can change.
