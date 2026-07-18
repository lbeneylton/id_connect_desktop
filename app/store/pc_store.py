import logging

logger = logging.getLogger(__name__)

class PcStore:

    def __init__(self):
        self.pcs:list[dict] = []
        self.listeners = []

    def set_pcs(self, pcs):
        logger.debug("Listeners: %d", len(self.listeners))
        self.pcs = pcs

        for callback in self.listeners:
            callback()

    def get_pcs(self):
        logger.debug("set_pcs chamado")
        return self.pcs
    
    def del_pc(self, id_connect: int) -> bool:
        for i, pc in enumerate(self.pcs):
            if pc["id_connect"] == id_connect:
                del self.pcs[i]

                for callback in self.listeners:
                    callback()

                logger.info(f"PC {id_connect} apagado")
                return True

        logger.info(f"PC {id_connect} não encontrado")
        return False          

    def subscribe(self, callback):
        logger.debug("Subscribe: %s", callback)
        if callback not in self.listeners:
            self.listeners.append(callback)

    def unsubscribe(self, callback):
        logger.debug("Unbscribe: %s", callback)
        if callback in self.listeners:
            self.listeners.remove(callback)


pc_store = PcStore()
