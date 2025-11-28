# MCP Workshop Environment Setup Guide

This guide helps you set up your development environment for the MCP Workshop.

## Prerequisites

- **Python 3.10+**
- **VS Code** with GitHub Copilot extension
- **Git** for version control
- **API Keys** (see below)

---

## Step 1: Install Python

### macOS
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

### Windows
1. Download from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify in PowerShell: `python --version`

### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv

# Verify
python3 --version
```

---

## Step 2: Clone the Repository

```bash
git clone <repository-url>
cd MCP-Workshop
```

---

## Step 3: Create Virtual Environment

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the start of your terminal prompt.

---

## Step 4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### Verify Installation
```bash
# Check MCP CLI
mcp --version

# Check Python packages
python -c "from mcp.server.fastmcp import FastMCP; print('FastMCP OK')"
python -c "from openai import OpenAI; print('OpenAI OK')"
python -c "from anthropic import Anthropic; print('Anthropic OK')"
```

---

## Step 5: Configure API Keys

### Create .env file
```bash
cp .env.example .env
```

### Edit .env with your keys
```env
# Required: OpenAI API Key
OPENAI_API_KEY=sk-...

# Optional: Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-...
```

### Getting API Keys

#### OpenAI
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign in or create account
3. Navigate to API Keys
4. Create new secret key

#### Anthropic (Optional)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in or create account
3. Navigate to API Keys
4. Create new key

---

## Step 6: Configure VS Code

### Install Required Extensions
1. Open VS Code
2. Go to Extensions (Cmd/Ctrl+Shift+X)
3. Install:
   - **GitHub Copilot**
   - **GitHub Copilot Chat**
   - **Python**
   - **Jupyter**

### Enable MCP in VS Code
1. Open VS Code Settings (Cmd/Ctrl+,)
2. Search for "MCP"
3. Find "Github > Copilot > Chat > Experimental > Mcp"
4. Enable it

### Add MCP Server Configuration
1. Open Command Palette (Cmd/Ctrl+Shift+P)
2. Type "Preferences: Open User Settings (JSON)"
3. Add your MCP server configuration:

```json
{
  "github.copilot.chat.experimental.mcp.servers": {
    "my-server": {
      "command": "python",
      "args": ["/full/path/to/your/server.py"]
    }
  }
}
```

---

## Step 7: Test Your Setup

### Test MCP Inspector
```bash
cd Labs/Session_1

# Create a test server
cat > test_server.py << 'EOF'
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Test Server")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
EOF

# Run with MCP Inspector
mcp dev test_server.py
```

The MCP Inspector should open in your browser.

### Test VS Code Integration
1. Restart VS Code after adding server config
2. Open GitHub Copilot Chat
3. You should see your MCP server in the list

---

## Troubleshooting

### "mcp: command not found"
```bash
# Make sure pip installed the CLI
pip install mcp[cli]

# Check if it's in PATH
which mcp  # macOS/Linux
where mcp  # Windows
```

### Virtual environment not activating
```bash
# Make sure you're in the project directory
cd MCP-Workshop

# Try creating fresh venv
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
```

### Import errors
```bash
# Reinstall dependencies
pip uninstall mcp -y
pip install -r requirements.txt
```

### VS Code not showing MCP servers
1. Check that the path in settings.json is correct
2. Restart VS Code completely
3. Check Output panel for errors (View > Output > GitHub Copilot Chat)

### API key errors
```bash
# Verify keys are loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:10] + '...')"
```

---

## Quick Reference

### Activate Environment
```bash
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\Activate.ps1  # Windows
```

### Run MCP Server
```bash
mcp dev server.py  # With Inspector
python server.py   # Direct
```

### Check Installed Packages
```bash
pip list | grep mcp
```

---

## Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Make sure virtual environment is activated
4. Ask your instructor for assistance
