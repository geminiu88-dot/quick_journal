"""Opens the journal pages in a hidden Chrome, on a pretend date, with an empty browser memory.

Every test starts from nothing: a new browser profile (no saved journal) and
a fake clock, so rules that depend on the day (new day, Friday, new week) can
be checked on any day. The page file is opened as it is (file://), exactly
like double-clicking index.html: no server, no internet.

    j = Journal("2026-11-27")         # Friday 27 Nov 2026, 09:00
    j.js("journalText()")             # run JavaScript in the page, get the result
    j.open("2026-11-30")              # same browser memory, three days later
"""
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT                # run.py --preview: the pages in preview/ instead
_pw = None
_browser = None


def browser():
    """One Chrome for the whole run (starting it is the slow part)."""
    global _pw, _browser
    if _browser is None:
        _pw = sync_playwright().start()
        try:
            _browser = _pw.chromium.launch()
        except Exception:
            # Claude's cloud sessions have Chrome in another place
            _browser = _pw.chromium.launch(executable_path=os.environ.get("CHROME", "/opt/pw-browsers/chromium"))
    return _browser


def close():
    global _pw, _browser
    if _browser:
        _browser.close()
        _pw.stop()
    _pw = _browser = None


class Journal:
    """index.html (or another page of the repo) on a pretend date."""

    def __init__(self, day, page="index.html", state=None, time="09:00"):
        self.ctx = browser().new_context(accept_downloads=True)
        self.page_name = page
        self.pg = None
        self.errors = []      # script errors on the page: a test fails if there are any
        self.dialogs = []     # confirm()/alert() texts; they are answered "OK"
        self.open(day, time)
        if state is not None:
            # a saved journal, as if the page had been used before: store it, then open the page again
            self.js("s => localStorage.setItem('journal-bc-v1', s)", json.dumps(state))
            self.open(day, time)

    def open(self, day, time="09:00"):
        """Open the page (again) on this day, keeping what the browser saved so far."""
        if self.pg:
            self.pg.close()
        self.pg = self.ctx.new_page()
        self.pg.on("pageerror", lambda e: self.errors.append(str(e)))
        self.pg.on("dialog", lambda d: (self.dialogs.append(d.message), d.accept()))
        self.pg.clock.install(time=f"{day}T{time}:00")
        self.pg.goto((PAGES / self.page_name).as_uri())
        return self

    def js(self, code, arg=None):
        """Run JavaScript in the page and return its value (code = an expression or a function)."""
        return self.pg.evaluate(code, arg)

    def text(self):
        """The journal text, one string per line."""
        return self.js("journalText()").split("\r\n")

    def set(self, code):
        """Change the journal (code works on S), then save and redraw, like typing in the form does."""
        self.js(f"() => {{ {code}; render(); save(); }}")

    def done(self):
        assert not self.errors, "script errors on the page: " + " | ".join(self.errors)
        self.ctx.close()
