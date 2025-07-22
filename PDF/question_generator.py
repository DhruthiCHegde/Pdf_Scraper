import os
import json
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# === Load model ===
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# === Load structured output ===
with open("output/structured_output.json", "r") as f:
    structured_data = json.load(f)

qa_output = []

# === Generate captions and questions ===
for page in structured_data:
    for img_path in page["images"]:
        if not os.path.exists(img_path):
            continue
        image = Image.open(img_path).convert("RGB")
        inputs = processor(image, return_tensors="pt")
        output = model.generate(**inputs)
        caption = processor.decode(output[0], skip_special_tokens=True)

        question = f"What can you infer or ask based on this image: '{caption}'?"

        qa_output.append({
            "caption": caption,
            "image_path": img_path,
            "generated_question": question
        })

# === Save as JSON ===
with open("output/questions.json", "w") as f:
    json.dump(qa_output, f, indent=2)

print("✅ AI-based questions saved to output/questions.json")