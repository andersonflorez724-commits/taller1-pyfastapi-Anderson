from views import trainee_view
from templates import trainee_template

def main():
    trainee_view.init_app_data()
    
    # Dispatch dictionary - estilo moderno
    menu = {
        "1": trainee_view.register_trainee_view,
        "2": trainee_view.edit_view,
        "3": trainee_view.delete_view,
        "4": trainee_view.search_view,
        "5": trainee_view.status_view,
        "6": trainee_view.export_view,
    }
    
    while True:
        opt = trainee_template.show_menu()
        if opt == "7":
            print("\n👋 ¡Hasta luego!")
            break
        fn = menu.get(opt)
        if fn:
            fn()
            input("\nEnter para continuar...")
        else:
            trainee_template.display_message({"type": "error", "text": "Opción inválida."})

if __name__ == "__main__":
    main()