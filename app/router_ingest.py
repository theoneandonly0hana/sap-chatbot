# app/router_ingest.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from .sap_client import get_backend
from .schemas import PurchaseOrderIn
from .extractors import (
    extract_from_image, extract_from_pdf,
    extract_from_excel, extract_from_csv,
    parse_po_from_text
)

router = APIRouter()

@router.post("/ingest/po")
async def ingest_po(file: UploadFile = File(...)):
    content = await file.read()
    name = file.filename.lower()

    try:
        if name.endswith((".png", ".jpg", ".jpeg")):
            text = extract_from_image(content)
            slots = parse_po_from_text(text)
        elif name.endswith(".pdf"):
            text = extract_from_pdf(content)
            slots = parse_po_from_text(text)
        elif name.endswith((".xlsx", ".xls")):
            df = extract_from_excel(content)
            # คาดหัวคอลัมน์: quantity, material_code, unit_price, vendor_code, currency
            created = []
            backend = get_backend()
            for _, row in df.iterrows():
                data = PurchaseOrderIn(
                    quantity=int(row.get("quantity", 1)),
                    material_code=str(row.get("material_code", "P-1001")),
                    unit_price=float(row.get("unit_price", 100.0)),
                    vendor_code=str(row.get("vendor_code", "V-THA-01")),
                    currency=str(row.get("currency", "THB")),
                )
                created.append(backend.create_purchase_order(data))
            return {"ok": True, "count": len(created), "data": created}
        elif name.endswith(".csv"):
            df = extract_from_csv(content)
            created = []
            backend = get_backend()
            for _, row in df.iterrows():
                data = PurchaseOrderIn(
                    quantity=int(row.get("quantity", 1)),
                    material_code=str(row.get("material_code", "P-1001")),
                    unit_price=float(row.get("unit_price", 100.0)),
                    vendor_code=str(row.get("vendor_code", "V-THA-01")),
                    currency=str(row.get("currency", "THB")),
                )
                created.append(backend.create_purchase_order(data))
            return {"ok": True, "count": len(created), "data": created}
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # สำหรับภาพ/PDF → ได้ slots จากข้อความ
        data = PurchaseOrderIn(**slots)
        po = get_backend().create_purchase_order(data)
        return {"ok": True, "data": po, "extracted_text_sample": (text[:400] if len(text) > 400 else text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ingest error: {e}")
