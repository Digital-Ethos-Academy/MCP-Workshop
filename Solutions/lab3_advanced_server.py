"""
Lab 3 Solution: Advanced MCP Server

This server demonstrates async tools with progress reporting,
resources with URI templates, and prompts.
"""

import asyncio
import json
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Context

mcp = FastMCP(
    "Advanced Demo Server",
    description="Demonstrates async tools, resources, and prompts"
)

# ============ SAMPLE DATA ============

# Document storage for resources
documents = {
    "readme": {
        "title": "Project README",
        "content": """# My Project

This is a sample project demonstrating MCP capabilities.

## Features
- Async tool execution
- Progress reporting
- Resource exposure
- Prompt templates

## Getting Started
1. Install dependencies
2. Configure your environment
3. Run the server
""",
        "created": "2024-01-15",
        "author": "Developer"
    },
    "api-docs": {
        "title": "API Documentation",
        "content": """# API Documentation

## Endpoints

### GET /users
Returns a list of all users.

### POST /users
Creates a new user.

### GET /users/{id}
Returns a specific user by ID.

## Authentication
All endpoints require Bearer token authentication.
""",
        "created": "2024-02-20",
        "author": "API Team"
    },
    "changelog": {
        "title": "Changelog",
        "content": """# Changelog

## v2.0.0 (2024-03-01)
- Major refactoring
- New async architecture
- Breaking: Changed API response format

## v1.1.0 (2024-02-15)
- Added progress reporting
- Bug fixes

## v1.0.0 (2024-01-01)
- Initial release
""",
        "created": "2024-03-01",
        "author": "Release Manager"
    }
}

# ============ ASYNC TOOLS ============


@mcp.tool()
async def process_data(items: int, ctx: Context) -> str:
    """Process a batch of items with progress reporting.

    Args:
        items: Number of items to process (1-100)
        ctx: MCP context for progress reporting

    Returns:
        Summary of processed items
    """
    if items < 1:
        return "Error: Must process at least 1 item"
    if items > 100:
        return "Error: Maximum 100 items allowed"

    results = []
    for i in range(items):
        # Simulate work
        await asyncio.sleep(0.1)

        # Report progress
        await ctx.report_progress(
            progress=i + 1,
            total=items,
            message=f"Processing item {i + 1} of {items}"
        )

        results.append(f"Item {i + 1}: processed")

    return f"Successfully processed {items} items:\n" + "\n".join(results[-5:])


@mcp.tool()
async def analyze_text(text: str, ctx: Context) -> str:
    """Analyze text with multiple analysis stages.

    Args:
        text: The text to analyze
        ctx: MCP context for progress reporting

    Returns:
        Analysis results
    """
    stages = [
        ("Tokenizing", lambda t: len(t.split())),
        ("Counting characters", lambda t: len(t)),
        ("Counting sentences", lambda t: t.count('.') + t.count('!') + t.count('?')),
        ("Calculating average word length", lambda t: sum(len(w) for w in t.split()) / max(len(t.split()), 1)),
        ("Finding unique words", lambda t: len(set(t.lower().split())))
    ]

    results = {}
    for i, (stage_name, analyzer) in enumerate(stages):
        await ctx.report_progress(
            progress=i + 1,
            total=len(stages),
            message=stage_name
        )
        await asyncio.sleep(0.2)
        results[stage_name] = analyzer(text)

    return f"""Text Analysis Results:
- Word count: {results['Tokenizing']}
- Character count: {results['Counting characters']}
- Sentence count: {results['Counting sentences']}
- Average word length: {results['Calculating average word length']:.2f}
- Unique words: {results['Finding unique words']}
"""


@mcp.tool()
async def fetch_multiple_urls(urls: list[str], ctx: Context) -> str:
    """Simulate fetching multiple URLs with progress.

    Args:
        urls: List of URLs to fetch
        ctx: MCP context for progress reporting

    Returns:
        Fetch results for each URL
    """
    results = []
    for i, url in enumerate(urls):
        await ctx.report_progress(
            progress=i + 1,
            total=len(urls),
            message=f"Fetching {url}"
        )
        # Simulate network delay
        await asyncio.sleep(0.3)
        results.append(f"  {url}: 200 OK (simulated)")

    return "Fetch Results:\n" + "\n".join(results)


# ============ RESOURCES ============


