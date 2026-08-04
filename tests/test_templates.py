"""Pruebas unitarias para la capa de templates (trainee_template)."""

from unittest import mock

import pytest

from helpers import trainee_ok
from templates import trainee_template


# --- Validadores individuales ---

@pytest.mark.parametrize(
    "validator, valor, esperado",
    [
        (trainee_template._validar_tipo_doc, "cc", "CC"),
        (trainee_template._validar_tipo_doc, "ti", "TI"),
        (trainee_template._validar_documento, "1234", "1234"),
        (trainee_template._validar_nombre, "  juan perez  ", "Juan Perez"),
        (trainee_template._validar_ficha, "3406", "3406"),
        (trainee_template._validar_programa, "  adso  ", "Adso"),
        (trainee_template._validar_email, "USER@EXAMPLE.COM", "user@example.com"),
    ],
)
def test_validadores_aceptan_valores_validos(validator, valor, esperado):
    ok, resultado = validator(valor)
    assert ok is True
    assert resultado == esperado


@pytest.mark.parametrize(
    "validator, valor",
    [
        (trainee_template._validar_tipo_doc, "XX"),
        (trainee_template._validar_documento, "12"),
        (trainee_template._validar_documento, "12ab"),
        (trainee_template._validar_nombre, "ab"),
        (trainee_template._validar_nombre, "juan1"),
        (trainee_template._validar_ficha, "34"),
        (trainee_template._validar_ficha, "340a"),
        (trainee_template._validar_programa, "ab"),
        (trainee_template._validar_email, "malo"),
        (trainee_template._validar_email, "a@b"),
    ],
)
def test_validadores_rechazan_valores_invalidos(validator, valor):
    ok, _ = validator(valor)
    assert ok is False


# --- _input_validado ---

def test_input_validado_repite_hasta_obtener_valor_valido(capsys):
    with mock.patch("builtins.input", side_effect=["", "12", "1234"]):
        resultado = trainee_template._input_validado(
            "Documento: ", trainee_template._validar_documento, "Documento"
        )
    assert resultado == "1234"
    salida = capsys.readouterr().out
    assert "no puede estar vacío" in salida
    assert "al menos 4 dígitos" in salida


def test_input_validado_editar_repite_con_valor_invalido(capsys):
    # "ab" es inválido (menos de 3 caracteres); Enter conserva el valor por defecto
    with mock.patch("builtins.input", side_effect=["ab", ""]):
        resultado = trainee_template._input_validado_editar(
            "Nombre", "Juan Perez", trainee_template._validar_nombre, "Nombre"
        )
    assert resultado == "Juan Perez"
    assert "al menos 3 caracteres" in capsys.readouterr().out


# --- get_trainee_input / ask_edit_data ---

def test_get_trainee_input_devuelve_dict_completo_y_normalizado():
    entradas = ["cc", "1234", "juan perez", "3406", "adso", "JUAN@EXAMPLE.COM"]
    with mock.patch("builtins.input", side_effect=entradas):
        data = trainee_template.get_trainee_input()
    assert data == {
        "tipo_doc": "CC",
        "documento": "1234",
        "nombre": "Juan Perez",
        "ficha": "3406",
        "programa": "Adso",
        "email": "juan@example.com",
    }


def test_ask_edit_data_mantiene_valores_por_defecto():
    entradas = ["", "juan perez", "", "adso", "NUEVO@EXAMPLE.COM"]
    with mock.patch("builtins.input", side_effect=entradas):
        data = trainee_template.ask_edit_data(trainee_ok())
    assert data == {
        "tipo_doc": "CC",
        "documento": "12345678",
        "nombre": "Juan Perez",
        "ficha": "3406204",
        "programa": "Adso",
        "email": "nuevo@example.com",
    }


# --- Funciones de salida ---

def test_display_message_imprime_mensaje(capsys):
    trainee_template.display_message({"type": "success", "text": "Registrado ok"})
    assert "Registrado ok" in capsys.readouterr().out


def test_display_trainees_list_sin_datos(capsys):
    trainee_template.display_trainees_list([])
    assert "No hay aprendices registrados." in capsys.readouterr().out


def test_display_trainees_list_con_datos(capsys):
    trainee_template.display_trainees_list([trainee_ok()])
    salida = capsys.readouterr().out
    assert "Juan Perez" in salida
    assert "12345678" in salida


def test_show_results_sin_resultados(capsys):
    trainee_template.show_results([], "juan")
    assert "Sin resultados para 'juan'" in capsys.readouterr().out


def test_show_results_con_resultados(capsys):
    trainee_template.show_results([trainee_ok()], "juan")
    salida = capsys.readouterr().out
    assert "1 resultado(s)" in salida
    assert "Juan Perez" in salida


# --- Funciones de entrada ---

def test_display_confirm_next_acepta_si(capsys):
    with mock.patch("builtins.input", return_value="s"):
        assert trainee_template.display_confirm_next() is True


def test_display_confirm_next_rechaza_no():
    with mock.patch("builtins.input", return_value="n"):
        assert trainee_template.display_confirm_next() is False


def test_show_menu_retorna_opcion(capsys):
    with mock.patch("builtins.input", return_value="7"):
        assert trainee_template.show_menu() == "7"
    assert "SISTEMA APRENDICES SENA" in capsys.readouterr().out


def test_ask_doc_retorna_documento(capsys):
    with mock.patch("builtins.input", return_value="12345678"):
        assert trainee_template.ask_doc("editar") == "12345678"


def test_confirm_retorna_true_si_es_s():
    with mock.patch("builtins.input", return_value="s"):
        assert trainee_template.confirm("¿Eliminar?") is True


def test_confirm_retorna_false_si_no_es_s():
    with mock.patch("builtins.input", return_value="x"):
        assert trainee_template.confirm("¿Eliminar?") is False


def test_ask_keyword_retorna_termino():
    with mock.patch("builtins.input", return_value="juan"):
        assert trainee_template.ask_keyword() == "juan"
