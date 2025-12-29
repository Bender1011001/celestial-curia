"""
The Celestial Curia - Book-as-Code Build Script
================================================
Ingests raw astrology text files, segments by headers, applies normalization,
converts citations, and outputs publication-ready Markdown chapters.
"""

import re
import os
from pathlib import Path


# ==================== CONFIGURATION ====================

BASE_DIR = Path(__file__).parent
SOURCE_DIR = BASE_DIR.parent  # Parent directory with all source .txt files
MANUSCRIPT_DIR = BASE_DIR / "manuscript"

# Source file paths (relative to SOURCE_DIR)
SOURCE_FILES = {
    "core_mechanics": "Traditional Astrology's Core Mechanics.txt",
    "binary_competency": "_The Binary Competency Framework of Classical Astrology_ Sect, Solar Proximity, and Bonatti's Considerations as Deterministic Rules of Planetary Engagement.txt",
    "ministerial_order": "_The Ministerial Order of Celestial Authority_ Ibn Ezra's Algorithm and the Calculus of Vitality.txt",
    "chronocrators": "The Nested Hierarchy of Chronocrators_ Dormancy, Activation, and the Sequential Unfolding of Natal Promise.txt",
    "medical": "The Inseparable Bond_ Medical Astrology's Integration of Celestial Cause and Physical Pathology.txt",
    "universal_causation": "# PART 8 EXTENDED_ UNIVERSAL CAUSATION AUDIT FOR DECEMBER 2025.txt",
    "monomoiria": "# Section Five Monomoiria—The Micro.txt",
    "arabic_parts": "Section_1_Arabic_Parts.md",
    "lunar_nodes": "Section_2_Lunar_Nodes.md",
    "fixed_stars": "Section_3_Fixed_Stars.md",
    "archetypal_baseline": "The Archetypal Baseline_ Thema Mundi, Aspect Natures, and the Philosophical Divide Between Egyptian and Ptolemaic Terms.txt",
    "celestial_hierarchies": "_The Hierarchy of Celestial Causation_ Universal and Particular Causes in Classical Astrology.txt",
    "comprehensive_treatment": "Comprehensive Treatment of Houses, Planetary Delineations, Dignities, and Aspects in Traditional Astrology.txt",
    "planetary_delineations": "Planetary Delineations From Ancient Sources.txt",
    "astrology_research": "Astrology Research and Analysis (1).txt",
    "improving_interpretation": "Improving Natal Chart Interpretation Guide (1).txt",
}


# ==================== TEXT CLEANING FUNCTIONS ====================

def clean_text(text):
    """Cleans up broken line wraps and common formatting artifacts."""
    if not text:
        return ""
    
    # Normalize escaped characters
    text = text.replace(r'\-', '-')
    text = text.replace(r'\#', '#')
    text = text.replace(r'\*', '*')
    text = text.replace(r'\&', '&')
    
    # Fix broken line wraps (word ending with letter, next line starts with lowercase)
    text = re.sub(r'(?<=[a-zA-Z,])\n(?=[a-z])', ' ', text)
    
    # Common OCR fixes
    ocr_fixes = {
        "positi ons": "positions",
        "Rena issance": "Renaissance",
        "intric ate": "intricate",
        "docum ent": "document",
        "process- ing": "processing",
        "htt ps://": "https://",
        "ht tps://": "https://",
        "wp- content": "wp-content",
    }
    for old, new in ocr_fixes.items():
        text = text.replace(old, new)
    
    # Generic hyphenation fix
    text = re.sub(r'([a-z])-\s+([a-z])', r'\1\2', text)
    
    return text


