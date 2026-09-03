from __future__ import annotations

import json
import re
from pathlib import Path

from hubwik import jsonld
from hubwik.html import article_html, box_html, esc, j, sections_from_markdown
from hubwik.load import load_workspace
from hubwik.paths import dist_dir, repo_root


def _join(*parts: str) -> str:
    return "".join(parts)


def _public_citation(source: str) -> bool:
    text = source.lower()
    if any(token in text for token in ("yield empty", "truncat", "not verified", "product record")):
        return False
    return any(token in source for token in ("RHS", "http://", "https://", "Grower knowledge"))


def _harvest_lines(crop: dict) -> list[str]:
    notes = crop.get("harvest_notes") or crop.get("harvest_method")
    raw: list[str] = []
    if isinstance(notes, list):
        raw = [str(x) for x in notes]
    elif isinstance(notes, str):
        raw = notes.splitlines()
    out = []
    for item in raw:
        for line in str(item).splitlines():
            cleaned = line.strip().lstrip("-").strip()
            if cleaned:
                out.append(cleaned)
    if not out:
        for stage in crop.get("growth_stages") or []:
            if not isinstance(stage, dict):
                continue
            label = str(stage.get("stage_id") or stage.get("stage_label") or "").lower()
            if "harvest" in label:
                action = stage.get("action") or stage.get("headline")
                if action:
                    out.append(str(action))
    return out


