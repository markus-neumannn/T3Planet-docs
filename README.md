# T3Planet Docs (Mintlify)

Official T3Planet product documentation — Mintlify source for [docs.t3planet.de](https://docs.t3planet.de/en/latest/) migration and hosting.

## Stack

- **Mintlify** (`docs.json` + Markdown)
- **Node 22 LTS** for local preview (`mint dev`)
- Custom assets: `custom.css`, `_static/`

## Local preview

```bash
npm i -g mint@latest
# Use Node 22 (Node 26+ breaks Mintlify)
mint login   # enables search against your Mintlify project index
mint dev
```

Fast LAN preview (cache proxy): see `scripts/start_fast_preview.sh`.

## Important paths

| Path | Purpose |
|------|---------|
| `docs.json` | Navigation, redirects, theme |
| `ExtNsT3AF/` | T3AF (shared AI) product docs |
| `AIFoundationExtensions/` | AI Universe hub |
| `_static/` | Logos, JS |
| `.mintignore` | Excludes `de/`, `Live-docs/`, `scripts/` from Mintlify build |

## Deploy to Mintlify

1. Connect this GitHub repo in the [Mintlify dashboard](https://dashboard.mintlify.com).
2. Set deploy branch (`master` or `main`).
3. Push → Mintlify builds and indexes search.

## License

Documentation content © T3Planet / NITSAN. See repository license notice (`COPYING`).

<!-- deploy: markus-only contributor history -->
