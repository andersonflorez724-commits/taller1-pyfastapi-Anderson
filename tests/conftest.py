"""Configuración compartida de pytest para el proyecto.

Añade la carpeta src/ al sys.path para poder importar los paquetes del
proyecto (models, views, templates) y define una fixture autouse que aísla
la persistencia del modelo en un directorio temporal entre cada test.
"""

import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from models import trainee_model  # noqa: E402


@pytest.fixture(autouse=True)
def aislar_persistencia(tmp_path):
    """
    Redirige la persistencia del modelo a un directorio temporal
    y limpia el estado global (trainees) antes y después de cada test.
    """
    trainee_model.DATA_DIR = tmp_path
    trainee_model.DATA_FILE = tmp_path / "trainees.json"
    trainee_model.trainees = []
    yield
    trainee_model.trainees = []
