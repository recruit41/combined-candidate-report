# Combined Candidate Report

A [Claude Code](https://code.claude.com) skill that turns two PDFs into one four-page hiring report
a CEO or CHRO can act on without reading anything else:

1. a **Recruit41 interview evaluation PDF** (behavioural + technofunctional sections from one interview), and
2. a **Thomas psychometric (PPA / DISC) PDF**.

The report has an executive snapshot with an honest composite score, a leadership lens, a technical
lens, and a closing page that turns every gap into a question only the hiring leader can answer.
Everything runs on your own machine. No candidate data leaves it.

## Install

In Claude Code:

```
/plugin marketplace add recruit41/combined-candidate-report
/plugin install combined-candidate-report@recruit41
```

Then, once per machine, install the headless browser used for PDF rendering. This needs
[`uv`](https://docs.astral.sh/uv/) and downloads Chromium (about 150 MB):

```bash
uv run --script ~/.claude/plugins/marketplaces/recruit41/plugins/combined-candidate-report/skills/combined-candidate-report/scripts/make_pdf.py --install
```

If Claude reports a Playwright "Executable doesn't exist" error at render time, re-run that command.

## Use

Put the two PDFs in a folder, open Claude Code in that folder, and ask:

> Make a combined candidate report from these two PDFs.

Claude reads both documents, fills the report template, renders it, and saves
`<Candidate_Name>_Combined_Candidate_Report.pdf` next to your inputs. It will tell you if a
psychometric report is registered to a different name than the candidate (the report is then
stamped "Sample" and those lines are marked illustrative).

You can also invoke the skill directly with `/combined-candidate-report`.

## What is in the box

```
plugins/combined-candidate-report/skills/combined-candidate-report/
├── SKILL.md                    extraction rules, writing rules, QA checklist
├── assets/template.html        report layout, print stylesheet, radar chart
├── scripts/make_pdf.py         HTML to A4 PDF; refuses to run with unfilled placeholders
└── examples/example-report.*   a fully worked example for a fictional candidate
```

The writing rules in `SKILL.md` are the substance: balanced framing on every below-bar rating,
a composite score that states its own formula, "weakest score" claims checked against every
number, and page-4 conditions that end on an open question rather than a speculative consequence.

## Working on this repo

Test the renderer against the example (Chromium must be installed, see above):

```bash
uv run --script plugins/combined-candidate-report/skills/combined-candidate-report/scripts/make_pdf.py \
  plugins/combined-candidate-report/skills/combined-candidate-report/examples/example-report.html \
  /tmp/example-report.pdf
```

Test the skill locally without publishing:

```
/plugin marketplace add /path/to/this/checkout
/plugin install combined-candidate-report@recruit41
```

Do not commit real candidate documents or generated reports to this repository. The example is
fictional on purpose.

## Licence

MIT. See `LICENSE`.
