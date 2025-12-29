#!/usr/bin/env python3
"""
Full Content Migration Script
Migrates all content from CLEAN_Complete_Reference_Fixed.md into the appropriate Quarto chapter files.
"""

import re
from pathlib import Path

SOURCE_FILE = Path("CLEAN_Complete_Reference_Fixed.md")
VOLUMES_DIR = Path("volumes")

# Mapping of source sections to target QMD files
CHAPTER_MAPPING = {
    # Volume I: Foundations
    "Part I: Foundations": "vol1-foundations/01-hierarchy.qmd",
    "Chapter 1: The Architecture of Destiny": "vol1-foundations/01-hierarchy.qmd",
    "Chapter 2: Mesopotamian Origins": "vol1-foundations/02-cosmos.qmd",
    "Chapter 3: The Egyptian": "vol1-foundations/02-cosmos.qmd",
    "Chapter 4: The Thema Mundi": "vol1-foundations/02-cosmos.qmd",
    "Chapter 5: Philosophical Foundations": "vol1-foundations/03-sect.qmd",
    
    # Volume II: Houses and Places
    "Chapter 6: The Twelve Houses": "vol2-places/11-houses.qmd",
    "Chapter 6a: The Lunar Nodes": "vol2-places/11-houses.qmd",
    "The First House": "vol2-places/11-houses.qmd",
    "The Second House": "vol2-places/11-houses.qmd",
    "The Third House": "vol2-places/11-houses.qmd",
    "The Fourth House": "vol2-places/11-houses.qmd",
    "The Fifth House": "vol2-places/11-houses.qmd",
    "The Sixth House": "vol2-places/11-houses.qmd",
    "The Seventh House": "vol2-places/11-houses.qmd",
    "The Eighth House": "vol2-places/11-houses.qmd",
    "The Ninth House": "vol2-places/11-houses.qmd",
    "The Tenth House": "vol2-places/11-houses.qmd",
    "The Eleventh House": "vol2-places/11-houses.qmd",
    "The Twelfth House": "vol2-places/11-houses.qmd",
    
    # Joys
    "Planetary Joy": "vol2-places/12-joys.qmd",
    
    # Volume I: Planetary Delineations
    "Chapter 7: Essential Dignities": "vol1-foundations/04-luminaries.qmd",
    "Chapter 7a: Monomoiria": "vol1-foundations/04-luminaries.qmd",
    "Chapter 7b: The Fixed Stars": "vol1-foundations/04-luminaries.qmd",
    
    # Volume III: Aspects
    "Chapter 8: The Ptolemaic Aspects": "vol3-dynamics/14-aspects.qmd",
    "The Doctrine of Aspects": "vol3-dynamics/14-aspects.qmd",
    
    # Time Lords (Volume IV)
    "Chronocrator": "vol4-prediction/17-timelords.qmd",
    "Time-Lord": "vol4-prediction/17-timelords.qmd",
    "Firdaria": "vol4-prediction/17-timelords.qmd",
    "Profection": "vol4-prediction/18-profections.qmd",
    "Zodiacal Releasing": "vol4-prediction/19-zodiacal-releasing.qmd",
    "Loosing of the Bond": "vol4-prediction/19-zodiacal-releasing.qmd",
}

def read_source():
    """Read the complete source file."""
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def extract_sections(content):
    """Extract all major sections from the source content."""
    # Split by major headings (# or ##)
    sections = re.split(r'\n(?=#{1,2}\s+)', content)
    return sections

def get_target_file(section_text):
    """Determine which QMD file this section belongs to."""
    first_line = section_text.strip().split('\n')[0]
    
    for pattern, target in CHAPTER_MAPPING.items():
        if pattern.lower() in first_line.lower() or pattern.lower() in section_text[:500].lower():
            return target
    
    return None

def main():
    print("Reading source file...")
    content = read_source()
    
    print(f"Source file size: {len(content):,} characters")
    
    # Count words
    words = len(content.split())
    print(f"Source file word count: {words:,} words")
    print(f"Estimated pages (250 words/page): {words // 250} pages")
    
    sections = extract_sections(content)
    print(f"Found {len(sections)} sections")
    
    # Group sections by target file
    file_contents = {}
    
    for section in sections:
        target = get_target_file(section)
        if target:
            if target not in file_contents:
                file_contents[target] = []
            file_contents[target].append(section)
    
    print(f"\nMapped sections to {len(file_contents)} target files:")
    for target, sections in file_contents.items():
        total_words = sum(len(s.split()) for s in sections)
        print(f"  {target}: {len(sections)} sections, ~{total_words:,} words")
    
    # Now write content to target files
    print("\nWriting content to QMD files...")
    
    for target, sections in file_contents.items():
        target_path = VOLUMES_DIR / target
        
        # Combine sections
        combined = "\n\n".join(sections)
        
        # Clean up the content for Quarto
        combined = combined.replace('\\[', '[')
        combined = combined.replace('\\]', ']')
        combined = combined.replace('\\newpage', '')
        
        # Write to file
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(combined)
        
        print(f"  Wrote {len(combined):,} chars to {target}")
    
    print("\nMigration complete!")
    print("\nNow run: quarto render --to pdf")

if __name__ == "__main__":
    main()
