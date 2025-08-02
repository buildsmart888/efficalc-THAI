#!/usr/bin/env python3
"""
Fix all curly quotes in generate_html.py
"""

def fix_generate_html():
    print("🔧 Fixing curly quotes in generate_html.py...")
    
    # Read the file
    with open('efficalc/generate_html.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace all curly quotes with straight quotes
    replacements = {
        '"': '"',  # RIGHT DOUBLE QUOTATION MARK → STRAIGHT DOUBLE QUOTE
        '"': '"',  # LEFT DOUBLE QUOTATION MARK → STRAIGHT DOUBLE QUOTE  
        ''': "'",  # RIGHT SINGLE QUOTATION MARK → STRAIGHT SINGLE QUOTE
        ''': "'",  # LEFT SINGLE QUOTATION MARK → STRAIGHT SINGLE QUOTE
    }
    
    total_replacements = 0
    for curly, straight in replacements.items():
        count = content.count(curly)
        if count > 0:
            content = content.replace(curly, straight)
            total_replacements += count
            print(f"  • Replaced {count} instances of '{curly}' with '{straight}'")
    
    if total_replacements > 0:
        # Create backup
        with open('efficalc/generate_html.py.backup', 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"  📄 Created backup: generate_html.py.backup")
        
        # Write fixed content
        with open('efficalc/generate_html.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed {total_replacements} curly quotes in generate_html.py")
        return True
    else:
        print("✅ No curly quotes found to fix")
        return False

if __name__ == "__main__":
    success = fix_generate_html()
    if success:
        print("\n🎯 Now test HTML generation again to verify the fix works!")
    else:
        print("\n❓ No changes made - file might already be clean")
