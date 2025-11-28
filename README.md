# Model Context Protocol Workshop

Welcome to the Model Context Protocol (MCP) Workshop! This 6-hour intensive workshop teaches you how to build, use, and evaluate MCP servers - the emerging standard for connecting AI applications to external tools and data sources.

## Workshop Overview

**Duration:** 6 hours (2 sessions × 3 hours)
**Format:** ~80% hands-on labs, ~20% lecture
**Prerequisites:** Python experience (1-3 years), familiarity with LLMs and APIs

### What You'll Learn

- Understand MCP architecture: servers, clients, hosts, and transports
- Use and evaluate publicly available MCP servers
- Build custom MCP servers using FastMCP (Python SDK)
- Implement tools, resources, and prompts
- Connect to MCP servers programmatically from your own applications
- Apply security best practices when evaluating third-party MCP servers

### What You'll Build

By the end of this workshop, you will have built a fully functional **Document Assistant MCP Server** with:
- Search and retrieval tools
- Document resources with URI patterns
- Reusable prompt templates
- Production-ready error handling

---

## Agenda

### Session 1: Foundations (3 hours)

| Time | Activity | Description |
|------|----------|-------------|
| 0:00-0:30 | Introduction to MCP | Architecture, concepts, comparison to REST APIs |
| 0:30-1:15 | **Lab 1: Using Public MCP Servers** | Configure VS Code + GitHub Copilot with MCP servers |
| 1:15-1:30 | Break | - |
| 1:30-2:00 | MCP Security & Best Practices | Evaluating servers, risks, trust boundaries |
| 2:00-2:45 | **Lab 2: Your First MCP Server** | Build a server with FastMCP decorators |
| 2:45-3:00 | Wrap-up & Q&A | Review, preview Session 2 |

### Session 2: Advanced (3 hours)

| Time | Activity | Description |
|------|----------|-------------|
| 0:00-0:30 | Advanced Tools & Resources | Async tools, resources, URI patterns |
| 0:30-1:15 | **Lab 3: Advanced Tools & Resources** | Build async tools, add resources, MCP client SDK |
| 1:15-1:30 | Break | - |
| 1:30-2:00 | Prompts & Production | MCP prompts, transport modes, deployment |
| 2:00-2:45 | **Lab 4: Capstone** | Build the Document Assistant MCP Server |
| 2:45-3:00 | Demo & Wrap-up | Participants demo their servers |

---

## Repository Structure

```
MCP-Workshop/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .env.example                   # API key template
├── utils/                         # Shared utilities
├── Labs/
│   ├── Session_1/
│   │   ├── README_Session_1.md    # Session 1 guide
│   │   ├── Lab_1_Using_Public_MCP_Servers.ipynb
│   │   ├── Lab_2_Your_First_MCP_Server.ipynb
│   │   └── assets/
│   └── Session_2/
│       ├── README_Session_2.md    # Session 2 guide
│       ├── Lab_3_Advanced_Tools_and_Resources.ipynb
│       ├── Lab_4_Capstone_Document_Assistant.ipynb
│       └── assets/
├── Solutions/                     # Reference implementations
├── Slides/                        # Presentation decks
└── Supporting_Materials/
    └── Environment_Setup_Guide.md
```

---

## Getting Started

### 1. Prerequisites

- **Python 3.10+** (required for MCP SDK)
- **VS Code** with GitHub Copilot extension
- **Git** for version control
- **OpenAI API Key** (for LLM interactions)

### 2. Clone the Repository

```bash
git clone <repository-url>
cd MCP-Workshop
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure API Keys

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-...
```

### 6. Verify Installation

```bash
# Test MCP CLI is installed
mcp --version

# Run the validation script (optional)
python -c "from utils import setup_llm_client; print('Setup OK')"
```

---

## Labs Overview

### Lab 1: Using Public MCP Servers
Learn to discover, install, and use publicly available MCP servers with VS Code and GitHub Copilot. Evaluate server quality and security considerations.

### Lab 2: Your First MCP Server
Build your first MCP server using FastMCP. Create tools with the `@mcp.tool()` decorator, run with `mcp dev`, and test with MCP Inspector.

### Lab 3: Advanced Tools & Resources
Implement async tools with progress reporting, expose data as resources with URI patterns, and learn to connect to MCP servers programmatically from Python code.

### Lab 4: Capstone - Document Assistant
Build a complete MCP server that serves as a document assistant with search tools, document resources, and analysis prompts.

---

## Key Resources

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [FastMCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [VS Code MCP Extension Guide](https://code.visualstudio.com/docs/copilot/copilot-extensibility-overview)

---

## Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'mcp'`
- **Solution:** Ensure your virtual environment is activated and run `pip install "mcp[cli]"`

**Issue:** MCP server won't start
- **Solution:** Check that you're using Python 3.10+ with `python --version`

**Issue:** VS Code doesn't recognize MCP server
- **Solution:** Restart VS Code after configuring MCP in settings.json

See `Supporting_Materials/Environment_Setup_Guide.md` for detailed troubleshooting.

---

## License

These materials are licensed for workshop use. Contact your program coordinator for redistribution rights.
