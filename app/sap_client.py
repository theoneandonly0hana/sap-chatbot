# sap_client.py
import os, json, time, pathlib
from typing import Any
from .schemas import PurchaseOrderIn, VendorIn

RUNTIME_DIR = pathlib.Path(".runtime/mock_sap")
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

class MockSAP:
    def __init__(self):
        self.po_file = RUNTIME_DIR / "purchase_orders.json"
        self.vendor_file = RUNTIME_DIR / "vendors.json"
        if not self.po_file.exists():
            self.po_file.write_text("[]", encoding="utf-8")
        if not self.vendor_file.exists():
            self.vendor_file.write_text("[]", encoding="utf-8")

    def _read(self, f):
        return json.loads(f.read_text(encoding="utf-8"))

    def _write(self, f, data):
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def create_purchase_order(self, data: PurchaseOrderIn):
        items = self._read(self.po_file)
        po_id = f"PO{int(time.time())}"
        total = data.total_amount()
        approved = total <= 50000
        rec = {
            "po_id": po_id,
            **data.model_dump(),
            "total_amount": total,
            "approved": approved,
            "created_at": int(time.time())
        }
        items.append(rec)
        self._write(self.po_file, items)
        return rec

    def list_purchase_orders(self):
        return self._read(self.po_file)[-5:]

    def create_vendor(self, data: VendorIn):
        items = self._read(self.vendor_file)
        code = f"V{int(time.time())}"
        rec = {"vendor_code": code, **data.model_dump()}
        items.append(rec)
        self._write(self.vendor_file, items)
        return rec


class RealSAP:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password

    def create_purchase_order(self, data: PurchaseOrderIn):
        # TODO: call SAP OData endpoint, e.g. /PurchaseOrder
        raise NotImplementedError("Wire this method to your SAP OData service.")

    def list_purchase_orders(self):
        raise NotImplementedError("Wire this method to your SAP OData service.")

    def create_vendor(self, data: VendorIn):
        raise NotImplementedError("Wire this method to your SAP OData service.")


def get_backend():
    mode = os.getenv("BACKEND_MODE", "mock").lower()
    if mode == "real":
        base = os.getenv("SAP_BASE_URL", "https://sap.example.com/odata/")
        user = os.getenv("SAP_USERNAME", "")
        pwd  = os.getenv("SAP_PASSWORD", "")
        return RealSAP(base, user, pwd)
    return MockSAP()
