---
title: "Custom MCP Tools"
description: "Custom MCP Tools for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "Custom MCP Tools"
---

Use custom MCP tools when your extension should expose safe TYPO3 operations to MCP clients such as Cursor, Claude Desktop, MCP Inspector, or the T3AF backend MCP Tools area.

MCP tools are callable through `tools/list` and `tools/call`. They can also appear in T3AF > MCP Tools when the extension provides card metadata.

## Architecture

**Tool handler**

A PHP service with an `execute()` method annotated with `#[McpTool]`.

**Tool schema**

T3AF introspects the handler signature and PHPDoc to publish parameters.

**Dependency injection**

Tool services must be public and tagged with `mcp.tool` in your extension.

**Invocation context**

T3AF applies MCP context such as workspace and provider selection before the handler runs.

**Backend MCP Tools area**

Editors can browse tools, inspect parameters, and test calls through the MCP Tools screen and playground workflow.

## Implementation steps

1. Create a handler class under `Classes/Mcp/Tool/`.
2. Implement `McpToolHandlerInterface` or use the `#[AsMcpTool]` class attribute.
3. Add `#[McpTool(name: '...', description: '...')]` to `execute()`.
4. Return a JSON string from `execute()`.
5. Register the class as a public service tagged with `mcp.tool`.
6. Flush caches.
7. Verify the tool with `tools/list` and `tools/call`.

## Minimal handler

```
use const JSON_THROW_ON_ERROR;
use Mcp\Capability\Attribute\McpTool;
use NITSAN\NsT3AF\Mcp\Contract\McpToolHandlerInterface;

final readonly class HelloTool implements McpToolHandlerInterface
{
    #[McpTool(
        name: 'myext_hello',
        description: 'Returns a greeting for the given name.',
    )]
    public function execute(string $name = 'world'): string
    {
        return json_encode(['message' => 'Hello ' . $name], JSON_THROW_ON_ERROR);
    }
}
```

## Service registration

```
services:
  _defaults:
    autowire: true
    autoconfigure: true

  _instanceof:
    NITSAN\NsT3AF\Mcp\Contract\McpToolHandlerInterface:
      tags: ['mcp.tool']
      public: true

  MyVendor\MyExt\Mcp\Tool\:
    resource: '../Classes/Mcp/Tool/*'
```

## Parameters

Map MCP input arguments to typed `execute()` parameters. Optional parameters need default values. Use PHPDoc `@param` descriptions so the backend MCP Tools screen can show useful parameter help.

T3AF can augment published schemas with global MCP context such as workspace or AI provider selection, depending on the tool type. Your handler should only declare the parameters it actually uses.

## Response lifecycle

Return a JSON string. For expected validation problems, return a structured JSON error. For unexpected failures, throw a clear exception and let the MCP layer map the failure for the client.

## Client usage

Cursor, Claude Desktop, MCP Inspector, and other MCP clients connect through the MCP Server configuration. After connection, the client discovers your tool through `tools/list` and calls it with `tools/call`.

Use:

- [MCP Server](/T3AF/Integrations/MCPServer/Index) for transport and client connection setup.
- [MCP Server — Testing guide](/T3AF/Integrations/MCPTesting/Index) for Cursor and Claude Desktop validation.
- [MCP Tools](/T3AF/Integrations/MCPTools/Index) for backend tool browsing and playground testing.

## Backend MCP Tools card

If your extension should appear as its own group in T3AF > MCP Tools, provide extension card metadata through the supported MCP tools card provider path. Tools are grouped by ownership, namespace inference, or configured tool prefix.

Use stable tool names such as `myext_action_name`. This keeps tools predictable for external clients and easier to find in the backend.

## Best practices

- Keep tool names stable after release.
- Use a unique prefix that matches your extension.
- Keep handlers thin and delegate business logic to services.
- Avoid calling backend controllers from MCP tools.
- Validate parameters before writing data.
- Respect TYPO3 workspace and backend-user context.
- Return JSON only.
- Do not expose secrets in responses or errors.

## Debugging

**Tool does not appear in ``tools/list``**

- Confirm the service is registered in the container.
- Confirm it is tagged with `mcp.tool`.
- Confirm the service is public.
- Confirm `execute()` has `#[McpTool]`.
- Flush TYPO3 caches.

**Tool appears under the wrong backend card**

- Confirm the tool name prefix matches the extension metadata.
- Add explicit ownership metadata if namespace inference cannot detect the extension.

**Client cannot call the tool**

- Verify the MCP Server connection first.
- Test the same tool in T3AF > MCP Tools.
- Check the input schema and required parameters.
- Review TYPO3 logs for handler exceptions.

## Related documentation

- [MCP Server](/T3AF/Integrations/MCPServer/Index)
- [MCP Tools](/T3AF/Integrations/MCPTools/Index)
- [MCP Server — Testing guide](/T3AF/Integrations/MCPTesting/Index)
- [Extension Integration](/T3AF/DeveloperGuide/ExtensionIntegration/Index)
