import customtkinter as ctk


class Card(ctk.CTkFrame):
    def __init__(self, master, alias, user_id):
        super().__init__(master, corner_radius=15, fg_color="#242424")

        self.user_id = user_id

        ctk.CTkLabel(
            self,
            text=alias,
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.id_label = ctk.CTkLabel(
            self,
            text=user_id,
            font=("Arial", 16),
            anchor="w",          # Alinha o texto à esquerda
            corner_radius=6,
            fg_color="transparent",
            padx=10,
            pady=6,
            cursor="hand2"
        )

        self.id_label.pack(
            fill="x",            # Ocupa toda a largura
            padx=15,
            pady=(0, 15)
        )

        self.id_label.bind("<Enter>", self.on_enter)
        self.id_label.bind("<Leave>", self.on_leave)
        self.id_label.bind("<Double-Button-1>", self.copy_id)

    def on_enter(self, event):
        self.id_label.configure(fg_color=("gray85", "gray30"))

    def on_leave(self, event):
        self.id_label.configure(fg_color="transparent")

    def copy_id(self, event):
        self.clipboard_clear()
        self.clipboard_append(self.user_id)

        texto = self.id_label.cget("text")
        self.id_label.configure(text="✅ Copiado!")

        self.after(300, lambda: self.id_label.configure(text=texto))
