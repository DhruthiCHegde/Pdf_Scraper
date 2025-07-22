import os
import fitz  # PyMuPDF
import pdfplumber
import json

PDF_PATH = "data/input.pdf"
OUTPUT_DIR = "output"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
JSON_OUTPUT = os.path.join(OUTPUT_DIR, "structured_output.json")

os.makedirs(IMAGES_DIR, exist_ok=True)

text_data = []
with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        text_data.append({"page": i + 1, "text": text})

doc = fitz.open(PDF_PATH)
structured_output = []

for page_num in range(len(doc)):
    page = doc[page_num]
    image_list = page.get_images(full=True)
    image_paths = []

    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_filename = f"page{page_num + 1}_image{img_index + 1}.{image_ext}"
        image_path = os.path.join(IMAGES_DIR, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        image_paths.append(image_path)

    structured_output.append({
        "page": page_num + 1,
        "text": text_data[page_num]["text"],
        "images": image_paths
    })

with open(JSON_OUTPUT, "w", encoding="utf-8") as json_file:
    json.dump(structured_output, json_file, indent=2, ensure_ascii=False)

print(f"\n✅ Extraction complete! JSON saved to: {JSON_OUTPUT}")