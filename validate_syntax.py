#!/usr/bin/env python3
"""
Syntax validator and fixer for main.py
"""
import ast
import re
import sys
from pathlib import Path

def validate_python_syntax(file_path):
    """Validate Python syntax and report errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the AST
        ast.parse(content)
        print(f"✅ {file_path} has valid Python syntax")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax Error in {file_path}:")
        print(f"   Line {e.lineno}: {e.text.strip() if e.text else 'N/A'}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False

def fix_common_issues(file_path):
    """Fix common syntax issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        changes_made = False
        
        for i, line in enumerate(lines, 1):
            original_line = line
            
            # Fix unterminated strings in decorators
            if '@app.' in line and line.strip().endswith('("/api/'):
                line = line.rstrip() + 'health")\n'
                changes_made = True
                print(f"🔧 Fixed line {i}: Completed unterminated string")
            
            # Fix incomplete decorators
            elif line.strip() == '@app.get("/api/':
                line = '@app.get("/api/health")\n'
                changes_made = True
                print(f"🔧 Fixed line {i}: Completed decorator")
            
            # Fix other common patterns
            elif re.match(r'^\s*@app\.(get|post|put|delete)\("/[^"]*$', line.strip()):
                # Find the incomplete route and complete it
                method_match = re.search(r'@app\.(\w+)\("([^"]*)', line)
                if method_match:
                    method = method_match.group(1)
                    partial_route = method_match.group(2)
                    
                    # Complete common routes
                    if partial_route.startswith('/api'):
                        complete_route = '/api/health'
                    else:
                        complete_route = partial_route + '"'
                    
                    line = f'@app.{method}("{complete_route}")\n'
                    changes_made = True
                    print(f"🔧 Fixed line {i}: Completed route decorator")
            
            fixed_lines.append(line)
        
        if changes_made:
            # Create backup
            backup_path = f"{file_path}.backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"📁 Backup created: {backup_path}")
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            print(f"✅ Fixed {file_path}")
            
        return changes_made
        
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

if __name__ == "__main__":
    file_path = "main.py"
    
    print("🔍 Validating Python syntax...")
    
    if not validate_python_syntax(file_path):
        print("\n🔧 Attempting to fix common issues...")
        if fix_common_issues(file_path):
            print("\n🔍 Re-validating after fixes...")
            validate_python_syntax(file_path)
        else:
            print("❌ Could not automatically fix the issues")
            sys.exit(1)