def compile_seed(crop: dict, profile: dict) -> dict:
    handle = crop["handle"]
    title = crop["crop_name"]
    flavour = str(crop.get("flavour") or crop.get("flavour_profile") or "")
    if flavour.endswith(("more", "slig", "whol", "cotyledons")):
        raise ValueError(f"truncated flavour on {handle}: {flavour!r}")
    sow = crop.get("sow") or ""
    harvest = crop.get("harvest") or ""
    claim = crop.get("claim") or crop.get("deck") or ""
    germ_min = crop.get("germination_days_min")
    germ_max = crop.get("germination_days_max")
    sow_html = f"<p>Sow {esc(sow)}. Use peat-free coco. Keep the surface just moist.</p>"
    if germ_min and germ_max:
        sow_html += f"<p>Germination {esc(germ_min)}–{esc(germ_max)} days in the crop record.</p>"
    grow_bits = ["<ol>"]
    stages = crop.get("growth_stages") or []
    if stages:
        for stage in stages:
            if not isinstance(stage, dict):
                continue
            grow_bits.append(
                f"<li><strong>{esc(stage.get('stage_label') or stage.get('stage_id'))}</strong>"
                f" — {esc(stage.get('timeline'))}. {esc(stage.get('action') or stage.get('headline'))}</li>"
            )
    else:
        light = crop.get("light_hours_min")
        grow_bits.append(
            "<li>Keep the surface just moist. "
            f"{'Six or more hours of light.' if not light else f'At least {esc(light)} hours of light.'}</li>"
        )
    grow_bits.append("</ol>")
    if crop.get("temp_min_c") not in (None, ""):
        grow_bits.append(f"<p>Keep at or above {esc(crop['temp_min_c'])}°C where the crop record sets a floor.</p>")
    lines = _harvest_lines(crop)
    first = f"First cut around {harvest}." if harvest else "Harvest when the treatise says the plant is ready."
    harvest_html = "".join(f"<p>{esc(p)}</p>" for p in [first, *lines])
    howto_harvest = lines[0] if lines else first
    faq_harvest = " ".join(lines[:4]) if lines else first
    mistakes = crop.get("beginner_mistakes") or []
    mist = ""
    if mistakes:
        mist = "<ul>" + "".join(
            f"<li><strong>{esc(m.get('mistake'))}</strong> — {esc(m.get('why'))} {esc(m.get('fix'))}</li>"
            for m in mistakes
            if isinstance(m, dict)
        ) + "</ul>"
    kitchen = crop.get("culinary_applications") or []
    kitc = ""
    if kitchen:
        kitc = "<ul>" + "".join(
            f"<li><strong>{esc(k.get('name'))}</strong> — {esc(k.get('method'))}</li>"
            for k in kitchen
            if isinstance(k, dict)
        ) + "</ul>"
    toc = [("sow", "How to sow"), ("grow", "Growing"), ("harvest", "Harvest")]
    sections = [
        ("sow", "How to sow", sow_html),
        ("grow", "Growing", "".join(grow_bits)),
        ("harvest", "Harvest", harvest_html),
    ]
    if mist:
        toc.append(("mistakes", "Common mistakes"))
        sections.append(("mistakes", "Common mistakes", mist))
    if kitc:
        toc.append(("kitchen", "In the kitchen"))
        sections.append(("kitchen", "In the kitchen", kitc))
    toc += [("faq", "Questions"), ("sources", "Sources")]
    faq = [
        (f"How long to grow {title.lower()} from seed?", f"First cut around {harvest}." if harvest else first),
        (f"How do I sow {title.lower()}?", f"{sow}. Use peat-free medium. Keep the surface just moist."),
        (f"How do I harvest {title.lower()}?", faq_harvest),
    ]
    sources = [
        (f"{title} Seed Pack", profile.get("seed_pack_path") or "/products/seed-pack"),
        ("Coco Soil treatise", "/pages/coco-soil"),
        ("HubWīk contents", profile.get("hall_path") or "/pages/hubwik"),
    ]
    source = str(crop.get("source") or "")
    if source and _public_citation(source):
        sources.append((source, ""))
    url = f"/pages/grow-{handle}"
    article = article_html(toc, sections, faq, sources)
    pack = crop.get("pack_g")
    pack_label = f"{pack:g} g" if isinstance(pack, (int, float)) else (str(pack) if pack else "")
    box = box_html(
        [
            ("Binomial", crop.get("latin") or crop.get("crop_latin") or ""),
            ("Family", crop.get("crop_family") or ""),
            ("Kind", crop.get("crop_kind") or crop.get("crop_type") or ""),
            ("Variety", crop.get("variety_name") or ""),
            ("Pack", pack_label),
            ("Sow", sow),
            ("First cut", harvest),
            ("Flavour", flavour),
            ("Price", profile.get("seed_pack_price") or ""),
        ]
    )
    seo_title = f"How to grow {title.lower()} from seed | HubWīk | {profile.get('name') or 'The Homestead Hub'}"
    objects = [
        jsonld.howto(f"How to grow {title} from seed", claim, [("Sow", sow), ("Grow", "Keep the surface just moist."), ("Harvest", howto_harvest)]),
        jsonld.faqpage(faq),
        jsonld.article(seo_title, claim, url, profile.get("name") or "The Homestead Hub"),
    ]
    return {
        "handle": handle,
        "crop_id": crop["crop_id"],
        "kind": "seed",
        "part": "growing",
        "part_label": "Growing",
        "title": title,
        "latin": crop.get("latin") or crop.get("crop_latin") or "",
        "claim": claim,
        "lede": crop.get("deck") or claim,
        "sow": sow,
        "harvest": harvest,
        "flavour": flavour,
        "url": url,
        "page_handle": f"grow-{handle}",
        "seo_title": seo_title,
        "box_cap": title,
        "box_html": box,
        "article": article,
        "faq": faq,
        "ld_objects": [obj for obj in objects if obj],
        "till_path": profile.get("seed_pack_path") or "/products/seed-pack",
        "till_label": f"Get {title} seed — £PRICE",
        "till_note": "Opens the Seed Pack till on this variety.",
        "price": profile.get("seed_pack_price") or "",
        "product_handle": "seed-pack",
        "ranking": True,
        "probe_query": f"how to grow {title.lower()} from seed UK",
        "harvest_marker": 'id="harvest"',
    }


