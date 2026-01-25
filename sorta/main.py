from pdf_extract import extract_pdf_text
from classifier import classify
from config_loader import load_config

config = load_config()
text = extract_pdf_text("/mnt/shared/Projects/sorta/test.pdf")

print(classify(text, config))
