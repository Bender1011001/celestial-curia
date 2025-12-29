
import os
import re

SOURCE_FILE = "_The Binary Competency Framework of Classical Astrology_ Sect, Solar Proximity, and Bonatti's Considerations as Deterministic Rules of Planetary Engagement.txt"
TARGET_FILE = "volumes/vol3-dynamics/15-bonification.qmd"

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
    
    # Extract Part II (Solar Proximity) and Part III (Bonatti)
    # Part II starts at "## PART II: FORENSIC CONDITIONS OF SOLAR PROXIMITY"
    # Part III ends at "## SYNTHESIS" or "## CONCLUSION"
    
    part2 = extract_section(source_text, "## PART II: FORENSIC CONDITIONS", "## PART III")
    part3 = extract_section(source_text, "## PART III: BONATTI", "## SYNTHESIS")
    synthesis = extract_section(source_text, "## SYNTHESIS", "## CONCLUSION")
    
    if part2 and part3:
        content = f"{part2}\n\n{part3}\n\n{synthesis}"
        # Title it "Conditions of Empowerment and Maltreatment" to bridge the terminology
        write_qmd(TARGET_FILE, content, "Conditions of Empowerment and Maltreatment: Solar Proximity and Bonatti's Considerations")
    else:
        print("Error extracting Bonification content")

if __name__ == "__main__":
    main()
