
import os

def write_placeholder(path, title, note):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    content = f"# {title}\n\n> [!NOTE]\n> {note}\n\n## Content Pending\n\nThis chapter requires the migration of specific source text regarding {title}."
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created placeholder {path}")

def main():
    write_placeholder("volumes/vol1-foundations/04-luminaries.qmd", "The Luminaries: Sun and Moon", "Source text for Sun/Moon delineations is currently missing.")
    write_placeholder("volumes/vol1-foundations/05-benefics.qmd", "The Benefics: Jupiter and Venus", "Source text for Jupiter/Venus delineations is currently missing.")
    write_placeholder("volumes/vol1-foundations/06-malefics.qmd", "The Malefics: Saturn and Mars", "Source text for Saturn/Mars delineations is currently missing.")
    write_placeholder("volumes/vol1-foundations/07-mercury.qmd", "Mercury: The Scribe", "Source text for Mercury delineation is currently missing.")

if __name__ == "__main__":
    main()
