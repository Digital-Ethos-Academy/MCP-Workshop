#!/usr/bin/env python3
"""
Notebook Verification Script for MCP Workshop

Validates all Jupyter notebooks in the workshop:
- JSON structure validity
- Cell metadata
- Python syntax in code cells
- Import availability
- Markdown cell content

Usage:
    python scripts/verify_notebooks.py
"""

import json
import ast
import sys
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print(f"\n{text}")
    print("=" * 50)


def verify_json_structure(notebook_path):
    """Verify the notebook is valid JSON."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def verify_notebook_metadata(notebook_path):
    """Verify notebook has required metadata."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'cells' not in data:
        return False, "Missing 'cells' key"
    
    if 'metadata' not in data:
        return False, "Missing 'metadata' key"
    
    cell_count = len(data['cells'])
    return True, f"Valid structure ({cell_count} cells)"


def verify_code_cells(notebook_path):
    """Verify Python syntax in all code cells."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    code_cells = [c for c in data['cells'] if c.get('cell_type') == 'code']
    errors = []
    
    for i, cell in enumerate(code_cells):
        source = ''.join(cell.get('source', []))
        if not source.strip():
            continue
        
        # Skip cells with shell commands or magic
        if source.strip().startswith(('!', '%', '%%')):
            continue
            
        try:
            ast.parse(source)
        except SyntaxError as e:
            errors.append(f"Cell {i+1}: {e.msg} at line {e.lineno}")
    
    if errors:
        return False, f"{len(errors)} syntax errors"
    
    return True, f"All {len(code_cells)} code cells valid"


def extract_imports(notebook_path):
    """Extract all imports from a notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    imports = set()
    
    for cell in data['cells']:
        if cell.get('cell_type') != 'code':
            continue
        
        source = ''.join(cell.get('source', []))
        
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except SyntaxError:
            continue
    
    return imports


def verify_imports(notebook_path):
    """Verify all imports are available."""
    imports = extract_imports(notebook_path)
    
    # Standard library modules to skip
    stdlib = {
        'os', 'sys', 'json', 're', 'pathlib', 'datetime', 'typing',
        'asyncio', 'subprocess', 'tempfile', 'shutil', 'time',
        'collections', 'functools', 'itertools', 'dataclasses',
        'abc', 'contextlib', 'io', 'textwrap', 'hashlib', 'uuid'
    }
    
    # Workshop-specific modules to skip (relative imports)
    workshop_modules = {'utils'}
    
    missing = []
    checked = []
    
    for module in imports:
        if module in stdlib or module in workshop_modules:
            continue
        
        checked.append(module)
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        return False, f"Missing: {', '.join(missing)}"
    
    return True, f"All {len(checked)} imports available"


def verify_markdown_cells(notebook_path):
    """Verify markdown cells have content."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    md_cells = [c for c in data['cells'] if c.get('cell_type') == 'markdown']
    empty_count = 0
    
    for cell in md_cells:
        content = ''.join(cell.get('source', [])).strip()
        if not content:
            empty_count += 1
    
    if empty_count > 0:
        return False, f"{empty_count} empty markdown cells"
    
    return True, f"{len(md_cells)} markdown cells OK"


def verify_notebook(notebook_path):
    """Run all verifications on a notebook."""
    # Get relative path for display
    try:
        rel_path = notebook_path.relative_to(Path.cwd())
    except ValueError:
        rel_path = notebook_path.name
    
    print(f"\n{rel_path}")
    
    checks = [
        ("json", verify_json_structure),
        ("metadata", verify_notebook_metadata),
        ("syntax", verify_code_cells),
        ("imports", verify_imports),
        ("markdown", verify_markdown_cells),
    ]
    
    all_passed = True
    
    for name, check_fn in checks:
        try:
            passed, message = check_fn(notebook_path)
            icon = "✓" if passed else "✗"
            print(f"  {icon} {name}: {message}")
            all_passed = all_passed and passed
        except Exception as e:
            print(f"  ✗ {name}: Error - {e}")
            all_passed = False
    
    return all_passed


def main():
    """Verify all notebooks in the workshop."""
    print("Notebook Verification for MCP Workshop")
    print("=" * 50)
    
    # Find all notebooks
    labs_dir = Path("Labs")
    if not labs_dir.exists():
        print("Error: Labs directory not found. Run from repository root.")
        return 1
    
    notebooks = list(labs_dir.rglob("*.ipynb"))
    
    if not notebooks:
        print("No notebooks found in Labs directory.")
        return 1
    
    print(f"\nFound {len(notebooks)} notebook(s)")
    
    all_passed = True
    for notebook in sorted(notebooks):
        passed = verify_notebook(notebook)
        all_passed = all_passed and passed
    
    print("\n" + "=" * 50)
    if all_passed:
        print("All notebooks passed verification!")
        return 0
    else:
        print("Some notebooks have issues. Please review above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
