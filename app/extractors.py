# app/extractors.py
import os, re, io, json
from typing import Dict, Any, Optional, Tuple, List
from PIL import Image
import pytesseract
import pdfplumber
import pandas as pd

# ถ้าต้องเซ็ต path Tesseract บน Windows ให้ปลดคอมเมนต์บรรทัดล่าง
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_from_image(img_bytes: bytes, lang: str = "tha+eng") -> str:
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    text = pytesseract.image_to_string(img, lang=lang)
    return text

def extract_from_pdf(pdf_bytes: bytes, lang: str = "tha+eng") -> str:
    text = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            text.append(t)
    full = "\n".join(text).strip()
    # ถ้า pdf ไม่มีเลเยอร์ข้อความ (เป็นสแกน) ให้ลอง OCR หน้าแรกเป็นอย่างน้อย
    if not full:
        first_page = pdfplumber.open(io.BytesIO(pdf_bytes)).pages[0]
        img = first_page.to_image(resolution=300).original
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        full = pytesseract.image_to_string(Image.open(io.BytesIO(buf.getvalue())), lang=lang)
    return full

def extract_from_excel(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_excel(io.BytesIO(file_bytes))

def extract_from_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_bytes))

# ---- Very simple field parsers (ตัวอย่าง baseline ปรับได้) ----
PO_PATTERNS = {
    "quantity": re.compile(r"(?:จำนวน|qty)\s*[:：]?\s*(\d+)", re.I),
    "material_code": re.compile(r"(?:รหัสสินค้า|material|sku)\s*[:：]?\s*([A-Za-z0-9\-]+)", re.I),
    "unit_price": re.compile(r"(?:ราคา(?:ต่อชิ้น)?|price)\s*[:：]?\s*(\d+(?:\.\d+)?)", re.I),
    "vendor_code": re.compile(r"(?:ผู้ขาย|vendor)\s*[:：]?\s*([A-Za-z0-9\-]+)", re.I),
}

def parse_po_from_text(text: str) -> Dict[str, Any]:
    slots = {}
    for k, rx in PO_PATTERNS.items():
        m = rx.search(text)
        if m:
            slots[k] = m.group(1)
    # post-process
    slots["quantity"] = int(slots.get("quantity", 1))
    slots["material_code"] = slots.get("material_code", "P-1001").upper()
    slots["unit_price"] = float(slots.get("unit_price", 100.0))
    slots["vendor_code"] = slots.get("vendor_code", "V-THA-01").upper()
    slots["currency"] = "THB"
    return slots
