"""Módulo responsável pelo gerenciamento de arquivos de configuração do AnyDesk."""

import os
import shutil
import logging
from datetime import datetime

# Configuração do Logger
logger = logging.getLogger(__name__)

# Caminho padrão para o arquivo de configuração do AnyDesk no Windows AppData
PATH_CONF = os.path.expanduser(r"~\AppData\Roaming\AnyDesk\user.conf")


class FileManager:
    """Responsável exclusivo pela leitura, escrita atômica e backup seguro de arquivos."""

    def __init__(self, user_conf: str):
        """Inicializa o FileManager com o caminho do arquivo de destino.

        Args:
            user_conf (str): Caminho absoluto para o arquivo de configuração (.conf).
        """
        self.user_conf = os.path.abspath(user_conf)

    def read_lines(self) -> list[str]:
        """Lê todas as linhas do arquivo de configuração de forma segura.

        Returns:
            list[str]: Lista de linhas lidas. Retorna uma lista vazia se o arquivo
                não existir.

        Raises:
            IOError: Se houver erro de leitura do arquivo.
        """
        if not os.path.exists(self.user_conf):
            logger.warning(f"O arquivo {self.user_conf} não existe.")
            return []

        try:
            with open(self.user_conf, "r", encoding="utf-8") as f:
                return f.readlines()
        except Exception as e:
            logger.error(f"Erro ao ler o arquivo {self.user_conf}: {e}")
            raise IOError(f"Não foi possível ler o arquivo de configuração: {e}") from e

    def write_atomic(self, lines: list[str]) -> None:
        """Escreve uma lista de linhas no arquivo de forma atômica.

        Garante a integridade dos dados escrevendo primeiro em um arquivo temporário (.tmp)
        e depois substituindo o arquivo final.

        Args:
            lines (list[str]): Linhas a serem salvas no arquivo.

        Raises:
            IOError: Se ocorrer erro na escrita ou substituição do arquivo.
        """
        tmp_path = self.user_conf + ".tmp"
        try:
            # Garante que o diretório pai existe
            os.makedirs(os.path.dirname(self.user_conf), exist_ok=True)

            with open(tmp_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            # Substitui atomicamente o arquivo antigo pelo novo
            os.replace(tmp_path, self.user_conf)
        except Exception as e:
            logger.error(f"Erro na escrita atômica em {self.user_conf}: {e}")
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            raise IOError(f"Falha na gravação atômica do arquivo: {e}") from e

    def backup(self) -> str:
        """Cria um backup datado do arquivo de configuração atual.

        O backup é salvo em uma pasta absoluta 'backups/' localizada no diretório
        raiz do aplicativo.

        Returns:
            str: Caminho completo para o arquivo de backup criado, ou string vazia
                se o arquivo original não existir ou falhar.
        """
        if not os.path.exists(self.user_conf):
            logger.warning(f"Arquivo {self.user_conf} não existe para backup.")
            return ""

        try:
            # Caminho absoluto da raiz do projeto para criar o diretório de backups
            app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            backup_dir = os.path.join(app_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)

            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_path = os.path.join(backup_dir, f"user_{ts}.conf")

            shutil.copy2(self.user_conf, backup_path)
            logger.info(f"Backup criado com sucesso em: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Falha ao realizar backup de {self.user_conf}: {e}")
            return ""


# Instância global configurada com o caminho padrão
file_manager = FileManager(PATH_CONF)