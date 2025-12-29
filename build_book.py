"""
Script to reorganize the astrology content into a proper book structure.
Parses the raw merged markdown and restructures it into chapters.
"""
import re
import os

def clean_text(text):
    """
    Cleans up broken line wraps and fixing formatting artifacts.
    """
    if not text:
        return ""
    
    # Normalize escaped characters first (common in some PDF conversions)
    text = text.replace(r'\-', '-')
    text = text.replace(r'\#', '#')
    text = text.replace(r'\*', '*')
    text = text.replace(r'\&', '&')
        
    # Fix broken line wraps: Join lines where end is word char and next is lowercase
    # Example: "The quick brown\nfox" -> "The quick brown fox"
    # But be careful not to merge list items or headers
    text = re.sub(r'(?<=[a-zA-Z,])\n(?=[a-z])', ' ', text)
    
    # COMMON OCR FIXES
    # Specific words reported by user
    text = text.replace("positi ons", "positions")
    text = text.replace("Rena issance", "Renaissance")
    text = text.replace("intric ate", "intricate")
    text = text.replace("docum ent", "document")
    text = text.replace("process- ing", "processing")
    
    # Fix URL artifacts
    text = text.replace("htt ps://", "https://")
    text = text.replace("ht tps://", "https://")
    text = text.replace("wp- content", "wp-content")
    
    # Generic hyphenation fix
    text = re.sub(r'([a-z])-\s+([a-z])', r'\1\2', text)
    
    return text

def extract_section_regex(content, start_pattern, end_pattern=None):
    """
    Extracts text between start_pattern and end_pattern using regex to allow for 
    whitespace variances/concatenation.
    """
    # Find start
    # Using re.DOTALL so . matches newlines, and re.IGNORECASE just in case
    # escaping pattern to be safe, but replacing space with \s+ to handle line breaks/spaces
    
    def to_regex(s):
        # Escape special chars, then replace spaces with \s+ to match multiline headers
        clean = re.escape(s)
        return clean.replace(r'\ ', r'\s+')

    start_regex = to_regex(start_pattern)
    match_start = re.search(start_regex, content, re.IGNORECASE | re.DOTALL)
    
    if not match_start:
        print(f"Warning: Start Pattern not found: '{start_pattern}'")
        return ""
    
    start_idx = match_start.end()
    
    if end_pattern:
        end_regex = to_regex(end_pattern)
        match_end = re.search(end_regex, content[start_idx:], re.IGNORECASE | re.DOTALL)
        
        if match_end:
            # content[start_idx:] is the slice, so we add start_idx to get absolute position
            end_idx = start_idx + match_end.start()
            extracted = content[start_idx:end_idx]
        else:
            print(f"Warning: End Pattern not found: '{end_pattern}' - taking rest of content.")
            extracted = content[start_idx:]
    else:
        extracted = content[start_idx:]
        
    return clean_text(extracted.strip())

