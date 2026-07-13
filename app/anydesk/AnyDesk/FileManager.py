import os
import shutil
import json
from datetime import datetime


class FileManager:
    def __init__(self, user_conf: str):
        self.user_conf = user_conf

    def read_lines(self) -> list[str]:
        """Lê arquivo e retorna uma lista de linhas"""
        with open(self.user_conf, "r", encoding="utf-8") as f:
            return f.readlines()

    def write_atomic(self, lines: list[str]) -> None:
        tmp = self.user_conf + ".tmp"

        with open(tmp, "w", encoding="utf-8") as f:
            f.writelines(lines)

        os.replace(tmp, self.user_conf)

    def backup(self) -> str:
        backup_dir = "backup"
        os.makedirs(backup_dir, exist_ok=True)

        ts = datetime.now().strftime("%d-%m-%Y_%H-%M")
        path = os.path.join(backup_dir, f"user_{ts}.conf")

        if os.path.exists(self.user_conf):
            shutil.copy2(self.user_conf, path)

        return path

    def write_json(self, path: str, data: list[dict]) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def generate_export_path(self, folder: str) -> str:
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        return os.path.join(folder, f"rosters_{timestamp}.json")
