#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright"]
# ///
"""Render a populated combined-candidate-report HTML file to a paginated A4 PDF.

Usage:
    uv run --script make_pdf.py <input.html> <output.pdf>

Browser: uses Playwright's own Chromium when it is installed, otherwise the
first Chromium/Chrome already on the machine (set CHROMIUM_PATH to pick one),
so sandboxes that block browser downloads still render. On a machine with no
Chromium at all, run `uv run --script make_pdf.py --install` once to download
the build Playwright needs.

Refuses to render while the HTML still contains unfilled {{TOKENS}} or
"FILL:" comments, so a half-populated template can't reach a PDF.
"""
import glob
import os
import pathlib
import re
import shutil
import subprocess
import sys

TOKEN = re.compile(r"\{\{[A-Z0-9_]+\}\}")
FILL_COMMENT = re.compile(r"<!--\s*FILL:")


def find_unfilled(html: str) -> list[str]:
    problems = sorted(set(TOKEN.findall(html)))
    if FILL_COMMENT.search(html):
        problems.append("<!-- FILL: ... --> comment(s) still present")
    return problems


def find_installed_chromium() -> str | None:
    """Return a Chromium/Chrome executable already on this machine, if any.

    Covers an explicit CHROMIUM_PATH, browsers on PATH, and Playwright builds
    from other versions (hosted sandboxes often preinstall one under
    PLAYWRIGHT_BROWSERS_PATH that doesn't match the version uv resolves).
    """
    explicit = os.environ.get("CHROMIUM_PATH")
    if explicit:
        return explicit

    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome"):
        found = shutil.which(name)
        if found:
            return found

    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH"), "~/.cache/ms-playwright",
             "~/Library/Caches/ms-playwright", "/ms-playwright", "/opt/pw-browsers"]
    patterns = ["chromium-*/chrome-linux*/chrome",
                "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
                "chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
                "chromium_headless_shell-*/chrome-*/headless_shell",
                "chromium_headless_shell-*/chrome-*/chrome-headless-shell"]
    for root in filter(None, roots):
        base = pathlib.Path(root).expanduser()
        for pattern in patterns:
            # Newest build first.
            for candidate in sorted(glob.glob(str(base / pattern)), reverse=True):
                if os.access(candidate, os.X_OK):
                    return candidate

    for candidate in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                      "/Applications/Chromium.app/Contents/MacOS/Chromium"):
        if os.access(candidate, os.X_OK):
            return candidate
    return None


def launch_chromium(p):
    explicit = os.environ.get("CHROMIUM_PATH")
    if not explicit and pathlib.Path(p.chromium.executable_path).exists():
        return p.chromium.launch()

    fallback = find_installed_chromium()
    if not fallback:
        print("No Chromium found. Run `uv run --script make_pdf.py --install` once, "
              "or set CHROMIUM_PATH to an installed Chromium/Chrome.")
        sys.exit(3)
    print(f"Using installed browser: {fallback}")
    return p.chromium.launch(executable_path=fallback)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--install":
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        return

    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    src = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2]).resolve()
    if not src.exists():
        print(f"Input HTML not found: {src}")
        sys.exit(1)

    unfilled = find_unfilled(src.read_text(encoding="utf-8"))
    if unfilled:
        print("Refusing to render: the template is not fully populated.")
        for item in unfilled:
            print(f"  - {item}")
        sys.exit(2)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = launch_chromium(p)
        page = browser.new_page()
        page.goto(src.as_uri())
        page.wait_for_timeout(400)  # let the radar-chart script finish drawing
        page.emulate_media(media="print")
        page.pdf(
            path=str(out),
            format="A4",
            print_background=True,
            margin={"top": "0.3in", "bottom": "0.3in", "left": "0.25in", "right": "0.25in"},
        )
        browser.close()

    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
