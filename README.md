<p align="center">
    <img alt="Piston Logo" src="https://github.com/engineer-man/piston/blob/master/var/docs/images/piston.svg" width=150 />
</p>

<h1 align="center">
    Piston MCP Server
</h1>

<p align="center">
    <strong><i>piston-mcp</i></strong> is an MCP server that allows LLMs to connect to and execute code using <a href="https://github.com/engineer-man/piston"><i>Piston</i></a>.
</p>

<div align="center">

[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/alvii147/piston-mcp/actions.yml?branch=main&label=GitHub%20Actions&logo=github)](https://github.com/alvii147/piston-mcp/actions) [![License](https://img.shields.io/github/license/alvii147/piston-mcp)](https://github.com/alvii147/piston-mcp/blob/main/LICENSE)

</div>

## Installation

You can try out *piston-mcp* locally without cloning it.

### :one: Install [uv](https://github.com/astral-sh/uv)

To try out *piston-mcp* you'll need to install `uv`:

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### :two: Install MCP Client

You will also need to download an MCP client to connect to *piston-mcp*, such as [Claude Desktop](https://claude.ai/download).

### :three: Update MCP Client Configuration

Update the MCP client's configuration with the following configuration to connect to *piston-mcp*:

```json
{
  "mcpServers": {
    "piston": {
      "command": "uv",
      "args": [
        "tool",
        "run",
        "--from",
        "git+https://github.com/alvii147/piston-mcp.git@main",
        "piston_mcp"
      ]
    }
  }
}
```

For Claude Desktop, the configuration file is usually in `~/Library/Application\ Support/Claude/claude_desktop_config.json` on MacOS/Linux machines, or `%APPDATA%\Claude\claude_desktop_config.json` on Windows machines.

## Usage

Once you've followed the steps above, your MCP client should successfully connect to *piston-mcp* and `piston` should show up as an available MCP server that offers the tool, `run_code`:

![Claude MCP Servers](docs/img/ClaudeMCPServers.png)

![Claude Run Code](docs/img/ClaudeRunCode.png)

Your MCP client should then be able to run code for you:

![Claude Demo](docs/img/ClaudeDemo.png)
