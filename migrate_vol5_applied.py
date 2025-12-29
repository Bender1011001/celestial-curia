
import os
import re

SOURCE_FILE = "celestial_curia/manuscript/06_Part_VI_Applied_Astrology/20_Synastry_Elections_Joys.md"

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
    
    # 1. Synastry -> 22-natal.qmd (as "Advanced Natal/Synastry")
    synastry = extract_section(source_text, "## I. Synastry", "## II. Electional")
    if synastry:
        # Append to existing or create new?
        # The chapter is currently empty placeholder.
        write_qmd("volumes/vol5-applied/22-natal.qmd", synastry, "Advanced Natal and Synastry")
        
    # 2. Elections -> 23-electional.qmd
    elections = extract_section(source_text, "## II. Electional", "## III. Planetary")
    if elections:
        write_qmd("volumes/vol5-applied/23-electional.qmd", elections, "Electional Protocols")

if __name__ == "__main__":
    main()
