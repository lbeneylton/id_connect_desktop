"""Gerencia a leitura dos arquivos de peers."""

import os
import toml
import logging

from app.rustdesk.Host import HostDTO

# Configuração do Logger
logger = logging.getLogger(__name__)

PATH_CONF = os.path.expanduser(r"~\AppData\Roaming\RustDesk")


class PeerManager:
    def __init__(self, path_conf: str = PATH_CONF) -> None:
        self.path_conf = os.path.abspath(path_conf)
        self.peers_dir = os.path.join(self.path_conf, "config", "peers")

    def read_peers(self) -> list[HostDTO]:
        """Lê todos os arquivos .toml e retorna a lista de peers."""
        peers = []

        if not os.path.exists(self.peers_dir):
            return peers

        for filename in os.listdir(self.peers_dir):
            if not filename.endswith(".toml"):
                continue

            file_path = os.path.join(self.peers_dir, filename)

            try:
                data = toml.load(file_path)

                alias = data.get("options", {}).get("alias")
                peer_id = int(os.path.splitext(filename)[0])

                peers.append(
                    HostDTO(
                        alias=alias or str(peer_id),
                        id_connect=peer_id,
                        provider="RUST",
                    )
                )

            except Exception as exc:
                logger.warning("Erro ao ler o peer '%s': %s", filename, exc)
                continue

        return peers

    def write_peers(self, peers: list[HostDTO]) -> None:
        """Cria um arquivo {id_connect}.toml para cada peer."""

        os.makedirs(self.peers_dir, exist_ok=True)

        for peer in peers:
            file_path = os.path.join(
                self.peers_dir,
                f"{peer.id_connect}.toml",
            )

            alias = peer.alias

            data = {
                "options": {
                    "alias": alias,
                },
                "info": {
                    "username": alias,
                    "hostname": alias,
                    "platform": "Windows",
                },
            }

            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    toml.dump(data, file)
            except Exception as exc:
                logger.error("Erro ao gravar o peer '%s': %s", alias, exc)
                
                

peer_manager = PeerManager(PATH_CONF)

# peers = peer_manager.read_peers()

# for peer in peers:
#     print(peer)


# peers = [
#     {
#         "alias": "Servidor A",
#         "id_connect": 123456789,
#         "provider": "RUST",
#     },
#     {
#         "alias": "Servidor B",
#         "id_connect": 987654321,
#         "provider": "RUST",
#     },
# ]

# peer_manager.write(peers)
