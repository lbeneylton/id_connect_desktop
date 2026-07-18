import logging

from app.rustdesk.PeerManager import PeerManager, peer_manager

from app.rustdesk.Host import HostDTO

from app.service.api import  ApiAccess, api


logger = logging.getLogger(__name__)


class RustMock():
    def export_hosts(self):
        logger.debug("EXPORT RUST MOCK")
        return True
    
    def import_hosts(self):
        logger.debug("IMPORT RUST MOCK")
        return True


class RustdeskService:
    def __init__(
        self,
        peer_manager: PeerManager = peer_manager,
        api: ApiAccess =api
    ):
        self.pm = peer_manager
        self.api = api


    def _load_hosts(self):
        try:
            hosts = self.pm.read_peers()
            
            logger.info("Arquivo de hosts do RustDesk lido.")
            logger.debug("Itens lidos: %s", hosts)

            if not hosts:
                logger.warning("Nenhum host local encontrado para exportação.")
                return None

            return hosts

        except Exception:
            
            logger.exception("Erro ao obter hosts locais.")
            return None

    def _send_hosts(self, hosts: list[HostDTO]) -> bool:
        # Cria o payload apenas se alias valido
        payload = [
            host.to_dict()
            for host in hosts
            if host.alias_valido
        ]

        try:
            self.api.enviar_aliases_para_exportacao(payload)
            
            logger.info("Hosts RustDesk exportados com sucesso.")
            logger.debug("Payload enviado: %s", payload)
            return True

        except Exception:
            logger.exception("Erro ao exportar hosts para a API.")
            return False

    def export_hosts(self) -> bool:
        hosts = self._load_hosts()
        if not hosts:
            return False

        return self._send_hosts(hosts)




    def import_hosts(self) -> bool:
        """Busca os hosts da API e grava os peers localmente.

        Returns:
            bool: True se a importação foi concluída com sucesso, False caso contrário.
        """
        try:
            # 1. Busca hosts da API
            remote_items = self.api.importar_rust_aliases()

            logger.info("Host Rust Buscados")
            logger.debug(f"API: {remote_items}")

            # Transformando em objetos HostDTO
            remote_hosts = [
                HostDTO(
                    id_connect=int(item["id_connect"]),
                    alias=item["alias"],
                    provider="RUST"
                )
                for item in remote_items
            ]

            # 2. Lê os peers locais
            local_hosts = self.pm.read_peers()

            # 3. Mescla utilizando o id_connect como chave
            merged = {
                item.id_connect: item
                for item in local_hosts
            }

            for item in remote_hosts:
                merged[item.id_connect] = item

            # 4. Ordena pelo alias
            sorted_hosts = sorted(
                merged.values(),
                key=lambda x: x.alias.lower()
            )

            # 5. Grava os peers
            self.pm.write_peers(sorted_hosts)

            logger.info("Importação de hosts RUST finalizada com sucesso.")
            return True

        except Exception:
            logger.exception("Erro na importação de hosts RUST.")
            return False
        




rust_service = RustdeskService()
rust_mock = RustMock()
