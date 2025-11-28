"""
Lab 4 Solution: Complete Document Assistant MCP Server

This is the full implementation including all extension challenges:
- Document creation
- Tag support
- Version history
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Configuration
DOCUMENTS_DIR = Path(__file__).parent / "documents"
VERSIONS_DIR = DOCUMENTS_DIR / ".versions"
TAGS_FILE = DOCUMENTS_DIR / ".tags.json"

# Ensure directories exist
DOCUMENTS_DIR.mkdir(exist_ok=True)
VERSIONS_DIR.mkdir(exist_ok=True)

# Create the MCP server
mcp = FastMCP(
    "Document Assistant",
    description="A complete MCP server for document management and analysis"
)

# Document storage
document_cache = {}
tags_cache = {}


def load_documents():
    """Load all documents from the documents directory."""
    global document_cache
    document_cache = {}

    if not DOCUMENTS_DIR.exists():
        return

    for filepath in DOCUMENTS_DIR.glob("*.md"):
        doc_id = filepath.stem
        stat = filepath.stat()

        document_cache[doc_id] = {
            "id": doc_id,
            "filename": filepath.name,
            "path": str(filepath),
            "content": filepath.read_text(),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }


def load_tags():
    """Load tags from the tags file."""
    global tags_cache
    if TAGS_FILE.exists():
        tags_cache = json.loads(TAGS_FILE.read_text())
    else:
        tags_cache = {}


def save_tags():
    """Save tags to the tags file."""
    TAGS_FILE.write_text(json.dumps(tags_cache, indent=2))


# Load data at startup
load_documents()
load_tags()


# ============ CORE TOOLS ============


@mcp.tool()
def list_documents() -> str:
    """List all available documents with their metadata.

    Returns:
        A formatted list of all documents with ID, filename, size, and modification date.
    """
    if not document_cache:
        return "No documents found."

    lines = ["Available Documents:", "=" * 50]

    for doc_id, doc in sorted(document_cache.items()):
        doc_tags = tags_cache.get(doc_id, [])
        tag_str = f" [Tags: {', '.join(doc_tags)}]" if doc_tags else ""

        lines.append(f"\nID: {doc_id}{tag_str}")
        lines.append(f"  Filename: {doc['filename']}")
        lines.append(f"  Size: {doc['size']} bytes")
        lines.append(f"  Modified: {doc['modified']}")

    return "\n".join(lines)


@mcp.tool()
def search_documents(query: str, case_sensitive: bool = False) -> str:
    """Search for documents containing the specified text.

    Args:
        query: The text to search for in document contents
        case_sensitive: Whether the search should be case-sensitive (default: False)

    Returns:
        A list of matching documents with excerpts showing where the query was found.
    """
    if not query.strip():
        return "Error: Please provide a search query."

    results = []
    flags = 0 if case_sensitive else re.IGNORECASE

    for doc_id, doc in document_cache.items():
        content = doc["content"]
        matches = list(re.finditer(re.escape(query), content, flags))

        if matches:
            first_match = matches[0]
            start = max(0, first_match.start() - 50)
            end = min(len(content), first_match.end() + 50)
            excerpt = content[start:end].replace("\n", " ")

            if start > 0:
                excerpt = "..." + excerpt
            if end < len(content):
                excerpt = excerpt + "..."

            results.append({
                "doc_id": doc_id,
                "filename": doc["filename"],
                "match_count": len(matches),
                "excerpt": excerpt
            })

    if not results:
        return f"No documents found containing '{query}'."

    lines = [f"Found {len(results)} document(s) matching '{query}':", "=" * 50]
    for result in results:
        lines.append(f"\nDocument: {result['doc_id']}")
        lines.append(f"  Matches: {result['match_count']}")
        lines.append(f"  Excerpt: {result['excerpt']}")

    return "\n".join(lines)


@mcp.tool()
def get_document_stats() -> str:
    """Get statistics about the document collection.

    Returns:
        Statistics including total documents, total size, and average document size.
    """
    if not document_cache:
        return "No documents in the collection."

    total_docs = len(document_cache)
    total_size = sum(doc["size"] for doc in document_cache.values())
    total_words = sum(len(doc["content"].split()) for doc in document_cache.values())
    total_tags = sum(len(tags) for tags in tags_cache.values())
    unique_tags = len(set(tag for tags in tags_cache.values() for tag in tags))

    return f"""Document Collection Statistics:
{'=' * 40}
Total Documents: {total_docs}
Total Size: {total_size:,} bytes
Average Size: {total_size // total_docs:,} bytes
Total Words: {total_words:,}
Average Words per Document: {total_words // total_docs:,}
Total Tags Applied: {total_tags}
Unique Tags: {unique_tags}
"""


# ============ DOCUMENT CREATION (Challenge 1) ============


@mcp.tool()
def create_document(doc_id: str, content: str, overwrite: bool = False) -> str:
    """Create a new document in the collection.

    Args:
        doc_id: The identifier for the new document (will be used as filename)
        content: The content of the document
        overwrite: Whether to overwrite if document exists (default: False)

    Returns:
        Success message or error
    """
    # Validate doc_id
    if not doc_id or not re.match(r'^[a-zA-Z0-9_-]+$', doc_id):
        return "Error: doc_id must contain only letters, numbers, underscores, and hyphens."

    filepath = DOCUMENTS_DIR / f"{doc_id}.md"

    # Check if exists
    if filepath.exists() and not overwrite:
        return f"Error: Document '{doc_id}' already exists. Use overwrite=True to replace it."

    # If overwriting, save version first
    if filepath.exists() and overwrite:
        _save_version(doc_id)

    # Write the file
    filepath.write_text(content)

    # Reload cache
    load_documents()

    return f"Successfully created document '{doc_id}' ({len(content)} characters)"


@mcp.tool()
def delete_document(doc_id: str, confirm: bool = False) -> str:
    """Delete a document from the collection.

    Args:
        doc_id: The document to delete
        confirm: Must be True to actually delete

    Returns:
        Success message or error
    """
    if doc_id not in document_cache:
        return f"Error: Document '{doc_id}' not found."

    if not confirm:
        return f"Warning: This will delete '{doc_id}'. Call again with confirm=True to proceed."

    # Save version before deleting
    _save_version(doc_id)

    # Delete file
    filepath = DOCUMENTS_DIR / f"{doc_id}.md"
    filepath.unlink()

    # Remove tags
    if doc_id in tags_cache:
        del tags_cache[doc_id]
        save_tags()

    # Reload cache
    load_documents()

    return f"Successfully deleted document '{doc_id}'"


# ============ TAG SUPPORT (Challenge 2) ============


@mcp.tool()
def add_tag(doc_id: str, tag: str) -> str:
    """Add a tag to a document.

    Args:
        doc_id: The document to tag
        tag: The tag to add

    Returns:
        Success message or error
    """
    if doc_id not in document_cache:
        return f"Error: Document '{doc_id}' not found."

    tag = tag.lower().strip()
    if not tag:
        return "Error: Tag cannot be empty."

    if doc_id not in tags_cache:
        tags_cache[doc_id] = []

    if tag in tags_cache[doc_id]:
        return f"Tag '{tag}' already exists on document '{doc_id}'."

    tags_cache[doc_id].append(tag)
    save_tags()

    return f"Added tag '{tag}' to document '{doc_id}'"


@mcp.tool()
def remove_tag(doc_id: str, tag: str) -> str:
    """Remove a tag from a document.

    Args:
        doc_id: The document to remove tag from
        tag: The tag to remove

    Returns:
        Success message or error
    """
    if doc_id not in document_cache:
        return f"Error: Document '{doc_id}' not found."

    tag = tag.lower().strip()

    if doc_id not in tags_cache or tag not in tags_cache[doc_id]:
        return f"Tag '{tag}' not found on document '{doc_id}'."

    tags_cache[doc_id].remove(tag)
    save_tags()

    return f"Removed tag '{tag}' from document '{doc_id}'"


@mcp.tool()
def search_by_tag(tag: str) -> str:
    """Find all documents with a specific tag.

    Args:
        tag: The tag to search for

    Returns:
        List of documents with the specified tag
    """
    tag = tag.lower().strip()
    matching_docs = []

    for doc_id, doc_tags in tags_cache.items():
        if tag in doc_tags:
            matching_docs.append(doc_id)

    if not matching_docs:
        return f"No documents found with tag '{tag}'."

    lines = [f"Documents with tag '{tag}':", "=" * 40]
    for doc_id in matching_docs:
        if doc_id in document_cache:
            doc = document_cache[doc_id]
            lines.append(f"\n- {doc_id}")
            lines.append(f"  Size: {doc['size']} bytes")
            lines.append(f"  All tags: {', '.join(tags_cache.get(doc_id, []))}")

    return "\n".join(lines)


@mcp.tool()
def list_tags() -> str:
    """List all tags and their document counts.

    Returns:
        List of all tags with counts
    """
    tag_counts = {}
    for doc_tags in tags_cache.values():
        for tag in doc_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    if not tag_counts:
        return "No tags defined."

    lines = ["All Tags:", "=" * 40]
    for tag, count in sorted(tag_counts.items()):
        lines.append(f"  {tag}: {count} document(s)")

    return "\n".join(lines)


# ============ VERSION HISTORY (Challenge 3) ============


def _save_version(doc_id: str):
    """Save current version of a document."""
    if doc_id not in document_cache:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_file = VERSIONS_DIR / f"{doc_id}_{timestamp}.md"
    version_file.write_text(document_cache[doc_id]["content"])


@mcp.tool()
def update_document(doc_id: str, new_content: str) -> str:
    """Update a document, saving the previous version.

    Args:
        doc_id: The document to update
        new_content: The new content

    Returns:
        Success message or error
    """
    if doc_id not in document_cache:
        return f"Error: Document '{doc_id}' not found."

    # Save current version
    _save_version(doc_id)

    # Write new content
    filepath = DOCUMENTS_DIR / f"{doc_id}.md"
    filepath.write_text(new_content)

    # Reload cache
    load_documents()

    return f"Updated document '{doc_id}'. Previous version saved."


@mcp.tool()
def list_versions(doc_id: str) -> str:
    """List all versions of a document.

    Args:
        doc_id: The document to list versions for

    Returns:
        List of all versions with timestamps
    """
    versions = list(VERSIONS_DIR.glob(f"{doc_id}_*.md"))

    if not versions:
        return f"No previous versions found for '{doc_id}'."

    lines = [f"Versions of '{doc_id}':", "=" * 40]

    for version_path in sorted(versions, reverse=True):
        # Extract timestamp from filename
        timestamp_str = version_path.stem.replace(f"{doc_id}_", "")
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            formatted_time = timestamp_str

        stat = version_path.stat()
        lines.append(f"\n  Version: {timestamp_str}")
        lines.append(f"    Date: {formatted_time}")
        lines.append(f"    Size: {stat.st_size} bytes")

    return "\n".join(lines)


@mcp.tool()
def restore_version(doc_id: str, version_id: str) -> str:
    """Restore a previous version of a document.

    Args:
        doc_id: The document to restore
        version_id: The version timestamp (e.g., "20240315_143022")

    Returns:
        Success message or error
    """
    version_path = VERSIONS_DIR / f"{doc_id}_{version_id}.md"

    if not version_path.exists():
        return f"Error: Version '{version_id}' not found for document '{doc_id}'."

    # Save current as a version first
    if doc_id in document_cache:
        _save_version(doc_id)

    # Restore the old version
    content = version_path.read_text()
    filepath = DOCUMENTS_DIR / f"{doc_id}.md"
    filepath.write_text(content)

    # Reload cache
    load_documents()

    return f"Restored document '{doc_id}' to version '{version_id}'"


# ============ RESOURCES ============


@mcp.resource("doc://{doc_id}")
def get_document(doc_id: str) -> str:
    """Get the full content of a specific document."""
    if doc_id not in document_cache:
        return f"Error: Document '{doc_id}' not found."
    return document_cache[doc_id]["content"]


@mcp.resource("docs://catalog")
def get_catalog() -> str:
    """Get the full document catalog as JSON."""
    catalog = []
    for doc_id, doc in document_cache.items():
        catalog.append({
            "id": doc["id"],
            "filename": doc["filename"],
            "size": doc["size"],
            "modified": doc["modified"],
            "word_count": len(doc["content"].split()),
            "tags": tags_cache.get(doc_id, [])
        })
    return json.dumps(catalog, indent=2)


@mcp.resource("doc://{doc_id}/metadata")
def get_document_metadata(doc_id: str) -> str:
    """Get metadata for a specific document."""
    if doc_id not in document_cache:
        return json.dumps({"error": f"Document '{doc_id}' not found."})

    doc = document_cache[doc_id]
    metadata = {
        "id": doc["id"],
        "filename": doc["filename"],
        "size": doc["size"],
        "modified": doc["modified"],
        "word_count": len(doc["content"].split()),
        "line_count": doc["content"].count("\n") + 1,
        "tags": tags_cache.get(doc_id, []),
        "versions": len(list(VERSIONS_DIR.glob(f"{doc_id}_*.md")))
    }
    return json.dumps(metadata, indent=2)


@mcp.resource("doc://{doc_id}/version/{version_id}")
def get_document_version(doc_id: str, version_id: str) -> str:
    """Get a specific version of a document."""
    version_path = VERSIONS_DIR / f"{doc_id}_{version_id}.md"

    if not version_path.exists():
        return f"Error: Version '{version_id}' not found for document '{doc_id}'."

    return version_path.read_text()


@mcp.resource("tags://all")
def get_all_tags() -> str:
    """Get all tags as JSON."""
    return json.dumps(tags_cache, indent=2)


# ============ PROMPTS ============


@mcp.prompt()
def summarize(doc_id: str) -> str:
    """Create a prompt to summarize a document."""
    if doc_id not in document_cache:
        return f"Error: Document '{doc_id}' not found."

    doc = document_cache[doc_id]
    tags = tags_cache.get(doc_id, [])
    tag_info = f"\nTags: {', '.join(tags)}" if tags else ""

    return f"""Please summarize the following document:

Document: {doc['filename']}{tag_info}
---
{doc['content']}
---

Provide:
1. A brief summary (2-3 sentences)
2. Key points (bullet list)
3. Any action items or next steps mentioned"""


@mcp.prompt()
def compare(doc_id_1: str, doc_id_2: str) -> str:
    """Create a prompt to compare two documents."""
    if doc_id_1 not in document_cache:
        return f"Error: Document '{doc_id_1}' not found."
    if doc_id_2 not in document_cache:
        return f"Error: Document '{doc_id_2}' not found."

    doc1 = document_cache[doc_id_1]
    doc2 = document_cache[doc_id_2]

    return f"""Please compare the following two documents:

=== Document 1: {doc1['filename']} ===
{doc1['content']}

=== Document 2: {doc2['filename']} ===
{doc2['content']}

Provide:
1. Main similarities between the documents
2. Key differences
3. How they might relate to each other
4. Any contradictions or inconsistencies"""


@mcp.prompt()
def extract_insights(doc_id: str, focus_area: str = "general") -> str:
    """Create a prompt to extract insights from a document."""
    if doc_id not in document_cache:
        return f"Error: Document '{doc_id}' not found."

    doc = document_cache[doc_id]

    focus_instructions = {
        "general": "Extract any important insights, patterns, or notable information.",
        "technical": "Focus on technical details, architecture decisions, and implementation specifics.",
        "business": "Focus on business impact, ROI, timelines, and strategic implications.",
        "security": "Focus on security considerations, risks, compliance requirements, and vulnerabilities."
    }

    instruction = focus_instructions.get(focus_area, focus_instructions["general"])

    return f"""Please analyze the following document and extract key insights:

Document: {doc['filename']}
Focus Area: {focus_area}
---
{doc['content']}
---

{instruction}

Format your response as:
1. Key Insights (numbered list)
2. Recommendations based on the document
3. Questions that should be addressed
4. Related topics to explore"""


@mcp.prompt()
def generate_questions(doc_id: str) -> str:
    """Create a prompt to generate questions about a document."""
    if doc_id not in document_cache:
        return f"Error: Document '{doc_id}' not found."

    doc = document_cache[doc_id]

    return f"""Based on the following document, generate thoughtful questions:

Document: {doc['filename']}
---
{doc['content']}
---

Generate:
1. 5 clarifying questions (things that are unclear or need more detail)
2. 5 follow-up questions (things to explore further)
3. 3 devil's advocate questions (potential issues or challenges)"""


@mcp.prompt()
def suggest_tags(doc_id: str) -> str:
    """Create a prompt to suggest tags for a document."""
    if doc_id not in document_cache:
        return f"Error: Document '{doc_id}' not found."

    doc = document_cache[doc_id]
    existing_tags = tags_cache.get(doc_id, [])

    # Get all existing tags in the system
    all_tags = set()
    for tags in tags_cache.values():
        all_tags.update(tags)

    return f"""Based on the following document, suggest appropriate tags:

Document: {doc['filename']}
Current Tags: {', '.join(existing_tags) if existing_tags else 'None'}
Existing Tags in System: {', '.join(sorted(all_tags)) if all_tags else 'None'}
---
{doc['content']}
---

Suggest:
1. 3-5 new tags that would help categorize this document
2. Prefer using existing tags when appropriate
3. Keep tags lowercase and use hyphens for multi-word tags
4. Explain why each tag is relevant"""


if __name__ == "__main__":
    mcp.run()
