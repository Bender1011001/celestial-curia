
import os
import re

# Source Files
BASE_REF = "The_Traditional_Astrologers_Complete_Reference.md"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_qmd(path, content, title):
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    full_content = f"# {title}\n\n{content}"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    print(f"Created {path}")

def main():
    base_content = read_file(BASE_REF)

    # --- Vol 2: Houses (Chapter 6) ---
    # From "## Chapter 6: The Twelve Houses" to "## Section Two" or next chapter
    houses_match = re.search(r"(## Chapter 6: The Twelve Houses.*?)## Section Two", base_content, re.DOTALL)
    if houses_match:
        write_qmd("volumes/vol2-places/11-houses.qmd", houses_match.group(1), "The Twelve Places")
    else:
        print("Chapter 6 (Houses) not found")

    # --- Vol 1: Dignity (Chapter 7) ---
    # From "## Chapter 7: Essential Dignities" to "## Chapter 7b"
    dignity_match = re.search(r"(## Chapter 7: Essential Dignities.*?)## Chapter 7b", base_content, re.DOTALL)
    if dignity_match:
        write_qmd("volumes/vol1-foundations/03b-dignity.qmd", dignity_match.group(1), "Essential Dignity")
    else:
        print("Chapter 7 (Dignity) not found")

    # --- Vol 1: Fixed Stars (Chapter 7b) ---
    # From "## Chapter 7b: The Fixed Stars" to "## Chapter 7c" or "## Chapter 8"
    stars_match = re.search(r"(## Chapter 7b: The Fixed Stars.*?)## Chapter 8", base_content, re.DOTALL)
    if stars_match:
        write_qmd("volumes/vol1-foundations/02b-stars.qmd", stars_match.group(1), "The Fixed Stars")
    else:
        print("Chapter 7b (Stars) not found")
        
    # --- Vol 3: Aspects (Chapter 8) ---
    # From "## Chapter 8: The Ptolemaic Aspects" to "## Chapter 9" or end of Part
    aspects_match = re.search(r"(## Chapter 8: The Ptolemaic Aspects.*?)## Chapter 9", base_content, re.DOTALL)
    if not aspects_match:
        # Try finding end of file or next Part if Ch 9 doesn't exist
        aspects_match = re.search(r"(## Chapter 8: The Ptolemaic Aspects.*?)# Part III", base_content, re.DOTALL)
    
    if aspects_match:
        write_qmd("volumes/vol3-dynamics/14-aspects.qmd", aspects_match.group(1), "The Doctrine of Aspects")
    else:
         # Fallback generic
        aspects_match = re.search(r"(## Chapter 8: The Ptolemaic Aspects.{5000})", base_content, re.DOTALL)
        if aspects_match:
             write_qmd("volumes/vol3-dynamics/14-aspects.qmd", aspects_match.group(1) + "\n(Truncated, check source)", "The Doctrine of Aspects")
        else:
            print("Chapter 8 (Aspects) not found")

if __name__ == "__main__":
    main()
