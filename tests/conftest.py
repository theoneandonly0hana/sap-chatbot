# tests/conftest.py
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]  # โฟลเดอร์โปรเจ็กต์ (ที่มีโฟลเดอร์ app/)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
