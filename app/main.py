import customtkinter as ctk
from app.views.list_computer import Computadores
from app.widgets.finder import FindPc

# Configurações do tema
ctk.set_appearance_mode("dark")  # dark, light ou system
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Host - IDs")
app.geometry("400x600")
app.resizable(width=False, height=True)


buscador = FindPc(app)
buscador.pack(
    fill="both",
    pady=(10, 20)
)

lista = Computadores(app)
lista.pack(
    fill="both",
    expand=True
)

app.mainloop()
