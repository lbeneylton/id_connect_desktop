"""Serviço de sincronização de hosts para o AnyDesk."""

import logging
from app.anydesk.FileManager import FileManager, file_manager
from app.anydesk.RosterParser import AnydeskParser, parser
from app.anydesk.Host import HostDTO
from app.service.api import ApiAccess, api

logger = logging.getLogger(__name__)

class MockAnydesk():
    def export_hosts(self):
        logger.debug("EXPORT ANY MOCK")
        return True
    
    def import_hosts(self):
        logger.debug("IMPORT ANY MOCK")
        return True


class AnydeskService:
    """Orquestra a sincronização (importação/exportação) de hosts entre arquivo local e API.

    Todas as operações são síncronas para delegar a gestão de threads à interface
    gráfica (GUI), evitando o congelamento da tela principal.
    """

    def __init__(
        self,
        parser: AnydeskParser = parser,
        file_manager: FileManager = file_manager,
        api: ApiAccess = api
    ):
        """Inicializa o serviço com dependências injetáveis.

        Args:
            parser (AnydeskParser): Parser para formatação do arquivo.
            file_manager (FileManager): Gerenciador de E/S de arquivos.
            api (ApiAccess): Acesso à API REST do IDS Connect.
        """
        self.parser = parser
        self.fm = file_manager
        self.api = api

    def get_local_hosts(self) -> list[HostDTO]:
        """Lê o arquivo local de configuração e extrai a lista de hosts parseados.

        Returns:
            list[HostDTO]: Lista de hosts obtidos do arquivo local.
        """
        try:
            lines = self.fm.read_lines()
            for line in lines:
                if self.parser.is_roster_line(line):
                    result = self.parser.parse_roster_line(line)
                    if result:
                        _, items = result
                        logger.info("Arquivo de hosts do AnyDesk lido")
                        logger.debug(f"Items lidos: {items}")
                        return items
                    
        except Exception as e:
            logger.error(f"Erro ao obter hosts locais: {e}")
        
        logger.warning("Nenhum host local encontrado para exportação.")
        return []

    def export_hosts(self) -> bool:
        """Exporta os hosts locais cadastrados no arquivo .conf para o servidor.

        Returns:
            bool: True se a exportação foi bem-sucedida, False caso contrário.
        """
        hosts = self.get_local_hosts()
        if not hosts:
            logger.warning("Nenhum host local encontrado para exportação.")
            return False

        try:
            # Ordena alfabeticamente pelo alias
            sorted_hosts = sorted(
                hosts,
                key=lambda x: x.alias.upper()
            )

            formatted_payload = [host.to_dict() for host in sorted_hosts]

            # Chamada síncrona para a API
            self.api.enviar_aliases_para_exportacao(formatted_payload)
            logger.info("Hosts AnyDesk exportados com sucesso.")
            logger.debug(f"API: {formatted_payload}")
            return True

        except Exception:
            logger.exception(f"Erro ao exportar hosts ANY")
            return False

    def import_hosts(self) -> bool:
        """Busca os hosts da API e grava no arquivo local apenas os inexistentes.

        Realiza o backup do arquivo local antes da escrita.

        Returns:
            bool: True se a importação foi concluída com sucesso, False caso contrário.
        """
        try:
            # 1. Faz backup preventivo do arquivo atual
            self.fm.backup()

            # 2. Busca hosts remotos da API (chamada síncrona)
            remote_items = self.api.importar_any_aliases()
            
            logger.info("Host Any Buscados")
            logger.debug(f"API: {remote_items}")

            # Transformando em objetos HostDTO
            remote_hosts = [
                HostDTO(
                    id_connect=int(item["id_connect"]),
                    alias=item["alias"],
                    provider="ANY"
                )
                for item in remote_items
            ]

            # 3. Lê hosts locais existentes
            local_hosts = self.get_local_hosts()

            # 4. Mescla mantendo locais e adicionando apenas registros não existentes
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

            # 6. Serializa para o formato da linha do roster do AnyDesk
            roster_line = self.parser.build_roster_line(sorted_hosts)

            # 7. reconstrói as linhas do arquivo mantendo as demais linhas intactas
            old_lines = self.fm.read_lines()
            new_lines = [
                line for line in old_lines
                if not self.parser.is_roster_line(line)
            ]
            new_lines.append(f"{roster_line}\n")

            # 8. Escreve o arquivo final de forma atômica
            self.fm.write_atomic(new_lines)
            logger.info("Importação de novos hosts finalizada com sucesso.")
            return True

        except Exception:
            logger.exception(f"Erro na importação de hosts")
            return False


any_service = AnydeskService()
any_mock =MockAnydesk()