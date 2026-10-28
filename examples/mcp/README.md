# MCP client configs

| File | Client | Auth |
|---|---|---|
| `cursor-mcp.oauth.json` | Cursor (`~/.cursor/mcp.json` or `.cursor/mcp.json`) | Apify OAuth sign-in |
| `cursor-mcp.token.json` | Cursor | `Authorization: Bearer` header; replace `<YOUR_APIFY_TOKEN>` |
| `vscode-mcp.json` | VS Code (`.vscode/mcp.json`) | OAuth; see the main README for the token variant |
| `claude_desktop_config.json` | Claude Desktop config file (local stdio server, Node.js 18+) | `APIFY_TOKEN` env var |

Claude.ai / Claude Desktop can also add the remote URL directly: Settings > Connectors > Add custom connector > `https://mcp.apify.com?tools=cleandata-labs/url-to-markdown`.

Never commit a file that contains a real token.
