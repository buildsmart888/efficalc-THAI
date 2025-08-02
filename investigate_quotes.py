#!/usr/bin/env python3
"""
Deep investigation of curly quotes source in HTML generation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si
from efficalc.report_builder import ReportBuilder

def investigate_curly_quotes():
    print("🔍 Investigating source of curly quotes in HTML generation...")
    print("=" * 70)
    
    # Generate HTML and extract lines with curly quotes
    report = ReportBuilder(concrete_beam_aci318m_si)
    html_content = report.get_html_as_str()
    
    lines = html_content.split('\n')
    problematic_lines = []
    
    for i, line in enumerate(lines, 1):
        if '"' in line or '"' in line or ''' in line or ''' in line:
            problematic_lines.append((i, line.strip()))
    
    print(f"Found {len(problematic_lines)} lines with curly quotes:")
    print("-" * 70)
    
    # Group by type of content
    latex_lines = []
    other_lines = []
    
    for line_num, line in problematic_lines[:20]:  # Show first 20
        if any(marker in line for marker in ['\\(', '\\)', 'katex', 'math']):
            latex_lines.append((line_num, line))
        else:
            other_lines.append((line_num, line))
        
        print(f"Line {line_num}: {line[:100]}{'...' if len(line) > 100 else ''}")
    
    if len(problematic_lines) > 20:
        print(f"... and {len(problematic_lines) - 20} more lines")
    
    print(f"\n📊 Analysis:")
    print(f"  • LaTeX/Math lines: {len(latex_lines)}")
    print(f"  • Other lines: {len(other_lines)}")
    
    # Check if it's coming from specific functions
    print(f"\n🔍 Checking common sources...")
    
    # Check Input/Calculation object strings
    curly_quote_chars = ['"', '"', "'", "'"]
    for char in curly_quote_chars:
        count = html_content.count(char)
        if count > 0:
            if len(char) == 1:
                char_code = f"U+{ord(char):04X}"
            else:
                char_code = f"MULTI:{[f'U+{ord(c):04X}' for c in char]}"
            print(f"  • Character '{char}' ({char_code}): {count} instances")
    
    # Look for specific patterns
    patterns_to_check = [
        'f_{c}^{\\prime}',
        'concrete',
        'strength', 
        'Input(',
        'Calculation(',
        'TextBlock(',
    ]
    
    print(f"\n🎯 Pattern analysis:")
    for pattern in patterns_to_check:
        # Find lines containing this pattern AND curly quotes
        matching_lines = [line for _, line in problematic_lines if pattern.lower() in line.lower()]
        if matching_lines:
            print(f"  • '{pattern}' appears in {len(matching_lines)} problematic lines")
            # Show one example
            if matching_lines:
                example = matching_lines[0][:120] + ('...' if len(matching_lines[0]) > 120 else '')
                print(f"    Example: {example}")

if __name__ == "__main__":
    investigate_curly_quotes()
