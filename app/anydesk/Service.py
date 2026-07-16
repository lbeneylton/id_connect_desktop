import os
import json

from FileManager import FileManager, file_manager
from RosterParser import AnydeskParser, parser
from Host import HostDTO

from service.api import  ApiAccess, api


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
        print(sorted_items)

        # MANDAR PARA API
        # self.api.exportar_all(sorted_items)        


        return True

    def import_json(self, file: str) -> bool:

        # RECEBER DA API
        self.fm.backup()

        try:
            with open(file, "r", encoding="utf-8") as f:
                new_items = json.load(f)
        except FileNotFoundError:
            return False

        # valid, msg = self.validator.validate_rosters(new_items)
        # if not valid:
        #     print(msg)
        #     return False

        existing = self._get_rosters()

        # merged = {
        #     i["id"]: i["alias"] for i in existing
        # }

        # merged.update({
        #     i["id"]: i["alias"] for i in new_items
        # })

        # sorted_rosters = sorted(
        #     [{"id": k, "alias": v} for k, v in merged.items()],
        #     key=lambda x: x["alias"].lower()
        # )

        # formatted = self.parser.build_roster_line(sorted_rosters)

        new_lines = [
            l for l in self.fm.read_lines()
            if not self.parser.is_roster_line(l)
        ]

       #  new_lines.append(f"ad.roster.items={formatted}\n")

        self.fm.write_atomic(new_lines)

        return True


service = AnydeskService()
service.export_hosts()