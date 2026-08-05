---
title: "System Requirements"
description: "System Requirements for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "System Requirements"
---

## Purpose

This page lists what your server and TYPO3 instance need before you install **EXT:ns_t3af**. Check these items on staging before production.

## Core requirements

- **TYPO3 CMS** — 12.4 LTS, 13.4 LTS, or 14.x
- **PHP** — 8.2 or higher (8.3 recommended)
- **Database** — MySQL 8.0+ or MariaDB 10.3+
- **Web server** — Apache or Nginx with HTTPS on production

## Required system extensions

- **workspaces** — Draft workspaces for MCP and safe edits
- **scheduler** — Background AI jobs

## Composer / package dependencies

T3AF is distributed as a T3Planet premium extension package. Do not use a public `composer require` command unless you have access to the required private package source.

**Depends on:**`nitsan/ns-license`, `typo3/cms-workspaces`, `typo3/cms-scheduler`

**Conflicts with:** other MCP server packages (`marekskopal/typo3-mcp-server`, `hn/typo3-mcp-server`, and similar). Remove conflicting packages before install.

## MCP server (optional)

If you plan to use the MCP server:

- **TYPO3** — 13.4+ or 14.3+ for full MCP support
- **HTTPS** — Required for OAuth in production
- **mcp/sdk** — Bundled with T3AF

See [MCP Server](/T3AF/MCPServer/Index).

## Server resources

- **PHP memory** — Minimum 256 MB; 512 MB or more recommended
- **Max execution time** — Minimum 60 seconds; 120 seconds or more recommended for long AI calls
- **Outbound HTTPS** — Required for AI API calls

## External services (at least one)

You need at least one of these before AI features work:

- **AI provider API key** — BYOK (Bring Your Own Key) mode
- **T3Planet Credits** — Managed billing mode (see [T3Planet Credits](/T3AF/T3PlanetCredits/Index))
- **DeepL / Google keys** — Optional, for translation settings in Extension Configuration

## Pre-install checklist

- TYPO3 12.4+ with the supported T3Planet package installation workflow
- PHP 8.2+ with extensions `mbstring`, `json`, `openssl`, `curl`
- HTTPS on production
- Scheduler cron active (every minute)
- API key or credits plan ready
- T3Planet license key for premium install — see [https://docs.t3planet.de/en/latest/License/Index.html](/License/Index)

When you are ready, continue with [Installation](/T3AF/Installation/Index).
