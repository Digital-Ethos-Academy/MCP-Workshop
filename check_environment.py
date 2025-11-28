#!/usr/bin/env python3
"""
MCP Workshop Environment Checker

Run this script to verify your environment is properly configured for the workshop.

Usage:
    python check_environment.py
"""

import sys
import os
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def print_status(name, status, message=""):
    """Print a status line."""
    icon = "✅" if status else "❌"
    msg = f" - {message}" if message else ""
    print(f"  {icon} {name}{msg}")


def check_python_version():
    """Check Python version is 3.10+."""
    version = sys.version_info
    ok = version.major == 3 and version.minor >= 10
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    return ok, version_str


def check_package(package_name, import_name=None):
    """Check if a package is installed and importable."""
    import_name = import_name or package_name
    try:
        __import__(import_name)
        return True, "installed"
    except ImportError:
        return False, "not installed"


def check_mcp_cli():
    """Check if MCP CLI is available."""
    try:
        result = subprocess.run(
            ["mcp", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip() or "available"
            return True, version
        return False, "command failed"
    except FileNotFoundError:
        return False, "not found in PATH"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, str(e)


def check_env_file():
    """Check if .env file exists."""
    env_path = Path(".env")
    if env_path.exists():
        return True, "found"
    return False, "not found (copy .env.example to .env)"


def check_api_key(key_name):
    """Check if an API key is set in environment."""
    from dotenv import load_dotenv
    load_dotenv()
    
    value = os.getenv(key_name)
    if value:
        # Show first few chars for verification
        masked = value[:8] + "..." if len(value) > 8 else "***"
        return True, f"set ({masked})"
    return False, "not set"


def check_fastmcp():
    """Check if FastMCP is importable."""
    try:
        from mcp.server.fastmcp import FastMCP
        return True, "available"
    except ImportError:
        return False, "not importable"


def main():
    """Run all environment checks."""
    print_header("MCP Workshop Environment Check")
    
    all_ok = True
    
    # Python version
    print("\n📦 Python Environment:")
    ok, msg = check_python_version()
    print_status(f"Python {msg}", ok, "3.10+ required" if not ok else "")
    all_ok = all_ok and ok
    
    # Core packages
    print("\n📚 Required Packages:")
    packages = [
        ("mcp", "mcp"),
        ("openai", "openai"),
        ("anthropic", "anthropic"),
        ("pydantic", "pydantic"),
        ("python-dotenv", "dotenv"),
        ("aiohttp", "aiohttp"),
        ("httpx", "httpx"),
    ]
    
    for pkg_name, import_name in packages:
        ok, msg = check_package(pkg_name, import_name)
        print_status(pkg_name, ok, msg)
        if pkg_name in ["mcp", "openai", "pydantic", "python-dotenv"]:
            all_ok = all_ok and ok
    
    # MCP CLI
    print("\n🔧 MCP CLI:")
    ok, msg = check_mcp_cli()
    print_status("mcp command", ok, msg)
    all_ok = all_ok and ok
    
    # FastMCP
    ok, msg = check_fastmcp()
    print_status("FastMCP", ok, msg)
    all_ok = all_ok and ok
    
    # Environment file
    print("\n🔐 Environment Configuration:")
    ok, msg = check_env_file()
    print_status(".env file", ok, msg)
    
    # API Keys
    if ok:  # Only check keys if .env exists
        ok, msg = check_api_key("OPENAI_API_KEY")
        print_status("OPENAI_API_KEY", ok, msg)
        all_ok = all_ok and ok
        
        ok, msg = check_api_key("ANTHROPIC_API_KEY")
        print_status("ANTHROPIC_API_KEY", ok, msg if ok else "optional")
    
    # Summary
    print_header("Summary")
    
    if all_ok:
        print("\n  🎉 Your environment is ready for the MCP Workshop!")
        print("\n  Next steps:")
        print("    1. Navigate to Labs/Session_1/")
        print("    2. Open Lab_1_Using_Public_MCP_Servers.ipynb")
        print("    3. Follow the instructions in the notebook")
    else:
        print("\n  ⚠️  Some issues were found. Please fix them before continuing.")
        print("\n  Common fixes:")
        print("    • pip install -r requirements.txt")
        print("    • pip install 'mcp[cli]'")
        print("    • cp .env.example .env  (then add your API keys)")
    
    print()
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
