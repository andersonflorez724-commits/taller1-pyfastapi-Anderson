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