import random, time, json, pathlib
R = pathlib.Path(".runtime/mock_sap"); R.mkdir(parents=True, exist_ok=True)
vendors = [{"vendor_code": f"V-THA-{i:03d}", "name": f"Vendor TH {i}", "tax_id": f"01055{100000+i}", "country":"TH"} for i in range(1,21)]
materials = [{"material_code": f"P-{1000+i}", "unit_price": random.choice([75,120,250,499.5]), "currency":"THB"} for i in range(1,21)]
(R/"vendors.json").write_text(json.dumps(vendors, ensure_ascii=False, indent=2), "utf-8")
pos=[]
for i in range(1,51):
    m=random.choice(materials); v=random.choice(vendors)
    pos.append({"po_id": f"PO{int(time.time())}{i}", "material_code": m["material_code"],
                "quantity": random.randint(1,9), "unit_price": m["unit_price"],
                "vendor_code": v["vendor_code"], "currency":"THB"})
(R/"purchase_orders.json").write_text(json.dumps(pos, ensure_ascii=False, indent=2), "utf-8")
print("Seeded vendors & POs.")