def compile_treatise(rec: dict, profile: dict) -> dict:
    sections = sections_from_markdown(rec.get("_body") or "")
    toc = [(sid, heading) for sid, heading, _body in sections]
    faq = [(item["q"], item["a"]) for item in rec.get("faq") or []]
    sources = [(item["title"], item.get("url") or "") for item in rec.get("sources") or []]
    toc += [("faq", "Questions"), ("sources", "Sources")]
    box_rows = [(row["label"], row["value"]) for row in rec.get("box") or []]
    url = rec.get("url") or f"/pages/{rec['handle']}"
    objects = [jsonld.article(rec.get("seo_title") or rec["title"], rec.get("lede") or rec.get("claim") or "", url, profile.get("name") or "The Homestead Hub")]
    if faq:
        objects.append(jsonld.faqpage(faq))
    howto = [(step["name"], step["text"]) for step in rec.get("howto") or []]
    if howto:
        objects.append(jsonld.howto(rec["title"], rec.get("lede") or "", howto))
    return {
        "handle": rec["handle"],
        "kind": rec.get("kind") or "shop",
        "part": rec.get("part") or rec.get("kind") or "shop",
        "part_label": rec.get("part_label") or rec.get("kind") or "",
        "title": rec["title"],
        "latin": rec.get("latin") or "",
        "claim": rec.get("claim") or "",
        "lede": rec.get("lede") or rec.get("claim") or "",
        "sow": "",
        "harvest": "",
        "flavour": "",
        "url": url,
        "page_handle": url.rsplit("/", 1)[-1],
        "seo_title": rec.get("seo_title") or rec["title"],
        "box_cap": rec.get("box_cap") or rec["title"],
        "box_html": box_html(box_rows),
        "article": article_html(toc, sections, faq, sources),
        "faq": faq,
        "ld_objects": [obj for obj in objects if obj],
        "till_path": rec.get("till_path") or "",
        "till_label": rec.get("till_label") or "",
        "till_note": rec.get("till_note") or "",
        "price": "",
        "product_handle": rec.get("product_handle") or "",
        "ranking": True,
    }


def compile_all(root: Path | None = None, profile_id: str = "thh") -> dict:
    workspace = load_workspace(root, profile_id)
    profile = workspace["profile"]
    rooms = []
    for handle in profile["knowledge_catalogue"]:
        crop = workspace["crops_by_handle"].get(handle)
        if not crop:
            raise ValueError(f"profile names {handle} but no crop file exists")
        rooms.append(compile_seed(crop, profile))
    for treatise in workspace["treatises"]:
        rooms.append(compile_treatise(treatise, profile))
    return {"profile": profile, "rooms": rooms, "workspace": workspace}


def ld_html(objects: list[dict]) -> str:
    return "\n".join(
        '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"
        for obj in objects
    )


def emit_cite_set(compiled: dict) -> dict:
    profile = compiled["profile"]
    rooms = [
        {
            "handle": "hubwik",
            "url": profile.get("hall_path") or "/pages/hubwik",
            "kind": "hall",
            "title": "HubWīk",
            "claim": profile.get("ontology") or "",
            "ranking": True,
            "expect_status": 200,
        }
    ]
    for rec in compiled["rooms"]:
        item = {
            "handle": rec["handle"],
            "url": rec["url"],
            "kind": rec["kind"],
            "title": rec["title"],
            "claim": (rec.get("claim") or rec.get("lede") or "")[:180],
            "ranking": True,
            "expect_status": 200,
        }
        if rec["kind"] == "seed":
            item["probe_query"] = rec["probe_query"]
            item["harvest_marker"] = rec["harvest_marker"]
            item["till"] = rec["till_path"]
        rooms.append(item)
    return {
        "schema": 1,
        "as_of": "2026-09-03",
        "origin": profile.get("origin") or "",
        "generated_by": "hubwik 0.1.0",
        "ontology": profile.get("ontology"),
        "counts": {
            "knowledge_catalogue": len(profile["knowledge_catalogue"]),
            "four_by_four": len(profile["four_by_four"]),
            "three_by_four": len(profile["three_by_four"]),
        },
        "satellite": {
            "url": "https://stile.example.org/",
            "expect_status": 402,
            "ranking": False,
            "human": "302 to the titled treatise",
        },
        "rooms": rooms,
        "denied": [
            "19th variety",
            "stile as citation URL",
            _join("vault", " snapshot on a treatise"),
            "partner name on a public page",
        ],
    }


