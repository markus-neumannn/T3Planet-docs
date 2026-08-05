---
title: "MCP Server"
description: "MCP Server for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "MCP Server"
---

## Purpose

Connect external AI agents to TYPO3 through the **Model Context Protocol (MCP)**. Tools like **Cursor**, **Claude Desktop**, and **n8n** can read pages, inspect schema, and update records (with permissions).

**Path:** T3AF → MCP Server

## What MCP does

- Read TYPO3 pages and content
- Inspect database schema
- Create or update records (with permissions)
- Call extension-registered tools (see [MCP Tools](/T3AF/MCPTools/Index))

## Enable MCP

1. Extension Configuration → set `enableMcpServer = 1`
2. Or use MCP Server → Advanced in the backend
3. Flush cache → status should show **Online**

## Health check

```
curl -sS -o /dev/null -w "%{http_code}" https://your-site.com/mcp
# Expect: 401 (auth required = good)
```

```
curl -sS https://your-site.com/.well-known/oauth-authorization-server/mcp
# Expect: JSON 200
```

## Connection methods

- **Remote OAuth** — Production and Cursor. Uses OAuth 2.1 with PKCE.
- **mcp-remote** — Simple HTTP clients. Uses URL token.
- **Local CLI** — DDEV and local development. Uses backend user and workspace.

## MCP modes

Set in the MCP Server top bar:

- **Context** — Agent reads TYPO3; AI runs outside TYPO3
- **Native** — TYPO3 runs AI on the server (uses provider or T3Planet Credits)

## Core tools (v1)

- `table_schema` — Field metadata for any table
- `pages_get` — Read one page
- `content_list` — List content on a page
- `write_table` — Create, update, or delete records

Child extensions can register more tools — visible in the **MCP Tools** tab.

## Workspaces

- **0** — Live workspace
- **1+** — Draft workspace

MCP edits respect the active workspace. Test writes in workspace `1` before live.

## Cursor example (stdio / DDEV)

```
{
  "mcpServers": {
    "typo3": {
      "command": "bash",
      "args": ["-lc", "cd /path/to/project && ddev exec php vendor/bin/typo3 ns_t3af:mcp:serve --no-startup-message -u admin -w 0"]
    }
  }
}
```

## Security

- Use **HTTPS** in production
- Treat URL tokens like passwords
- Limit which backend users can authorize OAuth
- Test in draft workspace before live writes
- Enable [AI Permissions](/T3AF/GovernanceAndAccess/Index) for multi-user sites

## When to enable MCP

- Developers use Cursor or Claude Desktop with TYPO3 daily
- Automation workflows via n8n need CMS access
- Staging environment for safe agent testing

## When not to enable yet

- Production site without HTTPS
- No clear policy for which admins may authorize agents
- Team has not completed [AI Providers](/T3AF/AIProviders/Index) setup

<Note>
- MCP protocol: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
</Note>
