
import os
import re

# Source Files
CHRONO_DOC = "The Nested Hierarchy of Chronocrators_ Dormancy, Activation, and the Sequential Unfolding of Natal Promise.txt"
MEDICAL_DOC = "The Inseparable Bond_ Medical Astrology's Integration of Celestial Cause and Physical Pathology.txt"
MUNDANE_DOC = "# PART 8 EXTENDED_ UNIVERSAL CAUSATION AUDIT FOR DECEMBER 2025.txt"
COMPUTE_DOC = "# The Four Micro-Calibrations for A.txt"

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {path} not found")
        return ""

def write_qmd(path, content, title):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    full_content = f"# {title}\n\n{content}"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    print(f"Created {path}")

def main():
    # --- Vol 4: Prediction (Chronocrators) ---
    chrono = read_file(CHRONO_DOC)
    if chrono:
        # Split logic could be added here, but for now dumping the whole file as the Time Lords chapter
        write_qmd("volumes/vol4-prediction/17-timelords.qmd", chrono, "The Hierarchy of Chronocrators")
        
    # --- Vol 5: Medical ---
    medical = read_file(MEDICAL_DOC)
    if medical:
        write_qmd("volumes/vol5-applied/22-medical.qmd", medical, "The Inseparable Bond: Medical Astrology")

    # --- Vol 5: Mundane ---
    mundane = read_file(MUNDANE_DOC)
    if mundane:
        write_qmd("volumes/vol5-applied/25-mundane.qmd", mundane, "Universal Causation: Mundane Astrology")

    # --- Vol 5: Computational (Theurgy/Algorithms) ---
    compute = read_file(COMPUTE_DOC)
    if compute:
        write_qmd("volumes/vol5-applied/23-algorithms.qmd", compute, "Computational Determinism")

if __name__ == "__main__":
    main()
