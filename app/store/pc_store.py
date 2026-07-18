import logging

logger = logging.getLogger(__name__)


class PcStore:

    def __init__(self):
        self.pcs = []
        self.listeners = []

    def set_pcs(self, pcs):
        logger.debug("Listeners: %d", len(self.listeners))
        self.pcs = pcs

        for callback in self.listeners:
            callback()

    def get_pcs(self):
        logger.debug("set_pcs chamado")
        return self.pcs

    def subscribe(self, callback):
        logger.debug("Subscribe: %s", callback)
        if callback not in self.listeners:
            self.listeners.append(callback)

    def unsubscribe(self, callback):
        logger.debug("Unbscribe: %s", callback)
        if callback in self.listeners:
            self.listeners.remove(callback)


pc_store = PcStore()
