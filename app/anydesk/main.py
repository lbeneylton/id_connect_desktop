import os

from AnyDesk.RosterParser import AnydeskParser
from AnyDesk.FileManager import FileManager
from AnyDesk.Validator import JsonValidator




def menu():
    print("\n=== ANYDESK ROSTER MANAGER ===")
    print("1 - Exportar hosts")
    print("2 - Importar hosts")
    print("0 - Sair")


def build_repo():
    parser = AnydeskParser()
    file_manager = FileManager(PATH_CONF)
    validator = JsonValidator()

    return AnydeskRepository(
        parser=parser,
        file_manager=file_manager,
        validator=validator
    )


def export_menu(repo, export_path):
    print("\n--- EXPORTAÇÃO ---")

    ok = repo.export_json(export_path)
    print("✔ OK" if ok else "✖ Falha")


def import_menu(repo, import_file):
    print("\n--- IMPORTAÇÃO ---")

    ok = repo.import_json(import_file)
    print("✔ OK" if ok else "✖ Falha")


def main():
    export_path = "exports"
    os.makedirs("import", exist_ok=True)
    import_file = os.path.join("import", "current.json")
    repo = build_repo()

    while True:
        menu()
        option = input("\nEscolha uma opção: ").strip()

        if option == "1":
            export_menu(repo, export_path)

        elif option == "2":
            import_menu(repo, import_file)

        elif option == "0":
            break

        else:
            print("❌ Opção inválida")


if __name__ == "__main__":
    main()
