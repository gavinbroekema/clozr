import fitz  # PyMuPDF
import csv
import os
import sys

def convert_bold_to_incremental_cloze(pdf_file, output_file):
    doc = fitz.open(pdf_file)
    rows = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block_num, block in enumerate(blocks):
            block_text = ""  # Initialize block text
            cloze_count = 1  # Start counting Cloze deletions within a block

            for line_num, line in enumerate(block.get("lines", [])):
                line_text = ""  # Initialize line text

                for span in line.get("spans", []):
                    text = span["text"].strip()

                    # Check if the text is bold (flag 16)
                    if span.get("flags", 0) & 16:
                        line_text += f"{{{{c{cloze_count}::{text}}}}} "  # Incremental Cloze
                        cloze_count += 1  # Increment the Cloze counter
                    else:
                        line_text += f"{text} "

                block_text += line_text.strip() + "\n"  # Keep line breaks inside a block

            # Add block text as a single column in the CSV row
            rows.append([block_text.strip()])  # Do not add a comma within the text

    # Write the processed text into a CSV file
    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)  # Write each block as a new row in the CSV

    print(f"Cloze-formatted text with incremental clozes saved as CSV at {output_file}")

if __name__ == "__main__":
    # 1) Get PDF path from argument or prompt
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
    else:
        pdf_file = input("Enter path to PDF file: ").strip().strip('"').strip("'")

    if not os.path.isfile(pdf_file):
        print("Error: PDF file not found.")
        sys.exit(1)

    # 2) Build output CSV path from input PDF name
    base_name = os.path.splitext(pdf_file)[0]
    output_file = base_name + ".csv"

    convert_bold_to_incremental_cloze(pdf_file, output_file)
