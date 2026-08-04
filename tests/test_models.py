"""Pruebas unitarias para la capa de modelos (trainee_model)."""

import json
from pathlib import Path

from helpers import trainee_ok
from models import trainee_model


# --- ensure_data_file_exists ---

def test_ensure_data_file_exists_creates_file():
    assert not trainee_model.DATA_FILE.exists()
    trainee_model.ensure_data_file_exists()
    assert trainee_model.DATA_FILE.exists()
    with trainee_model.DATA_FILE.open("r", encoding="utf-8") as f:
        assert json.load(f) == []


# --- load_from_json ---

def test_load_from_json_without_file_returns_empty_list():
    result = trainee_model.load_from_json()
    assert result == []
    assert trainee_model.trainees == []


def test_load_from_json_reads_existing_file():
    data = [trainee_ok(), trainee_ok("99999999", "Maria Torres", "1111")]
    with trainee_model.DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    assert trainee_model.load_from_json() == data
    assert len(trainee_model.trainees) == 2


def test_load_from_json_with_corrupt_file_returns_empty_list():
    with trainee_model.DATA_FILE.open("w", encoding="utf-8") as f:
        f.write("{esto no es json valido")
    assert trainee_model.load_from_json() == []


# --- save_to_json ---

def test_save_to_json_writes_current_trainees():
    trainee_model.trainees = [trainee_ok()]
    trainee_model.save_to_json()
    with trainee_model.DATA_FILE.open("r", encoding="utf-8") as f:
        assert json.load(f) == trainee_model.trainees


# --- get_all / search_by_document ---

def test_get_all_returns_current_trainees():
    trainee_model.trainees = [trainee_ok()]
    assert trainee_model.get_all() == [trainee_ok()]


def test_search_by_document_found():
    trainee_model.trainees = [trainee_ok(), trainee_ok("99999999")]
    found = trainee_model.search_by_document("99999999")
    assert found is not None
    assert found["nombre"] == "Juan Perez"


def test_search_by_document_not_found():
    trainee_model.trainees = [trainee_ok()]
    assert trainee_model.search_by_document("00000000") is None


# --- register_trainee ---

def test_register_trainee_success():
    assert trainee_model.register_trainee(trainee_ok()) is True
    assert len(trainee_model.get_all()) == 1
    # El aprendiz queda persistido en el archivo JSON
    assert len(trainee_model.load_from_json()) == 1


def test_register_trainee_duplicate_returns_false():
    trainee_model.trainees = [trainee_ok()]
    assert trainee_model.register_trainee(trainee_ok()) is False
    assert len(trainee_model.trainees) == 1


# --- upd_trainee ---

def test_upd_trainee_updates_data_and_preserves_documento():
    trainee_model.trainees = [trainee_ok()]
    data = {"nombre": "Juan Carlos Perez", "email": "jc.perez@example.com"}
    assert trainee_model.upd_trainee("12345678", data) is True
    updated = trainee_model.search_by_document("12345678")
    assert updated["nombre"] == "Juan Carlos Perez"
    assert updated["email"] == "jc.perez@example.com"
    assert updated["documento"] == "12345678"


def test_upd_trainee_not_found_returns_false():
    trainee_model.trainees = [trainee_ok()]
    assert trainee_model.upd_trainee("00000000", {"nombre": "X"}) is False


# --- rm_trainee ---

def test_rm_trainee_removes_and_returns_true():
    trainee_model.trainees = [trainee_ok(), trainee_ok("99999999")]
    assert trainee_model.rm_trainee("12345678") is True
    assert len(trainee_model.trainees) == 1
    assert trainee_model.search_by_document("12345678") is None


def test_rm_trainee_not_found_returns_false():
    trainee_model.trainees = [trainee_ok()]
    assert trainee_model.rm_trainee("00000000") is False
    assert len(trainee_model.trainees) == 1


# --- find_trainees ---

def test_find_trainees_by_partial_name_case_insensitive():
    trainee_model.trainees = [trainee_ok(), trainee_ok("99999999", "Maria Torres", "2222")]
    res = trainee_model.find_trainees("MARIA")
    assert [t["documento"] for t in res] == ["99999999"]


def test_find_trainees_by_exact_ficha():
    trainee_model.trainees = [trainee_ok(), trainee_ok("99999999", "Maria Torres", "2222")]
    res = trainee_model.find_trainees("2222")
    assert [t["documento"] for t in res] == ["99999999"]


def test_find_trainees_without_results():
    trainee_model.trainees = [trainee_ok()]
    assert trainee_model.find_trainees("zzzz") == []


# --- save_csv ---

def test_save_csv_without_data_writes_only_header():
    trainee_model.trainees = []
    path = trainee_model.save_csv()
    assert Path(path).read_text(encoding="utf-8").strip() == \
        "tipo_doc,documento,nombre,ficha,programa,email"


def test_save_csv_default_path_and_content():
    trainee_model.trainees = [trainee_ok()]
    path = trainee_model.save_csv()
    expected = trainee_model.DATA_DIR / "exported_trainees.csv"
    assert path == str(expected)
    content = expected.read_text(encoding="utf-8")
    lines = content.strip().splitlines()
    # Encabezado sin comillas
    assert lines[0] == "tipo_doc,documento,nombre,ficha,programa,email"
    # Los valores de cada fila van entre comillas
    assert '"12345678"' in lines[1]
    assert '"Juan Perez"' in lines[1]


def test_save_csv_custom_path(tmp_path):
    trainee_model.trainees = [trainee_ok()]
    custom = tmp_path / "custom_export.csv"
    assert trainee_model.save_csv(str(custom)) == str(custom)
    assert custom.exists()
