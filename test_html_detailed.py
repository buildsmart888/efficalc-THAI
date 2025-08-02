"""
Test HTML generation with detailed analysis
"""

def test_html_generation():
    import re
    from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si
    from efficalc.report_builder import ReportBuilder
    
    print("Testing HTML generation step by step...")
    
    # Generate HTML
    builder = ReportBuilder(concrete_beam_aci318m_si)
    html = builder.get_html_as_str()
    
    # Look for the specific line with Unicode
    lines = html.split('\n')
    for i, line in enumerate(lines):
        if any(ord(c) > 127 for c in line):
            print(f"Line {i+1} contains Unicode:")
            print(f"  Content: {repr(line)}")
            print(f"  Display: {line}")
            
            # Show specific Unicode characters
            for j, char in enumerate(line):
                if ord(char) > 127:
                    print(f"    Position {j}: '{char}' (U+{ord(char):04X})")
            print()
    
    # Check for common HTML entities that might need escaping
    entities_to_check = [
        ('&nbsp;', 'Non-breaking space'),
        ('&amp;', 'Ampersand'),
        ('&lt;', 'Less than'),
        ('&gt;', 'Greater than'),
        ('&quot;', 'Quote'),
        ('&#', 'Numeric entity'),
    ]
    
    print("HTML entities found:")
    for entity, description in entities_to_check:
        count = html.count(entity)
        if count > 0:
            print(f"  {entity}: {count} occurrences ({description})")
    
    # Check for potential MathJax/LaTeX issues
    math_patterns = [
        r'\\beta',
        r'\\epsilon',
        r'\\phi',
        r'\\rho',
        r'\{[^}]*\}',  # LaTeX subscripts/superscripts
    ]
    
    print("\nMath patterns found:")
    for pattern in math_patterns:
        matches = re.findall(pattern, html)
        if matches:
            print(f"  {pattern}: {len(matches)} matches")
            for match in matches[:3]:  # Show first 3 matches
                print(f"    {repr(match)}")

if __name__ == "__main__":
    test_html_generation()
