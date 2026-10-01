# Combined Candidate Report

A [Claude Code](https://code.claude.com) skill that turns two PDFs into one four-page hiring report
a CEO or CHRO can act on without reading anything else:

1. a **Recruit41 interview evaluation PDF** (one interview, whatever sections it evaluated), and
2. a **Thomas psychometric (PPA / DISC) PDF**.

The report has an executive snapshot with an honest composite score, two evidence lenses labelled
from whatever the interview actually assessed, and a closing page that turns every gap into a
question only the hiring leader can answer.
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
uv run --script ~/.claude/plugins/marketplaces/recruit41/scripts/make_pdf.py --install
```

Skip this if Chrome or Chromium is already installed: the renderer uses Playwright's own build
when present and otherwise falls back to any installed Chromium/Chrome (set `CHROMIUM_PATH` to
choose one). If Claude reports "No Chromium found" at render time, run the command above.

In hosted sessions (Claude.ai, cloud Claude Code) the report is written to the session's outputs
folder and attached to the reply as a download, since the session's own filesystem isn't
reachable from your machine.

## Use

Put the two PDFs in a folder, open Claude Code in that folder, and ask:

> Make a combined candidate report from these two PDFs.

Claude reads both documents, fills the report template, renders it, and saves
`<Candidate_Name>_Combined_Candidate_Report.pdf` next to your inputs. It will tell you if a
psychometric report is registered to a different name than the candidate (the report is then
stamped "Sample" and those lines are marked illustrative).

You can also invoke the skill directly with `/combined-candidate-report`.

### Other AI tools (ChatGPT / Codex, Cursor, Copilot, Gemini CLI, and others)

`SKILL.md` follows the open [Agent Skills](https://agentskills.io) format, so this folder works as-is
in any tool that supports it. There is no marketplace step; clone the repository into the tool's
skills directory:

```bash
git clone https://github.com/recruit41/combined-candidate-report.git ~/.agents/skills/combined-candidate-report
```

`~/.agents/skills` is what the ChatGPT desktop app and Codex read. For other tools, clone into their
documented user-level skills directory instead. Then run the one-time Chromium install from that
clone's `scripts/make_pdf.py --install`, put the two PDFs in a folder, and ask for a combined
candidate report as above.

## What is in the box

```
.claude-plugin/                 Claude Code marketplace + plugin manifests
SKILL.md                        extraction rules, writing rules, QA checklist
assets/template.html            report layout, print stylesheet, radar chart
scripts/make_pdf.py             HTML to A4 PDF; refuses to run with unfilled placeholders
examples/example-report.*       a fully worked example for a fictional candidate
```

The repository root is the plugin, and the plugin is a single skill, so the same folder is also a
drop-in skill for any other tool that reads the Agent Skills format.

The writing rules in `SKILL.md` are the substance: balanced framing on every below-bar rating,
a composite score that states its own formula, "weakest score" claims checked against every
number, and page-4 conditions that end on an open question rather than a speculative consequence.

## Working on this repo

Test the renderer against the example (Chromium must be installed, see above):

```bash
uv run --script scripts/make_pdf.py examples/example-report.html /tmp/example-report.pdf
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
