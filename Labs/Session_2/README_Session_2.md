# Session 2: Advanced MCP

## Overview

- **Synopsis:** In this session, you'll master advanced MCP concepts including async tools with progress reporting, resources for exposing data, prompts for reusable templates, and connecting to MCP servers programmatically. You'll apply everything to build a complete Document Assistant server.
- **Core Question:** How do we build production-ready MCP servers and integrate them into our applications?
- **Key Artifacts Produced:**
  - Advanced MCP server with async tools and resources
  - MCP client code for programmatic access
  - Complete Document Assistant MCP server (capstone)

## Learning Objectives

By the end of this session, you will be able to:

- Implement async tools with progress reporting
- Expose data through MCP resources with URI patterns
- Create reusable prompt templates
- Connect to MCP servers programmatically as a client
- Build a complete, production-ready MCP server

## Agenda

| Time | Activity | Type |
|------|----------|------|
| 0:00-0:30 | Advanced Tools & Resources | Lecture |
| 0:30-1:15 | Lab 3: Advanced Tools & Resources | Hands-on |
| 1:15-1:30 | Break | - |
| 1:30-2:00 | Prompts & Production | Lecture |
| 2:00-2:45 | Lab 4: Capstone - Document Assistant | Hands-on |
| 2:45-3:00 | Demo & Wrap-up | Presentation |

---

## Prerequisites & Setup

Ensure you've completed Session 1 and have:
- FastMCP installed and working
- Successfully tested servers with MCP Inspector
- VS Code configured with MCP support

---

## Core Concepts

### Async Tools

For long-running operations, use async tools with progress reporting:

```python
@mcp.tool()
async def long_operation(query: str, ctx: Context) -> str:
    \"\"\"A tool that takes time and reports progress.\"\"\"
    await ctx.report_progress(0, 100, \"Starting...\")
    # ... do work ...
    await ctx.report_progress(50, 100, \"Halfway there...\")
    # ... more work ...
    await ctx.report_progress(100, 100, \"Complete!\")
    return result
```

### MCP Resources

Resources expose read-only data through URI patterns:

```python
@mcp.resource(\"file://documents/{name}\")
def get_document(name: str) -> str:
    \"\"\"Read a document by name.\"\"\"
    return documents[name]
```

Resources are like GET endpoints - they provide data without side effects.

### MCP Prompts

Prompts define reusable templates with parameters:

```python
@mcp.prompt()
def analyze_prompt(topic: str) -> str:
    \"\"\"Generate an analysis prompt for a topic.\"\"\"
    return f\"Please analyze the following topic: {topic}\"
```

### MCP Client SDK

Connect to MCP servers programmatically:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        result = await session.call_tool(\"tool_name\", {\"arg\": \"value\"})
```

---

## Lab Instructions

### Lab 3: Advanced Tools & Resources

**Goal:** Build an MCP server with async tools, resources, and learn to connect as a client.

**Notebook:** `Lab_3_Advanced_Tools_and_Resources.ipynb`

**What You'll Do:**
1. Create async tools with progress reporting
2. Implement resources with URI patterns
3. Add error handling and validation
4. Write MCP client code to connect to servers programmatically

---

### Lab 4: Capstone - Document Assistant

**Goal:** Build a complete MCP server that serves as a document assistant.

**Notebook:** `Lab_4_Capstone_Document_Assistant.ipynb`

**What You'll Do:**
1. Design a document management system
2. Implement search and retrieval tools
3. Create document resources
4. Add analysis prompts
5. Test the complete system

**Final Server Features:**
- `search_documents(query)`: Search across documents
- `get_document_summary(doc_id)`: Get document summary
- `analyze_document(doc_id, aspect)`: Analyze specific aspects
- Resource: `doc://{doc_id}` for document access
- Prompt: Analysis templates for different document types

---

## Production Considerations

### Transport Modes

MCP supports multiple transport mechanisms:

| Transport | Use Case |
|-----------|----------|
| **stdio** | Local development, CLI tools |
| **SSE** | Web applications, real-time updates |
| **HTTP** | REST-style integration |

### Error Handling

Always handle errors gracefully:

```python
@mcp.tool()
def risky_operation(data: str) -> str:
    try:
        result = process(data)
        return result
    except ValidationError as e:
        raise McpError(f\"Invalid data: {e}\")
    except Exception as e:
        raise McpError(f\"Operation failed: {e}\")
```

### Security Best Practices

1. **Validate inputs**: Never trust user input
2. **Limit access**: Only expose necessary files/data
3. **Log operations**: Track tool usage for auditing
4. **Handle secrets**: Use environment variables, not hardcoded values

---

## Troubleshooting

### Common Issues

**Issue:** Async tool not working
- **Solution:** Ensure you're using `async def` and `await`

**Issue:** Resource URI not matching
- **Solution:** Check URI pattern syntax - use `{param}` for variables

**Issue:** MCP client connection fails
- **Solution:** Verify server is running and using correct transport

**Issue:** Progress not showing
- **Solution:** Ensure `Context` parameter is included in tool signature

---

## Key Takeaways

- Async tools enable long-running operations with user feedback
- Resources provide a clean way to expose read-only data
- Prompts create reusable, parameterized templates
- The MCP Client SDK enables programmatic server access
- Good error handling is essential for production servers

---

## Workshop Complete!

Congratulations on completing the MCP Workshop! You've learned:

1. **Session 1**: MCP fundamentals, public servers, basic server building
2. **Session 2**: Advanced patterns, resources, prompts, client SDK, capstone project

### Next Steps

- Explore the [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- Build MCP servers for your own use cases
- Contribute to the MCP ecosystem
- Integrate MCP into your applications
