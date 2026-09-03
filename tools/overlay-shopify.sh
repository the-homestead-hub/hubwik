#!/bin/sh
# Copy the HubWīk overlay into a private Shopify theme directory.
# Does not push. Does not read store credentials.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
dest=${1:-}

if [ -z "$dest" ] || [ ! -d "$dest" ]; then
  echo "usage: tools/overlay-shopify.sh /path/to/your/private/theme" >&2
  echo "That folder should already contain snippets/, sections/, assets/, templates/." >&2
  exit 1
fi

PYTHONPATH="$root/src" python3 -m hubwik build

mkdir -p "$dest/snippets" "$dest/sections" "$dest/assets" "$dest/templates"
cp "$root/dist/shopify/snippets/"*.liquid "$dest/snippets/"
cp "$root/adapters/shopify/snippets/"*.liquid "$dest/snippets/"
cp "$root/adapters/shopify/sections/"*.liquid "$dest/sections/"
cp "$root/adapters/shopify/assets/"*.css "$dest/assets/"
cp "$root/adapters/shopify/templates/"*.json "$dest/templates/"

echo "Copied HubWīk files into $dest"
echo "Next, in that theme folder:"
echo "  shopify theme dev"
echo "Then, when it looks right:"
echo "  shopify theme push --only snippets/thh-hubwik-lookup.liquid --only snippets/thh-hubwik-body.liquid --only snippets/thh-hubwik-index.liquid --only snippets/thh-hubwik-mark.liquid --only snippets/thh-hubwik-search-mark.liquid --only sections/thh-hubwik-hall.liquid --only sections/thh-hubwik-room.liquid --only assets/thh-hubwik.css --only templates/page.hubwik.json --only templates/page.hubwik-crop.json"
