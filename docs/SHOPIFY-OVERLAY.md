# Shopify overlay (private, by hand)

The public repo never talks to the shop. You copy files onto the theme
you already use, then push from your machine.

## Once

You need the Shopify CLI and a local copy of the live theme (the folder that
already has `snippets/` and `sections/`).

```bash
cd ~/hubwik
git pull
```

## Every time HubWīk changes

Replace `/path/to/theme` with that theme folder.

```bash
cd ~/hubwik
chmod +x tools/overlay-shopify.sh
./tools/overlay-shopify.sh /path/to/theme
```

That builds `dist/` and copies only HubWīk files into the theme.

Preview:

```bash
cd /path/to/theme
shopify theme dev
```

Open `/pages/hubwik` and one grow page (for example `/pages/grow-basil`).
The grow-page box image must be that variety’s Seed Pack front, not the
family grid hero. The room section matches the live Seed Pack variant by
title (and never falls back to the product hero on seed rooms).
Leave the room section’s Stile URL blank unless you are testing agents.

Push only those files (the script prints the exact `--only` list):

```bash
cd /path/to/theme
shopify theme push --only snippets/thh-hubwik-lookup.liquid --only snippets/thh-hubwik-body.liquid --only snippets/thh-hubwik-index.liquid --only snippets/thh-hubwik-mark.liquid --only snippets/thh-hubwik-search-mark.liquid --only sections/thh-hubwik-hall.liquid --only sections/thh-hubwik-room.liquid --only assets/thh-hubwik.css --only templates/page.hubwik.json --only templates/page.hubwik-crop.json
```

Use the store and theme you already use for Craft. Do not put those names,
theme IDs, or tokens in the public HubWīk repo or in GitHub Actions.
