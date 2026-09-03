# Contributing to HubWīk

Thank you for helping keep the book accurate. This is a small repository with
one lead maintainer. We want corrections and evidence more than we want a
nineteenth variety.

## Before you write code

1. Read [docs/EDITORIAL.md](docs/EDITORIAL.md) and [docs/SAFETY.md](docs/SAFETY.md).
2. Search existing issues. Use the issue form that matches the change.
3. For a crop correction, edit `data/crops/<id>.md` and keep `crop_id` and
   `handle` stable. The grow page is compiled from the record. Do not hand-edit
   `dist/`.
4. For a treatise, edit Markdown under `content/treatises/`.

## Developer Certificate of Origin

Every commit must include:

```
Signed-off-by: Your Name <you@example.com>
```

Use `git commit -s`. The sign-off is the [Developer Certificate of Origin,
version 1.1](DCO). There is no CLA. You keep copyright in your contribution and
license it under the same licences as the files you touch. See
[LICENSING.md](LICENSING.md).

## Rights and sources

If you adapt text or data from elsewhere, the pull request must state:

- the source (title, author or publisher, date, URL)
- the exact licence or public-domain basis
- what you changed

A citation is not permission. Incompatible or unlicensed material will be
rejected. Do not add images unless [docs/PROVENANCE.md](docs/PROVENANCE.md) can
record author, source, licence, required attribution, and modification status.

Do not contribute merchant identifiers, store credentials, private paths,
lot codes, or partner names.

## AI assistance

If a substantial part of a contribution was produced by an automated system,
say so in the pull request. You remain responsible for rights, accuracy, and
safety. Generated text that you have not checked is not acceptable on a grow
page.

## How to work locally

```bash
PYTHONPATH=src python3 -m hubwik check
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m hubwik build
```

`check` validates records, compiles, and scans for a rights-boundary leak.

## Pull requests

- One subject per pull request.
- Sign off every commit.
- Include a short test plan: which crop or treatise you changed, and that
  `hubwik check` passed.
- Safety-affecting claims must name jurisdiction, source date, and a reviewer
  as [docs/SAFETY.md](docs/SAFETY.md) requires.

Shiven reviews and merges. See [GOVERNANCE.md](GOVERNANCE.md).
