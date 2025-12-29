import os
from PyPDF2 import PdfMerger

# Directory containing PDFs
pdf_dir = r"c:\Users\admin\Downloads\Astrology Files-20251228T075743Z-1-001\Astrology Files\pdf"

# Get all PDF files and sort them alphabetically
pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])

print(f"Found {len(pdf_files)} PDF files to merge:\n")
for i, f in enumerate(pdf_files, 1):
    print(f"  {i}. {f}")

# Create merger
merger = PdfMerger()

# Add each PDF
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    print(f"\nAdding: {pdf_file}")
    merger.append(pdf_path)

# Output path
output_path = os.path.join(os.path.dirname(pdf_dir), "Astrology_Complete_Book.pdf")

# Write merged PDF
merger.write(output_path)
merger.close()

print(f"\n✓ Successfully merged all PDFs!")
print(f"✓ Output saved to: {output_path}")
