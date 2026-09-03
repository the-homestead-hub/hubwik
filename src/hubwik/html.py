from __future__ import annotations

import html
import json
import re


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def j(value) -> str:
    return json.dumps("" if value is None else value, ensure_ascii=False)


def box_html(rows: list[tuple[str, str]]) -> str:
    bits = ["<table>"]
    for label, value in rows:
        if value in (None, ""):
            continue
        bits.append(f"<tr><th>{esc(label)}</th><td>{esc(value)}</td></tr>")
    bits.append("</table>")
    return "\n".join(bits)


def toc_html(items: list[tuple[str, str]]) -> str:
    lis = "".join(f'<li><a href="#{esc(sid)}">{esc(heading)}</a></li>' for sid, heading in items)
    return f'<nav class="thh-hw-toc"><strong>On this page</strong><ol>{lis}</ol></nav>'


def faq_html(items: list[tuple[str, str]]) -> str:
    if not items:
        return ""
    bits = ['<section id="faq"><h2>Questions</h2><div class="thh-hw-faq">']
    for question, answer in items:
        bits.append(f"<details><summary>{esc(question)}</summary><p>{esc(answer)}</p></details>")
    bits.append("</div></section>")
    return "\n".join(bits)


def sources_html(items: list[tuple[str, str]]) -> str:
    if not items:
        return ""
    bits = ['<section id="sources"><h2>Sources</h2><ol class="thh-hw-src">']
    for title, url in items:
        if url:
            bits.append(f'<li><a href="{esc(url)}">{esc(title)}</a></li>')
        else:
            bits.append(f"<li>{esc(title)}</li>")
    bits.append("</ol></section>")
    return "\n".join(bits)


def sections_from_markdown(body: str) -> list[tuple[str, str, str]]:
    """Turn treatise markdown (## heading + HTML or prose) into section triples."""
    text = re.sub(r"^# .+\n+", "", body.strip(), count=1)
    parts = re.split(r"^## ", text, flags=re.M)
    sections = []
    for index, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
        if index == 0 and not text.lstrip().startswith("## "):
            continue
        heading, _, rest = part.partition("\n")
        heading = heading.strip()
        if heading.lower() in {"questions", "faq", "sources"}:
            continue
        sid = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-") or "section"
        html_body = rest.strip()
        if html_body and not html_body.lstrip().startswith("<"):
            paras = [p.strip() for p in re.split(r"\n\s*\n", html_body) if p.strip()]
            html_body = "".join(f"<p>{esc(p)}</p>" for p in paras)
        sections.append((sid, heading, html_body))
    return sections


def article_html(toc, sections, faq, sources) -> str:
    section_html = "".join(
        f'<section id="{esc(sid)}"><h2>{esc(heading)}</h2>{body.strip()}</section>'
        for sid, heading, body in sections
    )
    return "\n".join(x for x in (toc_html(toc), section_html, faq_html(faq), sources_html(sources)) if x)
