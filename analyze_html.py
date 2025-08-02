"""
Analyze HTML for encoding issues
"""

def analyze_html():
    from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si
    from efficalc.report_builder import ReportBuilder
    
    print("Analyzing HTML content for encoding issues...")
    
    builder = ReportBuilder(concrete_beam_aci318m_si)
    html = builder.get_html_as_str()
    
    print(f"HTML length: {len(html)} characters")
    
    # Check for problematic & symbols
    lines = html.split('\n')
    problematic_ampersand = []
    problematic_unicode = []
    
    for i, line in enumerate(lines):
        # Check for unescaped & (not &amp; &lt; &gt; etc.)
        if '&' in line:
            if not any(escaped in line for escaped in ['&amp;', '&lt;', '&gt;', '&quot;', '&nbsp;', '&#']):
                problematic_ampersand.append((i+1, line.strip()))
        
        # Check for non-ASCII characters
        for char in line:
            if ord(char) > 127:
                problematic_unicode.append((i+1, line.strip(), char, ord(char)))
                break  # Only report first unicode char per line
    
    print(f"\n=== PROBLEMATIC AMPERSANDS ===")
    print(f"Found {len(problematic_ampersand)} lines with unescaped &:")
    for line_num, line_content in problematic_ampersand[:10]:
        print(f"Line {line_num}: {line_content}")
    
    print(f"\n=== UNICODE CHARACTERS ===")
    print(f"Found {len(problematic_unicode)} lines with Unicode:")
    for line_num, line_content, char, code in problematic_unicode[:10]:
        print(f"Line {line_num}: '{char}' (U+{code:04X}) in: {line_content[:80]}...")
    
    # Check for specific problematic patterns
    patterns_to_check = [
        'φ', 'Φ',  # Greek phi
        'β', 'Β',  # Greek beta  
        'ε', 'Ε',  # Greek epsilon
        'ρ', 'Ρ',  # Greek rho
        '⋅', '•', '*',  # Various dots
        'è', 'é', 'ê', 'ë',  # French accents
        '+/-', '≥', '≤', '≠',  # Math symbols
        '°', '^2', '^3',  # Superscripts
    ]
    
    print(f"\n=== SPECIFIC PATTERNS ===")
    found_patterns = []
    for pattern in patterns_to_check:
        if pattern in html:
            count = html.count(pattern)
            found_patterns.append((pattern, count))
    
    if found_patterns:
        print("Found these problematic patterns:")
        for pattern, count in found_patterns:
            print(f"  '{pattern}': {count} occurrences")
    else:
        print("No specific problematic patterns found")
    
    return len(problematic_ampersand) == 0 and len(problematic_unicode) == 0

if __name__ == "__main__":
    is_clean = analyze_html()
    if is_clean:
        print("\n✅ HTML is clean - no encoding issues found")
    else:
        print("\n❌ HTML has encoding issues that need fixing")
