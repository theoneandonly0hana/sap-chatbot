# SAP Data Entry Chatbot — Starter (FastAPI)

A minimal, local-first chatbot to **simulate** SAP data-entry flows (e.g., Purchase Order) and later **switch** to real SAP via OData/RFC once credentials are available.

## Features
- Local web chat UI (`web/index.html`) talking to a FastAPI backend.
- Simple NLU (regex + keyword) for Thai/English intents.
- Data validation with Pydantic.
- **Two backends**:
  - `MockSAP`: writes JSON logs to `./.runtime/mock_sap/` (safe for demo).
  - `RealSAP`: stub showing how to call SAP OData (replace with real base URL + auth).
- Clean separation: `nlu.py`, `schemas.py`, `sap_client.py`, `router_chat.py`.

> Use **mock data only** and access SAP with authorized accounts, per your project’s policy.
> Switch the `BACKEND_MODE` env var when you are ready.
> 
> - BACKEND_MODE=mock (default)
> - BACKEND_MODE=real
>
> See `.env.example` for all variables.
 
## Quickstart
```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8088
```
Open: http://localhost:8088 and use the embedded chat.
(Or open `web/index.html` directly and point to the same port.)

## Example Prompts (TH/EN)
- "สร้าง PO ให้หน่อย จำนวน 3 ชิ้น รหัสสินค้า P-1001 ราคาต่อชิ้น 250 บาท ให้ผู้ขาย V-THA-01"
- "Create a purchase order for 3 units of P-1001 at 250 THB each for vendor V-THA-01"
- "สถานะ PO ล่าสุด"
- "ช่วยกรอกผู้ขายใหม่ ชื่อ: Demo Vendor Thailand, TAXID: 0105555555555"
- "help"

## Folder Layout
```
app/
  main.py          # FastAPI app + static mount
  router_chat.py   # /chat endpoint
  nlu.py           # super-light NLU (regex/keywords)
  schemas.py       # Pydantic models
  sap_client.py    # MockSAP + RealSAP stubs
web/
  index.html       # simple chat UI
  chat.js
tests/
  test_nlu.py
```

## Roadmap
- Swap NLU to Rasa/Transformers.
- Add authentication (JWT) and audit logging.
- Plug to SAP BTP / SAP Gateway OData.
- Integrate Teams/LINE OA via webhook (optional).
