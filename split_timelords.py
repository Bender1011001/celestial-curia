
import os
import re

SOURCE_FILE = "volumes/vol4-prediction/17-timelords.qmd"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_qmd(path, content, title):
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    full_content = f"# {title}\n\n{content}"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    print(f"Updated {path}")

def extract_section(text, start_pattern, end_pattern):
    pattern = f"({start_pattern}.*?){end_pattern}"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def main():
    if not os.path.exists(SOURCE_FILE):
        print(f"Source file {SOURCE_FILE} not found.")
        return

    source_text = read_file(SOURCE_FILE)
    
    # --- 1. Zodiacal Releasing -> 19-zodiacal-releasing.qmd ---
    # Looking for "PART II: B. Zodiacal Releasing" type headers
    zr_content = extract_section(source_text, "## PART II.*Zodiacal Releasing", "## PART III")
    if zr_content:
        # Also include Loosing of the Bond (PART III) as it relates to ZR
        lb_content = extract_section(source_text, "## PART III", "## PART IV")
        full_zr = f"{zr_content}\n\n{lb_content}" if lb_content else zr_content
        write_qmd("volumes/vol4-prediction/19-zodiacal-releasing.qmd", full_zr, "Zodiacal Releasing")
    
    # --- 2. Profections -> 18-profections.qmd ---
    # Looking for "D. Annual Profections" or similar
    prof_content = extract_section(source_text, "Annual Profections: The Annual Filter", "## PART III") # This pattern might need adjustment
    # Actually, Profections appear around line 195: "### D. Annual Profections"
    # And "PART V: THE LORD OF THE YEAR" is also Profections related.
    
    prof_part1 = extract_section(source_text, "### D. Annual Profections", "## PART III")
    prof_part2 = extract_section(source_text, "## PART V", "## PART VI")
    
    if prof_part1:
         full_prof = f"{prof_part1}\n\n{prof_part2}" if prof_part2 else prof_part1
         write_qmd("volumes/vol4-prediction/18-profections.qmd", full_prof, "Annual Profections")

    # --- 3. Clean up the original 17-timelords (General + Firdaria) ---
    # It should keep Intro, Part I (Dormancy), and Part II C (Firdaria), Part IV (Day/Night Firdaria)
    # This is more complex to "replace" efficiently, maybe just overwrite with the intro + firdaria parts?
    
    intro = extract_section(source_text, "## Executive Summary", "## PART II")
    part1 = extract_section(source_text, "## PART I", "## PART II")
    # Firdaria is Part II C + Part IV
    firdaria = extract_section(source_text, "### C. Firdaria", "### D. Annual Profections")
    firdaria_detail = extract_section(source_text, "## PART IV", "## PART V")
    
    if intro and part1 and firdaria:
        new_17 = f"{intro}\n\n{part1}\n\n## The Hierarchy of Chronocrators\n\n{firdaria}\n\n{firdaria_detail}"
        write_qmd("volumes/vol4-prediction/17-timelords.qmd", new_17, "The Hierarchy of Chronocrators")

if __name__ == "__main__":
    main()
