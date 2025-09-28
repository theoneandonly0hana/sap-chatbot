from app.schemas import PurchaseOrderIn
from app.sap_client import MockSAP

def test_po_under_limit_is_approved():
    data = PurchaseOrderIn(material_code="P-1001", quantity=5, unit_price=2000, vendor_code="V-001")
    sap = MockSAP()
    po = sap.create_purchase_order(data)
    assert po["total_amount"] == 10000
    assert po["approved"] is True

def test_po_over_limit_needs_approval():
    data = PurchaseOrderIn(material_code="P-2000", quantity=1000, unit_price=100, vendor_code="V-002")
    sap = MockSAP()
    po = sap.create_purchase_order(data)
    assert po["total_amount"] == 100000
    assert po["approved"] is False

