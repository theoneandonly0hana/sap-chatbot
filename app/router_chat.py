from fastapi import APIRouter
from pydantic import BaseModel
from .nlu import parse_intent
from .sap_client import get_backend
from .schemas import PurchaseOrderIn, VendorIn

router = APIRouter()

class ChatIn(BaseModel):
    message: str

@router.post("/chat")
def chat(payload: ChatIn):
    text = payload.message.strip()
    intent, slots = parse_intent(text)

    backend = get_backend()

    if intent == "create_po":
        data = PurchaseOrderIn(**slots)
        po = backend.create_purchase_order(data)
        note = ""
        if not po["approved"]:
            note = " (ต้องขออนุมัติ)"
        return {
            "reply": f"สร้าง PO เรียบร้อย (demo): {po['po_id']}{note}",
            "intent": intent,
            "data": po
        }

    if intent == "create_vendor":
        data = VendorIn(**slots)
        v = backend.create_vendor(data)
        return {"reply": f"เพิ่มผู้ขายเรียบร้อย (demo): {v['vendor_code']}", "intent": intent, "data": v}

    if intent == "status_po":
        items = backend.list_purchase_orders()
        if not items:
            return {"reply": "ยังไม่มี PO ในระบบ (demo).", "intent": intent}
        lines = [f"{i['po_id']}: {i['material_code']} x{i['quantity']} @ {i['unit_price']} ({i['vendor_code']})" for i in items]
        return {"reply": "PO ล่าสุด:\n- " + "\n- ".join(lines), "intent": intent, "data": items}

    if intent == "help":
        return {"reply": "ฉันช่วยได้: create PO, create vendor, ดูสถานะ PO, พิมพ์ 'help' เพื่อดูตัวอย่าง", "intent": intent}

    return {"reply": "ฉันยังไม่เข้าใจ ลองพิมพ์ 'help' ดูนะ", "intent": intent}
