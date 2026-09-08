---
name: combined-candidate-report
description: Combine a Recruit41 interview evaluation PDF (behavioural + technical sections from one interview) and a Thomas psychometric PDF into one four-page, executive-ready PDF for a hiring decision. Use when the user points to those two documents and asks for a combined candidate report, 360 report, or hiring decision report.
---

# Combined Candidate Report

Produces a four-page A4 PDF for leadership hiring: an executive summary the CEO/CHRO can act on
alone, two evidence "lenses" (Leadership & Decision-Making; Technical & Functional Fit), and a
closing page that turns every gap into the specific question only the hiring leader, not the AI,
can answer from their own organisational context.

Files in this skill (paths are relative to this SKILL.md; when installed as a plugin the skill
root is `${CLAUDE_PLUGIN_ROOT}/skills/combined-candidate-report/`):

| Path | Purpose |
|---|---|
| `assets/template.html` | Report structure, CSS, radar chart, print stylesheet. Placeholder-driven. |
| `scripts/make_pdf.py` | Headless-Chromium renderer. Refuses to run while placeholders remain. |
| `examples/example-report.html` | Fully worked, fictional example. Read it for tone and evidence density. |

## Inputs (exactly two files, one optional third)

1. **Recruit41 interview evaluation PDF.** One interview covering both a behavioural round and a
   technofunctional/technical round for a single candidate. Contains section-by-section ratings
   out of 5, an "Above bar" / "Meets bar" / "Below bar" verdict per sub-criterion, and an AI
   narrative with direct quotes from the transcript.
2. **Thomas psychometric PDF** (PPA / DISC profile). Self Image graph, Work Mask graph, Behaviour
   Under Pressure graph, descriptive words, motivators, general comments.
3. *(Optional)* **Resume.** Used only for the 4-5 field identity strip on page 1.

If file 1 or 2 is missing, ask for it rather than guessing. If the psychometric report's name
does not match the candidate's, that is expected in some client workflows (their psychometric
tool is not integrated). Proceed, but keep the "Sample" banner and flag those lines as
illustrative everywhere the report cites them.

## Process

1. **Read both PDFs in full.** Do not skim. Direct quotes in the output must be verbatim from a
   source, never paraphrased and then presented as a quote.
2. **Extract candidate identity.** Name, role applied for, and (from the resume if supplied,
   otherwise from whatever the interview report states) current role, one defining prior stint,
   education, years of experience. Never invent an employer name, date, or degree you cannot
   verify from a source. Drop an item rather than guess it.
3. **Extract behavioural evidence.** Per competency section: the section rating, each
   sub-criterion rating and verdict, and the 2-4 evidence points under each.
4. **Extract technical evidence** the same way, from the technofunctional section(s) only. Do not
   reuse the behavioural section's content here even though it is in the same document.
5. **Extract the psychometric read.** Profile description, descriptive words, and any sentence
   about communication style, decision-making style, or stakeholder orientation. These are what
   tend to triangulate against the interview evidence. Thomas reports have no 0-5 score; do not
   invent one.
6. **Compute the composite score honestly.** Average the behavioural overall rating and the
   technical-section(s) average. Put the actual formula in `{{COMPOSITE_SCORE_FORMULA}}`
   (e.g. "Avg. of behavioural & technical scores"). Never label it "N lenses" when only two
   produce numbers.
7. **Rank gaps correctly.** Before calling anything "the weakest score", list every numeric
   rating you extracted and compare them. Do not assume the technical section is weakest
   because it is discussed last.
