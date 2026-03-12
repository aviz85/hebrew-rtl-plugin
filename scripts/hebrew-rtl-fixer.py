#!/usr/bin/env python3
"""
Hebrew RTL Paragraph Fixer
Adds U+202B (RLE) marker to the start of paragraphs that begin with Hebrew text.
"""

import sys
import re

def is_hebrew_letter(char):
    """Check if character is Hebrew"""
    return '\u0590' <= char <= '\u05FF'

def find_first_letter(text):
    """Find the first letter (skipping numbers, punctuation, whitespace)"""
    for char in text:
        if char.isalpha():
            return char
    return None

def fix_paragraph(paragraph):
    """Add RTL marker if paragraph starts with Hebrew text"""
    if not paragraph.strip():
        return paragraph

    # Find first letter (skip non-alpha characters)
    first_letter = find_first_letter(paragraph)

    if first_letter is None:
        # No letters found, return as is
        return paragraph

    # Check if first letter is Hebrew
    if is_hebrew_letter(first_letter):
        # Add RTL marker at the very beginning
        return '\u202B' + paragraph

    # English or other language, keep as is
    return paragraph

def fix_hebrew_rtl(content):
    """Process content and add RTL markers to Hebrew lines"""
    # Process each line individually
    lines = content.split('\n')
    fixed_lines = [fix_paragraph(line) for line in lines]
    return '\n'.join(fixed_lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: hebrew-rtl-fixer.py <file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix RTL
        fixed_content = fix_hebrew_rtl(content)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        print(f"✓ Fixed Hebrew RTL markers in {filepath}")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
