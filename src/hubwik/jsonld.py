from __future__ import annotations


def howto(name: str, desc: str, steps: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": desc,
        "step": [{"@type": "HowToStep", "name": n, "text": t} for n, t in steps if n and t],
    }


def faqpage(items: list[tuple[str, str]]) -> dict | None:
    if not items:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in items
        ],
    }


def article(title: str, desc: str, url_path: str, author: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "url": url_path,
        "author": {"@type": "Organization", "name": author},
    }
