from dataclasses import dataclass


@dataclass
class HostDTO:
    id_connect: int
    alias: str
    provider:str = "ANY"

