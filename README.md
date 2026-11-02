# sumy-function

An **Azure Functions** app that exposes a text summarization capability as an **MCP (Model Context Protocol) prompt trigger**. It uses [sumy](https://github.com/miso-belica/sumy) — a pure-Python extractive summarization library — so no external AI API or LLM is required.

## How it works

The function uses **LSA (Latent Semantic Analysis)** — one of several extractive algorithms provided by `sumy` — to select the most important sentences from a piece of text.

Key components:

| Component | Role |
|---|---|
| `azure-functions` | Hosts the function and wires up the MCP prompt trigger |
| `sumy` `PlaintextParser` | Tokenizes raw text into sentences |
| `sumy` `LsaSummarizer` | Ranks and selects the top-N sentences |
| MCP `mcp_prompt_trigger` | Exposes the summarizer as a named prompt (`code_review_checklist`) that any MCP-compatible client can invoke |

The MCP server metadata (name, version, instructions) is configured in `host.json` under the `extensions.mcp` section.

## Project structure

```
sumy-function/
├── function_app.py        # Azure Function entry point & MCP prompt trigger
├── host.json              # Azure Functions host config + MCP server settings
├── local.settings.json    # Local environment variables (not committed to source control)
├── requirements.txt       # Python dependencies
└── .vscode/
    ├── launch.json        # Debug configuration (attach to running Functions host)
    ├── settings.json      # Azure Functions VS Code extension settings
    └── tasks.json         # Pre-launch task: func host start
```

## Prerequisites

| Tool | Purpose |
|---|---|
| Python 3.9+ | Runtime |
| [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local) | Run & debug functions locally |
| [Azurite](https://learn.microsoft.com/azure/storage/common/storage-use-azurite) | **Required for local tests** — emulates Azure Storage (used by `AzureWebJobsStorage`) |
| VS Code + [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) | Optional, but recommended |

> **Note:** `local.settings.json` sets `AzureWebJobsStorage` to `UseDevelopmentStorage=true`, which means Azurite **must be running** before you start the function locally, otherwise the host will fail to start.

## Getting started

### 1. Clone the repository

```bash
git clone <repo-url>
cd sumy-function
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Azurite (required for local tests)

Install Azurite via npm if you haven't already:

```bash
npm install -g azurite
```

Then start it in a separate terminal:

```bash
azurite --silent --location .azurite --debug .azurite\debug.log
```

Alternatively, use the **Azurite** VS Code extension and click **Start Azurite** from the status bar.

### 5. Run the function locally

```bash
func start
```

The Functions host will start and register the MCP prompt endpoint. You should see output similar to:

```
Functions:
    summarizer_mcp: mcpPrompt
```

### 6. Debug in VS Code

Open the project in VS Code and press **F5** (or select *Run → Start Debugging*). The pre-launch task automatically starts the Functions host and the debugger attaches on port `9091`.

## Configuration

### `host.json` — MCP server settings

```json
"extensions": {
  "mcp": {
    "serverName": "TestServer",
    "serverVersion": "2.0.0",
    "instructions": "Some test instructions on how to use the server",
    "encryptClientState": true
  }
}
```

Edit these values to match your own server name/version before deploying.

### `local.settings.json` — local environment variables

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python"
  }
}
```

When deploying to Azure, replace `UseDevelopmentStorage=true` with your actual Azure Storage connection string (or a Managed Identity reference).

## Deploying to Azure

Use the Azure Functions VS Code extension or the CLI:

```bash
az login
func azure functionapp publish <your-function-app-name>
```

Make sure the Function App is configured with:
- **Runtime**: Python 3.9+
- **Functions runtime version**: ~4
- **App setting** `AzureWebJobsStorage` pointing to a real Azure Storage account
- **Authentication**: The app uses `AuthLevel.FUNCTION`, meaning requests must include the **system key** in the `x-functions-key` header (or `code` query parameter). System keys are managed under *Function App → App keys* in the Azure portal and are intended for extension-to-extension communication — not for end users or function-level callers.

## Available summarization algorithms

`sumy` ships with several extractive algorithms. To swap out LSA for another, change the import and instantiation in `function_app.py`:

| Algorithm | Import |
|---|---|
| LSA (current) | `from sumy.summarizers.lsa import LsaSummarizer` |
| LexRank | `from sumy.summarizers.lex_rank import LexRankSummarizer` |
| TextRank | `from sumy.summarizers.text_rank import TextRankSummarizer` |
| Luhn | `from sumy.summarizers.luhn import LuhnSummarizer` |
| KL-Sum | `from sumy.summarizers.kl import KLSummarizer` |

## License

See the individual dependency licenses for `sumy` and `azure-functions`.
