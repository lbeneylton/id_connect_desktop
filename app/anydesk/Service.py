import json

from app.anydesk.FileManager import FileManager, file_manager
from app.anydesk.RosterParser import AnydeskParser, parser
from app.anydesk.Host import HostDTO

from app.service.api import  ApiAccess, api


class AnydeskService:
    def __init__(
        self,
        parser: AnydeskParser = parser,
        file_manager: FileManager = file_manager,
        api: ApiAccess = api
    ):
        self.parser = parser
        self.fm = file_manager
        self.api = api


    def _get_rosters(self) -> list[HostDTO]:
        """
        fm -> Le todas as linhasw
        parser -> Procura a linha de rosters
        retorna se achar
        retorna [] se não achar
        """
        for line in self.fm.read_lines():
            result = self.parser.parse_roster_line(line)

            if result:
                _, items = result
                return items

        return []

    # -----------------------
    # METODOS PUBLICOS
    # ------------------------

    def export_hosts(self) -> bool:
        """
        Recupera os rosters do arquivo
        Organiza em ordem alfabetica
        Cria o json com historico
        """
        
        # Recupera uma lista de objetos HostDTO
        items = self._get_rosters()

        if not items:
            return False

        # Ordena alfabeticamente pelo alias (desnecessario talvez)
        sorted_items = sorted(
            items,
            key=lambda x: x.alias.upper()
        )
    
        
        try:  
            formated = []
            for item in sorted_items:
                formated.append(
                    {
                        "id_connect": int(item.id_connect),
                        "alias": item.alias,
                        "provider": item.provider,
                    }
                )
            
            self.api.exportar_all(formated)        
        except Exception as e:
            print(str(e))
            return False

        return True


    def import_hosts(self):

        self.fm.backup()

        def processar_importacao(items: dict):
            new_items = [
                HostDTO(**item)
                for item in items
            ]

            try:
                for item in new_items:
                    print(item, "\n\n")

                existing = self._get_rosters()

                merged = {
                    item.id_connect: item
                    for item in existing
                }

                for item in new_items:
                    merged[item.id_connect] = item


                sorted_rosters = sorted(
                    merged.values(),
                    key=lambda x: x.alias.lower()
                )


                formatted = self.parser.build_roster_line(
                    sorted_rosters
                )


                new_lines = [
                    l for l in self.fm.read_lines()
                    if not self.parser.is_roster_line(l)
                ]


                new_lines.append(
                    f"ad.roster.items={formatted}\n"
                )


                self.fm.write_atomic(new_lines)

                return True


            except Exception as erro:
                print("Erro import hosts:", erro)
                return False 


        # chama API e espera retorno
        self.api.importar_all(
            processar_importacao
        )




service = AnydeskService()
