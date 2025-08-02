#!/usr/bin/env python3
"""
Check generate_html.py for curly quotes
"""

def check_generate_html():
    print("🔍 Checking generate_html.py for curly quotes...")
    
    with open('efficalc/generate_html.py', 'rb') as f:
        content = f.read()
    
    text = content.decode('utf-8')
    lines = text.split('\n')
    
    curly_chars = {
        '"': 'RIGHT DOUBLE QUOTE',
        '"': 'LEFT DOUBLE QUOTE', 
        ''': 'RIGHT SINGLE QUOTE',
        ''': 'LEFT SINGLE QUOTE'
    }
    
    issues = []
    for i, line in enumerate(lines, 1):
        for char, desc in curly_chars.items():
            if char in line:
                issues.append((i, char, desc, line.strip()))
    
    if issues:
        print(f"❌ Found {len(issues)} curly quotes in generate_html.py:")
        for line_num, char, desc, line_content in issues[:15]:
            print(f"Line {line_num}: '{char}' ({desc})")
            print(f"  Content: {line_content[:100]}...")
            print()
    else:
        print("✅ No curly quotes found in generate_html.py")
    
    return len(issues)

if __name__ == "__main__":
    count = check_generate_html()
    print(f"Total issues: {count}")
