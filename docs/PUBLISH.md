# Publication packet and remaining gate

Local work for v0.1 lives in this repository. Creating the public GitHub
repository is **gated**. Do not run the commands in “After approval” until
Shiven says the packet is accepted.

## Proposed initial commit

A single signed-off commit on `main` that contains the curated public tree:
records, compiler, adapter, stile example, licences, tests, and workflows.
No vault Git history. No `dist/`. No extract script.

Suggested message:

```
Publish HubWīk v0.1 as a standalone public source.

Recovered treatises and crop records without private history, merchant
identifiers, or generated HTML as canon.

Signed-off-by: Shiven <shiven@shiven.co.uk>
```

Use the committer identity already configured on the machine. Do not rewrite
Git config for the sign-off.

## Licence map

See [LICENSING.md](../LICENSING.md) and [REUSE.toml](../REUSE.toml).

## Inclusion and exclusion

See [BOUNDARY.md](BOUNDARY.md) and the boundary canvas beside the chat.

## Known limitations in v0.1

- Six catalogue crops are `incomplete` (chives, cress, dill, pea, spring onion,
  Swiss chard): growing instruction is present; yield is still open.
- No images.
- No public observation ledger.
- Shopify deploy stays a private overlay. The public adapter has no store
  credentials and no variant identifiers.
- The stile example accepts no payment. Settlement, wallets, facilitators,
  and production routes stay out.
- Profile prices are catalogue notes, not a live till.
- The public THH profile records 18 / 16 / 12 membership as of 2026-09-03.

## Local verification

From a clean checkout:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m hubwik check
PYTHONPATH=src python3 -m hubwik build
python3 -m http.server 8765 --directory dist/pages
```

Inspect `hubwik.html`, every `grow-*.html`, JSON-LD on those pages,
`dist/cite_set.json`, and `dist/shopify/snippets/`.

## After approval

Only then:

1. `gh repo create the-homestead-hub/hubwik --public --source=. --remote=origin --push`
2. Enable Issues, private vulnerability reporting, and a ruleset that requires
   signed-off commits, reviews on `main`, and protection of `.github/workflows/`
3. Tag `v0.1.0`
4. Open the three starter issues under `docs/starter-issues/`
5. Point private consumers at that tag (see the lock file in homestead-ops)

Never put store credentials in public Actions. Never flip the private vault
or operations repositories to public as a substitute for this repository.
