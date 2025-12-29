
import os
import re

# Source Files
BASE_REF = "The_Traditional_Astrologers_Complete_Reference.md"
SECT_DOC = "_The Binary Competency Framework of Classical Astrology_ Sect, Solar Proximity, and Bonatti's Considerations as Deterministic Rules of Planetary Engagement.txt"

# Target Files
VOL1_PATH = "volumes/vol1-foundations"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_qmd(path, content, title):
    full_content = f"# {title}\n\n{content}"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    print(f"Created {path}")

def main():
    base_content = read_file(BASE_REF)
    sect_content = read_file(SECT_DOC)

    # --- Extract Vol 1, Chap 1: The Architecture of Destiny ---
    # Regex to find Chapter 1 up to Chapter 2
    # Note: Adjust regex based on actual file content inspection
    chap1_match = re.search(r"(## Chapter 1: The Architecture of Destiny.*?)## Chapter 2", base_content, re.DOTALL)
    if chap1_match:
        write_qmd(f"{VOL1_PATH}/01-hierarchy.qmd", chap1_match.group(1), "The Celestial Hierarchy")
    else:
        print("Chapter 1 not found in base ref")

    # --- Extract Vol 1, Chap 2: Mesopotamian/Cosmos ---
    chap2_match = re.search(r"(## Chapter 2: Mesopotamian Origins.*?)2\.4", base_content, re.DOTALL) # Example ending, need to be robust
    if chap2_match:
        write_qmd(f"{VOL1_PATH}/02-cosmos.qmd", chap2_match.group(1), "The Architecture of the Cosmos")
    else:
        print("Chapter 2 not found in base ref")

    # --- Extract Vol 1, Chap 3: Sect (from separate file) ---
    # Extract just the Sect section from the Binary Competency Framework
    sect_match = re.search(r"(## PART I: THE DOCTRINE OF SECT.*?)(?=## Layer 2|## PART II)", sect_content, re.DOTALL)
    if sect_match:
        write_qmd(f"{VOL1_PATH}/03-sect.qmd", sect_match.group(1), "The Doctrine of Sect")
    else:
        # Fallback: take the whole first part if precise regex fails
         write_qmd(f"{VOL1_PATH}/03-sect.qmd", sect_content[:2000], "The Doctrine of Sect (Fallback)")
         print("Specific Sect section regex failed, using fallback")

if __name__ == "__main__":
    main()
