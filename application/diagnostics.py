from datetime import datetime
import json
import os

diagnostics_path = os.path.join(os.path.dirname(__file__), "diagnostics.json")
with open(diagnostics_path, 'w', encoding='utf-8'):
    pass

logs = []

def register_log(fn):
    logs.append(fn)

def log(id, source, msg):
    entry = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": id,
        "source": source,
        "msg": msg
    }
    
    with open(diagnostics_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    for fn in list(logs):
        try:
            fn(entry["datetime"], entry["id"], entry["source"], entry["msg"])
        except Exception:
            pass