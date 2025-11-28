# Student Guide: Model Context Protocol Workshop

Welcome to the Model Context Protocol (MCP) Workshop! This guide will help you navigate the learning journey and get the most out of each lab.

---

## 📚 Workshop Overview

### What You'll Learn

By the end of this workshop, you will:
- Understand the Model Context Protocol architecture and components
- Connect to and use public MCP servers with AI applications
- Build custom MCP servers with tools, resources, and prompts
- Create a production-ready document assistant using advanced MCP patterns

### Time Commitment

| Session | Duration | Labs Covered |
|---------|----------|--------------|
| Session 1 | 3 hours | Labs 1 & 2 |
| Session 2 | 3 hours | Labs 3 & 4 |
| **Total** | **6 hours** | **4 Labs** |

---

## 🗺️ Learning Path

```
┌──────────────────────────────────────────────────────────────────┐
│                    MCP WORKSHOP LEARNING PATH                     │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  SESSION 1: MCP Foundations (3 hours)                           │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │   Lab 1 (60 min)    │    │   Lab 2 (90 min)    │            │
│  │  Public MCP Servers │ ─→ │  First MCP Server   │            │
│  │  • Client setup     │    │  • FastMCP basics   │            │
│  │  • Server discovery │    │  • Tool creation    │            │
│  │  • Tool invocation  │    │  • Resource serving │            │
│  └─────────────────────┘    └─────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  SESSION 2: Advanced MCP (3 hours)                              │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │   Lab 3 (60 min)    │    │   Lab 4 (120 min)   │            │
│  │  Advanced Patterns  │ ─→ │  Capstone Project   │            │
│  │  • Complex tools    │    │  • Document server  │            │
│  │  • Resources        │    │  • Full integration │            │
│  │  • Prompt templates │    │  • Production code  │            │
│  └─────────────────────┘    └─────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Lab-by-Lab Walkthrough

### Lab 1: Using Public MCP Servers (60 minutes)

**Learning Objectives:**
- Understand the MCP client-server architecture
- Connect to public/community MCP servers
- Invoke tools and consume resources

**Key Concepts:**
- MCP transports (stdio, SSE)
- Tool schemas and invocation
- Server discovery and configuration

**Exercises:**
1. Configure MCP client connection
2. Discover available tools
3. Invoke tools with parameters
4. Handle tool responses

**Tips for Success:**
- Read the MCP specification overview first
- Pay attention to transport configuration
- Understand the difference between tools and resources

---

### Lab 2: Your First MCP Server (90 minutes)

**Learning Objectives:**
- Build a custom MCP server using FastMCP
- Implement tools with typed parameters
- Serve static and dynamic resources

**Key Concepts:**
- FastMCP framework basics
- Tool decorators and schemas
- Resource URIs and MIME types

**Exercises:**
1. Set up FastMCP project structure
2. Create text utility tools
3. Add resources for configuration
4. Test with MCP Inspector

**Tips for Success:**
- Start with the simplest tool possible
- Use type hints for automatic schema generation
- Test incrementally with the MCP Inspector

---

### Lab 3: Advanced Tools and Resources (60 minutes)

**Learning Objectives:**
- Create tools with complex parameter schemas
- Implement dynamic resources with templates
- Build reusable prompt templates

**Key Concepts:**
- Nested parameter schemas
- Resource templates with URI patterns
- Prompt template composition

**Exercises:**
1. Build tools with complex input types
2. Create parameterized resources
3. Design prompt templates
4. Chain operations together

**Tips for Success:**
- Plan your schema before implementation
- Use Pydantic models for complex types
- Test edge cases with unusual inputs

---

### Lab 4: Capstone - Document Assistant (120 minutes)

**Learning Objectives:**
- Design a complete MCP server architecture
- Implement document processing tools
- Create a production-ready solution

**Key Concepts:**
- Server architecture design
- Document chunking and search
- Error handling and validation

**Exercises:**
1. Design your server architecture
2. Implement core document tools
3. Add search functionality
4. Create client integration

**Tips for Success:**
- Review the solution architecture first
- Build incrementally, testing each component
- Focus on error handling for robustness

---

## 📖 MCP Concepts Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - A protocol for connecting AI models to external tools and data |
| **Tool** | A function that an AI can invoke to perform actions or retrieve information |
| **Resource** | Static or dynamic data that can be read by an AI client |
| **Prompt** | A template for common interaction patterns |
| **Transport** | The communication layer (stdio, SSE, HTTP) |
| **FastMCP** | A Python framework for building MCP servers quickly |
| **Server** | A process that exposes tools, resources, and prompts via MCP |
| **Client** | An application (like Claude Desktop) that connects to MCP servers |
| **Schema** | The JSON Schema defining tool parameters |
| **URI** | The identifier for a resource (e.g., `resource://config/settings`) |

