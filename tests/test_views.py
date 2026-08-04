"""Pruebas unitarias para la capa de vistas (trainee_view)."""

from unittest import mock

import pytest

from helpers import trainee_ok
from models import trainee_model
from views import trainee_view


# --- validate_trainee_data ---

def test_validate_valid_data():
    assert trainee_view.validate_trainee_data(trainee_ok()) == (True, None)


@pytest.mark.parametrize(
    "campo, valor, fragmento_error",
    [
        ("tipo_doc", "XX", "Tipo de documento"),
        ("documento", "12A34", "dígitos"),
        ("nombre", "ab", "3 caracteres"),
        ("ficha", "3406A", "numérico"),
        ("programa", "ab", "descriptivo"),
        ("email", "correo-invalido", "correo"),
    ],
)
def test_validate_rechaza_datos_invalidos(campo, valor, fragmento_error):
    data = trainee_ok()
    data[campo] = valor
    ok, err = trainee_view.validate_trainee_data(data)
    assert ok is False
    assert fragmento_error.lower() in err.lower()


# --- init_app_data ---

def test_init_app_data_loads_from_json():
    trainee_model.trainees = [trainee_ok()]
    trainee_model.save_to_json()
    trainee_model.trainees = []
    trainee_view.init_app_data()
    assert len(trainee_model.get_all()) == 1


# --- register_trainee_view ---

def test_register_trainee_view_invalid_data_shows_error():
    data = trainee_ok()
    data["email"] = "malo"
    with mock.patch.object(trainee_view.trainee_template, "get_trainee_input", return_value=data), \
         mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.register_trainee_view()
    display.assert_called_once()
    msg = display.call_args[0][0]
    assert msg["type"] == "error"
    assert "Validación fallida" in msg["text"]
    assert len(trainee_model.get_all()) == 0


def test_register_trainee_view_duplicate_shows_error():
    trainee_model.register_trainee(trainee_ok())
    with mock.patch.object(trainee_view.trainee_template, "get_trainee_input", return_value=trainee_ok()), \
         mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.register_trainee_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "error"
    assert "Ya existe" in msg["text"]
    assert len(trainee_model.get_all()) == 1


def test_register_trainee_view_success():
    with mock.patch.object(trainee_view.trainee_template, "get_trainee_input", return_value=trainee_ok()), \
         mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.register_trainee_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "success"
    assert "registrado" in msg["text"]
    assert len(trainee_model.get_all()) == 1


# --- status_view ---

def test_status_view_displays_all_trainees():
    trainee_model.trainees = [trainee_ok(), trainee_ok("99999999", "Maria Torres")]
    with mock.patch.object(trainee_view.trainee_template, "display_trainees_list") as display:
        trainee_view.status_view()
    display.assert_called_once_with(trainee_model.get_all())


# --- edit_view ---

def test_edit_view_document_not_found():
    with mock.patch.object(trainee_view.trainee_template, "ask_doc", return_value="00000000"), \
         mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.edit_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "error"
    assert "no encontrado" in msg["text"]


def test_edit_view_invalid_data_shows_error():
    trainee_model.trainees = [trainee_ok()]
    data = trainee_ok()
    data["email"] = "malo"
    with mock.patch.object(trainee_view.trainee_template, "ask_doc", return_value="12345678"), \
         mock.patch.object(trainee_view.trainee_template, "ask_edit_data", return_value=data), \
         mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.edit_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "error"
    assert trainee_model.search_by_document("12345678")["email"] == "juan.perez@example.com"


def test_edit_view_success_updates_model():
    trainee_model.trainees = [trainee_ok()]
    edited = trainee_ok()
    edited["nombre"] = "Juan Carlos Perez"
    with mock.patch.object(trainee_view.trainee_template, "ask_doc", return_value="12345678"), \
         mock.patch.object(trainee_view.trainee_template, "ask_edit_data", return_value=edited), \
         mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.edit_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "success"
    assert trainee_model.search_by_document("12345678")["nombre"] == "Juan Carlos Perez"


# --- delete_view ---

def test_delete_view_document_not_found():
    with mock.patch.object(trainee_view.trainee_template, "ask_doc", return_value="00000000"), \
         mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.delete_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "error"
    assert "no existe" in msg["text"]


def test_delete_view_cancelled():
    trainee_model.trainees = [trainee_ok()]
    with mock.patch.object(trainee_view.trainee_template, "ask_doc", return_value="12345678"), \
         mock.patch.object(trainee_view.trainee_template, "confirm", return_value=False), \
         mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.delete_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "info"
    assert "Cancelado" in msg["text"]
    assert len(trainee_model.get_all()) == 1


def test_delete_view_success_removes_trainee():
    trainee_model.trainees = [trainee_ok()]
    with mock.patch.object(trainee_view.trainee_template, "ask_doc", return_value="12345678"), \
         mock.patch.object(trainee_view.trainee_template, "confirm", return_value=True), \
         mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.delete_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "success"
    assert len(trainee_model.get_all()) == 0


# --- search_view ---

def test_search_view_shows_matching_results():
    trainee_model.trainees = [trainee_ok(), trainee_ok("99999999", "Maria Torres")]
    with mock.patch.object(trainee_view.trainee_template, "ask_keyword", return_value="juan"), \
         mock.patch.object(trainee_view.trainee_template, "show_results") as show:
        trainee_view.search_view()
    show.assert_called_once()
    res, kw = show.call_args[0]
    assert kw == "juan"
    assert [t["documento"] for t in res] == ["12345678"]


def test_search_view_without_results_shows_empty():
    trainee_model.trainees = []
    with mock.patch.object(trainee_view.trainee_template, "ask_keyword", return_value="juan"), \
         mock.patch.object(trainee_view.trainee_template, "show_results") as show:
        trainee_view.search_view()
    show.assert_called_once()
    res, kw = show.call_args[0]
    assert kw == "juan"
    assert res == []


# --- export_view ---

def test_export_view_without_data_shows_error():
    with mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.export_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "error"
    assert "No hay datos" in msg["text"]


def test_export_view_success_creates_csv():
    trainee_model.trainees = [trainee_ok()]
    with mock.patch.object(trainee_view.trainee_template, "display_message") as display:
        trainee_view.export_view()
    msg = display.call_args[0][0]
    assert msg["type"] == "success"
    assert "Exportado" in msg["text"]
    assert (trainee_model.DATA_DIR / "exported_trainees.csv").exists()
