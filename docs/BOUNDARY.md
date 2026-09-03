# Rights and publication boundary

This file is the inclusion and exclusion law for the public repository.
It names *kinds* of material. It does not reprint merchant identifiers,
credentials, or private paths.

## Included

| Source | How it entered | Licence in this repo |
|---|---|---|
| 18 crop records | Curated extraction from private product-knowledge files, then cleaned | CC BY 4.0 |
| 9 treatises (lore, shop-explained, titled) | Recovered from the 2026 generator tree, then edited | CC BY 4.0 |
| Crop and observation schemas | Public row shapes only | CC BY 4.0 |
| THH profile `data/profiles/thh.json` | Public membership and ontology line | CC BY 4.0 |
| Compiler under `src/hubwik/` | New portable package; not the private generator history | Apache-2.0 |
| Shopify adapter Liquid and CSS | Hand-authored HubWīk surfaces only | Apache-2.0 |
| Stile example | Parameterised Worker; no account, wallet, or production hostname | Apache-2.0 |
| Community, licence, and safety policy | Written for this repository | CC BY 4.0 |

The private vault Git history was not copied. Commit `821bd71` was a recovery
point, not a parent of this repository.

## Redacted from recovered material

- Reconciliation notes and build-process sentences
- Truncated flavour clauses (the compiler now refuses a clipped flavour)
- Kit copy that claimed a “full listed seed range” for the Four by Four
- SKU rows, lot codes, and product or variant identifiers
- Theme identifiers, store slugs, and cloud account identifiers
- Absolute workstation paths
- Partner names and recruitment notes
- Horizon essays on grow or kit pages

## Generated — never canon

`dist/` is a build product: HTML previews, `cite_set.json`, ontology text, and
Shopify snippets. Contribute the record that produces them.

## Excluded entirely

| Kind | Why |
|---|---|
| Vault tasks, audits, strategy, and partner-recruitment playbooks | Private operations |
| Observation “order of approach” and named-grower lists | Private; the row *shape* is public |
| QA screenshots, diagnostics, graph caches, PDF virtualenvs | Local debris |
| Full shop themes | Not HubWīk; a theme is a private overlay |
| Live prices as a feed, stock, SKUs, lot codes, product GIDs | Merchant state |
| Credentials, tokens, and secret stores | Credentials |
| Unreleased settlement, wallets, facilitators, production routes | Separate security review |
| Private dashboard Record-desk work | Separate private change |
| Images without a completed provenance row | Rights |

## Checks

`python3 -m hubwik check` compiles the book and scans tracked text for
credential patterns, merchant identifier shapes, private absolute paths, and
reconciliation-note phrases. A hit fails the build.

Pull-request workflows run that check with read-only permissions and no
secrets. They do not deploy.