---

## 💰 API Cost Estimates

This workshop uses AI APIs. Here are estimated costs per lab:

| Lab | API Calls | Estimated Cost |
|-----|-----------|----------------|
| Lab 1 | 5-10 tool calls | $0.01 - $0.05 |
| Lab 2 | Minimal (local testing) | $0.00 - $0.02 |
| Lab 3 | 10-15 tool calls | $0.02 - $0.10 |
| Lab 4 | 20-30 tool calls | $0.10 - $0.30 |
| **Total Workshop** | ~50-60 calls | **$0.15 - $0.50** |

**Cost Optimization Tips:**
- Use short test inputs during development
- Leverage MCP Inspector for local testing (no API costs)
- Complete exercises before running full integrations

---

## ⚠️ Common Pitfalls & Solutions

### Connection Issues

**Problem:** MCP server won't connect  
**Solution:** Check that the transport is configured correctly and the server process is running

**Problem:** "Tool not found" errors  
**Solution:** Verify tool names match exactly (case-sensitive)

### Development Issues

**Problem:** Type errors in tool parameters  
**Solution:** Ensure type hints match expected schema types

**Problem:** Resource not loading  
**Solution:** Check URI format and ensure resource is registered

### Runtime Issues

**Problem:** Server crashes on tool invocation  
**Solution:** Add try/except blocks and return proper error responses

**Problem:** Slow response times  
**Solution:** Check for blocking I/O operations; use async where appropriate

---

## 🛠️ Development Environment

### Required Software

- Python 3.10 or higher
- pip (Python package manager)
- VS Code or similar editor
- Terminal access

### Required Packages

```bash
pip install -r requirements.txt
```

Key dependencies:
- `mcp[cli]>=1.0.0` - MCP SDK with CLI tools
- `openai>=1.0.0` - OpenAI API client
- `anthropic>=0.18.0` - Anthropic API client
- `pydantic>=2.0.0` - Data validation

### Environment Variables

Create a `.env` file with:
```bash
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

### Verify Setup

```bash
python check_environment.py
```

---

## 📁 Repository Structure

```
MCP-Workshop/
├── Labs/
│   ├── Session_1/           # Labs 1 & 2
│   │   ├── Lab_1_Using_Public_MCP_Servers.ipynb
│   │   └── Lab_2_Your_First_MCP_Server.ipynb
│   └── Session_2/           # Labs 3 & 4
│       ├── Lab_3_Advanced_Tools_and_Resources.ipynb
│       └── Lab_4_Capstone_Document_Assistant.ipynb
├── Solutions/               # Reference implementations
├── Slides/                  # Session presentations
├── Supporting_Materials/    # This guide and more
└── utils/                   # Shared utilities
```

---

## 🎯 Success Checklist

### Lab 1 Completion
- [ ] Connected to a public MCP server
- [ ] Successfully invoked a tool
- [ ] Retrieved a resource
- [ ] Understood transport configuration

### Lab 2 Completion
- [ ] Created a FastMCP server
- [ ] Implemented at least 2 tools
- [ ] Added at least 1 resource
- [ ] Tested with MCP Inspector

### Lab 3 Completion
- [ ] Built tools with complex schemas
- [ ] Created dynamic resources
- [ ] Designed prompt templates
- [ ] Chained multiple operations

### Lab 4 Completion
- [ ] Designed server architecture
- [ ] Implemented document tools
- [ ] Added search functionality
- [ ] Integrated with client application

---

## 🆘 Getting Help

1. **Check the slides** - Session slides contain helpful diagrams and explanations
2. **Review solutions** - Reference implementations are in the `Solutions/` directory
3. **Ask instructors** - Raise your hand or use the chat feature
4. **MCP Documentation** - https://modelcontextprotocol.io/

---

## 🚀 Next Steps After the Workshop

1. **Explore more MCP servers** - Check the MCP server directory
2. **Build your own server** - Apply patterns from Lab 4
3. **Integrate with Claude Desktop** - Configure your server in Claude
4. **Join the community** - Contribute to MCP ecosystem

---

Good luck with your MCP journey! 🎉
