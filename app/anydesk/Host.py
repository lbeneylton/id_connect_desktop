from dataclasses import dataclass


@dataclass(frozen=True)
class HostDTO:
    """
    Data Transfer Object representando um host (alias do AnyDesk).

    Attributes:
        id_connect (int): Identificador de conexão do AnyDesk.
        alias (str): Nome amigável/apelido associado ao host.
        provider (str): Provedor de conexão (padrão 'ANY' para AnyDesk).
    """
    id_connect: int
    alias: str
    provider: str = "ANY"

    def to_dict(self) -> dict:
        """Converte o DTO para um dicionário compatível com a API."""
        return {
            "id_connect": self.id_connect,
            "alias": self.alias,
            "provider": self.provider,
        }