def main():
    source_path = r"c:\Users\admin\Downloads\Astrology Files-20251228T075743Z-1-001\Astrology Files\pdf\Astrology_Complete_Book.md"
    output_path = r"c:\Users\admin\Downloads\Astrology Files-20251228T075743Z-1-001\Astrology Files\The_Traditional_Astrologers_Complete_Reference.md"

    with open(source_path, 'r', encoding='utf-8') as f:
        full_content = f.read()

    # --- DEFINE MARKERS FOR SECTIONS ---
    # Based on manual inspection of the source file
    
    # SOURCE 1: The Delineation Codex
    START_CODEX_INTRO = "The Philological and Technical Framework"
    START_P1_SIGNS = "Part 1: Planets in Signs"
    START_P2_HOUSES = "Part 2: Planets in Houses"
    START_P3_ASPECTS = "Part 3: Aspects with Sect Modulation"
    START_P4_CASES = "Part 4: Worked Historical Examples"
    
    # SOURCE 2: The Celestial Mirror
    START_MIRROR_INTRO = "Introduction: The Architecture of Destiny"
    START_ORIGINS = "Historical Origins and the Evolution"
    START_EGYPTIAN = "The Egyptian Contribution"
    START_HELLENISTIC = "The Hellenistic Synthesis"
    START_INDIA = "The Transmission to India"
    START_MECHANICS = "Fundamental Principles: The Mechanics"
    START_COMPARATIVE = "Comparative Systems Analysis"
    
    # SOURCE 3: Missing Foundational Codex
    START_HOUSES_DEEP = "The Traditional Significations of the Twelve Houses"
    START_PLANETS_DEEP = "The Complete Planetary Delineation Codex"
    START_DIGNITIES = "Comprehensive Tables of Essential Dignities"
    START_ASPECTS_DEEP = "The Ptolemaic Aspects"
    
    # SOURCE 4: Compendium
    START_COMPENDIUM_INTRO = "The Astrology Compendium"
    START_PHILOSOPHY_CONTEXT = "Philosophical and Cultural Context"
    START_CRITIQUE = "Scientific, Mathematical, and Psychological"
    
    # --- ASSEMBLE BOOK ---

    book = []
    
    # FRONT MATTER
    book.append("# The Traditional Astrologer's Complete Reference\n## A Reconstruction of Pre-1700 Celestial Science\n\n---\n")
    book.append("# Table of Contents\n\n(Generated automatically based on structure)\n\n---\n")
    book.append("# Foreword\n\nThe documents assembled herein represent a comprehensive synthesis of pre-1700 astrological tradition...\n\n---\n")

    # --- CLEANING HELPERS ---
    def clean_chapter_content(text):
        if not text: return ""
        # Remove source numbering like "2.1 ", "1. ", "2.2 ", "**6\. " at start of lines
        # Handles optional bold/italic markers AND escaped dots
        text = re.sub(r'^(\*\*|__)?\d+(\\?\.\d+)*\\?\.?\s+', '', text, flags=re.MULTILINE)
        return text

    # --- NEW CONTENT BLOCKS (USER SUPPLIED GAPS) ---
    
    TEXT_SUBSTITUTE_KING = """
### The Substitute King Protocol (Shar Puhi)
The "Shar Puhi" ritual reveals the transactional nature of Mesopotamian fate. If an eclipse threatened the King (e.g., Sun in an angle), the omens were not viewed as absolute but as a celestial warrant. The King would abdicate, placing a commoner (often a criminal or prisoner) on the throne to "absorb" the eclipse's malefic decree. After the danger passed (usually 100 days), the substitute was executed, satisfying the celestial debt with blood while preserving the royal line. This proves that ancient fate was jurisprudential—a legal obligation that could be transferred.
"""

    TEXT_OMEN_GEO = """
### The Legal Binding of Quadrants (Mundane Geography)
In the Enuma Anu Enlil, lunar eclipses are not general threats but targeted legal decrees based on the obscured quadrant of the Moon. This provides the "Targeting Logic" for mundane predictions:
*   **Quadrant I (South):** Akkad (Babylonia).
*   **Quadrant II (East):** Elam (Persia).
*   **Quadrant III (West):** Amurru (Syria).
*   **Quadrant IV (North):** Subartu (Assyria).
"""

    TEXT_TERMS_LOGIC = """
### The Socio-Biological Rationale of the Terms
The Egyptian Terms system follows a distinct logic of entropy. Note that the malefics (Mars and Saturn) are consistently placed at the *end* of the signs (the final degrees). This reflects the empirical reality that all physical cycles—whether biological, political, or material—conclude with decay (Saturn) or severance (Mars). The "Terms" differ from the "Signs" because they map the *process* of a planet moving through a domain, inevitably encountering the forces of entropy as it concludes its journey.
"""

    TEXT_ALMUTEN_SCALE = """
### The Detailed Almuten Algorithm (Weighted Accidental Dignity)
The calculation of the Almuten Figuris requires a precise scoring of Accidental Dignity based on house placement and temporal rulership. This point-summing method (Ibn Ezra) identifies the "Guardian of the Chart":

**1. House-Based Scores:**
*   **1st House:** +12 points
*   **10th House:** +11 points
*   **7th House:** +10 points
*   **4th House:** +9 points
*   **11th House:** +8 points
*   **5th House:** +7 points
*   **2nd House:** +6 points
*   **9th House:** +5 points
*   **8th House:** +4 points
*   **3rd House:** +3 points
*   **12th House:** +2 points
*   **6th House:** +1 point

**2. Temporal Rulership:**
*   **Ruler of the Day:** +7 points
*   **Ruler of the Hour:** +6 points
(Based on the Chaldean Order of planetary hours).
"""

    TEXT_VITALITY_TABLE = """
### The Calculus of Vitality: Planetary Years
To determine the potential lifespan (Hyleg/Alcocoden), one must use the Great, Mean, and Least years of the planets. The Alcocoden (Guardian of Life) awards years based on its condition.

| Planet  | Great Years | Mean Years | Least (Lesser) Years |
| :--- | :--- | :--- | :--- |
| **Saturn**  | 57 | 43.5 | 30 |
| **Jupiter** | 79 | 45.5 | 12 |
| **Mars**    | 66 | 40.5 | 15 |
| **Sun**     | 120| 69.5 | 19 |
| **Venus**   | 82 | 45   | 8  |
| **Mercury** | 76 | 48   | 20 |
| **Moon**    | 108| 66.5 | 25 |

**Witnessing Modifiers:**
*   **Benefics (Jupiter/Venus):** If aspecting the Alcocoden, add their *Lesser Years* regarding the type of aspect (Conjunction/Trine/Sextile). If weak, add only months or weeks.
*   **Malefics (Saturn/Mars):** If aspecting (Square/Opposition), subtract their *Lesser Years* (or months/weeks) from the total vitality.
"""

    TEXT_LOOSING_BOND = """
### Loosing of the Bond: Temporal Thresholds
In Zodiacal Releasing (Aphesis), the "Loosing of the Bond" (LB) represents a major structural shift in the life narrative. This jump to the opposing sign only occurs in signs where the **Planetary Minor Years exceed 17.5 years**.

**Thresholds for Major Reversals:**
*   **Cancer (Moon):** LB occurs at **25 years**.
*   **Leo (Sun):** LB occurs at **19 years**.
*   **Capricorn/Aquarius (Saturn):** LB occurs at **30 years**.
*   **Gemini/Virgo (Mercury):** LB occurs at **20 years**.
*   *Note: Signs ruled by Jupiter (12), Mars (15), and Venus (8) do not trigger a Loosing of the Bond because their periods represent a single "loop" under the 17.5-year threshold.*
"""

    TEXT_MEDICAL_GALEN = """
### Medical Mechanics: Galen's 16-Sided Figure
While the 7, 14, and 21-day Lunar cycles provide the baseline for critical days, advanced medical astrology employs **Galen's 16-Sided Figure**. This algorithm uses **22.5° increments** (half-semisquares) to track rapid, acute changes in the decumbiture chart. This higher resolution is essential for tracking fevers (like malaria) where the crisis points shift faster than the standard lunar phases allow, marking critical windows for intervention.
"""

    # --- NEW GAP CONTENT BLOCKS (TIER 2) ---

    TEXT_NODES = """
## Chapter 6a: The Lunar Nodes (Caput et Cauda Draconis)

The Lunar Nodes represent the intersection points of the Moon's orbit with the Ecliptic, functioning as powerful vortices of intake and expulsion.

### The North Node (Caput Draconis)
*   **Nature:** Jupiterian/Venusian but compulsive.
*   **Function:** Intake, amplification, greed, materialization. Where the North Node falls, the native experiences an insatiable hunger to consume and grow, often manifesting as worldly success but potentially leading to excess.

### The South Node (Cauda Draconis)
*   **Nature:** Saturnine/Martial and purifying.
*   **Function:** Expulsion, diminution, spirituality, loss. Where the South Node falls, the native experiences a decrease in material attachment, often signifying talents brought from the past but which must now be released or spiritualized.

### Nodal Axis Delineation
*   **Nodes in Angles:** Fated events affecting the life direction.
*   **Nodes in Succedent/Cadent:** Psychological complexes and background influences.
*   **Bendings:** Planets squaring the Nodal Axis are under extreme tension (skipped steps).
"""

    TEXT_FIXED_STARS = """
## Chapter 7b: The Fixed Stars and Constellations

Beyond the planetary spheres lie the Fixed Stars, which operate with intense, binary power—bestowing either eminence or ruin without the modulation of the planets.

### The Royal Stars (Watchers of the Directions)
1.  **Aldebaran (9° Gemini):** Watcher of the East. Mars/Venus nature. Bestows honor and integrity, but falls if integrity is compromised.
2.  **Regulus (29° Leo/0° Virgo):** Watcher of the North. Mars/Jupiter nature. Bestows great power and authority, but warns against revenge.
3.  **Antares (9° Sagittarius):** Watcher of the West. Mars/Jupiter nature. Extreme intensity and success, but danger of self-destruction/obsession.
4.  **Fomalhaut (3° Pisces):** Watcher of the South. Venus/Mercury nature. Artistic and spiritual eminence, but warns against corruption.

### Other Critical Stars
*   **Algol (26° Taurus):** The Demon Star. Saturn/Jupiter nature. Associated with beheading (losing one's head), intense passion, and protection from evil if mastered.
*   **Spica (23° Libra):** The Ear of Corn. Venus/Mars nature. Brilliant gifts, protection, and success.
*   **Sirius (14° Cancer):** The Dog Star. Jupiter/Mars nature. Burning ambition and mundane renown.

**Orbs:** 
*   **1st Magnitude:** 2° 30'
*   **2nd Magnitude:** 1° 30'
*   **Conjunctions Only:** Traditional doctrine prioritizes conjunctions (especially parans) over aspects.
"""

    TEXT_ANTISCIA_RECEPTION = """
### Antiscia and Contra-Antiscia (Shadow Points)
Mirror points across the Solstice Axis (0° Cancer/0° Capricorn).
*   **Antiscia:** Planets equidistant from the solstice axis "see" each other. Equivalent to a Conjunction (hidden connection).
*   **Contra-Antiscia:** Planets opposite the Antiscion point. Equivalent to an Opposition.

### Reception Mechanisms
*   **Mutual Reception:** Two planets in each other's domiciles. They "exchange" roles, assisting each other out of difficulties.
*   **Mixed Reception:** Reception by Exaltation, Triplicity, or Term. Lesser assistance but still valid mitigation.
*   **Rescue:** A planet receiving a malefic aspect from a planet it receives (in its dignity) prevents the worst of the harm.
"""

    TEXT_ACCIDENTAL_DIG = """
### Accidental Dignity Assessment
While Essential Dignity describes the *quality* of a planet, Accidental Dignity describes its *strength to act*.

**1. Motion:**
*   **Direct:** Normal capacity.
*   **Retrograde:** Internalized, delayed, or contrary psychological expression. Malefics become more unpredictable; Benefics less helpful.
*   **Stationary:** Extreme intensity and focus (Direct or Retrograde).
*   **Speed:** Fast (acting quickly/impulsively) vs. Slow (deliberate/sluggish).

**2. Solar Phase:**
*   **Oriental (Rising before Sun):** Masculine/Active planets (Mars, Jupiter, Saturn) prefer this.
*   **Occidental (Setting after Sun):** Feminine/Passive planets (Venus, Moon) prefer this. Mercury varies.

**3. Hayz and Halb:**
*   **Hayz:** A masculine planet in a masculine sign during the day, above the horizon; or feminine/feminine/night/below. (Perfect alignment).
*   **Halb:** Meeting only sect and sign requirements but wrong hemisphere.
*   **Scoring:** Hayz typically adds +1 to +3 points in weighted systems.
"""

    TEXT_LOTS = """
## Chapter 10a: The Arabic Parts (Lots)

The Lots represent calculated points that synthesize the Solar, Lunar, and Ascendant principles.

### The Lot of Fortune (Tyche)
*   **Signification:** The body, chance, material fortune, inconsistent events. An alternate "Lunar Ascendant."
*   **Day Formula:** Asc + Moon - Sun
*   **Night Formula:** Asc + Sun - Moon

### The Lot of Spirit (Daimon)
*   **Signification:** The will, career, deliberate action, the mind. The "Solar" counterpart.
*   **Day Formula:** Asc + Sun - Moon
*   **Night Formula:** Asc + Moon - Sun

### The Lot of Eros (Necessity/Desire)
*   **Signification:** Relational desires, romantic unions, social bonds.
*   **Day Formula:** Asc + Venus - Spirit
*   **Night Formula:** Asc + Spirit - Venus
"""

    TEXT_TIME_LORDS_EXTRA = """
### Firdaria (The Persian Period System)
A planetary period system governing long-term chapters of life, strictly based on Sect.
*   **Day Charts:** Sun (10y) -> Venus (8y) -> Mercury (13y) -> Moon (9y) -> Saturn (11y) -> Jupiter (12y) -> Mars (7y) -> Nodes (3y/2y).
*   **Night Charts:** Moon (9y) -> Saturn (11y) -> Jupiter (12y) -> Mars (7y) -> Sun (10y) -> Venus (8y) -> Mercury (13y) -> Nodes.

### Decennials (Hellenistic General Periods)
A general time-lord system using 10 years and 9 months (129 months) as a base, distributed among planets based on their order in the chart. Used alongside Zodiacal Releasing.
"""

    TEXT_ASPECT_CONDITIONS = """
### Perfection and Denial: Aspect Conditions
In Horary and Event astrology, an applying aspect does not guarantee a result. The "Conditions of Bonatti" apply:

1.  **Prohibition:** A faster planet intervenes between the significators before they perfect the aspect.
2.  **Refranation:** The applying planet turns retrograde before perfecting the aspect.
3.  **Translation of Light:** A faster planet separates from one significator and applies to the other, bridging the gap.
4.  **Collection of Light:** Two significators do not aspect each other, but both apply to a heavier third planet, which "collects" their light and perfects the matter.
5.  **Frustration:** The aspect is perfected, but the receiving planet is destroyed by a malefic immediately after.
"""

    # --- NEW CRITICAL GAPS (TIER 3) ---

    TEXT_DODECATEMORIA = """
## Chapter 7c: The Dodecatemoria (Twelfth-Parts)

The Dodecatemoria (or "Twelfth-Parts") is a recursive dignity system where each sign is subdivided into 12 micro-signs of 2.5 degrees each. This reveals the "hidden essence" of a planet—its internal motivation.

**Calculation Formula:**
1.  Take the degree of the planet within its sign (0–30).
2.  Multiply by 12.
3.  Add the result to the planet's original longitude (in absolute longitude 0–360).
4.  Project the resulting position to find the "Dodecatemoria Sign."

*Example:* A planet at 10° Aries.
10 * 12 = 120°.
10° Aries + 120° = 10° Leo.
The planet has a "Leo overtone" or hidden agenda.

**Usage:**
*   **Hidden Intent:** Reveals specific details in horary questions (e.g., a "friend" significator with a 12th-part in the 12th house may be a secret enemy).
*   **Rectification:** The Dodecatemoria of the Ascendant often aligns with the natal Moon or its variations.
"""

    TEXT_MORE_LOTS = """
### Additional Hermetic Lots
Valens and the Hellenistic tradition list dozens of Lots. Key additional calculations:

*   **Lot of Necessity (Ananke):** Constraints, enemies, inescapable fate.
    *   Day: Asc + Lot of Fortune - Lot of Spirit
    *   Night: Asc + Lot of Spirit - Lot of Fortune
*   **Lot of Eros:** Relational desires and appetites.
    *   Day: Asc + Venus - Spirit
    *   Night: Asc + Spirit - Venus
*   **Lot of Victory (Nike):** Success, contest, enterprise.
    *   Day: Asc + Jupiter - Spirit
    *   Night: Asc + Spirit - Jupiter
*   **Lot of Courage (Tolma):** Boldness, military action.
    *   Day: Asc + Fortune - Mars
    *   Night: Asc + Mars - Fortune
*   **Lot of Marriage (Men):**
    *   Day: Asc + Venus - Saturn
    *   Night: Asc + Saturn - Venus
    *   *Note: Specific formulas vary by author; Valens prefers this for general marital stability.*
*   **Lot of Basis:** Foundation, vitality, minimum support.
    *   Day/Night: Asc + Fortune - Spirit (or strictly Shortest Arc between Fortune/Spirit projected from Asc).
"""

    TEXT_PROFECTIONS = """
## Chapter 19a: Annual Profections (The Time-Lord of the Year)

Annual Profection is the foundational predictive technique, identifying the "Lord of the Year" who activates specific chart potentials.

**The Algorithm:**
1.  **Movement:** The Ascendant moves forward **30 degrees (1 sign) per year**, starting from the rising sign at age 0.
2.  **The Profected Sign:** The sign the Ascendant reaches is the "Sign of the Year."
3.  **The Lord of the Year:** The planetary ruler of that sign becomes the Time-Lord. All transits *to* this planet, and all transits *by* this planet, become the most critical events of the year.
4.  **Activation:** Any planets located in the Profected Sign (natal) are also "activated" for the year.

**Cycle of Years:**
*   **1st House Years:** Age 0, 12, 24, 36, 48, 60... (Identity, Body)
*   **2nd House Years:** Age 1, 13, 25, 37, 49, 61... (Assets, Resources)
*   **6th House Years:** Age 5, 17, 29, 41... (Illness, Toil) - Often difficult.
*   **10th House Years:** Age 9, 21, 33, 45... (Career, Reputation) - Peaks.
"""

    TEXT_ZR_FULL = """
## Chapter 19b: Zodiacal Releasing (Aphesis) Activation Logic

Zodiacal Releasing (from Valens) partitions time using the Lot of Spirit (Career/Destiny) or Lot of Fortune (Body/Health).

**Level hierarchy:**
1.  **Level 1 (General):** Periods of years (Planetary Minor Years).
2.  **Level 2 (Sub-periods):** Months (Planetary Minor Years / 12).
3.  **Level 3 (Sub-sub):** Days.

**Activation Logic (The Peak Periods):**
*   **Angles from the Lot:** The signs angular (1st, 4th, 7th, 10th) to the Lot being released are the most active/consequential "Peak Periods."
    *   **Foregrounds (1st/10th):** Intense activity, visibility, high stakes.
    *   **Opposite (7th):** Challenges, culminates, public interaction.
    *   **Subterraneous (4th):** Private foundations, endings, roots.
*   **Pre-Peak Prep:** The period occurring *before* a Peak period often involves "preparation" or labor leading to the event.
*   **Loosing of the Bond (LB):** As noted, if the sequence hits a sign >17.5 years (Cap/Aqu, Cancer, Leo, Gemini/Virgo), it jumps to the opposite sign to complete the duration, signifying a major reversal or "break/release" in the narrative.
"""

    TEXT_PRIMARY_DIR = """
## Chapter 19c: Primary Directions (The Primum Mobile)

Primary Directions are the "Master Clock" of traditional astrology, predicting specific dates of major life events by measuring the rotation of the Earth (Primum Mobile) after birth.

**The Conceptual Mechanic:**
*   **Equatability:** 1 degree of Right Ascension (RA) moving over the Meridian = 1 Year of Life (Ptolemy key). Variations include Naibod (0°59'08" = 1 year).
*   **Motion:** Directions do not move planets through the zodiac; they move the *sphere of the sky* (Significators and Promissors) over the local angles/horizon.
*   **Calculation:**
    1.  Determine the **Significator** (e.g., Ascendant, Sun).
    2.  Determine the **Promissor** (e.g., Mars, or the terms of Mars).
    3.  Calculate the **Arc of Direction**: The distance (in RA/Oblique Ascension) required to rotate the sphere until the Promissor reaches the position of the Significator.
    4.  **Convert Arc to Time:** 1 degree arc ≈ 1 year of life.

*Note: Requires precise birth time (within 4 minutes) as 4 minutes of time = 1 degree of arc = 1 year of life.*
"""

    # PART I: FOUNDATIONS
    book.append("# Part I: Foundations of the Celestial Science\n")
    
    book.append("## Chapter 1: The Architecture of Destiny\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_MIRROR_INTRO, START_ORIGINS)))
    
    book.append("\n## Chapter 2: Mesopotamian Origins\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_ORIGINS, START_EGYPTIAN)))
    # INSERT GAP 3 & 4
    book.append(TEXT_SUBSTITUTE_KING)
    book.append(TEXT_OMEN_GEO)

    book.append("\n## Chapter 3: The Egyptian & Hellenistic Synthesis\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_EGYPTIAN, START_INDIA)))
    
    book.append("\n## Chapter 4: The Thema Mundi\n")
    section_thema = extract_section_regex(full_content, "Thema Mundi (World Chart)", "3. Astrology Research")
    if not section_thema or len(section_thema) < 50:
         section_thema = extract_section_regex(full_content, "The Archetypal Baseline", "3. Astrology Research")
    book.append(clean_chapter_content(section_thema))
        
    book.append("\n## Chapter 5: Philosophical Foundations\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_PHILOSOPHY_CONTEXT, START_CRITIQUE)))

    # PART II: MECHANICS
    book.append("\n# Part II: The Mechanics of the Natal Chart\n")
    
    book.append("\n## Chapter 6: The Twelve Houses\n")
    book.append("### Historical Origins of the Houses\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, "3.2 The Twelve Houses: Systems", "3.3 Essential Dignities")))
    
    book.append("\n### House Meanings (Deep Dive)\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_HOUSES_DEEP, START_PLANETS_DEEP)))
    
    # NEW: Nodes (Chapter 6a) - READING FROM RESEARCH FILE (SECTION II)
    nodes_research_path = r"c:\Users\admin\Downloads\Astrology Files-20251228T075743Z-1-001\Astrology Files\Section_2_Lunar_Nodes.md"
    try:
        with open(nodes_research_path, 'r', encoding='utf-8') as f:
             nodes_content = f.read()
             nodes_content = nodes_content.replace("# Section II: The Lunar Nodes (Caput and Cauda Draconis)", "## Chapter 6a: The Lunar Nodes (Caput and Cauda Draconis)")
             book.append("\n" + nodes_content + "\n")
             print(f"✓ Injected Lunar Nodes Catalogue from {nodes_research_path}")
    except Exception as e:
        print(f"Warning: Could not read Nodes Research file: {e}")
        book.append(TEXT_NODES)

    book.append("\n## Chapter 7: Essential Dignities\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_DIGNITIES, START_ASPECTS_DEEP)))
    
    # GAP 6: Terms Logic
    book.append(TEXT_TERMS_LOGIC)
    
    # NEW: Fixed Stars (Chapter 7b) - READING FROM RESEARCH FILE (SECTION III)
    stars_research_path = r"c:\Users\admin\Downloads\Astrology Files-20251228T075743Z-1-001\Astrology Files\Section_3_Fixed_Stars.md"
    try:
        with open(stars_research_path, 'r', encoding='utf-8') as f:
             stars_content = f.read()
             stars_content = stars_content.replace("# Section III: Expanded Fixed Star Catalogue (The Eighth Sphere)", "## Chapter 7b: The Fixed Stars (The Eighth Sphere)")
             book.append("\n" + stars_content + "\n")
             print(f"✓ Injected Fixed Stars Catalogue from {stars_research_path}")
    except Exception as e:
        print(f"Warning: Could not read Stars Research file: {e}")
    
    # --- INSERT MONOMOIRIA SECTION (USER REQUEST) ---
    monomoiria_path = r"c:\Users\admin\Downloads\Astrology Files-20251228T075743Z-1-001\Astrology Files\# Section Five Monomoiria—The Micro.txt"
    try:
        with open(monomoiria_path, 'r', encoding='utf-8') as f:
            mono_content = f.read()
            # Fix header level to match book structure (H1 -> H2, etc if needed)
            # The file starts with "# Section Five...". Let's make it "## Chapter 7a"
            mono_content = mono_content.replace("# Section Five: Monomoiria—The Micro-Dignity of Individual Degree Rulership", "## Chapter 7a: Monomoiria—The Micro-Dignity")
            book.append("\n" + mono_content + "\n")
            print(f"✓ Injected Monomoiria section from {monomoiria_path}")
    except Exception as e:
        print(f"Warning: Could not read Monomoiria file: {e}")
    
    # NEW: Fixed Stars (Chapter 7b)
    book.append(TEXT_FIXED_STARS)
    
    # NEW: Dodecatemoria (Chapter 7c)
    book.append(TEXT_DODECATEMORIA)

    book.append("\n## Chapter 8: The Ptolemaic Aspects\n")
    
    # Special cleaning for Aspects to ensure it doesn't run into Compendium intro
    aspects_text = extract_section_regex(full_content, START_ASPECTS_DEEP, START_COMPENDIUM_INTRO)
    # Truncate if it hits "The Astrology Compendium" again
    if "The Astrology Compendium" in aspects_text:
        aspects_text = aspects_text.split("The Astrology Compendium")[0]
    book.append(clean_chapter_content(aspects_text))
    
    # NEW: Antiscia & Reception
    book.append(TEXT_ANTISCIA_RECEPTION)

    book.append("\n## Chapter 9: Sect and Planetary Competency\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, "Binary Competency Framework", "Jurisprudential Audit")))

    book.append("\n## Chapter 10: The Jurisprudential Audit\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, "Jurisprudential Audit Framework", "Astrological Hierarchies")))
    # INSERT GAP 2
    book.append(TEXT_ALMUTEN_SCALE)
    # NEW: Accidental Dignity
    book.append(TEXT_ACCIDENTAL_DIG)
    
    # NEW: Arabic Parts (Chapter 10a) - READING FROM RESEARCH FILE (SECTION I)
    lots_research_path = r"c:\Users\admin\Downloads\Astrology Files-20251228T075743Z-1-001\Astrology Files\Section_1_Arabic_Parts.md"
    try:
        with open(lots_research_path, 'r', encoding='utf-8') as f:
             lots_content = f.read()
             # Ideally renaming header if needed, but the file starts with H1 "Section I". 
             # Let's adjust it to be "Chapter 10a" structure if it has # Section I...
             lots_content = lots_content.replace("# Section I: Complete Catalogue of Arabic Parts (Lots)", "## Chapter 10a: The Complete Catalogue of Arabic Parts")
             book.append("\n" + lots_content + "\n")
             print(f"✓ Injected Detailed Lots Catalogue from {lots_research_path}")
    except Exception as e:
        print(f"Warning: Could not read Lots Research file: {e}")
        # Fallback to simple text if file fails (though we just created it)
        book.append(TEXT_LOTS)
        book.append(TEXT_MORE_LOTS)

    # PART III: DELINEATION CODEX
    book.append("\n# Part III: The Delineation Codex\n")
    
    book.append("\n## Chapter 11-17: Planets in the Twelve Signs\n")
    book.append("*(Reference Table Data)*\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_P1_SIGNS, START_P2_HOUSES)))
    
    book.append("\n## Chapter 18: Planets in the Twelve Houses\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_P2_HOUSES, START_P3_ASPECTS)))

    # PART IV: TIME AND PREDICTION
    book.append("\n# Part IV: Time and Prediction\n")
    
    book.append("\n## Chapter 19: Predictive Mechanisms\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, "5. Predictive Mechanisms: Unfolding Time", "6. Medical Astrology")))
    # INSERT GAP 1 & 7
    book.append(TEXT_VITALITY_TABLE)
    book.append(TEXT_LOOSING_BOND)
    # NEW: Time Lords (Chapters 19a, 19b, 19c)
    book.append(TEXT_PROFECTIONS)
    book.append(TEXT_ZR_FULL)
    book.append(TEXT_PRIMARY_DIR)
    
    # Extra Time Lords (Firdaria/Decennials)
    book.append(TEXT_TIME_LORDS_EXTRA)
    
    book.append("\n## Chapter 20: Aspects and Time Modulation\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_P3_ASPECTS, START_P4_CASES)))
    # NEW: Aspect Conditions
    book.append(TEXT_ASPECT_CONDITIONS)

    # PART V: APPLIED TRADITIONS
    book.append("\n# Part V: Applied Traditions\n")
    
    book.append("\n## Chapter 21: Medical Astrology\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, "6. Medical Astrology and Melothesia", START_PHILOSOPHY_CONTEXT)))
    # INSERT GAP 5
    book.append(TEXT_MEDICAL_GALEN)
    
    book.append("\n## Chapter 22: Comparative Systems\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_COMPARATIVE, "5. Predictive Mechanisms"))) 

    # PART VI: CASE STUDIES
    book.append("\n# Part VI: Case Studies\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, START_P4_CASES, "Appendix: Glossarial Index")))

    # BACK MATTER
    book.append("\n# Appendices\n")
    book.append(clean_chapter_content(extract_section_regex(full_content, "Appendix: Glossarial Index", "Sources Used:")))
    
    book.append("\n# Bibliography\n")
    
    # Fix the garbled bibliography
    section_biblio = extract_section_regex(full_content, "Works cited")
    # Clean up bibliography: separate links
    section_biblio = re.sub(r'(\))\s*(\[)', r'\1\n\n\2', section_biblio)
    # Remove any trailing "The Astrology Compendium" noise if present
    # Using regex to catch variations like ".The Astrology Compendium" or "The Astrology Compendium"
    section_biblio = re.split(r'[:\.]?\s*The Astrology Compendium', section_biblio, flags=re.IGNORECASE)[0]
        
    book.append(section_biblio)    

    # WRITE FILE
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(book))

    print(f"✓ Book successfully reconstructed at: {output_path}")

if __name__ == "__main__":
    main()
