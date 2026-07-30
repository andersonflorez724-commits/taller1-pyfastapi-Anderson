import re


def _validar_tipo_doc(valor):
    """Valida tipo de documento en tiempo real."""
    valor = valor.upper()
    if valor not in ["CC", "TI", "CE"]:
        return False, "Tipo de documento inválido. Opciones: CC, TI, CE"
    return True, valor

def _validar_documento(valor):
    """Valida número de documento en tiempo real."""
    if not valor.isdigit():
        return False, "El documento debe contener solo dígitos numéricos."
    if len(valor) < 4:
        return False, "El documento debe tener al menos 4 dígitos."
    return True, valor

def _validar_nombre(valor):
    """Valida nombre completo en tiempo real."""
    valor = valor.strip().title()
    if len(valor) < 3:
        return False, "El nombre debe tener al menos 3 caracteres."
    if not all(c.isalpha() or c.isspace() for c in valor):
        return False, "El nombre solo debe contener letras y espacios."
    return True, valor

def _validar_ficha(valor):
    """Valida número de ficha en tiempo real."""
    if not valor.isdigit():
        return False, "La ficha debe ser un valor numérico."
    if len(valor) < 4:
        return False, "La ficha debe tener al menos 4 dígitos."
    return True, valor

def _validar_programa(valor):
    """Valida programa de formación en tiempo real."""
    valor = valor.strip().title()
    if len(valor) < 3:
        return False, "El programa debe tener al menos 3 caracteres."
    return True, valor

def _validar_email(valor):
    """Valida correo electrónico en tiempo real."""
    valor = valor.strip().lower()
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, valor):
        return False, "Correo inválido. Ejemplo: usuario@dominio.com"
    return True, valor


def _input_validado(prompt, validator, field_name):
    """Solicita input y valida en tiempo real, repitiendo hasta que sea válido."""
    while True:
        valor = input(prompt).strip()
        if not valor:
            print(f"  ⚠️  El campo '{field_name}' no puede estar vacío.")
            continue
        ok, resultado = validator(valor)
        if ok:
            return resultado
        print(f"  ⚠️  {resultado}")


def get_trainee_input():
    """Solicita al usuario los datos del aprendiz incluyendo el correo."""
    print("\n--- 📝 REGISTRO DE APRENDIZ ---")
    id = input("Número de documento: ").strip()
    type_id = input("Tipo de documento (CC/TI/CE): ").strip().upper()
    name = input("Nombre completo: ").strip().title()
    group_code = input("Número de Ficha: ").strip()
    program = input("Programa de Formación: ").strip().title()
    email = input("Correo electrónico: ").strip().lower()

    return {
        "tipo_doc": type_id,
        "documento": id,
        "nombre": name,
        "ficha": group_code,
        "programa": program,
        "email": email,
    }


def display_message(message):
    icons = {"success": "✅ ", "error": "⚠️ ", "info": "ℹ️ "}
    print(f"\n{icons.get(message['type'], '')} {message['text']}")


def display_trainees_list(trainees_list):
    if not trainees_list:
        print("\nNo hay aprendices registrados.")
        return

    print("\n--- Lista de Aprendices Registrados ---")
    for trai in trainees_list:
        print(
            f"Doc: {trai['tipo_doc']} {trai['documento']} | "
            f"Nombre: {trai['nombre']} | "
            f"Ficha: {trai['ficha']} | "
            f"Programa: {trai['programa']} | "
            f"Email: {trai['email']}"
        )


def display_confirm_next():
    """Pregunta al usuario si desea registrar otro aprendiz."""
    display_message({"type": "info", "text": "¿Deseas registrar otro aprendiz? (s/n)"})

    next = input("").strip().lower()
    return next == "s"


# === NUEVAS FUNCIONES ===

def show_menu():
    print("\n" + "="*50)
    print("   🎓 SISTEMA APRENDICES SENA")
    print("="*50)
    for k,v in {"1":"Registrar","2":"Editar","3":"Eliminar",
                 "4":"Buscar","5":"Listar","6":"Exportar CSV","7":"Salir"}.items():
        print(f"  {k}. {v}")
    print("="*50)
    return input("Opción: ").strip()

def ask_doc(action):
    print(f"\n--- 🔧 Documento a {action} ---")
    return input(f"Doc del aprendiz a {action}: ").strip()

def ask_edit_data(t):
    print("\n--- ✏️ Editar (Enter = mantener) ---")
    def q(prompt, default):
        v = input(f"{prompt} [{default}]: ").strip()
        return v or default
    return {
        "tipo_doc": q("Tipo doc", t["tipo_doc"]).upper(),
        "documento": t["documento"],
        "nombre": q("Nombre", t["nombre"]).title(),
        "ficha": q("Ficha", t["ficha"]),
        "programa": q("Programa", t["programa"]).title(),
        "email": q("Email", t["email"]).lower(),
    }

def confirm(msg):
    return input(f"\n⚠️ {msg} (s/n): ").strip().lower() == "s"

def ask_keyword():
    print("\n--- 🔍 Buscar ---")
    return input("Nombre o ficha: ").strip()

def show_results(res, kw):
    if not res:
        print(f"\nSin resultados para '{kw}'")
        return
    print(f"\n--- {len(res)} resultado(s) ---")
    for t in res:
        print(f"  {t['tipo_doc']} {t['documento']} | {t['nombre']} | F:{t['ficha']} | {t['programa']} | {t['email']}")