8. **Write with balanced framing everywhere.** For every below-bar or critical rating, state
   what the candidate actually did well in that same scenario before the gap ("stayed composed,
   but had not sequenced a response", not just "had not sequenced a response"). This applies to
   prose, scenario cards, and the page-4 conditions equally.
9. **Build page 4 as decision conditions, not a risk list.** Each gap becomes (a) what the gap
   is, grounded in the real rating and evidence, and (b) one genuinely open question only the
   hiring leader can answer from context the report-writer does not have (team structure, plant
   setup, culture, mandate). End on the question. Do not add a speculative consequence sentence
   after it.
10. **Populate the template.** Copy `assets/template.html` to the working folder as
    `<Candidate_Name>_Combined_Candidate_Report.html`, replace every `{{TOKEN}}`, write every
    `FILL:` block fresh, and delete the `FILL:` comments. Remove the `.option-note` block unless
    the psychometric name mismatch applies. Fill the `axes` array in the script at the bottom.
11. **Render.** `uv run --script scripts/make_pdf.py <populated.html> <output.pdf>` (use the
    absolute path to `make_pdf.py` under the skill root). The script exits with code 2 and lists
    what is missing if any placeholder remains. Output is one A4 page per report section; the
    print CSS already handles pagination, do not add your own page-break logic.
12. **Sanity-check before handing off**, every time:
    - Every number in the PDF traces to a number in a source PDF.
    - Every quote is verbatim.
    - Every "weakest" / "lowest" claim is numerically correct against the full list of ratings.
    - No below-bar rating is stated without its balancing positive.
    - The composite-score caption matches how the score was actually computed.
    - The PDF is exactly four pages. If a section spilled, see "Template contract".

## Template contract (`assets/template.html`)

- `{{ALL_CAPS}}` tokens are short fields: replace in place.
- Comments starting `FILL:` mark longer blocks (narrative paragraphs, evidence bullets, scenario
  cards, condition cards). Write them fresh from the extracted evidence following the pattern the
  comment describes; they are not fill-in-the-blank strings. Delete the comment when done.
- `{{RECOMMENDATION_STATUS}}` and each `{{SCENARIO_N_CHIP}}` take one of `good`, `warning`,
  `critical`. Map Above bar to `good`, Meets bar to `warning`, Below bar to `critical`.
- Scenario cards and condition blocks may be added or removed to match the evidence. Three to
  five conditions is typical.
- Do not restructure the CSS or the radar-chart script. The `@media print` block is tuned so each
  `.page` article fits one A4 page at the current scale. If a candidate has unusually dense
  evidence and a section overflows, shrink the print `html { font-size }` slightly rather than
  letting a section spill onto a second sheet.
- Fonts load from Google Fonts; offline, the fallback stack (Georgia / system sans / monospace)
  renders fine and pagination still holds.

## Reference example

`examples/example-report.html` is a complete instance of this template for a **fictional**
candidate, company, and interviewer. Every name, employer, and quote in it is invented; the
scores and structure mirror a real report reviewed by a hiring team. Read it for tone, evidence
density, balanced framing, and page-4 style. Do not copy its prose.

## Known failure modes (each found and fixed once already; check for them every run)

- **Wrong "weakest score" claims.** Calling the gap currently being written about "the weakest"
  without comparing the other numbers.
- **Overstated composite methodology.** Labelling a score as a composite of three lenses when
  only two produced numbers.
- **One-sided negative framing.** A below-bar rating almost always has a real, specific positive
  in the source evidence (composure, correct partial knowledge, right instinct). Find it and
  state it first.
- **Evidence mis-tagged to the wrong score.** When one sentence blends facts from two different
  sub-ratings, tag each fact with the rating it came from or split into two bullets.
- **Résumé reprint.** The identity strip is 4-5 fields for orientation. The report's job is the
  synthesis, not the CV.
- **Executive summary that previews instead of summarising.** "Pages 2-4 cover X, Y, Z" is a
  table of contents. Page 1 must carry the decision on its own.

## Output

Save the PDF as `<Candidate_Name>_Combined_Candidate_Report.pdf` next to the two source PDFs.
Offer to delete the intermediate `.html` once the PDF is confirmed; keep it if the user may want
edits. Never write candidate data into the skill or plugin folder itself.
