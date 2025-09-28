import re

# Very light "rule/regex" NLU supporting TH/EN demo.
# Returns (intent, slots)

def _extract_number(text_norm: str):
    """
    Short form:
      'สร้าง PO 3 P-1001 250 V-THA-01'
    NOTE: text_norm ต้องถูก normalize (ppo->po, ช่องว่างขีด -> '-') และ lower() มาก่อน
    """
    m = re.search(
        r"สร้าง\s*po\s+(\d+)\s+([a-z0-9\-]+)\s+(\d+(?:\.\d+)?)\s+([a-z0-9\-]+)",
        text_norm,
        flags=re.I,
    )
    if m:
        return "create_po", {
            "quantity": int(m.group(1)),
            "material_code": m.group(2).upper(),
            "unit_price": float(m.group(3)),
            "vendor_code": m.group(4).upper(),
            "currency": "THB",
        }
    return None

def parse_intent(text: str):
    # ทำสำเนา & normalize (lowercase + typo + ช่องว่างขีด)
    t = text.strip().lower()
    t = t.replace("ppo", "po")            # แก้สะกดผิด
    t = re.sub(r"\s*-\s*", "-", t)        # 'V-    -THA-01' -> 'V-THA-01'

    # HELP
    if t in {"help", "ช่วยด้วย", "วิธีใช้", "usage"}:
        return "help", {}

    # STATUS PO
    if "สถานะ po" in t or "po ล่าสุด" in t or "status po" in t:
        return "status_po", {}

    # CREATE PO (short-form ก่อน)
    res = _extract_number(t)
    if res:
        return res

    # CREATE PO (long-form TH/EN)
    if ("สร้าง" in t or "create" in t) and (re.search(r"p+o", t) or "purchase order" in t):
        qty_match      = re.search(r"(จำนวน|qty)\s*[:：]?\s*(\d+)", t, flags=re.I)
        material_match = re.search(r"(รหัสสินค้า|material|sku)\s*[:：]?\s*([a-z0-9\-]+)", t, flags=re.I)
        price_match    = re.search(r"(ราคา(?:ต่อชิ้น)?|price)\s*[:：]?\s*(\d+(?:\.\d+)?)", t, flags=re.I)
        vendor_match   = re.search(r"(ผู้ขาย|vendor)\s*[:：]?\s*([a-z0-9\-]+)", t, flags=re.I)

        slots = {
            "quantity": int(qty_match.group(2)) if qty_match else 1,
            "material_code": material_match.group(2).upper() if material_match else "P-1001",
            "unit_price": float(price_match.group(2)) if price_match else 100.0,
            "vendor_code": vendor_match.group(2).upper() if vendor_match else "V-THA-01",
            "currency": "THB",
        }
        return "create_po", slots

    # CREATE VENDOR (ย้ายมาหลัง PO เพื่อไม่ให้แย่ง match)
    if "ผู้ขาย" in t or "vendor" in t:
        name_match = re.search(r"(ชื่อ|name)\s*[:：]\s*([^,]+)", text, flags=re.I)
        tax_match  = re.search(r"(taxid|tax id|เลขผู้เสียภาษี)\s*[:：]\s*([0-9A-Za-z\-]+)", text, flags=re.I)
        name  = name_match.group(2).strip() if name_match else "Demo Vendor"
        taxid = tax_match.group(2).strip() if tax_match else "0105555555555"
        return "create_vendor", {"name": name, "tax_id": taxid, "country": "TH"}

    return "unknown", {}
