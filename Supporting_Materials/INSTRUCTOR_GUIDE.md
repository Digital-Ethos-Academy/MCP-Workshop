# Instructor Guide: Model Context Protocol Workshop

This guide provides instructors with everything needed to deliver the MCP Workshop effectively.

---

## 📋 Workshop Overview

### Format
- **Duration:** 6 hours total (two 3-hour sessions)
- **Delivery:** Hands-on lab-based learning
- **Audience:** Developers familiar with Python and AI APIs
- **Class Size:** 10-30 students recommended

### Prerequisites for Students
- Python 3.10+ programming experience
- Basic understanding of REST APIs
- Familiarity with AI/LLM concepts
- Access to OpenAI and/or Anthropic API keys

---

## ⏱️ Detailed Timing Tables

### Session 1: MCP Foundations (3 hours)

| Time | Duration | Activity | Notes |
|------|----------|----------|-------|
| 0:00 | 15 min | Welcome & Setup | Verify environments, distribute materials |
| 0:15 | 30 min | Session 1 Slides | Cover MCP architecture, transports, concepts |
| 0:45 | 60 min | Lab 1: Public MCP Servers | Guided + independent work |
| 1:45 | 15 min | Break | Answer questions informally |
| 2:00 | 45 min | Lab 2: Your First MCP Server | Part 1 - Setup and first tool |
| 2:45 | 15 min | Lab 2 Continued | Part 2 - Resources and testing |

### Session 2: Advanced MCP (3 hours)

| Time | Duration | Activity | Notes |
|------|----------|----------|-------|
| 0:00 | 10 min | Session 1 Recap | Quick review of key concepts |
| 0:10 | 20 min | Session 2 Slides | Advanced patterns, architecture |
| 0:30 | 60 min | Lab 3: Advanced Patterns | Complex tools, resources, prompts |
| 1:30 | 15 min | Break | Check student progress |
| 1:45 | 90 min | Lab 4: Capstone | Document assistant project |
| 3:15 | 15 min | Wrap-up & Q&A | Presentations, next steps |

---

## 🎯 Lab Facilitation Notes

### Lab 1: Using Public MCP Servers

**Key Teaching Points:**
1. MCP is a protocol, not a library - emphasize the abstraction
2. Transports (stdio vs SSE) are interchangeable to the application
3. Tool schemas are auto-generated from server definitions

**Common Student Issues:**
- **API key not configured:** Have students run `python check_environment.py`
- **Transport confusion:** Use the analogy of HTTP vs HTTPS - same protocol, different transport
- **Tool name mismatches:** Remind students tool names are case-sensitive

**Checkpoints:**
- [ ] All students can connect to a server
- [ ] All students can invoke a tool successfully
- [ ] Students understand the request/response cycle

---

### Lab 2: Your First MCP Server

**Key Teaching Points:**
1. FastMCP handles all protocol complexity
2. Type hints generate JSON Schema automatically
3. Decorators make tool/resource registration declarative

**Common Student Issues:**
- **Import errors:** Ensure `mcp[cli]` is installed, not just `mcp`
- **Server won't start:** Check for Python syntax errors
- **Tool not appearing:** Verify decorator is correct (`@mcp.tool()`)

**Demonstration Moments:**
- Live code a simple tool, showing the decorator pattern
- Show MCP Inspector for testing without a client
- Demonstrate how type hints become schema

**Checkpoints:**
- [ ] All students have a running server
- [ ] All students have at least one working tool
- [ ] Students can test with MCP Inspector

---

### Lab 3: Advanced Tools and Resources

**Key Teaching Points:**
1. Complex schemas enable rich tool inputs
2. Resources can be static or dynamic
3. Prompt templates encourage consistent interactions

**Common Student Issues:**
- **Pydantic validation errors:** Remind students to match types exactly
- **Resource URI confusion:** Explain the `resource://` scheme
- **Template not working:** Check parameter placeholders match

**Advanced Discussion Topics:**
- When to use tools vs resources
- Design patterns for prompt templates
- Error handling strategies

**Checkpoints:**
- [ ] Students can create tools with nested parameters
- [ ] Students understand resource templates
- [ ] Students can design prompt templates

---

### Lab 4: Capstone - Document Assistant

**Key Teaching Points:**
1. Architecture matters - plan before coding
2. Document processing requires chunking strategies
3. Search can be simple (text matching) or complex (embeddings)

**Common Student Issues:**
- **Overwhelmed by scope:** Break down into phases (see solution)
- **File handling errors:** Emphasize error handling patterns
- **Integration problems:** Test components individually first

**Scaffolding Approach:**
1. Provide architecture diagram upfront
2. Give partial implementations for struggling students
3. Share working solution at 75% mark for reference

**Checkpoints:**
- [ ] Students have documented their architecture
- [ ] Core document tools are working
- [ ] At least basic search is functional

---

## 📊 Assessment Rubric for Capstone

### Scoring Criteria (Total: 100 points)

| Criteria | Points | Excellent (100%) | Good (75%) | Needs Work (50%) |
|----------|--------|------------------|------------|------------------|
| **Architecture** | 20 | Clear, well-documented design | Reasonable structure | Ad-hoc organization |
| **Tool Implementation** | 25 | All tools work correctly | Most tools functional | Some tools incomplete |
| **Resource Handling** | 20 | Dynamic resources with templates | Static resources work | Minimal resource support |
| **Error Handling** | 15 | Comprehensive validation | Basic error handling | Crashes on bad input |
| **Code Quality** | 10 | Clean, documented, typed | Readable code | Works but messy |
| **Integration** | 10 | Full client integration | Partial integration | Tools work in isolation |

