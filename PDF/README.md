# PDF AI Question Generator

## Part 1: PDF Text & Image Extraction

### Steps:
1. Place your PDF file in `data/` folder and name it `input.pdf`.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the extraction:
```bash
python main.py
```

- Text + image metadata will be saved in `output/structured_output.json`
- Images will be saved in `output/images/`

---

## Part 2: AI-Based Question Generation

### Steps:
1. Run the AI generator script:
```bash
python question_generator.py
```

- It generates captions from images using BLIP
- Forms basic questions from those captions
- Final output saved to: `output/questions.json`