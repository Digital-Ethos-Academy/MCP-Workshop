# MCP Workshop Solutions

This directory contains reference implementations for all workshop labs.

## Solution Files

### Lab 2: Text Utility Server
- **File:** `lab2_text_utility_server.py`
- **Description:** Complete implementation of the text utility server with word count, character count, reverse text, and uppercase conversion tools.

### Lab 3: Advanced MCP Server
- **File:** `lab3_advanced_server.py`
- **Description:** Demonstrates async tools with progress reporting, resources with URI templates, and prompts.

### Lab 4: Document Assistant (Complete)
- **File:** `lab4_document_assistant_complete.py`
- **Description:** Full implementation including all extension challenges:
  - Document creation and deletion
  - Tag support (add, remove, search by tag)
  - Version history (save, list, restore versions)

## Running the Solutions

1. Navigate to the Solutions directory:
   ```bash
   cd Solutions
   ```

2. Run with MCP Inspector:
   ```bash
   mcp dev lab2_text_utility_server.py
   ```

3. Or run as a standalone server:
   ```bash
   python lab2_text_utility_server.py
   ```

## VS Code Configuration

Add to your `settings.json`:

```json
{
  "github.copilot.chat.experimental.mcp.servers": {
    "solution-server": {
      "command": "python",
      "args": ["/path/to/Solutions/lab4_document_assistant_complete.py"]
    }
  }
}
```

## Notes

- These are reference implementations - there may be multiple valid approaches
- Students are encouraged to add their own enhancements
- The solutions demonstrate best practices for:
  - Clear docstrings for tool discovery
  - Type hints for all parameters
  - Error handling for edge cases
  - Logical organization of tools, resources, and prompts