### Grading Scale
- **90-100:** Exceeds expectations - Production ready
- **75-89:** Meets expectations - Solid implementation
- **60-74:** Approaching expectations - Core functionality works
- **Below 60:** Needs additional support

---

## ❓ Common Student Questions

### Conceptual Questions

**Q: How is MCP different from a REST API?**
> MCP is a higher-level protocol designed specifically for AI model interactions. It provides structured tool schemas, type safety, and standardized patterns. REST APIs require custom integration for each service.

**Q: Can I use MCP with models other than Claude?**
> Yes! MCP is model-agnostic. The protocol works with any AI that can make structured tool calls. OpenAI's function calling, for example, maps naturally to MCP tools.

**Q: Why use FastMCP instead of the raw protocol?**
> FastMCP handles all the protocol machinery (JSON-RPC, schema generation, transport management). Writing a raw MCP server would require implementing all this yourself.

### Technical Questions

**Q: How do I debug MCP server issues?**
> Use the MCP Inspector (`mcp-inspector` CLI) to test your server without a full client. Add logging to your server code. Check transport configuration.

**Q: Can I have async tools?**
> Yes! FastMCP supports both sync and async tool implementations. Use `async def` for I/O-bound operations.

**Q: How do I handle authentication?**
> MCP itself doesn't specify authentication. For local servers (stdio), the process isolation provides security. For remote servers (SSE), implement authentication at the transport layer.

**Q: What's the difference between tools and resources?**
> Tools are actions (verbs) - they do something. Resources are data (nouns) - they provide information. Use tools for operations that have side effects or require computation. Use resources for static or parameterized data retrieval.

---

## 🛠️ Pre-Workshop Checklist

### 1 Week Before
- [ ] Verify all notebooks run without errors
- [ ] Check API quotas for class size
- [ ] Prepare backup API keys for students without them
- [ ] Test slides and projector setup

### 1 Day Before
- [ ] Clone fresh repository
- [ ] Run `python check_environment.py`
- [ ] Run `python scripts/verify_notebooks.py`
- [ ] Prepare student environment setup guide

### Day of Workshop
- [ ] Arrive 30 minutes early
- [ ] Have `Solutions/` directory ready for sharing
- [ ] Prepare troubleshooting station
- [ ] Have documentation links ready

---

## 🚑 Troubleshooting Guide

### Environment Issues

**Problem:** Python version mismatch
```bash
# Check version
python --version

# Solution: Use pyenv or conda to get Python 3.10+
pyenv install 3.10.12
pyenv local 3.10.12
```

**Problem:** Package installation failures
```bash
# Try upgrading pip first
pip install --upgrade pip

# Install with verbose output
pip install -v mcp[cli]
```

**Problem:** API keys not loading
```bash
# Verify .env file exists
ls -la .env

# Check key format (no quotes needed)
cat .env
# Should look like:
# OPENAI_API_KEY=sk-...
```

### MCP-Specific Issues

**Problem:** Server won't start
```bash
# Check for syntax errors
python -m py_compile your_server.py

# Run with verbose output
python -v your_server.py
```

**Problem:** MCP Inspector not connecting
```bash
# Verify mcp-inspector is installed
which mcp-inspector

# Try reinstalling
pip uninstall mcp-inspector
pip install mcp-inspector
```

**Problem:** Tools not appearing in client
- Verify tool is decorated with `@mcp.tool()`
- Check tool function has type hints
- Ensure server is running without errors

---

## 📚 Additional Resources for Instructors

### Official Documentation
- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Server Directory](https://github.com/modelcontextprotocol/servers)

### Teaching Resources
- Session 1 Slides: `Slides/Session_1_MCP_Foundations.html`
- Session 2 Slides: `Slides/Session_2_Advanced_MCP.html`
- Solution implementations: `Solutions/` directory

### Reference Implementations
- `Solutions/lab2_text_utility_server.py` - Basic server example
- `Solutions/lab3_advanced_server.py` - Advanced patterns
- `Solutions/lab4_document_assistant_complete.py` - Full capstone solution

---

## 📝 Post-Workshop Tasks

### Immediately After
- [ ] Collect student feedback
- [ ] Note any recurring issues
- [ ] Record questions for FAQ updates

### Within 1 Week
- [ ] Review feedback for improvements
- [ ] Update notebooks if issues found
- [ ] Share additional resources with students

### Ongoing
- [ ] Keep MCP SDK version current
- [ ] Update for protocol changes
- [ ] Add new examples as ecosystem grows

---

## 🎓 Instructor Tips

1. **Start with the "why"** - Students learn better when they understand the problem MCP solves
2. **Live code confidently** - Make mistakes deliberately to show debugging
3. **Use the MCP Inspector** - It's the fastest way to demonstrate tool behavior
4. **Encourage experimentation** - Let students try their own tool ideas
5. **Reference real servers** - Point to the MCP server directory for inspiration
6. **Pace for the room** - Check progress before moving on
7. **Leverage solutions wisely** - Share progressively, not all at once

---

Thank you for teaching the MCP Workshop! 🙏
