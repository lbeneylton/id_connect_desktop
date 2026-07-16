"""Interpreta e monta a linha do arquivo"""
from Host import HostDTO


class AnydeskParser():
    """Classe para parser e formatação da linha"""
    ROSTER_PREFIX = "ad.roster.items="

    def _split_key_value(self, line: str) -> list[str]:
        """
        Quebra a linha de rosters e retorna

            key = ad.roster.items<br>
            value = host0, host1, alias; ...

            key, values"""
        return line.split("=", 1)

    def _is_valid_host(self, parts: list) -> bool:
        """Verifica o formato do roster

            host0, host1, alias"""

        # Tem que ter 3 partes
        if len(parts) < 3:
            return False

        # Obrigatoriamente precisa do host0 e do alias
        if not parts[0]:
            return False

        if not parts[2]:
            return False

        return True

    def _extract_rosters(self, line_rosters: str) -> list[str]:
        """Converte da linha de strings para lista de rosters

            list[roster1, roster2, ...]"""
        return [r.strip() for r in line_rosters.split(";") if r.strip()]

    def _parse_host(self, roster: str) -> HostDTO | None:
        """Retorna o objeto de roster
        """
        parts = []
        for p in roster.split(","):
            parts.append(p.strip())

        if not self._is_valid_host(parts):
            return None

        return HostDTO(
            id_connect=parts[0],
            alias=parts[2],
            provider="ANY"
        ) 
       

    # -----------------------
    # METODOS PUBLICOS
    # ------------------------
    def is_roster_line(self, line: str) -> bool:
        """Retorna se é a linha dos rosters"""
        return line.startswith(self.ROSTER_PREFIX)

    def parse_roster_line(self, line: str) -> tuple[str, list[HostDTO]] | None:
        """
            Verifica se é a linha de rosters<br>
            Corta a linha de rosters<br>
            Para cada roster extrai este<br>
            Analisa as partes do host (Verificando o formato )<br>
            Adiciona o dicionario (id, alias) numa lista<br>
            Retorna essa lista analisada"""

        # Verifica se é a linha Host do AnyDesk
        if not self.is_roster_line(line):
            return None

        # Quebra a linha em chave e valores
        key, values = self._split_key_value(line)

        parsed = [] # Lista de objetos Hosts
        for item in self._extract_rosters(values):
            roster = self._parse_host(item)

            if roster:
                parsed.append(roster)

        return key, parsed

    def build_roster_line(self, hosts: list[HostDTO]) -> str:
        """formato do roster: id,id,alias,;"""
        rosters = "".join(
            f"{h.id_connect},{h.id_connect},{h.alias},;"
            for h in hosts
        )
        return f"{self.ROSTER_PREFIX}{rosters}"

parser = AnydeskParser()