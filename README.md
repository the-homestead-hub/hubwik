# HubWīk

Open household-growing records and a compiler that turns them into citable
pages. Spoken **Hub Wick**. The shop is the house. This book is the wick.

HubWīk is Agripædia: standing knowledge of a working windowsill, not a second
brand and not a chatbot. Treatises stay open. Live price, stock, and checkout
stay at a shop till. A stile may answer HTTP 402 to agents for scarce
computation; it is never a citation URL.

This repository is the canonical public source. Private vaults, store
credentials, and settlement services consume a versioned release. They are not
upstream.

## What is here

| Path | What it is |
|---|---|
| `data/crops/` | One Markdown record per variety. Structured frontmatter is canon for generated grow pages. |
| `data/profiles/thh.json` | The Homestead Hub membership: 18 in the catalogue, 16 in the Four by Four, 12 in the Three by Four. |
| `data/schema/` | Crop and observation row shapes. |
| `content/treatises/` | Lore, shop-explained, and titled pages as Markdown. |
| `src/hubwik/` | Compiler. Stdlib only. |
| `adapters/shopify/` | HubWīk Liquid and CSS. Not a full theme. |
| `examples/stile/` | Parameterised 402 example. No wallet. |
| `dist/` | Generated HTML, JSON-LD, cite set, and Liquid. Never edit it by hand. |

`data/crops/` may grow beyond any one merchant’s range. Volatile price, stock,
SKUs, product identifiers, and credentials belong in a private deploy overlay.

## Quick start

Python 3.11 or newer. No third-party runtime packages.

```bash
git clone https://github.com/the-homestead-hub/hubwik.git
cd hubwik
PYTHONPATH=src python3 -m hubwik check
PYTHONPATH=src python3 -m hubwik build
python3 -m http.server 8765 --directory dist/pages
```

Open `http://127.0.0.1:8765/hubwik.html`. That preview is generated from the
records. The live book, when a shop publishes it, is a cite-face of the same
source.

Optional install:

```bash
python3 -m pip install -e .
hubwik check
hubwik build
```

## Ontology

Eighteen varieties in the knowledge catalogue. Sixteen ship in the Four by Four.
Twelve ship in the Three by Four. Any variety, £2.99.

That line is data. The hall prints it once. Grow pages teach the crop.

## Licence

- Software: [Apache-2.0](LICENSES/Apache-2.0.txt)
- Prose and original data: [CC BY 4.0](LICENSES/CC-BY-4.0.txt)

See [LICENSING.md](LICENSING.md) and [TRADEMARKS.md](TRADEMARKS.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
Contributions are under the Developer Certificate of Origin, version 1.1.
There is no CLA.

Safety-affecting claims (edibility, toxicity, allergens, pesticides, manure,
preservation, children, pets, pregnancy) need elevated review. See
[docs/SAFETY.md](docs/SAFETY.md).

## Status

v0.1. Known limits are listed in [docs/PUBLISH.md](docs/PUBLISH.md).
Shiven is the lead maintainer.