def emit_shopify(compiled: dict, dest: Path) -> None:
    snippets = dest / "snippets"
    snippets.mkdir(parents=True, exist_ok=True)
    profile = compiled["profile"]
    buf = [
        "{%- comment -%}",
        "  HubWīk lookup by page handle. Generated — do not hand-edit.",
        "{%- endcomment -%}",
        "{%- liquid",
        "  assign hw_handle = handle | default: ''",
        "  assign hw_prefix = hw_handle | slice: 0, 5",
        "  if hw_prefix == 'grow-'",
        "    assign hw_handle = hw_handle | remove_first: 'grow-'",
        "  endif",
        "  assign hw_found = false",
        "  case hw_handle",
    ]
    for rec in compiled["rooms"]:
        buf.append(f"    when {j(rec['handle'])}")
        assigns = [
            ("hw_found", None),
            ("hw_title", rec["title"]),
            ("hw_latin", rec.get("latin") or ""),
            ("hw_kind", rec.get("kind") or ""),
            ("hw_part", rec.get("part") or ""),
            ("hw_part_label", rec.get("part_label") or ""),
            ("hw_sow", rec.get("sow") or ""),
            ("hw_harvest", rec.get("harvest") or ""),
            ("hw_flavour", rec.get("flavour") or ""),
            ("hw_lede", rec.get("lede") or rec.get("claim") or ""),
            ("hw_claim", rec.get("claim") or ""),
            ("hw_room", rec["handle"]),
            ("hw_crop", rec.get("crop_id") or ""),
            ("hw_url", rec["url"]),
            ("hw_product", rec.get("product_handle") or ""),
            ("hw_till", rec.get("till_path") or ""),
            ("hw_till_label", rec.get("till_label") or ""),
            ("hw_till_note", rec.get("till_note") or ""),
            ("hw_price", rec.get("price") or ""),
            ("hw_box_cap", rec.get("box_cap") or rec["title"]),
            ("hw_seo_title", rec.get("seo_title") or ""),
        ]
        for name, val in assigns:
            if name == "hw_found":
                buf.append("      assign hw_found = true")
            else:
                buf.append(f"      assign {name} = {j(val)}")
    buf += ["  endcase", "-%}"]
    (snippets / "thh-hubwik-lookup.liquid").write_text("\n".join(buf) + "\n", encoding="utf-8")

    body = [
        "{%- comment -%}",
        "  HubWīk treatise HTML. Slot: article | box | ld. Generated — do not hand-edit.",
        "{%- endcomment -%}",
        "{%- case hw_room -%}",
    ]
    for rec in compiled["rooms"]:
        body.append(f"{{% when {j(rec['handle'])} %}}")
        body.append("{% if hw_slot == 'box' %}")
        body.append(rec["box_html"])
        body.append("{% elsif hw_slot == 'ld' %}")
        body.append(ld_html(rec["ld_objects"]))
        body.append("{% else %}")
        body.append(rec["article"])
        body.append("{% endif %}")
    body.append("{%- endcase -%}")
    text = "\n".join(body) + "\n"
    if _join("vault", " snapshot") in text.lower() or re.search(
        _join("Observed live ", "price on 20") + r"\d\d", text
    ):
        raise ValueError("generated body contains a reconciliation note")
    (snippets / "thh-hubwik-body.liquid").write_text(text, encoding="utf-8")

    growing = ",".join(profile["knowledge_catalogue"])
    lore = ",".join(profile["lore"])
    shop = ",".join(profile["shop"])
    titled = ",".join(profile["titled"])
    sow_now = ",".join(profile["sow_now"])
    index = [
        "{%- comment -%} Generated hall keys and ontology. Do not hand-edit. {%- endcomment -%}",
        "{%- liquid",
        f"  assign hw_ontology = {j(profile['ontology'])}",
        f"  assign hw_lore = {j(lore)} | split: ','",
        f"  assign hw_growing = {j(growing)} | split: ','",
        f"  assign hw_shop = {j(shop)} | split: ','",
        f"  assign hw_titled = {j(titled)} | split: ','",
        f"  assign hw_sow_now = {j(sow_now)} | split: ','",
        f"  assign hw_total = {len(profile['lore']) + len(profile['knowledge_catalogue']) + len(profile['shop']) + len(profile['titled'])}",
        f"  assign hw_count_label = {j(str(len(profile['lore']) + len(profile['knowledge_catalogue']) + len(profile['shop']) + len(profile['titled'])) + ' rooms · 4 parts')}",
        "-%}",
    ]
    (snippets / "thh-hubwik-index.liquid").write_text("\n".join(index) + "\n", encoding="utf-8")


