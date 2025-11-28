# Session 1: MCP Foundations

## Overview

- **Synopsis:** In this session, you'll learn the fundamentals of the Model Context Protocol (MCP) - the emerging standard for connecting AI applications to external tools and data. You'll start by using publicly available MCP servers, learn to evaluate their security, and then build your first MCP server from scratch.
- **Core Question:** How do we safely extend AI assistants with external capabilities using a standardized protocol?
- **Key Artifacts Produced:**
  - Configured MCP servers in VS Code + GitHub Copilot
  - Your first custom MCP server with tools

## Learning Objectives

By the end of this session, you will be able to:

- Explain the MCP architecture: servers, clients, hosts, and transports
- Install and configure publicly available MCP servers
- Evaluate MCP servers for security risks and quality
- Build a basic MCP server using FastMCP and Python decorators
- Test MCP servers using the MCP Inspector

## Agenda

| Time | Activity | Type |
|------|----------|------|
| 0:00-0:30 | Introduction to MCP | Lecture |
| 0:30-1:15 | Lab 1: Using Public MCP Servers | Hands-on |
| 1:15-1:30 | Break | - |
| 1:30-2:00 | MCP Security & Best Practices | Lecture |
| 2:00-2:45 | Lab 2: Your First MCP Server | Hands-on |
| 2:45-3:00 | Wrap-up & Q&A | Discussion |

---

## Prerequisites & Setup

### Software Requirements

- VS Code with GitHub Copilot extension installed and activated
- Python 3.10+ installed
- Virtual environment activated with workshop dependencies

### Environment Setup

```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux

# Verify MCP CLI is installed
mcp --version
```

### API Keys

Your `.env` file should contain:
```env
OPENAI_API_KEY=sk-...
```

---

## Core Concepts

### What is MCP?

The **Model Context Protocol (MCP)** is an open standard that enables AI applications to connect with external data sources and tools through a unified interface. Think of it like USB-C for AI - a standardized way to plug different capabilities into any AI application.

### MCP Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        HOST                             │
│  (VS Code, Claude Desktop, Custom App)                  │
│                                                         │
│   ┌─────────────┐    ┌─────────────┐                   │
│   │   CLIENT    │    │   CLIENT    │                   │
│   └──────┬──────┘    └──────┬──────┘                   │
└──────────┼──────────────────┼───────────────────────────┘
           │                  │
           │ MCP Protocol     │ MCP Protocol
           │                  │
    ┌──────┴──────┐    ┌──────┴──────┐
    │   SERVER    │    │   SERVER    │
    │ (filesystem)│    │  (GitHub)   │
    └─────────────┘    └─────────────┘
```

**Key Components:**
- **Host**: The AI application (VS Code, Claude Desktop, custom app)
- **Client**: The component that connects to MCP servers (managed by host)
- **Server**: Exposes tools, resources, and prompts via MCP protocol
- **Transport**: Communication layer (stdio, SSE, HTTP)

### MCP Primitives

1. **Tools**: Functions the AI can call to perform actions
2. **Resources**: Read-only data the AI can access (like GET endpoints)
3. **Prompts**: Reusable prompt templates with parameters

---

## Lab Instructions

### Lab 1: Using Public MCP Servers

**Goal:** Learn to discover, install, and use publicly available MCP servers with VS Code and GitHub Copilot.

**Notebook:** `Lab_1_Using_Public_MCP_Servers.ipynb`

**What You'll Do:**
1. Explore the MCP server ecosystem
2. Configure VS Code settings for MCP
3. Install and test the filesystem MCP server
4. Install and test a web search MCP server
5. Evaluate server quality and security

**Key Concepts:**
- MCP server configuration in `settings.json`
- Server capabilities and permissions
- Testing servers before production use

**Reference Demo:** Setting up MCP in Claude Code (instructor demonstration)

---

### Lab 2: Your First MCP Server

**Goal:** Build your first MCP server using FastMCP with custom tools.

**Notebook:** `Lab_2_Your_First_MCP_Server.ipynb`

**What You'll Do:**
1. Create a new MCP server with FastMCP
2. Add tools using the `@mcp.tool()` decorator
3. Implement input validation with type hints
4. Test your server with `mcp dev` and MCP Inspector
5. Connect your server to VS Code

**Key Concepts:**
- FastMCP server creation
- Tool definition with decorators
- Type hints and docstrings for tool descriptions
- Server testing and debugging

---

## Security & Best Practices

### Evaluating Public MCP Servers

Before installing any MCP server, evaluate:

| Criteria | What to Check |
|----------|---------------|
| **Source Code** | Is it open source? Can you audit it? |
| **Author** | Reputable organization? Active maintainer? |
| **Permissions** | What does it access? Files? Network? |
| **Activity** | Recently updated? Active community? |
| **Reviews** | What do others say about it? |

### Trust Boundaries

Understand what an MCP server can access:

- **Filesystem servers**: Can read/write files in specified directories
- **API servers**: Can make network requests on your behalf
- **Database servers**: Can execute queries against your data

### Best Practices

1. **Review before installing**: Read the source code or documentation
2. **Limit permissions**: Configure minimum necessary access
3. **Use sandboxing**: Consider container isolation for untrusted servers
4. **Monitor activity**: Watch for unexpected behavior
5. **Keep updated**: Apply security patches promptly

### Red Flags

- No source code available
- Requests excessive permissions
- No documentation or unclear purpose
- Abandoned or unmaintained project
- Negative community feedback

---

## Troubleshooting

### Common Issues

**Issue:** MCP server not appearing in VS Code
- **Solution:** Restart VS Code after modifying `settings.json`

**Issue:** `mcp: command not found`
- **Solution:** Ensure `mcp[cli]` is installed: `pip install "mcp[cli]"`

**Issue:** Server starts but tools don't work
- **Solution:** Check tool docstrings - they're required for tool discovery

**Issue:** Permission denied errors
- **Solution:** Check server configuration for correct paths and permissions

---

## Key Takeaways

- MCP provides a standardized way to extend AI applications with external capabilities
- Public MCP servers should be evaluated for security before use
- FastMCP makes it easy to build custom MCP servers in Python
- Tools need clear docstrings and type hints for proper discovery
- The MCP Inspector is essential for testing and debugging

---

## What's Next

In Session 2, you'll learn:
- Advanced tool patterns (async, progress reporting)
- MCP resources for exposing data
- MCP prompts for reusable templates
- Connecting to MCP servers programmatically
- Building a complete Document Assistant server
