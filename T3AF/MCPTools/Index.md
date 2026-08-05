---
title: "MCP Tools"
description: "MCP Tools for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "MCP Tools"
---

## Purpose

The **MCP Tools** screen lists every tool an AI agent can call against your TYPO3 instance. Core tools ship with T3AF. Child extensions can register additional tools.

**Path:** T3AF → MCP Tools

## What you see

- **Tool catalog** — All registered MCP tools with descriptions
- **Playground** — Test a tool call without leaving the backend
- **Extension cards** — Tools contributed by installed T3Planet AI extensions

## Core tools (v1)

These tools are available when the [MCP Server](/T3AF/MCPServer/Index) is enabled:

- `table_schema` — Field metadata for any database table
- `pages_get` — Read a single page record
- `content_list` — List content elements on a page
- `write_table` — Create, update, or delete records (permission-controlled)

**Warning:** Test write operations in a **draft workspace** before using live workspace `0`.

## Extension-registered tools

When T3AI, T3AC, T3AS, or other connected extensions are installed, their MCP tools appear automatically in the catalog. Each card shows:

- Tool name and description
- Required permissions
- Link to the extension documentation

## Playground workflow

1. Open **T3AF → MCP Tools** in the TYPO3 backend.
2. Select a tool from the catalog (start with read-only tools like `pages_get`).
3. Fill in required fields (page UID, table name, and so on).
4. Run the tool and inspect the JSON response before connecting external agents.

## Why use the playground

- Verify MCP is online before configuring Cursor
- Debug permission errors with a known backend user
- Show stakeholders what agents can access without installing client software

## Security

- Tools respect backend user permissions and workspace context
- OAuth and URL tokens are configured on the [MCP Server](/T3AF/MCPServer/Index) screen
- Limit which admin users may authorize external agents
- Use draft workspaces for `write_table` tests

## When to use MCP Tools vs MCP Server

- **MCP Server** — Enable connectivity, OAuth, and client configuration
- **MCP Tools** — Browse tools, test calls, see extension contributions

See [MCP Server](/T3AF/MCPServer/Index) for connection setup.
