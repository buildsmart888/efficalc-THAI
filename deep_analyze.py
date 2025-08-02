"""
Deep analysis of HTML content for remaining encoding issues
"""

def deep_analyze_html():
    from examples.concrete_aci318m_si_example import concrete_beam_aci318m_si, concrete_column_aci318m_si
    from efficalc.report_builder import ReportBuilder
    import re
    
    print("=== DEEP HTML ANALYSIS ===")
    
    # Test both functions
    for name, func in [("Beam", concrete_beam_aci318m_si), ("Column", concrete_column_aci318m_si)]:
        print(f"\n--- {name} Analysis ---")
        
        builder = ReportBuilder(func)
        html = builder.get_html_as_str()
        
        print(f"HTML length: {len(html)}")
        
        # Check for all potential problematic patterns
        issues = []
        
        # 1. Check for unescaped & (not &amp; &lt; etc.)
        unescaped_amp = re.findall(r'&(?![a-zA-Z0-9#]{1,7};)', html)
        if unescaped_amp:
            issues.append(f"Unescaped & found: {len(unescaped_amp)} occurrences")
            print(f"  ❌ Unescaped &: {len(unescaped_amp)} found")
            # Show context around first few
            for i, match in enumerate(unescaped_amp[:3]):
                pos = html.find(match)
                context = html[max(0, pos-20):pos+20]
                print(f"    Context {i+1}: ...{context}...")
        
        # 2. Check for HTML entities that might be problematic
        entities = {
            '&amp;': html.count('&amp;'),
            '&lt;': html.count('&lt;'),
            '&gt;': html.count('&gt;'),
            '&quot;': html.count('&quot;'),
            '&nbsp;': html.count('&nbsp;'),
            '&#': len(re.findall(r'&#\d+;', html)),
        }
        
        print("  HTML entities:")
        for entity, count in entities.items():
            if count > 0:
                print(f"    {entity}: {count}")
        
        # 3. Check for Unicode characters
        unicode_chars = []
        for i, char in enumerate(html):
            if ord(char) > 127:
                unicode_chars.append((i, char, ord(char)))
        
        if unicode_chars:
            issues.append(f"Unicode characters: {len(unicode_chars)} found")
            print(f"  ❌ Unicode chars: {len(unicode_chars)} found")
            for i, (pos, char, code) in enumerate(unicode_chars[:5]):
                context = html[max(0, pos-10):pos+10]
                print(f"    {i+1}. '{char}' (U+{code:04X}) at pos {pos}: ...{repr(context)}...")
        
        # 4. Check for specific LaTeX/MathJax patterns that might cause issues
        math_patterns = [
            (r'\\[a-zA-Z]+', 'LaTeX commands'),
            (r'\{[^}]*\}', 'Braces'),
            (r'f&\\#x27;', 'Escaped apostrophe in formula'),
            (r'&\\#x27;', 'Escaped apostrophe'),
            (r'\\cdot', 'LaTeX cdot'),
            (r'\\frac', 'LaTeX fractions'),
        ]
        
        print("  LaTeX/Math patterns:")
        for pattern, desc in math_patterns:
            matches = re.findall(pattern, html)
            if matches:
                print(f"    {desc}: {len(matches)} matches")
                if 'x27' in pattern:  # Show problematic patterns
                    for match in matches[:3]:
                        print(f"      {repr(match)}")
        
        # 5. Look for specific error patterns
        error_patterns = [
            ('Misplaced', 'Misplaced errors'),
            ('LaTeX Error', 'LaTeX errors'),
            ('&#x27;', 'Hex encoded apostrophe'),
            ("f'_c", 'Prime notation in variable names'),
        ]
        
        print("  Error indicators:")
        for pattern, desc in error_patterns:
            count = html.count(pattern)
            if count > 0:
                print(f"    ❌ {desc}: {count} found")
                issues.append(f"{desc}: {count}")
        
        if not issues:
            print("  ✅ No obvious issues found")
        
        # Save a sample of the HTML for manual inspection
        sample_file = f"html_sample_{name.lower()}.txt"
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(html[:2000])  # First 2000 chars
        print(f"  📄 Sample saved to: {sample_file}")

if __name__ == "__main__":
    deep_analyze_html()
