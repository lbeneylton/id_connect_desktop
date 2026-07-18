import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from app.store.pc_store import pc_store
from app.service import api


class Card(ctk.CTkFrame):
    def __init__(self, master, alias: str, id_connect: str, provider: str):
        super().__init__(master, corner_radius=15, fg_color="#242424")

        self.id_connect = id_connect
        self.provider = provider
        self.alias = alias
        
        self.store = pc_store
        self.api = api

        # Linha superior
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            top,
            text=alias,
            font=("Arial", 18, "bold")
        ).pack(side="left")

        # Botão apagar
        ctk.CTkButton(
            top,
            text="🗑",
            width=32,
            height=32,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#B71C1C",
            text_color="#FF5555",
            command=self.confirm_delete
        ).pack(side="right")

        self.id_label = ctk.CTkLabel(
            self,
            text=f"{self.provider.capitalize()}: {self.id_connect}",
            font=("Arial", 16),
            anchor="w",
            corner_radius=6,
            fg_color="transparent",
            padx=10,
            pady=2,
            cursor="hand2"
        )

        self.id_label.pack(fill="x", padx=15, pady=(0, 15))

        self.id_label.bind("<Enter>", self.on_enter)
        self.id_label.bind("<Leave>", self.on_leave)
        self.id_label.bind("<Double-Button-1>", self.copy_id)

    def confirm_delete(self):
        msg = CTkMessagebox(
            master=self.winfo_toplevel(),
            width=300,
            height=50,
            title="Confirmar exclusão",
            message=f'Deseja apagar o card "{self.alias}"?',
            icon="warning",
            option_1="Cancelar",
            option_2="Apagar",
            topmost=True
        )

        if msg.get() == "Apagar":
            self._apagar_api(int(self.id_connect))
            self.store.del_pc(int(self.id_connect))
            self.destroy()

    def on_enter(self, event):
        self.id_label.configure(fg_color=("gray85", "gray30"))

    def on_leave(self, event):
        self.id_label.configure(fg_color="transparent")

    def copy_id(self, event):
        self.clipboard_clear()
        self.clipboard_append(self.id_connect)

        self.id_label.configure(text="✅ Copiado!")

        self.after(
            300,
            lambda: self.id_label.configure(
                text=f"{self.provider.capitalize()}: {self.id_connect}"
            )
        )
        
    def _apagar_api(self, id_connect: int):
        self.api.api.apagar_alias