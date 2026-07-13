import os
import json

from AnyDesk.Validator import JsonValidator
from AnyDesk.FileManager import FileManager
from AnyDesk.RosterParser import AnydeskParser


class AnydeskRepository:
    def __init__(
        self,
        parser: AnydeskParser,
        file_manager: FileManager,
        validator: JsonValidator
    ):
        self.parser = parser
        self.fm = file_manager
        self.validator = validator

    def _get_rosters(self) -> list[dict]:
        for line in self.fm.read_lines():
            result = self.parser.parse_roster_line(line)

            if result:
                _, items = result
                return items

        return []

    # -----------------------
    # METODOS PUBLICOS
    # ------------------------

    def export_json(self,  folder: str) -> bool:
        """
        Recupera os rosters do arquivo
        Organiza em ordem alfabetica
        Cria o json com historico
        """
        items = self._get_rosters()

        if not items:
            return False

        sorted_items = sorted(
            items,
            key=lambda x: x["alias"].lower()
        )

        # MANDAR PARA API

        # gera JSON atual
        self.fm.write_json(
            os.path.join(folder, "current.json"),
            sorted_items
        )

        # gera histórico
        self.fm.write_json(
            self.fm.generate_export_path(folder),
            sorted_items
        )

        return True

    def import_json(self, file: str) -> bool:

        # RECEBER DA API
        self.fm.backup()

        try:
            with open(file, "r", encoding="utf-8") as f:
                new_items = json.load(f)
        except FileNotFoundError:
            return False

        valid, msg = self.validator.validate_rosters(new_items)
        if not valid:
            print(msg)
            return False

        existing = self._get_rosters()

        merged = {
            i["id"]: i["alias"] for i in existing
        }

        merged.update({
            i["id"]: i["alias"] for i in new_items
        })

        sorted_rosters = sorted(
            [{"id": k, "alias": v} for k, v in merged.items()],
            key=lambda x: x["alias"].lower()
        )

        formatted = self.parser.build_roster_line(sorted_rosters)

        new_lines = [
            l for l in self.fm.read_lines()
            if not self.parser.is_roster_line(l)
        ]

        new_lines.append(f"ad.roster.items={formatted}\n")

        self.fm.write_atomic(new_lines)

        return True
