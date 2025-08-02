#!/usr/bin/env python3
"""
Automated fix for encoding issues in efficalc-THAI project
Focuses on user-facing files and critical components
"""

import os
import re
from typing import Dict, List, Tuple

# Define the critical patterns to fix
CRITICAL_FIXES = {
    # Mathematical notation fixes
    "'": "'",  # Curly apostrophe to straight
    """: '"',  # Curly quotes to straight
    """: '"',  # Curly quotes to straight
    "*": "*",  # Middle dot to asterisk for multiplication
    "^2": "^2",  # Superscript 2
    "^3": "^3",  # Superscript 3
    "+/-": "+/-",  # Plus-minus symbol
    
    # Common Unicode fixes for LaTeX compatibility
    "-": "-",  # Em dash
    "-": "-",  # En dash
    "...": "...",  # Ellipsis
    "'": "'",  # Prime symbol
    """: '"',  # Double prime
}

# Variable name fixes for engineering notation
VARIABLE_FIXES = {
    r"f'_c": r"f_{c}^{\prime}",  # Concrete strength
    r"f'_y": r"f_{y}^{\prime}",  # Steel yield strength  
    r"f'_s": r"f_{s}^{\prime}",  # Steel stress
}

# Files to prioritize (user-facing and core library)
PRIORITY_FILES = [
    "examples/concrete_aci318m_si_example.py",
    "examples/concrete_beam_neutral_axis.py", 
    "examples/point_load_beam_moment_and_deflection.py",
    "examples/point_load_beam_si_units.py",
    "examples/si_units_demo.py",
    "examples/steel_beam_moment_strength.py",
    "examples/steel_beam_optimizer.py",
    "efficalc/calculation_runner.py",
    "efficalc/generate_html.py",
    "efficalc/report_builder.py",
    "efficalc/si_units.py",
]

def fix_file_encoding(filepath: str, dry_run: bool = True) -> Tuple[bool, List[str]]:
    """
    Fix encoding issues in a single file
    Returns (changes_made, list_of_changes)
    """
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # Apply critical character fixes
        for old_char, new_char in CRITICAL_FIXES.items():
            if old_char in content:
                count = content.count(old_char)
                content = content.replace(old_char, new_char)
                changes.append(f"Replaced {count} instances of '{old_char}' with '{new_char}'")
        
        # Apply variable name fixes using regex
        for old_pattern, new_pattern in VARIABLE_FIXES.items():
            matches = re.findall(old_pattern, content)
            if matches:
                content = re.sub(old_pattern, new_pattern, content)
                changes.append(f"Fixed variable notation: {old_pattern} → {new_pattern}")
        
        # Only write if changes were made and not dry run
        if content != original_content:
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                changes.append(f"✅ File updated: {filepath}")
            else:
                changes.append(f"🔍 Would update: {filepath}")
            return True, changes
        else:
            return False, ["No changes needed"]
            
    except Exception as e:
        return False, [f"Error processing {filepath}: {str(e)}"]

def main():
    print("🔧 Fixing critical encoding issues in efficalc-THAI...")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    total_files_fixed = 0
    all_changes = []
    
    # First pass: dry run on priority files
    print("📋 DRY RUN - Checking priority files...")
    for rel_path in PRIORITY_FILES:
        full_path = os.path.join(base_dir, rel_path)
        changed, changes = fix_file_encoding(full_path, dry_run=True)
        if changed:
            print(f"\n📄 {rel_path}")
            for change in changes:
                print(f"  • {change}")
            all_changes.extend(changes)
    
    if all_changes:
        print(f"\n💡 Found {len(all_changes)} potential fixes")
        response = input("\n🚀 Apply these fixes? (y/N): ").strip().lower()
        
        if response == 'y':
            print("\n🔨 Applying fixes...")
            for rel_path in PRIORITY_FILES:
                full_path = os.path.join(base_dir, rel_path)
                changed, changes = fix_file_encoding(full_path, dry_run=False)
                if changed:
                    total_files_fixed += 1
                    print(f"✅ Fixed: {rel_path}")
        else:
            print("❌ Cancelled by user")
    else:
        print("✨ No critical encoding issues found in priority files!")
    
    print(f"\n📊 Summary: {total_files_fixed} files updated")
    print("🎯 Focus on user-facing examples and core library completed")

if __name__ == "__main__":
    main()
