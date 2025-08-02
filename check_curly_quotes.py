#!/usr/bin/env python3
"""
Check for curly quotes in report_builder.py binary content
"""

def check_curly_quotes_in_file():
    print("🔍 Checking for curly quotes in report_builder.py...")
    
    with open('efficalc/report_builder.py', 'rb') as f:
        content = f.read()
    
    # Convert to string and split lines
    text = content.decode('utf-8')
    lines = text.split('\n')
    
    curly_chars = {
        '"': 'U+201C (LEFT DOUBLE QUOTATION MARK)',
        '"': 'U+201D (RIGHT DOUBLE QUOTATION MARK)',
        ''': 'U+2018 (LEFT SINGLE QUOTATION MARK)',
        ''': 'U+2019 (RIGHT SINGLE QUOTATION MARK)'
    }
    
    found_issues = []
    
    for i, line in enumerate(lines, 1):
        for char, description in curly_chars.items():
            if char in line:
                found_issues.append((i, char, description, line.strip()))
    
    if found_issues:
        print(f"❌ Found {len(found_issues)} lines with curly quotes:")
        print("-" * 60)
        for line_num, char, desc, line_content in found_issues:
            print(f"Line {line_num}: Contains '{char}' ({desc})")
            print(f"  Content: {line_content}")
            print()
    else:
        print("✅ No curly quotes found in report_builder.py")
    
    return found_issues

if __name__ == "__main__":
    issues = check_curly_quotes_in_file()
    print(f"Total issues: {len(issues)}")
