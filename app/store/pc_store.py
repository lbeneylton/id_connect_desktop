class PcStore:

    def __init__(self):
        self.pcs = []
        self.listeners = []

    def set_pcs(self, pcs):
        self.pcs = pcs

        for callback in self.listeners:
            callback()

    def get_pcs(self):
        return self.pcs

    def subscribe(self, callback):
        if callback not in self.listeners:
            self.listeners.append(callback)

    def unsubscribe(self, callback):
        if callback in self.listeners:
            self.listeners.remove(callback)


pc_store = PcStore()
