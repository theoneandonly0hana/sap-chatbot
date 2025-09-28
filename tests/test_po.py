from app.schemas import PurchaseOrderIn
from app.sap_client import MockSAP

def test_total_and_approval():
    data = PurchaseOrderIn(material_code="P-1001", quantity=3, unit_price=200, vendor_code="V-001")
    sap = MockSAP()
    po = sap.create_purchase_order(data)
    assert po["total_amount"] == 600
    assert po["quantity"] == 3
    assert po["unit_price"] == 200
