"""Interpreta e monta a linha de roster do arquivo de configuração do AnyDesk."""

import logging
from app.anydesk.Host import HostDTO

logger = logging.getLogger(__name__)


class AnydeskParser:
    """Classe responsável pelo parsing e formatação da linha de rosters do AnyDesk."""

    ROSTER_PREFIX = "ad.roster.items="

    def _split_key_value(self, line: str) -> tuple[str, str]:
        """Divide a linha do roster em chave e valor.

        Args:
            line (str): Linha de roster bruta.

        Returns:
            tuple[str, str]: Chave (prefixo) e valor (rosters).
        """
        parts = line.split("=", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return parts[0], ""

    def _is_valid_host(self, parts: list[str]) -> bool:
        """Valida se as partes extraídas do roster contêm os dados necessários.

        Formato esperado: [host0, host1, alias]

        Args:
            parts (list[str]): Partes divididas de um único item do roster.

        Returns:
            bool: True se o formato for válido, False caso contrário.
        """
        if len(parts) < 3:
            return False

        # Obrigatoriamente precisa do identificador (parts[0]) e do alias (parts[2])
        if not parts[0].strip() or not parts[2].strip():
            return False

        return True

    def _extract_rosters(self, line_rosters: str) -> list[str]:
        """Converte a string de valores em uma lista de itens de roster individuais.

        Args:
            line_rosters (str): A porção de valores da linha (ex: "id,id,alias;id,id,alias;").

        Returns:
            list[str]: Lista de rosters brutos individuais.
        """
        return [r.strip() for r in line_rosters.split(";") if r.strip()]

    def _parse_host(self, roster: str) -> HostDTO | None:
        """Converte uma string de roster bruto em um objeto HostDTO.

        Args:
            roster (str): String com formato 'id,id,alias'.

        Returns:
            HostDTO | None: Objeto HostDTO estruturado, ou None se inválido.
        """
        parts = [p.strip() for p in roster.split(",")]

        if not self._is_valid_host(parts):
            return None

        try:
            id_val = int(parts[0])
            return HostDTO(
                id_connect=id_val,
                alias=parts[2],
                provider="ANY"
            )
        except ValueError:
            logger.warning(f"ID inválido no roster: '{parts[0]}'")
            return None

    # -----------------------
    # METODOS PUBLICOS
    # ------------------------
    def is_roster_line(self, line: str) -> bool:
        """Verifica se a linha fornecida é a linha de configuração de rosters.

        Args:
            line (str): Linha de configuração a verificar.

        Returns:
            bool: True se começar com o prefixo correct, False caso contrário.
        """
        return line.startswith(self.ROSTER_PREFIX)

    def parse_roster_line(self, line: str) -> tuple[str, list[HostDTO]] | None:
        """Analisa a linha de rosters e extrai a chave e a lista de objetos HostDTO.

        Args:
            line (str): Linha de roster vinda do arquivo .conf.

        Returns:
            tuple[str, list[HostDTO]] | None: Chave e lista de hosts extraídos,
                ou None se a linha não for de roster.
        """
        if not self.is_roster_line(line):
            return None

        key, values = self._split_key_value(line)
        parsed_hosts = []

        for item in self._extract_rosters(values):
            host = self._parse_host(item)
            if host:
                parsed_hosts.append(host)

        return key, parsed_hosts

    def build_roster_line(self, hosts: list[HostDTO]) -> str:
        """Gera a linha formatada do roster para persistência a partir dos DTOs.

        Formato final gerado: ad.roster.items=id,id,alias,;id,id,alias,;

        Args:
            hosts (list[HostDTO]): Lista de hosts.

        Returns:
            str: Linha contendo a chave e os valores formatados.
        """
        rosters = "".join(
            f"{h.id_connect},{h.id_connect},{h.alias},;"
            for h in hosts
        )
        return f"{self.ROSTER_PREFIX}{rosters}"


parser = AnydeskParser()