import json
from pathlib import Path

# Configuración dinámica de la ruta absoluta a data/aprendices.json
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "trainees.json"

trainees = []

def ensure_data_file_exists():
    """Garantiza la existencia de la carpeta data y el archivo JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

def load_from_json():
    """Carga los aprendices guardados en el archivo JSON."""
    global trainees
    ensure_data_file_exists()
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            trainees = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        trainees = []
    return trainees

def save_to_json():
    """Guarda los aprendices en el archivo JSON."""
    ensure_data_file_exists()
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(trainees, f, ensure_ascii=False, indent=4)

def get_all():
    return trainees

def search_by_document(document):
    for a in trainees:
        if a["documento"] == document:
            return a
    return None

def register_trainee(new_trainee):
    if search_by_document(new_trainee["documento"]):
        return False
    trainees.append(new_trainee)
    save_to_json()
    return True


# === FUNCIONES NUEVAS ===

def upd_trainee(doc_id, data):
    """Actualiza aprendiz por documento. Retorna True si existe."""
    for i, t in enumerate(trainees):
        if t["documento"] == doc_id:
            trainees[i] = {**t, **data, "documento": doc_id}
            save_to_json()
            return True
    return False

def rm_trainee(doc_id):
    """Elimina aprendiz por documento usando filter."""
    global trainees
    prev = len(trainees)
    trainees = [t for t in trainees if t["documento"] != doc_id]
    if len(trainees) < prev:
        save_to_json()
        return True
    return False

def find_trainees(keyword):
    """Busca por nombre (parcial) o ficha (exacta)."""
    k = keyword.lower()
    return [t for t in trainees if k in t["nombre"].lower() or keyword == t["ficha"]]

def save_csv(path=None):
    """Exporta a CSV manualmente (sin csv module)."""
    path = path or str(DATA_DIR / "exported_trainees.csv")
    cols = ["tipo_doc","documento","nombre","ficha","programa","email"]
    with open(path, "w", encoding="utf-8") as f:
        f.write(",".join(cols) + "\n")
        for t in trainees:
            row = ",".join(f'"{t[c]}"' for c in cols)
            f.write(row + "\n")
    return path