@mcp.resource("doc://{doc_id}")
def get_document(doc_id: str) -> str:
    """Get the content of a specific document.

    Args:
        doc_id: The document identifier

    Returns:
        The document content
    """
    if doc_id not in documents:
        return f"Error: Document '{doc_id}' not found. Available: {', '.join(documents.keys())}"

    doc = documents[doc_id]
    return doc["content"]


@mcp.resource("doc://{doc_id}/metadata")
def get_document_metadata(doc_id: str) -> str:
    """Get metadata for a specific document.

    Args:
        doc_id: The document identifier

    Returns:
        JSON metadata for the document
    """
    if doc_id not in documents:
        return json.dumps({"error": f"Document '{doc_id}' not found"})

    doc = documents[doc_id]
    return json.dumps({
        "id": doc_id,
        "title": doc["title"],
        "created": doc["created"],
        "author": doc["author"],
        "content_length": len(doc["content"])
    }, indent=2)


@mcp.resource("docs://index")
def get_document_index() -> str:
    """Get an index of all available documents.

    Returns:
        JSON list of all documents with their IDs and titles
    """
    index = [
        {"id": doc_id, "title": doc["title"], "created": doc["created"]}
        for doc_id, doc in documents.items()
    ]
    return json.dumps(index, indent=2)


@mcp.resource("config://settings")
def get_settings() -> str:
    """Get the current server settings.

    Returns:
        JSON configuration settings
    """
    return json.dumps({
        "version": "1.0.0",
        "max_items": 100,
        "supported_formats": ["md", "txt", "json"],
        "features": {
            "async_tools": True,
            "progress_reporting": True,
            "resources": True,
            "prompts": True
        }
    }, indent=2)


# ============ PROMPTS ============


@mcp.prompt()
def summarize_document(doc_id: str) -> str:
    """Create a prompt to summarize a document.

    Args:
        doc_id: The document to summarize
    """
    if doc_id not in documents:
        return f"Error: Document '{doc_id}' not found."

    doc = documents[doc_id]
    return f"""Please summarize the following document:

Title: {doc['title']}
Author: {doc['author']}
Created: {doc['created']}

Content:
---
{doc['content']}
---

Provide:
1. A brief summary (2-3 sentences)
2. Key points (bullet list)
3. Target audience
"""


@mcp.prompt()
def compare_documents(doc_id_1: str, doc_id_2: str) -> str:
    """Create a prompt to compare two documents.

    Args:
        doc_id_1: First document to compare
        doc_id_2: Second document to compare
    """
    if doc_id_1 not in documents:
        return f"Error: Document '{doc_id_1}' not found."
    if doc_id_2 not in documents:
        return f"Error: Document '{doc_id_2}' not found."

    doc1 = documents[doc_id_1]
    doc2 = documents[doc_id_2]

    return f"""Please compare these two documents:

=== Document 1: {doc1['title']} ===
Author: {doc1['author']}
{doc1['content']}

=== Document 2: {doc2['title']} ===
Author: {doc2['author']}
{doc2['content']}

Analyze:
1. Key similarities
2. Key differences
3. How they relate to each other
4. Which is more comprehensive
"""


@mcp.prompt()
def code_review(language: str = "python") -> str:
    """Create a prompt template for code review.

    Args:
        language: The programming language (default: python)
    """
    return f"""Please review the following {language} code:

```{language}
[INSERT CODE HERE]
```

Review criteria:
1. Code correctness
2. Error handling
3. Performance considerations
4. Code style and readability
5. Security concerns
6. Suggestions for improvement

Format your review as:
- Overall assessment (Good/Needs Work/Major Issues)
- Specific issues found (numbered list)
- Recommendations (numbered list)
"""


@mcp.prompt()
def explain_concept(topic: str, audience: str = "intermediate") -> str:
    """Create a prompt to explain a technical concept.

    Args:
        topic: The topic to explain
        audience: Target audience level (beginner/intermediate/advanced)
    """
    audience_guidance = {
        "beginner": "Use simple language, avoid jargon, include analogies",
        "intermediate": "Assume basic knowledge, include practical examples",
        "advanced": "Include technical details, edge cases, and best practices"
    }

    guidance = audience_guidance.get(audience, audience_guidance["intermediate"])

    return f"""Please explain the following concept:

Topic: {topic}
Target Audience: {audience}
Guidelines: {guidance}

Structure your explanation as:
1. What it is (definition)
2. Why it matters (importance)
3. How it works (mechanism)
4. When to use it (use cases)
5. Example (practical demonstration)
6. Common pitfalls to avoid
"""


if __name__ == "__main__":
    mcp.run()
