
import os
import re

SOURCE_FILE = "pdf/Planetary Delineations From Ancient Sources.txt"

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
    source_text = read_file(SOURCE_FILE)
    
    # --- 1. The Malefics (Saturn & Mars) -> 06-malefics.qmd ---
    saturn = extract_section(source_text, "3. Saturn: The Greater Malefic", "4. Jupiter: The Greater Benefic")
    mars = extract_section(source_text, "5. Mars: The Lesser Malefic", "6. The Sun: The Luminary")
    
    if saturn and mars:
        content = f"{saturn}\n\n{mars}"
        write_qmd("volumes/vol1-foundations/06-malefics.qmd", content, "The Malefics: Saturn and Mars")
    else:
        print("Error extracting Malefics")

    # --- 2. The Benefics (Jupiter & Venus) -> 05-benefics.qmd ---
    jupiter = extract_section(source_text, "4. Jupiter: The Greater Benefic", "5. Mars: The Lesser Malefic")
    venus = extract_section(source_text, "7. Venus: The Lesser Benefic", "8. Mercury: The Common Star")
    
    if jupiter and venus:
        content = f"{jupiter}\n\n{venus}"
        write_qmd("volumes/vol1-foundations/05-benefics.qmd", content, "The Benefics: Jupiter and Venus")
    else:
        print("Error extracting Benefics")

    # --- 3. The Luminaries (Sun & Moon) -> 04-luminaries.qmd ---
    sun = extract_section(source_text, "6. The Sun: The Luminary", "7. Venus: The Lesser Benefic")
    moon = extract_section(source_text, "9. The Moon: The Luminary", "10. Comparative Analysis")
    
    if sun and moon:
        content = f"{sun}\n\n{moon}"
        write_qmd("volumes/vol1-foundations/04-luminaries.qmd", content, "The Luminaries: Sun and Moon")
    else:
        print("Error extracting Luminaries")

    # --- 4. Mercury -> 07-mercury.qmd ---
    mercury = extract_section(source_text, "8. Mercury: The Common Star", "9. The Moon: The Luminary")
    
    if mercury:
        write_qmd("volumes/vol1-foundations/07-mercury.qmd", mercury, "Mercury: The Scribe")
    else:
        print("Error extracting Mercury")

if __name__ == "__main__":
    main()
