# init_data.py (เวอร์ชันอ่าน pdf)
import pathlib, json
from datasets import load_dataset
import pdfplumber
import re, io
from PIL import Image
import pytesseract
RUNTIME_DIR = pathlib.Path(".runtime/mock_sap")
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

def parse_po_from_pdf(pdf_obj) -> dict:
    # แปลง pdfplumber.PDF → text
    text = ""
    for page in pdf_obj.pages:
        text += page.extract_text() or ""

    # baseline regex หา fields (สมมุติว่ามี pattern แบบนี้ในเอกสาร)
    po_id = re.search(r"PO\s*[:：]?\s*(\d+)", text)
    supplier = re.search(r"Supplier\s*[:：]?\s*(\w+)", text)
    product = re.search(r"Product\s*[:：]?\s*(\w+)", text)
    qty = re.search(r"Quantity\s*[:：]?\s*(\d+)", text)
    price = re.search(r"Unit\s*Price\s*[:：]?\s*(\d+\.?\d*)", text)

    qty_val = int(qty.group(1)) if qty else 1
    price_val = float(price.group(1)) if price else 100.0
    total = qty_val * price_val

    return {
        "po_id": f"PO{po_id.group(1) if po_id else '000'}",
        "quantity": qty_val,
        "material_code": product.group(1) if product else "P-000",
        "unit_price": price_val,
        "vendor_code": supplier.group(1) if supplier else "V-000",
        "currency": "THB",
        "total_amount": total,
        "approved": total <= 50000,
        "created_at": 0
    }

def main():
    ds = load_dataset("AyoubChLin/northwind_PurchaseOrders")
    records = ds["train"]

    mock_pos = []
    for row in records:
        pdf_obj = row["pdf"]
        po_data = parse_po_from_pdf(pdf_obj)
        mock_pos.append(po_data)

    out_file = RUNTIME_DIR / "purchase_orders.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(mock_pos, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(mock_pos)} POs to {out_file}")
def pdf_to_text(pdf_obj) -> str:
    text_parts = []
    for page in pdf_obj.pages:
        txt = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
        text_parts.append(txt)
    text = "\n".join(text_parts).strip()

    if not text:  # scanned PDF → OCR หน้าแรก
        p0 = pdf_obj.pages[0]
        img = p0.to_image(resolution=300).original
        buf = io.BytesIO(); img.save(buf, format="PNG")
        text = pytesseract.image_to_string(Image.open(io.BytesIO(buf.getvalue())), lang="eng+tha")
    return text

def parse_po_fields(text: str) -> dict:
    # สร้างตัวช่วยหา pattern หลายแบบ
    def find_one(patterns):
        for pat in patterns:
            m = re.search(pat, text, flags=re.I)
            if m:
                return m.group(1).strip()
        return None

    # PO ID
    po_id = find_one([
        r"(?:^|\b)(?:PO|Purchase\s*Order)\s*[:#]?\s*([A-Z]?\d{3,})",
        r"(?:หมายเลข\s*PO|เลขที่ใบสั่งซื้อ)\s*[:#]?\s*([A-Z]?\d{3,})",
    ]) or "000"

    # Vendor / Supplier Code
    vendor = find_one([
        r"(?:Vendor|Supplier)(?:\s*Code)?\s*[:#]?\s*([A-Z0-9\-]+)",
        r"(?:ผู้ขาย|ผู้จัดส่ง)(?:\s*รหัส)?\s*[:#]?\s*([A-Z0-9\-]+)",
    ]) or "V-000"

    # Material/Product Code
    material = find_one([
        r"(?:Material|Product)(?:\s*Code)?\s*[:#]?\s*([A-Z0-9\-./]+)",
        r"(?:รหัสสินค้า)\s*[:#]?\s*([A-Z0-9\-./]+)",
    ]) or "P-000"

    # Quantity
    qty_str = find_one([
        r"(?:Qty|Quantity)\s*[:#]?\s*(\d+)",
        r"(?:จำนวน)\s*[:#]?\s*(\d+)",
    ]) or "1"
    quantity = int(re.sub(r"[^\d]", "", qty_str) or "1")

    # Unit Price
    price_str = find_one([
        r"(?:Unit\s*Price|Price(?:/Unit)?)\s*[:#]?\s*([\d,]+(?:\.\d+)?)",
        r"(?:ราคา(?:ต่อชิ้น)?)\s*[:#]?\s*([\d,]+(?:\.\d+)?)",
    ]) or "100"
    unit_price = float(re.sub(r"[^\d.]", "", price_str) or "100")

    return {
        "po_id": f"PO{po_id}",
        "vendor_code": vendor.upper(),
        "material_code": material.upper(),
        "quantity": quantity,
        "unit_price": unit_price,
    }

def build_po_record(fields: dict) -> dict:
    total = fields["quantity"] * fields["unit_price"]
    return {
        **fields,
        "currency": "THB",
        "total_amount": total,
        "approved": total <= 50000,
        "created_at": 0
    }


if __name__ == "__main__":
    main()
