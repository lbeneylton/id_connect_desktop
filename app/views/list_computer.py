import customtkinter as ctk

from app.store.pc_store import pc_store
from app.widgets.card import Card


class Computadores(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label_sem_pcs = None

        pc_store.subscribe(
            self.atualizar
        )

        self._adicionar_header()
        self._criar_scroll()
        self._carregar_computadores()

    def _adicionar_header(self):
        self.label_pcs = ctk.CTkLabel(
            self,
            text="Computadores",
            font=("Arial", 25, "bold")
        )

        self.label_pcs.pack(
            fill="x",
            pady=(10, 0)
        )

    def _criar_scroll(self):
        self.scroll = ctk.CTkScrollableFrame(
            self,
            corner_radius=15,
            fg_color="transparent"
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            pady=(0, 10)
        )

    def _carregar_computadores(self):
        self.atualizar()

    def _adicionar_card(self, computador):
        card = Card(
            self.scroll,
            alias=computador["alias"],
            user_id=computador["id_connect"],
            provider=computador["provider"]
        )

        card.pack(
            fill="x",
            padx=5,
            pady=5
        )

    def atualizar(self):
        print("Atualizando lista")
        pcs = pc_store.get_pcs()

        # remove cards antigos, mas preserva o label de vazio
        for widget in self.scroll.winfo_children():
            if widget != self.label_sem_pcs:
                widget.destroy()

        if not pcs:
            self._mostrar_sem_pcs()
            return

        self._ocultar_sem_pcs()

        # criar novamente
        for pc in pcs:
            self._adicionar_card(pc)

    def _mostrar_sem_pcs(self):
        if self.label_sem_pcs is None or not self.label_sem_pcs.winfo_exists():
            self.label_sem_pcs = ctk.CTkLabel(
                self.scroll,
                text="Nenhum PC encontrado",
                font=("Arial", 18, "bold")
            )

        self.label_sem_pcs.pack(
            pady=20
        )

    def _ocultar_sem_pcs(self):
        if self.label_sem_pcs:
            self.label_sem_pcs.pack_forget()