def standardize_terminology(text):
    """Replace deprecated terminology with standardized forms."""
    replacements = [
        # Essential Dignity context: Terms → Bounds
        (r'\bTerms\b(?=\s+(?:of|ruler|rulership|dignity|system|Egyptian|Ptolemaic))', 'Bounds'),
        (r'\bterm ruler\b', 'bound ruler'),
        (r'\bterm rulership\b', 'bound rulership'),
        # House terminology: Topoi → Places
        (r'\bTopoi\b', 'Places'),
        (r'\btopos\b', 'place'),
        # Hyleg standardization
        (r'\bApheta\b', 'Hyleg'),
        (r'\bHylaj\b', 'Hyleg'),
        # Alcocoden standardization
        (r'\bKadukhudāh\b', 'Alcocoden'),
        (r'\bKadkhudah\b', 'Alcocoden'),
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def apply_modern_filter(text):
    """Remove or reframe 20th-century psychological terminology."""
    # Direct replacements
    psychological_terms = {
        r'\bArchetype\b': 'Celestial Type',
        r'\barchetypal\b': 'celestial',
        r'\bSubconscious\b': 'Hidden Influence',
        r'\bsubconscious\b': 'hidden influence',
        r'\bEgo\b': 'Essential Self',
        r'\bego\b': 'essential self',
        r'\bEvolutionary\b': 'Sequential',
        r'\bevolutionary\b': 'sequential',
        r'\bPsychological Block\b': 'Impediment',
        r'\bpsychological block\b': 'impediment',
        r'\bPsychological\b': 'Temperamental',
        r'\bpsychological\b': 'temperamental',
    }
    
    for pattern, replacement in psychological_terms.items():
        text = re.sub(pattern, replacement, text)
    
    # Remove Jungian references entirely or mark as modern
    text = re.sub(r'\bJungian\b', '[modern interpretation]', text, flags=re.IGNORECASE)
    
    return text


def fix_report_phrasing(text):
    """Convert report-style phrasing to book-style."""
    report_phrases = {
        r'This report aims to': 'This book aims to',
        r'This report will': 'This book will',
        r'this report': 'this work',
        r'The research shows': 'The tradition demonstrates',
        r'We have found': 'The sources establish',
        r'Our analysis': 'The analysis',
    }
    
    for pattern, replacement in report_phrases.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def convert_citations_to_footnotes(text):
    """
    Convert [Number] citations to Markdown footnotes.
    Extracts references from the end of the document and inserts inline.
    """
    # Find reference section
    ref_patterns = [
        r'\n(?:Works cited|References|REFERENCES|Bibliography)\s*\n',
        r'\n\[1\]\s+\[',  # Backup pattern for numbered reference lists
    ]
    
    ref_section_start = None
    for pattern in ref_patterns:
        match = re.search(pattern, text)
        if match:
            ref_section_start = match.start()
            break
    
    if not ref_section_start:
        return text  # No references found
    
    main_text = text[:ref_section_start]
    ref_text = text[ref_section_start:]
    
    # Parse references: [N] URL or text
    ref_dict = {}
    ref_pattern = r'\[(\d+)\]\s*\[?([^\n\[]+)'
    for match in re.finditer(ref_pattern, ref_text):
        num = match.group(1)
        citation = match.group(2).strip().rstrip(']')
        # Clean up URL artifacts
        citation = re.sub(r'\s*-\s*', ' - ', citation)
        ref_dict[num] = citation
    
    # Replace inline citations with footnotes
    def replace_citation(match):
        num = match.group(1)
        if num in ref_dict:
            return f'^[{ref_dict[num]}]'
        return match.group(0)  # Keep original if not found
    
    main_text = re.sub(r'\[(\d+)\]', replace_citation, main_text)
    
    return main_text


def normalize_headers(text):
    """Ensure proper header hierarchy."""
    lines = text.split('\n')
    result = []
    
    for line in lines:
        # Remove excessive hash marks
        if line.startswith('#####'):
            line = '###' + line[5:]
        result.append(line)
    
    return '\n'.join(result)


def format_tables(text):
    """Attempt to fix malformed Markdown tables."""
    # This is a basic pass - complex table fixing may need manual review
    lines = text.split('\n')
    result = []
    in_table = False
    
    for i, line in enumerate(lines):
        # Detect potential table rows (tab or multiple spaces between values)
        if '\t' in line and not line.startswith('#'):
            # Convert tabs to pipes
            parts = [p.strip() for p in line.split('\t') if p.strip()]
            if len(parts) >= 2:
                if not in_table:
                    in_table = True
                    # Add header separator if this looks like a header
                    result.append('| ' + ' | '.join(parts) + ' |')
                    result.append('|' + '---|' * len(parts))
                else:
                    result.append('| ' + ' | '.join(parts) + ' |')
                continue
        else:
            in_table = False
        
        result.append(line)
    
    return '\n'.join(result)


def full_clean_pass(text):
    """Apply all cleaning and normalization passes."""
    text = clean_text(text)
    text = standardize_terminology(text)
    text = apply_modern_filter(text)
    text = fix_report_phrasing(text)
    text = normalize_headers(text)
    text = format_tables(text)
    text = convert_citations_to_footnotes(text)
    return text


# ==================== CONTENT EXTRACTION ====================

def read_source_file(filename):
    """Read a source file with proper encoding handling."""
    filepath = SOURCE_DIR / filename
    if not filepath.exists():
        print(f"  ⚠ Warning: Source file not found: {filename}")
        return ""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()


def extract_section(content, start_pattern, end_pattern=None):
    """Extract text between patterns using regex."""
    def to_regex(s):
        clean = re.escape(s)
        return clean.replace(r'\ ', r'\s+')
    
    start_regex = to_regex(start_pattern)
    match_start = re.search(start_regex, content, re.IGNORECASE | re.DOTALL)
    
    if not match_start:
        return ""
    
    start_idx = match_start.end()
    
    if end_pattern:
        end_regex = to_regex(end_pattern)
        match_end = re.search(end_regex, content[start_idx:], re.IGNORECASE | re.DOTALL)
        if match_end:
            end_idx = start_idx + match_end.start()
            return content[start_idx:end_idx].strip()
    
    return content[start_idx:].strip()


# ==================== CHAPTER BUILDERS ====================

def build_chapter_01():
    """Part I, Chapter 1: The Philosophical Engine"""
    print("  Building 01_Philosophical_Engine.md...")
    
    content = []
    content.append("# Part I: Foundations of the Celestial Science\n")
    content.append("## Chapter 1: The Philosophical Engine\n")
    content.append("""
### Introduction: The Architecture of Determinism

The study of traditional astrology—encompassing the Hellenistic, Arabic, and Latin Medieval traditions—is fundamentally a study of celestial mechanics applied to human destiny. Unlike the psychological astrology of the 20th century, which often prioritizes the subjective internal experience and the potential for character transformation, traditional astrology operates as a rigorous, deterministic system of physics. It posits a universe where the quality of time is measurable, the duration of life is calculable, and the condition of a planet is a forensic fact rather than a symbolic feeling.

To practice this art as it was intended by figures such as Vettius Valens, Claudius Ptolemy, and Guido Bonatti requires more than intuition; it demands a mastery of the "mechanical gears" that drive the system. These gears are the algorithms of vitality, the geometry of the primordial "World Chart" (Thema Mundi), the literal spatial definitions of the houses (Places), and the precise error-checking protocols of forensic analysis.
""")
    
    # Add from core mechanics
    core_text = read_source_file(SOURCE_FILES["core_mechanics"])
    if core_text:
        intro_section = extract_section(core_text, "Introduction: The Architecture of Determinism", "Part 1:")
        if intro_section:
            content.append(full_clean_pass(intro_section))
    
    # Add from celestial hierarchies
    hier_text = read_source_file(SOURCE_FILES["celestial_hierarchies"])
    if hier_text:
        content.append("\n### The Hierarchy of Celestial Causation\n")
        hier_section = extract_section(hier_text, "Executive Summary", "PART I:")
        if hier_section:
            content.append(full_clean_pass(hier_section))
    
    return '\n'.join(content)


def build_chapter_02():
    """Part I, Chapter 2: The Archetypal Baseline (Thema Mundi)"""
    print("  Building 02_Archetypal_Baseline.md...")
    
    content = []
    content.append("## Chapter 2: The Archetypal Baseline — Thema Mundi\n")
    
    # Add from archetypal baseline source
    arch_text = read_source_file(SOURCE_FILES["archetypal_baseline"])
    if arch_text:
        content.append(full_clean_pass(arch_text))
    else:
        # Fallback from core mechanics
        core_text = read_source_file(SOURCE_FILES["core_mechanics"])
        if core_text:
            thema_section = extract_section(core_text, "Part 2: Thema Mundi", "Part 3:")
            if thema_section:
                content.append(full_clean_pass(thema_section))
    
    return '\n'.join(content)


def build_chapter_03():
    """Part I, Chapter 3: The Doctrine of Sect"""
    print("  Building 03_Doctrine_of_Sect.md...")
    
    content = []
    content.append("## Chapter 3: The Doctrine of Sect (Hairesis)\n")
    
    binary_text = read_source_file(SOURCE_FILES["binary_competency"])
    if binary_text:
        # Extract sect section
        sect_section = extract_section(binary_text, "PART I: THE DOCTRINE OF SECT", "PART II:")
        if sect_section:
            content.append(full_clean_pass(sect_section))
    
    return '\n'.join(content)


def build_chapter_04():
    """Part II, Chapter 4: Essential Dignity"""
    print("  Building 04_Essential_Dignity.md...")
    
    content = []
    content.append("# Part II: The Celestial State\n")
    content.append("## Chapter 4: Essential Dignity — Rulership, Exaltation, and Bounds\n")
    
    # Add from ministerial order (dignity scoring)
    min_text = read_source_file(SOURCE_FILES["ministerial_order"])
    if min_text:
        dignity_section = extract_section(min_text, "The Dignity Scoring System", "Aggregation Across")
        if dignity_section:
            content.append(full_clean_pass(dignity_section))
    
    # Add monomoiria section
    mono_text = read_source_file(SOURCE_FILES["monomoiria"])
    if mono_text:
        content.append("\n### Monomoiria: Degree Rulership\n")
        # Clean header
        mono_text = mono_text.replace("# Section Five: Monomoiria—The Micro-Dignity of Individual Degree Rulership", "")
        content.append(full_clean_pass(mono_text))
    
    return '\n'.join(content)


def build_chapter_05():
    """Part II, Chapter 5: Accidental Dignity"""
    print("  Building 05_Accidental_Dignity.md...")
    
    content = []
    content.append("## Chapter 5: Accidental Dignity — House Placement and Solar Proximity\n")
    
    binary_text = read_source_file(SOURCE_FILES["binary_competency"])
    if binary_text:
        # Extract solar proximity section
        solar_section = extract_section(binary_text, "PART II: FORENSIC CONDITIONS OF SOLAR PROXIMITY", "PART III:")
        if solar_section:
            content.append(full_clean_pass(solar_section))
    
    # Add accidental dignity from ministerial order
    min_text = read_source_file(SOURCE_FILES["ministerial_order"])
    if min_text:
        acc_section = extract_section(min_text, "Accidental Dignity Modifiers", "Interpretation:")
        if acc_section:
            content.append("\n### House-Based Scoring\n")
            content.append(full_clean_pass(acc_section))
    
    return '\n'.join(content)


def build_chapter_06():
    """Part II, Chapter 6: Planetary Delineations"""
    print("  Building 06_Planetary_Delineations.md...")
    
    content = []
    content.append("## Chapter 6: Planetary Delineations by Sign\n")
    
    delin_text = read_source_file(SOURCE_FILES["planetary_delineations"])
    if delin_text:
        content.append(full_clean_pass(delin_text))
    
    # Add from comprehensive treatment
    comp_text = read_source_file(SOURCE_FILES["comprehensive_treatment"])
    if comp_text:
        planets_section = extract_section(comp_text, "Planetary Delineations", "Dignities")
        if planets_section:
            content.append(full_clean_pass(planets_section))
    
    return '\n'.join(content)


def build_chapter_07():
    """Part II, Chapter 7: Stars and Nodes"""
    print("  Building 07_Stars_and_Nodes.md...")
    
    content = []
    content.append("## Chapter 7: The Fixed Stars and Lunar Nodes\n")
    
    # Add lunar nodes
    nodes_text = read_source_file(SOURCE_FILES["lunar_nodes"])
    if nodes_text:
        content.append("### The Lunar Nodes (Caput et Cauda Draconis)\n")
        # Clean header
        nodes_text = nodes_text.replace("# Section II: The Lunar Nodes (Caput and Cauda Draconis)", "")
        content.append(full_clean_pass(nodes_text))
    
    # Add fixed stars
    stars_text = read_source_file(SOURCE_FILES["fixed_stars"])
    if stars_text:
        content.append("\n### The Fixed Stars (The Eighth Sphere)\n")
        stars_text = stars_text.replace("# Section III: Expanded Fixed Star Catalogue (The Eighth Sphere)", "")
        content.append(full_clean_pass(stars_text))
    
    return '\n'.join(content)


def build_chapter_08():
    """Part III, Chapter 8: The Twelve Places"""
    print("  Building 08_Twelve_Places.md...")
    
    content = []
    content.append("# Part III: The Terrestrial State\n")
    content.append("## Chapter 8: The Twelve Places (House Significations)\n")
    
    core_text = read_source_file(SOURCE_FILES["core_mechanics"])
    if core_text:
        houses_section = extract_section(core_text, "Part 3: Complete House Topoi", "Part 4:")
        if houses_section:
            content.append(full_clean_pass(houses_section))
    
    return '\n'.join(content)


def build_chapter_09():
    """Part III, Chapter 9: Aspects and Geometry"""
    print("  Building 09_Aspects_and_Geometry.md...")
    
    content = []
    content.append("## Chapter 9: Aspects and Celestial Geometry\n")
    
    binary_text = read_source_file(SOURCE_FILES["binary_competency"])
    if binary_text:
        # Bonatti's considerations
        bonatti_section = extract_section(binary_text, "PART III: BONATTI'S 146 CONSIDERATIONS", "SYNTHESIS:")
        if bonatti_section:
            content.append("### Bonatti's Considerations: Disqualifying Conditions\n")
            content.append(full_clean_pass(bonatti_section))
    
    # Aspects from core mechanics
    core_text = read_source_file(SOURCE_FILES["core_mechanics"])
    if core_text:
        aspect_section = extract_section(core_text, "2B. The Derivation of Aspect Natures", "2C.")
        if aspect_section:
            content.append("\n### The Nature of Aspects\n")
            content.append(full_clean_pass(aspect_section))
    
    return '\n'.join(content)


def build_chapter_10():
    """Part III, Chapter 10: The Hermetic Lots"""
    print("  Building 10_Hermetic_Lots.md...")
    
    content = []
    content.append("## Chapter 10: The Hermetic Lots (Arabic Parts)\n")
    
    lots_text = read_source_file(SOURCE_FILES["arabic_parts"])
    if lots_text:
        # Clean header
        lots_text = lots_text.replace("# Section I: Complete Catalogue of Arabic Parts (Lots)", "")
        content.append(full_clean_pass(lots_text))
    
    return '\n'.join(content)


def build_chapter_11():
    """Part IV, Chapter 11: Almuten Figuris"""
    print("  Building 11_Almuten_Figuris.md...")
    
    content = []
    content.append("# Part IV: The Algorithms of Fate\n")
    content.append("## Chapter 11: The Almuten Figuris — Captain of the Soul\n")
    
    min_text = read_source_file(SOURCE_FILES["ministerial_order"])
    if min_text:
        almuten_section = extract_section(min_text, "PART I: THE IBN EZRA ALGORITHM", "PART II:")
        if almuten_section:
            content.append(full_clean_pass(almuten_section))
    
    return '\n'.join(content)


def build_chapter_12():
    """Part IV, Chapter 12: Calculus of Vitality"""
    print("  Building 12_Calculus_of_Vitality.md...")
    
    content = []
    content.append("## Chapter 12: The Calculus of Vitality — Hyleg and Alcocoden\n")
    
    # From ministerial order
    min_text = read_source_file(SOURCE_FILES["ministerial_order"])
    if min_text:
        vitality_section = extract_section(min_text, "PART II: THE CALCULUS OF VITALITY", "PART III:")
        if vitality_section:
            content.append(full_clean_pass(vitality_section))
    
    # From core mechanics
    core_text = read_source_file(SOURCE_FILES["core_mechanics"])
    if core_text:
        hyleg_section = extract_section(core_text, "Part 1: The Hyleg and Alcocoden", "Part 2:")
        if hyleg_section:
            content.append("\n### The Complete Algorithm\n")
            content.append(full_clean_pass(hyleg_section))
    
    return '\n'.join(content)


def build_chapter_13():
    """Part V, Chapter 13: Hierarchy of Time"""
    print("  Building 13_Hierarchy_of_Time.md...")
    
    content = []
    content.append("# Part V: The Chronocrators — Time-Lord Systems\n")
    content.append("## Chapter 13: The Nested Hierarchy of Chronocrators\n")
    
    chrono_text = read_source_file(SOURCE_FILES["chronocrators"])
    if chrono_text:
        hierarchy_section = extract_section(chrono_text, "PART I: THE PRINCIPLE OF DORMANCY", "PART II:")
        if hierarchy_section:
            content.append(full_clean_pass(hierarchy_section))
        
        nested_section = extract_section(chrono_text, "PART II: THE NESTED HIERARCHY", "PART III:")
        if nested_section:
            content.append("\n### The Three-Level Hierarchy\n")
            content.append(full_clean_pass(nested_section))
    
    return '\n'.join(content)


def build_chapter_14():
    """Part V, Chapter 14: Zodiacal Releasing"""
    print("  Building 14_Zodiacal_Releasing.md...")
    
    content = []
    content.append("## Chapter 14: Zodiacal Releasing (Aphesis)\n")
    
    chrono_text = read_source_file(SOURCE_FILES["chronocrators"])
    if chrono_text:
        zr_section = extract_section(chrono_text, "B. Zodiacal Releasing:", "C. Firdaria:")
        if zr_section:
            content.append(full_clean_pass(zr_section))
        
        # Loosing of the Bond
        lob_section = extract_section(chrono_text, "PART III: THE LOOSING OF THE BOND", "PART IV:")
        if lob_section:
            content.append("\n### The Loosing of the Bond\n")
            content.append(full_clean_pass(lob_section))
    
    return '\n'.join(content)


def build_chapter_15():
    """Part V, Chapter 15: Firdaria"""
    print("  Building 15_Firdaria.md...")
    
    content = []
    content.append("## Chapter 15: Firdaria — The Planetary Periods\n")
    
    chrono_text = read_source_file(SOURCE_FILES["chronocrators"])
    if chrono_text:
        firdaria_section = extract_section(chrono_text, "PART IV: DAY VS. NIGHT FIRDARIA", "PART V:")
        if firdaria_section:
            content.append(full_clean_pass(firdaria_section))
    
    # Also from core mechanics
    core_text = read_source_file(SOURCE_FILES["core_mechanics"])
    if core_text:
        firdaria_core = extract_section(core_text, "7B. Firdaria", "Conclusion")
        if firdaria_core:
            content.append("\n### The Chaldean Sequence\n")
            content.append(full_clean_pass(firdaria_core))
    
    return '\n'.join(content)


def build_chapter_16():
    """Part V, Chapter 16: Annual Profections"""
    print("  Building 16_Annual_Profections.md...")
    
    content = []
    content.append("## Chapter 16: Annual Profections — The Lord of the Year\n")
    
    chrono_text = read_source_file(SOURCE_FILES["chronocrators"])
    if chrono_text:
        profections_section = extract_section(chrono_text, "D. Annual Profections:", "PART III:")
        if profections_section:
            content.append(full_clean_pass(profections_section))
        
        # Lord of the Year as filter
        lord_section = extract_section(chrono_text, "PART V: THE LORD OF THE YEAR", "PART VI:")
        if lord_section:
            content.append("\n### The Lord of the Year as Transit Filter\n")
            content.append(full_clean_pass(lord_section))
    
    return '\n'.join(content)


def build_chapter_18():
    """Part VI, Chapter 18: Medical Astrology"""
    print("  Building 18_Medical_Astrology.md...")
    
    content = []
    content.append("# Part VI: Applied Astrology\n")
    content.append("## Chapter 18: Medical Astrology — Decumbiture and Critical Days\n")
    
    medical_text = read_source_file(SOURCE_FILES["medical"])
    if medical_text:
        content.append(full_clean_pass(medical_text))
    
    return '\n'.join(content)


def build_chapter_19():
    """Part VI, Chapter 19: Mundane Astrology"""
    print("  Building 19_Mundane_Astrology.md...")
    
    content = []
    content.append("## Chapter 19: Mundane Astrology — Eclipses and Universal Causation\n")
    
    mundane_text = read_source_file(SOURCE_FILES["universal_causation"])
    if mundane_text:
        content.append(full_clean_pass(mundane_text))
    
    return '\n'.join(content)


def build_bibliography():
    """Back Matter: Bibliography"""
    print("  Building bibliography.md...")
    
    content = []
    content.append("# Bibliography and Sources\n")
    content.append("""
## Primary Sources

- **Ptolemy, Claudius.** *Tetrabiblos.* Translated by F.E. Robbins. Loeb Classical Library.
- **Valens, Vettius.** *Anthology.* Translated by Mark Riley.
- **Bonatti, Guido.** *Liber Astronomiae.* Translated by Benjamin Dykes.
- **Maternus, Firmicus.** *Mathesis.* Translated by Jean Rhys Bram.
- **Ibn Ezra, Abraham.** *The Beginning of Wisdom.* Translated by Meira Epstein.
- **Lilly, William.** *Christian Astrology.* 1647.

## Secondary Sources and Commentary

- Brady, Bernadette. *The Hyleg and Alcocoden.* [PDF]
- Zoller, Robert. *The Arabic Parts in Astrology.*
- Brennan, Chris. *Hellenistic Astrology: The Study of Fate and Fortune.*
- George, Demetra. *Ancient Astrology in Theory and Practice.*

---

*This bibliography is not exhaustive. Individual chapters contain inline citations to specific sources.*
""")
    
    return '\n'.join(content)


# ==================== MAIN BUILD FUNCTION ====================

def build_manuscript():
    """Main function to build all manuscript chapters."""
    print("\n" + "="*60)
    print("THE CELESTIAL CURIA - BOOK BUILD")
    print("="*60 + "\n")
    
    # Define output mappings
    chapters = [
        ("01_Part_I_Foundations", "01_Philosophical_Engine.md", build_chapter_01),
        ("01_Part_I_Foundations", "02_Archetypal_Baseline.md", build_chapter_02),
        ("01_Part_I_Foundations", "03_Doctrine_of_Sect.md", build_chapter_03),
        ("02_Part_II_Celestial_State", "04_Essential_Dignity.md", build_chapter_04),
        ("02_Part_II_Celestial_State", "05_Accidental_Dignity.md", build_chapter_05),
        ("02_Part_II_Celestial_State", "06_Planetary_Delineations.md", build_chapter_06),
        ("02_Part_II_Celestial_State", "07_Stars_and_Nodes.md", build_chapter_07),
        ("03_Part_III_Terrestrial_State", "08_Twelve_Places.md", build_chapter_08),
        ("03_Part_III_Terrestrial_State", "09_Aspects_and_Geometry.md", build_chapter_09),
        ("03_Part_III_Terrestrial_State", "10_Hermetic_Lots.md", build_chapter_10),
        ("04_Part_IV_Algorithms", "11_Almuten_Figuris.md", build_chapter_11),
        ("04_Part_IV_Algorithms", "12_Calculus_of_Vitality.md", build_chapter_12),
        ("05_Part_V_Chronocrators", "13_Hierarchy_of_Time.md", build_chapter_13),
        ("05_Part_V_Chronocrators", "14_Zodiacal_Releasing.md", build_chapter_14),
        ("05_Part_V_Chronocrators", "15_Firdaria.md", build_chapter_15),
        ("05_Part_V_Chronocrators", "16_Annual_Profections.md", build_chapter_16),
        ("06_Part_VI_Applied_Astrology", "18_Medical_Astrology.md", build_chapter_18),
        ("06_Part_VI_Applied_Astrology", "19_Mundane_Astrology.md", build_chapter_19),
        ("99_Back_Matter", "bibliography.md", build_bibliography),
    ]
    
    success_count = 0
    for part_dir, filename, builder_func in chapters:
        try:
            content = builder_func()
            if content:
                output_path = MANUSCRIPT_DIR / part_dir / filename
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ Written: {part_dir}/{filename}")
                success_count += 1
            else:
                print(f"  ⚠ Empty content for: {filename}")
        except Exception as e:
            print(f"  ✗ Error building {filename}: {e}")
    
    print("\n" + "="*60)
    print(f"BUILD COMPLETE: {success_count}/{len(chapters)} chapters generated")
    print("="*60 + "\n")
    
    print("Next steps:")
    print("  1. Review generated .md files in /manuscript/")
    print("  2. Run Pandoc to compile PDF:")
    print("     pandoc metadata.yaml manuscript/**/*.md -o The_Celestial_Curia.pdf --toc --number-sections")
    print()


if __name__ == "__main__":
    build_manuscript()
