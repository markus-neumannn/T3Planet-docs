# Slug match live: ExtNsT3AF + Index-suffix FAQ fix

Date: 2026-08-07

## Goal
Mintlify page slugs match live RTD. Legacy `/T3AF/...` redirects to ExtNsT3AF. Bare-leaf live paths (Support, BuyNow, FAQ) must not use an extra `/Index` segment when live does not.

## A. ExtNsFriendlyCaptcha FAQ slug (fixed)

| Check | Result |
|-------|--------|
| Live | `/ExtNsFriendlyCaptcha/FAQ` (`FAQ.html`) |
| Before | `ExtNsFriendlyCaptcha/FAQ/Index.md` → `/ExtNsFriendlyCaptcha/FAQ/Index` |
| After | `ExtNsFriendlyCaptcha/FAQ.md` → `/ExtNsFriendlyCaptcha/FAQ` |
| `git mv` Index → parent FAQ.md | PASS |
| Empty `FAQ/` removed | PASS |
| Nav `ExtNsFriendlyCaptcha/FAQ` | PASS |
| Redirect `/ExtNsFriendlyCaptcha/FAQ/Index` → `/ExtNsFriendlyCaptcha/FAQ` | PASS |
| Redirect `/ExtNsFriendlyCaptcha/FAQ/Index.html` → `/ExtNsFriendlyCaptcha/FAQ` | PASS |

Local preview (`:3000` via cache proxy, mint `:3001`):

| URL | Result |
|-----|--------|
| `/ExtNsT3AF/Index` | 200 — title T3AF |
| `/ExtNsFriendlyCaptcha/FAQ` | 200 — title FAQ |
| `/ExtNsFriendlyCaptcha/FAQ/Index` | 307 → `/ExtNsFriendlyCaptcha/FAQ` |

## B. Full Index-suffix scan vs live `objects.inv`

Source: `https://docs.t3planet.de/en/latest/objects.inv` (cached `scripts/qa-final/objects.inv`)

- Live `std:doc` paths: **743**
- Live paths **not** ending with `/Index` (bare leaves): **118**
- Match (`.md` exists at bare path): **117**
- Mismatch (only `{path}/Index.md`): **1** before fix, **0** after
- Folder-with-children (keep Index + bare→Index redirect): **0**
- Missing both (non-content): `history` (Sphinx util)

### Index-suffix mismatches found and fixed

1. **`ExtNsFriendlyCaptcha/FAQ`**
   - Live: `/ExtNsFriendlyCaptcha/FAQ`
   - Was: `ExtNsFriendlyCaptcha/FAQ/Index.md` only
   - Fix: moved to `ExtNsFriendlyCaptcha/FAQ.md`; nav + redirects updated

No other bare-leaf Index-suffix mismatches. Support/BuyNow pages already use `Name.md`.

## C. Preview restart

```
launchctl kickstart -k "gui/$(id -u)/com.nitsan.mintlify.dev"
```

Mint took ~2–3 minutes to become ready on `:3001`; cache proxy then bound `:3000`. Curl checks above succeeded.

## D. LIVE_ONLY after fixes

| Metric | Count |
|--------|------:|
| live std:doc | 743 |
| LIVE_ONLY (no mint file) | 1 |
| LIVE_ONLY Sphinx utils | 1 (`history`) |
| LIVE_ONLY encoding-only | 0 |
| LIVE_ONLY true content misses | **0** |

True content misses: **0** (encoding-only OK). Remaining LIVE_ONLY is Sphinx utility `history` only.

## ExtNsT3AF rename (prior)

- `T3AF/` → `ExtNsT3AF/` complete; nav uses `ExtNsT3AF/...`
- Legacy `/T3AF` family redirects retained

## Artifacts

- `scripts/qa-final/objects.inv`
- `scripts/qa-final/_index_suffix_scan.json` (pre-fix scan snapshot may list FAQ mismatch)
- `scripts/qa-final/_live_only_after_slug_fix.json`