def _page(title: str, body: str) -> str:
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{esc(title)}</title>\n"
        "<link rel=\"stylesheet\" href=\"preview.css\">\n"
        "</head>\n<body class=\"thh-hw\">\n"
        f"{body}\n</body>\n</html>\n"
    )


def emit_pages(compiled: dict, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    index = []
    hall = compiled["profile"]
    seeds = [rec for rec in compiled["rooms"] if rec["kind"] == "seed"]
    others = [rec for rec in compiled["rooms"] if rec["kind"] != "seed"]
    seed_lis = "".join(
        f'<li><a href="{esc(rec["page_handle"])}.html">{esc(rec["title"])}</a>'
        f" — {esc(rec.get('claim') or rec.get('lede') or '')}</li>"
        for rec in seeds
    )
    other_lis = "".join(
        f'<li><a href="{esc(rec["page_handle"])}.html">{esc(rec["title"])}</a>'
        f" — {esc(rec.get('claim') or rec.get('lede') or '')}</li>"
        for rec in others
    )
    hall_body = (
        "<article class=\"thh-hw-preview\">"
        "<p class=\"thh-hw__kicker\">HubWīk · local preview</p>"
        "<h1>HubWīk</h1>"
        f"<p>{esc(hall['ontology'])}</p>"
        f"<p>{esc(hall.get('spoken_line') or '')}</p>"
        "<h2>Growing</h2>"
        f"<ol>{seed_lis}</ol>"
        "<h2>Treatises</h2>"
        f"<ol>{other_lis}</ol>"
        "</article>"
    )
    (dest / "hubwik.html").write_text(_page("HubWīk", hall_body), encoding="utf-8")
    index.append({"handle": "hubwik", "url": hall.get("hall_path"), "kind": "hall", "title": "HubWīk"})
    for rec in compiled["rooms"]:
        body = (
            "<article class=\"thh-hw-preview\">"
            f"<p class=\"thh-hw__kicker\"><a href=\"hubwik.html\">HubWīk</a> · {esc(rec.get('part_label') or rec['kind'])}</p>"
            f"<h1>{esc(rec['title'])}</h1>"
            f"<p>{esc(rec.get('lede') or rec.get('claim'))}</p>"
            f"{rec['box_html']}{rec['article']}{ld_html(rec['ld_objects'])}"
            "</article>"
        )
        (dest / f"{rec['page_handle']}.html").write_text(_page(rec["seo_title"], body), encoding="utf-8")
        index.append({"handle": rec["page_handle"], "url": rec["url"], "kind": rec["kind"], "title": rec["title"]})
    (dest / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    css_src = Path(compiled["workspace"]["root"]) / "adapters" / "shopify" / "assets" / "thh-hubwik.css"
    extra = (
        "\nbody.thh-hw{margin:0;padding:24px;}"
        "\n.thh-hw-preview{max-width:72ch;margin:0 auto;}"
        "\n.thh-hw-preview table{width:100%;border-collapse:collapse;margin:1em 0;}"
        "\n.thh-hw-preview th{text-align:left;padding:4px 12px 4px 0;width:9rem;}"
        "\n.thh-hw-preview .thh-hw__kicker{letter-spacing:.04em;text-transform:uppercase;font-size:12px;}"
        "\n@media (max-width:640px){body.thh-hw{padding:16px;}}\n"
    )
    css = css_src.read_text(encoding="utf-8") + extra if css_src.exists() else extra
    (dest / "preview.css").write_text(css, encoding="utf-8")


def write_dist(root: Path | None = None, profile_id: str = "thh") -> dict:
    root = root or repo_root()
    compiled = compile_all(root, profile_id)
    dest = dist_dir(root)
    dest.mkdir(parents=True, exist_ok=True)
    cite = emit_cite_set(compiled)
    (dest / "cite_set.json").write_text(json.dumps(cite, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    emit_pages(compiled, dest / "pages")
    emit_shopify(compiled, dest / "shopify")
    (dest / "ontology.txt").write_text(compiled["profile"]["ontology"] + "\n", encoding="utf-8")
    return compiled
