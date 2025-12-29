
import os
import shutil

# Configuration Mapping based on _quarto.yml vs Actual
# We will create empty/placeholder files for those that are missing to fix the build immediately.
# Then I will manually consolidate or move content if needed, but priority 1 is green build.

MISSING_FILES = [
    ("volumes/vol3-dynamics/15-bonification.qmd", "Bonification and Maltreatment", "Content currently merged in Aspects or pending migration."),
    ("volumes/vol4-prediction/18-profections.qmd", "Annual Profections", "Content pending separation from Chronocrators."),
    ("volumes/vol4-prediction/19-zodiacal-releasing.qmd", "Zodiacal Releasing", "Content pending separation from Chronocrators."),
    ("volumes/vol5-applied/22-natal.qmd", "Natal Practice", "General synthesis chapter."),
    ("volumes/vol5-applied/23-electional.qmd", "Electional Astrology", "Content pending migration."),
    ("volumes/vol5-applied/24-theurgy.qmd", "Astrological Theurgy", "Content pending migration."),
    ("volumes/appendices/glossary.qmd", "Glossary of Traditional Terms", "Definitions of key terms."),
    ("volumes/appendices/tables.qmd", "Reference Tables", "Essential dignity and years tables.")
]

# Rename maps (Actual -> Target) if existing files have wrong names
RENAMES = {
    "volumes/vol5-applied/22-medical.qmd": "volumes/vol5-applied/22-natal.qmd", # Example partial match
    # Realized I created 22-medical.qmd but config wants 22-natal.qmd OR config should change.
    # Decide: Update Config is cleaner, but user wants "fix build".
    # Strategy: Create the exact files `_quarto.yml` asks for.
}

def create_file(path, title, note):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        content = f"# {title}\n\n> [!NOTE]\n> {note}\n\n## Under Construction\n\nThis chapter is currently being drafted."
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {path}")
    else:
        print(f"Exists: {path}")

def main():
    # 1. Create missing chapters referenced in _quarto.yml
    for path, title, note in MISSING_FILES:
        create_file(path, title, note)

    # 2. Check strict config compliance
    # Vol 5 config asks for: 22-natal, 23-electional, 24-theurgy, 25-mundane
    # I have: 22-medical.qmd, 23-algorithms.qmd, 25-mundane.qmd
    
    # I will specifically fix Vol 5 by renaming/copying content to match config
    if os.path.exists("volumes/vol5-applied/22-medical.qmd"):
        # Append medical content to 22-natal or rename?
        # Let's keep 22-medical as strictly medical, but config needs to be updated or file renamed.
        # Decision: Create 22-natal as new, Keep 22-medical but REMOVE from build or ADD to config?
        # The user report says "chapter X not found", implies strict config mismatch.
        # I will create the exact files requested.
        pass

if __name__ == "__main__":
    main()
