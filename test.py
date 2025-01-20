import re
import inspect
import importlib
from pathlib import Path

def get_docstring(import_path):
    """Get docstring for a given import path."""
    try:
        # Handle cases where import path is just the object name (e.g. "login")
        if "." not in import_path:
            import_path = f"huggingface_hub.{import_path}"
            
        # Split into module path and object name
        *module_parts, obj_name = import_path.split('.')
        
        # Import the module
        module = importlib.import_module('.'.join(module_parts))
        
        # Get the object
        obj = getattr(module, obj_name)
        
        # Get and format docstring
        docstring = inspect.getdoc(obj)
        return f"```python\n{docstring}\n```" if docstring else f"No docstring found for {import_path}"
    except Exception as e:
        return f"Error fetching docstring for {import_path}: {str(e)}"

def process_markdown_file(file_path):
    """Process a markdown file and replace [[autodoc]] directives."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all autodoc directives
    pattern = r'\[\[autodoc\]\] ([^\n]+)'
    
    def replace_autodoc(match):
        import_path = match.group(1)
        docstring = get_docstring(import_path)
        return f"### {import_path}\n\n{docstring}\n"
    
    # Replace all autodoc directives with actual docstrings
    new_content = re.sub(pattern, replace_autodoc, content)
    
    # Only write if content has changed
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

def process_docs_directory(docs_dir):
    """Process all markdown files in the docs directory."""
    docs_path = Path(docs_dir)
    for md_file in docs_path.rglob('*.md'):
        if '[[autodoc]]' in md_file.read_text(encoding='utf-8'):
            print(f"Processing {md_file}")
            process_markdown_file(md_file)

# Usage
process_docs_directory('docs/source')