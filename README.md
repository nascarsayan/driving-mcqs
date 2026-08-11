# Driving MCQs — Learner's Licence Flashcards

Interactive flashcards for the Indian learner's licence (LLR) test, built from the official
Parivahan question bank. **431 questions, 95 road-sign images.**

### ▶ [Open the flashcards](https://nascarsayan.github.io/driving-mcqs/)

No install, no sign-up, no server. The whole app is a single self-contained HTML file with the
sign images embedded, so it also works offline — save the page and open it on a plane.

## Studying

| | |
|---|---|
| **Answer** | Click an option, or press <kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd> — you get instant feedback with the correct answer |
| **Decks** | All · Signs (95) · Rules (336) · Starred · Tricky |
| **Spaced repetition** | Leitner boxes: a right answer promotes a card (New → Learning → … → Mastered), a wrong one sends it back to the start |
| **Order** | Question order by default (Q1 → Q436); hit the shuffle button or <kbd>X</kbd> to randomise, weakest cards first |
| **Reveal mode** | The ◐ button hides the multiple choice — read the question, press <kbd>R</kbd> to flip, like a paper flashcard |
| **Tricky deck** | Auto-collects every card you miss more often than you get right |

Progress is saved in your browser's local storage, so you can close the tab and pick up where you
left off. The ⟳ button clears it.

Other keys: <kbd>Space</kbd> / <kbd>→</kbd> next · <kbd>←</kbd> back · <kbd>S</kbd> star.

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

## Disclaimer

An unofficial study aid. The question bank is the property of the Ministry of Road Transport &
Highways, Government of India. Always confirm current rules with your local RTO — road rules and the
official question set can change.
