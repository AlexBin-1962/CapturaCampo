import json, sys

# Archivos de entrada/salida
GEO_IN  = "secciones.geojson"
CATALOG = "mun_catalog.json"   # {"1":"Abasolo", "2":"Acámbaro", ...}
GEO_OUT = "secciones_enriquecidas.geojson"

# Carga
with open(GEO_IN, "r", encoding="utf-8") as f: fc = json.load(f)
with open(CATALOG, "r", encoding="utf-8") as f: catalog = json.load(f)

def to_code(v):
    # Acepta strings o números; normaliza a entero (sin ceros a la izquierda)
    try: return str(int(str(v).strip()))
    except: return None

# Campos posibles de código en tu GeoJSON (ajusta si hace falta)
CODE_KEYS = ["MUNICIPIO", "MUN", "CVE_MUN", "MUN_ID"]

for feat in fc.get("features", []):
    p = feat.get("properties", {})
    code_val = None
    for k in CODE_KEYS:
        if k in p and p[k] not in (None, ""):
            code_val = to_code(p[k]); break
    nombre = catalog.get(code_val) if code_val else None
    if nombre:
        p["NOMBREMUN"] = nombre  # <<<<< nuevo campo con el nombre
        # Opcional: si ya existían otros nombres, puedes mantenerlos.
    feat["properties"] = p

with open(GEO_OUT, "w", encoding="utf-8") as f:
    json.dump(fc, f, ensure_ascii=False)
print(f"Listo: {GEO_OUT}")
