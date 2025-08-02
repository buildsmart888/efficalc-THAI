#!/usr/bin/env python3
"""
Find the exact source of curly quotes in the generated HTML
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si
from efficalc.report_builder import ReportBuilder

def find_curly_quote_source():
    print("🔍 Finding exact source of curly quotes...")
    print("=" * 60)
    
    # Generate HTML
    report = ReportBuilder(concrete_beam_aci318m_si)
    html_content = report.get_html_as_str()
    
    # Find all lines with curly right double quote
    lines = html_content.split('\n')
    quote_lines = []
    
    for i, line in enumerate(lines, 1):
        if '"' in line:
            quote_lines.append((i, line.strip()))
    
    print(f"Found curly quotes (\") in {len(quote_lines)} lines:")
    print("-" * 60)
    
    # Show actual content with quotes
    for line_num, line in quote_lines[:10]:  # First 10 lines
        # Highlight the curly quotes
        highlighted_line = line.replace('"', '**"**')
        print(f"Line {line_num}: {highlighted_line}")
        
        # Extract the part with quotes for analysis
        if len(line) > 150:
            quote_start = line.find('"')
            if quote_start >= 0:
                start = max(0, quote_start - 50)
                end = min(len(line), quote_start + 100)
                snippet = line[start:end]
                print(f"         Context: ...{snippet}...")
        print()
    
    if len(quote_lines) > 10:
        print(f"... and {len(quote_lines) - 10} more lines with curly quotes")
    
    # Check if these are in specific sections
    print("\n🎯 Analyzing quote locations:")
    
    # Count by content type
    html_quotes = 0
    latex_quotes = 0
    calculation_quotes = 0
    other_quotes = 0
    
    for _, line in quote_lines:
        line_lower = line.lower()
        if any(tag in line_lower for tag in ['<div', '<span', '<p', '<h', 'style=']):
            html_quotes += 1
        elif any(latex in line_lower for latex in ['\\(', '\\)', 'katex', 'mathjax']):
            latex_quotes += 1  
        elif any(calc in line_lower for calc in ['input', 'calculation', 'heading']):
            calculation_quotes += 1
        else:
            other_quotes += 1
    
    print(f"  • HTML/CSS attributes: {html_quotes}")
    print(f"  • LaTeX/Math expressions: {latex_quotes}") 
    print(f"  • Calculation content: {calculation_quotes}")
    print(f"  • Other content: {other_quotes}")
    
    # Save a sample to file for detailed inspection
    sample_file = "curly_quotes_sample.txt"
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write("Sample lines with curly quotes:\n")
        f.write("=" * 40 + "\n\n")
        for line_num, line in quote_lines[:20]:
            f.write(f"Line {line_num}:\n{line}\n\n")
    
    print(f"\n💾 Saved sample to {sample_file} for detailed inspection")

if __name__ == "__main__":
    find_curly_quote_source()
