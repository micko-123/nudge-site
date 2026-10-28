"""Builds the Nudge website and checks it before you push.

    python build.py

1. Turns legal-src/privacy.md and legal-src/terms.md into privacy/index.html
   and terms/index.html.
2. Checks config.json, the file the app reads to learn about updates, and
   stops with a clear message if something in it could hurt users.
3. Warns about anything still to fill in: [brackets] and the DRAFT line.

Only Python's standard library is used: nothing to install.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<main>
<p class="back"><a href="../">&larr; Nudge</a></p>
{body}
</main>
</body>
</html>
"""


def inline(text):
    """Bold, links and plain URLs, with everything else escaped."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"(https?://[^\s)<]+)",
        lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>',
        text,
    )
    return text


def markdown_to_html(source):
    """The small part of Markdown the legal texts use: headings, paragraphs,
    bullet lists (with wrapped lines), tables and bold."""
    out = []
    lines = source.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("# "):
            out.append(f"<h1>{inline(line[2:])}</h1>")
            i += 1
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in cells):
                    rows.append(cells)
                i += 1
            head, *body = rows
            out.append('<div class="table"><table>')
            out.append(
                "<thead><tr>"
                + "".join(f"<th>{inline(c)}</th>" for c in head)
                + "</tr></thead><tbody>"
            )
            for r in body:
                out.append(
                    "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                )
            out.append("</tbody></table></div>")
        elif line.startswith("- "):
            items = []
            while i < len(lines) and (
                lines[i].startswith("- ") or lines[i].startswith("  ")
            ):
                if lines[i].startswith("- "):
                    items.append(lines[i][2:].strip())
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append(
                "<ul>" + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ul>"
            )
        else:
            para = []
            while (
                i < len(lines)
                and lines[i].strip()
                and not lines[i].startswith(("#", "|", "- "))
            ):
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


def build_page(name, title):
    source = (ROOT / "legal-src" / f"{name}.md").read_text(encoding="utf-8")
    target = ROOT / name / "index.html"
    target.parent.mkdir(exist_ok=True)
    target.write_text(
        PAGE.format(title=title, body=markdown_to_html(source)), encoding="utf-8"
    )
    left = sorted(set(re.findall(r"\[[^\]]+\]", source)))
    warnings = []
    if "DRAFT" in source:
        warnings.append(f"{name}: the DRAFT line is still there")
    if left:
        warnings.append(f"{name}: still to fill in: {', '.join(left)}")
    return warnings


def check_config():
    """The app trusts this file, so mistakes are stopped here, not on phones."""
    path = ROOT / "config.json"
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"config.json is not valid JSON: {e}"]
    problems = []
    if config.get("schema") != 1:
        problems.append('config.json: "schema" must be 1')
    update = config.get("update")
    if not isinstance(update, dict):
        return problems + ['config.json: an "update" section is needed']
    latest = update.get("latest_build")
    minimum = update.get("min_build")
    for key, value in (("latest_build", latest), ("min_build", minimum)):
        if not isinstance(value, int) or value < 1:
            problems.append(f"config.json: {key} must be a whole number from 1")
    if isinstance(latest, int) and isinstance(minimum, int):
        if minimum > latest:
            problems.append(
                "config.json: min_build is above latest_build. That would "
                "force everyone to update to a version that does not exist."
            )
        if latest > 10000:
            problems.append("config.json: latest_build looks wrong (over 10000)")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(update.get("latest_version", ""))):
        problems.append('config.json: latest_version must look like "1.2.0"')
    notes = update.get("notes", {})
    for lang, items in notes.items():
        if not isinstance(items, list) or len(items) > 6:
            problems.append(f"config.json: notes.{lang} must be a list of up to 6")
            continue
        for item in items:
            if not isinstance(item, str) or len(item) > 140:
                problems.append(
                    f"config.json: each note must be text of 140 characters "
                    f"or fewer: {item!r}"
                )
            elif "<" in str(item) or "http" in str(item):
                problems.append(
                    f"config.json: notes are plain text, no links or tags: {item!r}"
                )
    reason = update.get("reason", {})
    for lang, text in reason.items():
        if not isinstance(text, str) or len(text) > 200:
            problems.append(f"config.json: reason.{lang} must be text up to 200")
    return problems


def main():
    warnings = build_page("privacy", "Nudge — Privacy Policy")
    warnings += build_page("terms", "Nudge — Terms of Service")
    problems = check_config()
    print("Built privacy/index.html and terms/index.html.")
    for w in warnings:
        print(f"  TO DO  {w}")
    if problems:
        for p in problems:
            print(f"  STOP   {p}")
        print("Fix config.json before you push.")
        sys.exit(1)
    print("config.json looks right.")


if __name__ == "__main__":
    main()
