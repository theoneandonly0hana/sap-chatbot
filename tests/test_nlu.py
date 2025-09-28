from app.nlu import parse_intent

def test_create_po():
    intent, slots = parse_intent('สร้าง PO จำนวน 2 รหัสสินค้า P-1001 ราคา 50 ผู้ขาย V-THA-01')
    assert intent == 'create_po'
    assert slots['quantity'] == 2
    assert slots['material_code'] == 'P-1001'
    assert slots['unit_price'] == 50.0
    assert slots['vendor_code'] == 'V-THA-01'





