---
name: combined-candidate-report
description: Combine a Recruit41 interview evaluation PDF and a Thomas psychometric PDF into one four-page, executive-ready PDF for a hiring decision. Use when the user points to those two documents and asks for a combined candidate report, 360 report, or hiring decision report.
---

# Combined Candidate Report

Produces a four-page A4 PDF for leadership hiring: an executive summary the CEO/CHRO can act on
alone, two evidence pages whose framing follows whatever the interview actually assessed, and a
closing page that turns every gap into the specific question only the hiring leader, not the AI,
can answer from their own organisational context.

Files in this skill (paths are relative to this SKILL.md; when installed as a Claude Code plugin
that folder is `${CLAUDE_PLUGIN_ROOT}`):

| Path | Purpose |
|---|---|
| `assets/template.html` | Report structure, CSS, radar chart, print stylesheet. Placeholder-driven. |
| `scripts/make_pdf.py` | Headless-Chromium renderer. Refuses to run while placeholders remain. |
| `examples/example-report.html` | Fully worked, fictional example. Read it for tone and evidence density. |

## Inputs (exactly two files, one optional third)

1. **Recruit41 interview evaluation PDF.** One interview for a single candidate, containing one or
   more evaluated sections. Each section carries a rating out of 5, an "Above bar" / "Meets bar" /
   "Below bar" verdict per sub-criterion, and an AI narrative with direct quotes from the
   transcript.

   **Do not expect any particular section to be present, and do not match on section titles.**
   Section titles and evaluation criteria are generated per role, so the same kind of section is
   titled differently from one job to the next, and an interview may legitimately contain no
   behavioural section, or no technical one.
2. **Thomas psychometric PDF** (PPA / DISC profile). Self Image graph, Work Mask graph, Behaviour
   Under Pressure graph, descriptive words, motivators, general comments.
3. *(Optional)* **Resume.** Used only for the 4-5 field identity strip on page 1.

If file 1 or 2 is missing, ask for it rather than guessing. Do not ask for a "behavioural round"
or a "technical round" as separate files: both live inside file 1 when they exist at all. If the psychometric report's name
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
3. **Group the evaluated sections by what they assess, not by what they are called.** Read each
   section's goal and its criteria, ignore introduction and closing, and place it in one of:
   - **How the candidate works and decides** — past incidents, stakeholder handling, conflict,
     ownership of decisions, judgement under ambiguity.
   - **What the candidate knows and can do** — technical or functional depth, knowledge questions,
     hands-on work, design, case analysis, and verification of past technical delivery.

   A section about past work can fall in either group depending on whether its criteria examine
   behaviour or technical depth, so decide from the criteria. Record which sections went where;
   the lens labels and the composite-score caption both depend on it.
4. **Extract the evidence group by group.** Per section: the section rating, each sub-criterion
   rating and verdict, and the 2-4 evidence points under each. Keep the groups separate; do not
   reuse one group's content in the other even though both are in the same document.
5. **Extract the psychometric read.** Profile description, descriptive words, and any sentence
   about communication style, decision-making style, or stakeholder orientation. These are what
   tend to triangulate against the interview evidence. Thomas reports have no 0-5 score; do not
   invent one.
6. **Compute the composite score honestly.** Average the section ratings you actually extracted,
   and say what you averaged in `{{COMPOSITE_SCORE_FORMULA}}` (e.g. "Avg. of behavioural &
   technical scores", or "Avg. of the three evaluated sections"). Never describe the score as
   covering a group that produced no number, and never label it "N lenses" when fewer than N
   produced numbers.
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
    absolute path to `make_pdf.py` next to this SKILL.md). The script exits with code 2 and lists
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
- The two evidence pages are labelled by `{{LENS1_TITLE}}` / `{{LENS1_BADGE}}` and
  `{{LENS2_TITLE}}` / `{{LENS2_BADGE}}`. Name them after the groups you actually found, for
  example "Leadership & Decision-Making" with badge "Behavioural + Psychometric", and
  "Technical & Functional Fit" with a badge naming the sections that fed it. Do not use the word
  "technofunctional" unless the source report does.
- **If the interview produced only one group, do not invent the other.** Give page 2 to the group
  you have, and use page 3 for the psychometric read triangulated against that same evidence plus
  the resume-grounded context. Relabel both kickers and badges to say what each page really is,
  and keep the report at four pages.
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
- **Assuming a section exists because past reports had it.** The interview may carry no
  behavioural section, or no technical one. Report what is there; do not leave a lens half-empty
  or pad it from the other group.
- **Matching sections by title.** Titles are generated per role, so "Past Work Experience",
  "Stakeholder Alignment" and "Plant Leadership" can all be the same kind of section. Classify by
  the criteria underneath.
- **Executive summary that previews instead of summarising.** "Pages 2-4 cover X, Y, Z" is a
  table of contents. Page 1 must carry the decision on its own.

## Output

Save the PDF as `<Candidate_Name>_Combined_Candidate_Report.pdf` next to the two source PDFs.
Offer to delete the intermediate `.html` once the PDF is confirmed; keep it if the user may want
edits. Never write candidate data into the skill or plugin folder itself.
