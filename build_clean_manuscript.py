
import glob
import os
import re

# Define the build list in order
match_files = [
    {
        "filename": "The_Traditional_Astrologers_Complete_Reference.md",
        "title": None, # Base file, uses its own structure
        "type": "BASE"
    },
    {
        "filename": "_The Binary Competency Framework of Classical Astrology_ Sect, Solar Proximity, and Bonatti's Considerations as Deterministic Rules of Planetary Engagement.txt",
        "title": "The Binary Competency Framework",
        "type": "ESSAY"
    },
    {
        "filename": "_The Ministerial Order of Celestial Authority_ Ibn Ezra's Algorithm and the Calculus of Vitality.txt",
        "title": "The Ministerial Order of Celestial Authority",
        "type": "ESSAY"
    },
    {
        "filename": "The Nested Hierarchy of Chronocrators_ Dormancy, Activation, and the Sequential Unfolding of Natal Promise.txt",
        "title": "The Nested Hierarchy of Chronocrators",
        "type": "ESSAY"
    },
    {
        "filename": "The Inseparable Bond_ Medical Astrology's Integration of Celestial Cause and Physical Pathology.txt",
        "title": "Medical Astrology: The Inseparable Bond",
        "type": "ESSAY"
    },
    {
        "filename": "# The Four Micro-Calibrations for A.txt",
        "title": "Computational Determinism: The Four Micro-Calibrations",
        "type": "ESSAY"
    },
    {
        "filename": "# PART 8 EXTENDED_ UNIVERSAL CAUSATION AUDIT FOR DECEMBER 2025.txt",
        "title": "Universal Causation Audit (December 2025)",
        "type": "ESSAY"
    },
    {
        "filename": "# Section Five Monomoiria—The Micro.txt",
        "title": "Appendix A: Monomoiria Tables",
        "type": "APPENDIX"
    },
    {
        "filename": "# Advanced Ptolemaic Astrological T.txt",
        "title": "Appendix B: Advanced Ptolemaic Techniques",
        "type": "APPENDIX"
    },
    {
        "filename": "_The Jurisprudential Audit Framework.txt",
        "title": "Appendix C: The Jurisprudential Audit Framework",
        "type": "APPENDIX"
    }
]

OUTPUT_FILE = "CLEAN_Complete_Reference_Fixed.md"

def clean_content(content, file_type):
    # Remove BOM if present
    content = content.lstrip('\ufeff')
    
    # Normalize line endings
    content = content.replace('\r\n', '\n')
    
    # If it's the Base file, essentially leave it alone, but ensure it starts clean
    if file_type == "BASE":
        return content

    # For other files, we want to ensure they start with a proper header
    # Remove existing title-like lines at the very top if they are redundant? 
    # Actually, most files start with a header. We will prepend a massive header if we define one.
    
    # Simple regex to fix common formatting issues in raw text
    # e.g. "Page 1" footers, etc. (Not strictly checking here, just basic cleanup)
    
    return content

def main():
    final_content = []
    
    for item in match_files:
        fname = item["filename"]
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                raw_text = f.read()
                
            print(f"Processing: {fname}...")
            
            cleaned_text = clean_content(raw_text, item["type"])
            
            # Add Page Break
            final_content.append("\n\n\\newpage\n\n")
            
            # Append content
            final_content.append(cleaned_text)
            
        except FileNotFoundError:
            print(f"WARNING: File not found: {fname}")
            # Try fuzzy match if exact name fails?
            # For now, simplistic approach
            continue 

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("".join(final_content))
    
    print(f"\nSuccessfully created {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
