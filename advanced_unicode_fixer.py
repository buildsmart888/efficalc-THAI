#!/usr/bin/env python3
"""
Advanced encoding fixer for efficalc-THAI project
Handles all Unicode issues including curly quotes in generated HTML
"""

import os
import re
from typing import Dict, List, Tuple

# Complete Unicode character mapping
UNICODE_FIXES = {
    # Curly quotes (the main culprits!)
    "'": "'",   # Left single quotation mark U+2018
    "'": "'",   # Right single quotation mark U+2019  
    """: '"',   # Left double quotation mark U+201C
    """: '"',   # Right double quotation mark U+201D
    
    # Other problematic characters
    "·": "*",   # Middle dot U+00B7
    "²": "^2",  # Superscript two U+00B2
    "³": "^3",  # Superscript three U+00B3
    "±": "+/-", # Plus-minus sign U+00B1
    "—": "-",   # Em dash U+2014
    "–": "-",   # En dash U+2013
    "…": "...", # Horizontal ellipsis U+2026
    "′": "'",   # Prime U+2032
    "″": '"',   # Double prime U+2033
    
    # Special spacing
    "\u00A0": " ",  # Non-breaking space
    "\u2009": " ",  # Thin space
    "\u200A": " ",  # Hair space
    "\u2028": "\n", # Line separator
    "\u2029": "\n", # Paragraph separator
}

def fix_unicode_in_text(text: str) -> Tuple[str, List[str]]:
    """
    Fix Unicode characters in text
    Returns (fixed_text, list_of_changes)
    """
    original_text = text
    changes = []
    
    for unicode_char, replacement in UNICODE_FIXES.items():
        if unicode_char in text:
            count = text.count(unicode_char)
            text = text.replace(unicode_char, replacement)
            changes.append(f"Replaced {count} instances of '{unicode_char}' (U+{ord(unicode_char):04X}) with '{replacement}'")
    
    return text, changes

def fix_file_unicode(filepath: str, dry_run: bool = True) -> Tuple[bool, List[str]]:
    """
    Fix Unicode issues in a file
    Returns (changes_made, list_of_changes)
    """
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content, changes = fix_unicode_in_text(content)
        
        if fixed_content != content:
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                changes.append(f"✅ File updated: {filepath}")
            else:
                changes.append(f"🔍 Would update: {filepath}")
            return True, changes
        else:
            return False, ["No Unicode issues found"]
            
    except Exception as e:
        return False, [f"Error processing {filepath}: {str(e)}"]

def scan_and_fix_project(base_dir: str, dry_run: bool = True):
    """
    Scan entire project for Unicode issues and optionally fix them
    """
    print("🔍 Scanning project for Unicode encoding issues...")
    print("=" * 60)
    
    total_files_scanned = 0
    total_files_with_issues = 0
    all_changes = []
    
    # Scan Python files
    for root, dirs, files in os.walk(base_dir):
        # Skip .git, __pycache__, .venv directories
        dirs[:] = [d for d in dirs if not d.startswith(('.git', '__pycache__', '.venv', 'node_modules'))]
        
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.rst')):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, base_dir)
                
                total_files_scanned += 1
                changed, changes = fix_file_unicode(filepath, dry_run=dry_run)
                
                if changed:
                    total_files_with_issues += 1
                    print(f"\n📄 {rel_path}")
                    for change in changes:
                        print(f"  • {change}")
                    all_changes.extend(changes)
    
    print(f"\n📊 Scan Summary:")
    print(f"  • Files scanned: {total_files_scanned}")
    print(f"  • Files with issues: {total_files_with_issues}")
    print(f"  • Total changes: {len(all_changes)}")
    
    return total_files_with_issues, all_changes

def test_html_generation():
    """
    Test HTML generation to catch runtime Unicode issues
    """
    print("\n🧪 Testing HTML generation for Unicode issues...")
    
    try:
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        
        from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si
        from efficalc.report_builder import ReportBuilder
        
        # Generate HTML
        report = ReportBuilder(concrete_beam_aci318m_si)
        html_content = report.get_html_as_str()
        
        # Check for Unicode issues in generated HTML
        fixed_html, changes = fix_unicode_in_text(html_content)
        
        if changes:
            print("❌ HTML generation still produces Unicode issues:")
            for change in changes[:10]:  # Show first 10 issues
                print(f"  • {change}")
            if len(changes) > 10:
                print(f"  • ... and {len(changes) - 10} more issues")
                
            # This suggests the issue is in the source code or templates
            print("\n💡 These issues likely come from:")
            print("  • LaTeX expressions in calculation strings")
            print("  • Comments or docstrings in calculation functions")  
            print("  • Template files or HTML generation code")
            
            return False
        else:
            print("✅ HTML generation produces clean output!")
            return True
            
    except Exception as e:
        print(f"❌ Error testing HTML generation: {str(e)}")
        return False

def main():
    print("🔧 Advanced Unicode Fixer for efficalc-THAI")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # First: scan project files
    files_with_issues, all_changes = scan_and_fix_project(base_dir, dry_run=True)
    
    # Second: test HTML generation
    html_clean = test_html_generation()
    
    print(f"\n🎯 Results:")
    print(f"  • Source files with Unicode issues: {files_with_issues}")
    print(f"  • HTML generation clean: {'Yes' if html_clean else 'No'}")
    
    if files_with_issues > 0:
        response = input(f"\n🚀 Fix {files_with_issues} files with Unicode issues? (y/N): ").strip().lower()
        if response == 'y':
            print("\n🔨 Applying fixes...")
            scan_and_fix_project(base_dir, dry_run=False)
    
    if not html_clean:
        print("\n⚠️  HTML generation still has issues.")
        print("💡 Consider checking LaTeX expressions and calculation strings in source files.")

if __name__ == "__main__":
    main()
