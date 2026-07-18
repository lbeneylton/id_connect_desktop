import logging

from app.rustdesk.PeerManager import PeerManager, peer_manager

from app.rustdesk.Host import HostDTO

from app.service.api import  ApiAccess, api


logger = logging.getLogger(__name__)


class RustMock():
    def export_hosts(self):
        logger.debug("EXPORT MOCK")
        return True
    
    def import_hosts(self):
        logger.debug("IMPORT MOCK")
        return True


class RustdeskService:
    def __init__(
        self,
        peer_manager: PeerManager = peer_manager,
        api: ApiAccess =api
    ):
        self.pm = peer_manager
        self.api = api


    def export_hosts(self) -> bool:
        """
        Recupera os rosters do arquivo
        Organiza em ordem alfabetica
        Cria o json com historico
        """
        
        # Recupera uma lista de objetos HostDTO
        try:
            items = self.pm.read_peers()
            logger.debug(f"items: {items}")
            logger.debug("Arquivo de host do RustDesk lido")
            
        except Exception as e:
            logger.error(f"Erro ao obter hosts locais: {e}")

        if not items:
            logger.warning("Nenhum host local encontrado para exportação.")
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
            
            self.api.enviar_aliases_para_exportacao(formated)
            
            logger.info("Hosts RustDesk exportados com sucesso.")        
            logger.debug(formated)
            
            return True
        
        except Exception as e:
            logger.exception("Erro ao exportar hosts RUST")
            return False


    def import_hosts(self) -> bool:
        """Busca os hosts da API e grava os peers localmente.

        Returns:
            bool: True se a importação foi concluída com sucesso, False caso contrário.
        """
        try:
            # 1. Busca hosts da API
            remote_items = self.api.obter_aliases_para_importacao()

            remote_items = [
                item
                for item in remote_items
                if item.get("provider") == "RUST"
            ]

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
