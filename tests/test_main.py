"""Pruebas unitarias para el punto de entrada de la aplicación (main)."""

from unittest import mock

from main import main


def test_main_sale_con_opcion_7(capsys):
    with mock.patch("builtins.input", return_value="7"):
        main()
    assert "Hasta luego" in capsys.readouterr().out


def test_main_muestra_error_con_opcion_invalida(capsys):
    with mock.patch("builtins.input", side_effect=["9", "7"]):
        main()
    salida = capsys.readouterr().out
    assert "Opción inválida" in salida
    assert "Hasta luego" in salida


def test_main_ejecuta_opcion_de_listado(capsys):
    # Opción 5 (listar) + Enter para continuar + opción 7 (salir)
    with mock.patch("builtins.input", side_effect=["5", "", "7"]):
        main()
    salida = capsys.readouterr().out
    assert "No hay aprendices registrados." in salida
    assert "Hasta luego" in salida
