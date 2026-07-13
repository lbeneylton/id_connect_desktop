import customtkinter as ctk

from service.api import api
from store.pc_store import pc_store


class FindPc(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.timer_busca = None
        self.texto_busca = ctk.StringVar()
        self.ultima_busca = None

        self.texto_busca.trace_add(
            "write",
            self._verificar_busca
        )

        self._criar_topo()
        self._criar_entry()

    def _criar_topo(self):
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=15, pady=(15, 0))

        self.label_name = ctk.CTkLabel(
            topo,
            text="Nome PC",
            font=("Arial", 20, "bold")
        )
        self.label_name.pack(side="left")

        botoes = ctk.CTkFrame(topo, fg_color="transparent")
        botoes.pack(side="right")

        self.btn_exportar = ctk.CTkButton(
            botoes,
            text="↑",
            width=35,
            height=35,
            command=self.exportar
        )
        self.btn_exportar.pack(side="left", padx=(0, 5))

        self.btn_importar = ctk.CTkButton(
            botoes,
            text="↓",
            width=35,
            height=35,
            command=self.importar
        )
        self.btn_importar.pack(side="left")

    def _criar_label(self):
        self.label_name = ctk.CTkLabel(
            self,
            text="Nome PC",
            font=("Arial", 20, "bold")
        )

        self.label_name.pack(
            anchor="w",
            padx=15,
            pady=(15, 0)
        )

    def _criar_entry(self):
        self.name_pc = ctk.CTkEntry(
            self,
            placeholder_text="Digite o nome do PC",
            height=40,
            corner_radius=10,
            textvariable=self.texto_busca
        )

        self.name_pc.pack(
            fill="x",
            padx=30,
            pady=10
        )

    def _verificar_busca(self, *args):
        texto = self.texto_busca.get().strip()

        # cancela timer anterior
        if self.timer_busca:
            self.after_cancel(self.timer_busca)

        # se tiver 3 ou menos caracteres limpa a lista
        if len(texto) <= 3:
            self.ultima_busca = None
            pc_store.set_pcs([])
            return

        # espera 500ms antes de buscar
        self.timer_busca = self.after(
            500,
            lambda: self.buscar_pc(texto)
        )

    def buscar_pc(self, texto: str):
        if texto == self.ultima_busca:
            return

        self.ultima_busca = texto.strip().upper()

        api.buscar_computadores(
            texto.strip().upper(),
            self.receber_resultado
        )

    def receber_resultado(self, pcs):
        self.after(
            0,
            lambda: pc_store.set_pcs(pcs)
        )

    def exportar(self):
        print("Exportar")

    def importar(self):
        print("Importar")
