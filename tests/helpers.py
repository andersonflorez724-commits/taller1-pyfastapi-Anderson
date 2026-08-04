"""Helpers compartidos por los tests del proyecto."""


def trainee_ok(documento="12345678", nombre="Juan Perez", ficha="3406204"):
    """Devuelve un dict con todos los campos válidos de un aprendiz."""
    return {
        "tipo_doc": "CC",
        "documento": documento,
        "nombre": nombre,
        "ficha": ficha,
        "programa": "Analisis y Desarrollo de Software",
        "email": "juan.perez@example.com",
    }
