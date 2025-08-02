"""
Scan entire project for problematic characters that might cause LaTeX/HTML encoding issues
"""

import os
import re

def scan_project_for_special_chars():
    """Scan all Python files in the project for potentially problematic characters"""
    
    # Characters that often cause LaTeX/HTML issues
    problematic_chars = {
        "'": "Apostrophe (use LaTeX \\prime)",
        """: "Curly quote (use straight quote)",
        """: "Curly quote (use straight quote)", 
        "'": "Curly apostrophe (use straight apostrophe)",
        "'": "Curly apostrophe (use straight apostrophe)",
        "-": "En dash (use hyphen -)",
        "-": "Em dash (use hyphen -)",
        "...": "Ellipsis (use ...)",
        "°": "Degree symbol (use \\degree)",
        "^2": "Superscript 2 (use ^2)",
        "^3": "Superscript 3 (use ^3)",
        "φ": "Greek phi (use \\phi)",
        "β": "Greek beta (use \\beta)",
        "ε": "Greek epsilon (use \\epsilon)",
        "ρ": "Greek rho (use \\rho)",
        "σ": "Greek sigma (use \\sigma)",
        "τ": "Greek tau (use \\tau)",
        "α": "Greek alpha (use \\alpha)",
        "γ": "Greek gamma (use \\gamma)",
        "δ": "Greek delta (use \\delta)",
        "λ": "Greek lambda (use \\lambda)",
        "μ": "Greek mu (use \\mu)",
        "π": "Greek pi (use \\pi)",
        "ω": "Greek omega (use \\omega)",
        "⋅": "Center dot (use \\cdot or *)",
        "•": "Bullet (use \\bullet)",
        "*": "Middle dot (use \\cdot or *)",
        "×": "Multiplication (use \\times or *)",
        "÷": "Division (use \\div or /)",
        "+/-": "Plus-minus (use \\pm)",
        "≤": "Less than or equal (use \\leq)",
        "≥": "Greater than or equal (use \\geq)",
        "≠": "Not equal (use \\neq)",
        "≈": "Approximately (use \\approx)",
        "∞": "Infinity (use \\infty)",
        "∑": "Sum (use \\sum)",
        "∫": "Integral (use \\int)",
        "√": "Square root (use \\sqrt)",
        "∂": "Partial (use \\partial)",
        "∆": "Delta (use \\Delta)",
        "∇": "Nabla (use \\nabla)",
    }
    
    # Directories to scan
    dirs_to_scan = ['examples', 'efficalc', 'tests']
    
    issues_found = []
    
    for directory in dirs_to_scan:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            # Check for problematic characters
                            for line_num, line in enumerate(content.split('\n'), 1):
                                for char, description in problematic_chars.items():
                                    if char in line:
                                        # Find position in line
                                        positions = [i for i, c in enumerate(line) if c == char]
                                        for pos in positions:
                                            context = line[max(0, pos-20):pos+20]
                                            issues_found.append({
                                                'file': file_path,
                                                'line': line_num,
                                                'char': char,
                                                'description': description,
                                                'context': context,
                                                'full_line': line.strip()
                                            })
                        
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
    
    # Report findings
    if issues_found:
        print(f"🔍 Found {len(issues_found)} potential encoding issues:")
        print("=" * 80)
        
        # Group by file
        by_file = {}
        for issue in issues_found:
            file_path = issue['file']
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(issue)
        
        for file_path, file_issues in by_file.items():
            print(f"\n📄 {file_path}")
            print("-" * 60)
            
            for issue in file_issues:
                print(f"  Line {issue['line']}: '{issue['char']}' - {issue['description']}")
                print(f"    Context: ...{issue['context']}...")
                print(f"    Full line: {issue['full_line']}")
                print()
        
        # Provide recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("=" * 80)
        print("1. Replace apostrophes (') in variable names with LaTeX notation:")
        print("   f'_c → f_{c}^{\\prime}")
        print("   f'_y → f_{y}^{\\prime}")
        print()
        print("2. Replace Greek letters with LaTeX commands:")
        print("   φ → \\phi")
        print("   β → \\beta")
        print("   ε → \\epsilon")
        print()
        print("3. Replace special symbols with LaTeX or ASCII:")
        print("   ⋅ → \\cdot or *")
        print("   +/- → \\pm")
        print("   ≥ → \\geq")
        print()
        print("4. Use only ASCII characters in strings that will be processed by LaTeX/HTML")
        
    else:
        print("✅ No problematic characters found!")
        print("All files appear to use safe ASCII or proper LaTeX notation.")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    print("🔍 Scanning efficalc-THAI project for problematic characters...")
    print()
    is_clean = scan_project_for_special_chars()
    
    if is_clean:
        print("\n🎉 Project is clean! No encoding issues should occur.")
    else:
        print("\n⚠️  Please fix the issues above to prevent 'Misplaced &' errors.")
