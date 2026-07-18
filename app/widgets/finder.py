import time
import threading
import logging
import customtkinter as ctk

from app.anydesk.Service import any_mock as any_service
from app.rustdesk.Service import rust_mock as rust_service

from app.service.api import api
from app.store.pc_store import pc_store

logger = logging.getLogger(__name__)


class LoadingDialog(ctk.CTkToplevel):
    def __init__(self, master, texto):
        super().__init__(master)

        self.title("")
        self.geometry("300x120")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(
            self,
            text=texto,
            font=("Arial", 16)
        )
        self.label.pack(expand=True)

        self.update_idletasks()

        x = master.winfo_rootx() + (
            master.winfo_width() // 2
        ) - 150

        y = master.winfo_rooty() + (
            master.winfo_height() // 2
        ) - 60

        self.geometry(f"+{x}+{y}")

        self.grab_set()
class FindPc(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.timer_busca = None
        self.texto_busca = ctk.StringVar()
        self.ultima_busca = None
        
        self.loading = None
        self.loading_start = 0

        self.texto_busca.trace_add(
            "write",
            self._verificar_busca
        )

        self._criar_topo()
        self._criar_entry()

    # ---------------------
    # Auxiliares 
    # ---------------------
    def _criar_label(self, master):
        """Cria Label no top"""
        self.label_name = ctk.CTkLabel(
            master,
            text="Nome PC",
            font=("Arial", 20, "bold")
        )
        
        self.label_name.pack(side="left")
    
    def _criar_botoes(self, master):
        # Frame para os botoes
        botoes = ctk.CTkFrame(master, fg_color="transparent")
        botoes.pack(side="right")

        # Botão Exportar
        self.btn_exportar = ctk.CTkButton(
            botoes,
            text="↑",
            width=35,
            height=35,
            command=self.exportar
        )
        self.btn_exportar.pack(side="left", padx=(0, 5))

        # Botão Importar
        self.btn_importar = ctk.CTkButton(
            botoes,
            text="↓",
            width=35,
            height=35,
            command=self.importar
        )
        self.btn_importar.pack(side="left")
    
    def _criar_topo(self):
        """Cria linha com nome e botões"""
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=15, pady=(15, 0))

        self._criar_label(topo)
        self._criar_botoes(topo)

    def _criar_entry(self):
        """Cria a entrada para pesquisa"""
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

    # ---------------------
    # Busca dos computadores
    # ---------------------
    def _verificar_busca(self, *args):
        """Verifica se faz a busca"""
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

    # -----------------
    # Exportação
    # -----------------
    def _fim_exportacao(self, sucesso_any, sucesso_rust):
        tempo_minimo = 1.0  # segundos

        tempo_passado = time.time() - self.loading_start

        if tempo_passado < tempo_minimo:
            espera = int((tempo_minimo - tempo_passado) * 1000)

            self.after(
                espera,
                lambda: self._fim_exportacao(sucesso_any, sucesso_rust)
            )
            return        
        
        
        if self.loading:
            self.loading.grab_release()
            self.loading.destroy()
            self.loading = None

        self.btn_exportar.configure(state="normal")
        self.btn_importar.configure(state="normal")

        if sucesso_any:
            logger.info("Exportação ANY concluída com sucesso.")
        else:
            logger.error("Erro ao exportar ANY os computadores.")
            
        if sucesso_rust:
            logger.info("Exportação RUST concluída com sucesso.") 
        else:
            logger.error("Erro ao exportar RUST os computadores.")    

    def _exportar_thread(self):
        try:
            sucesso_any = any_service.export_hosts()
            sucesso_rust = rust_service.export_hosts()
            
        except Exception as e:
            logger.exception(f"Erro durante a exportação")
            sucesso_any = False
            sucesso_rust = False

        self.after(
            0,
            lambda: self._fim_exportacao(sucesso_any, sucesso_rust)
        )

    def exportar(self):
        self.btn_exportar.configure(state="disabled")
        self.btn_importar.configure(state="disabled")
        
        self.loading_start = time.time()
        
        self.loading = LoadingDialog(
            self, 
            "Exportando hosts..."
        )

        threading.Thread(
            target=self._exportar_thread,
            daemon=True
        ).start()
        
        
    # -----------------
    # Importação
    # -----------------        
    def _fim_importacao(self, sucesso_any, sucesso_rust):
        tempo_minimo = 1.0  # segundos

        tempo_passado = time.time() - self.loading_start

        if tempo_passado < tempo_minimo:
            espera = int((tempo_minimo - tempo_passado) * 1000)

            self.after(
                espera,
                lambda: self._fim_importacao(sucesso_any, sucesso_rust)
            )
            return
        
        if self.loading:
            self.loading.grab_release()
            self.loading.destroy()
            self.loading = None

        self.btn_exportar.configure(state="normal")
        self.btn_importar.configure(state="normal")

        if sucesso_any:
            logger.info("Importação ANY concluída com sucesso.")
        else:
            logger.error("Erro ao importar ANY os computadores.")

        if sucesso_rust:
            logger.info("Importação RUST concluída com sucesso.")
        else:
            logger.error("Erro ao importar RUST os computadores.")   
        
    def _importar_thread(self):
        try:
            sucesso_any = any_service.import_hosts()
            sucesso_rust = rust_service.import_hosts()

        except Exception as e:
            logger.exception(f"Erro durante a importação")
            sucesso_any = False
            sucesso_rust = False

        self.after(
            0,
            lambda: self._fim_importacao(sucesso_any, sucesso_rust)
        )

    def importar(self):
        self.btn_exportar.configure(state="disabled")
        self.btn_importar.configure(state="disabled")
        
        self.loading_start = time.time()
        
        self.loading = LoadingDialog(
            self, 
            "Importando hosts..."
        )

        threading.Thread(
            target=self._importar_thread,
            daemon=True
        ).start()
