import requests
import threading
import time
import logging

# Configuração do Logger
logger = logging.getLogger(__name__)

API_URL = "https://ids-connect.onrender.com"


class ApiAccess:

    def __init__(self, api_url=API_URL):
        self.api_url = api_url
        self.busca_id = 0
        self.lock = threading.Lock()

    def _executar_thread(self, funcao, nome):
        threading.Thread(
            target=funcao,
            name=nome,
            daemon=False
        ).start()

    def _get_json(self, url, **kwargs):
        resposta = requests.get(
            url,
            timeout=10,
            **kwargs
        )

        resposta.raise_for_status()

        return resposta.json()

    def _post_json(self, url, **kwargs):
        resposta = requests.post(
            url,
            timeout=10,
            **kwargs
        )

        resposta.raise_for_status()

        return resposta.json()

    def buscar_computadores(self, texto: str, callback= lambda x: logger.info(x)):

        with self.lock:
            self.busca_id += 1
            id_atual = self.busca_id

        def tarefa():
            inicio = time.time()

            try:
                dados = self._get_json(
                    f"{self.api_url}/alias",
                    params={
                        "texto": texto
                    }
                )

                resultado = dados.get(
                    "aliases",
                    []
                )
                
                resultado = dados.get("aliases", [])

            except Exception:
                logger.exception(f"Erro busca")
                return


            logger.info(
                f"Tempo API {time.time() - inicio:.2f}s"
            )

            # Descarta respostas de buscas antigas
            with self.lock:
                if id_atual != self.busca_id:
                    logger.debug(
                        f"Busca ignorada: {texto}"
                    )
                    return

            if not resultado:
                logger.warning("Nenhum computador encontrado")

            logger.info(resultado)
            callback(resultado)

        self._executar_thread(
            tarefa,
            "busca-alias"
        )

    def importar_all(self, callback= lambda x: logger.info(x)):

        def tarefa():

            try:

                dados = self._get_json(
                    f"{self.api_url}/import"
                )

                aliases = dados.get("aliases", [])
                
                callback(aliases)


            except Exception as erro:
                logger.error(f"Erro import: {erro}")



        self._executar_thread(
            tarefa,
            "import-anydesk"
        )

    def obter_aliases_para_importacao(self) -> list[dict]:
        """Busca de forma síncrona os aliases da API para importação.

        Returns:
            list[dict]: Lista de dicionários representando os aliases recebidos.
        """
        dados = self._get_json(f"{self.api_url}/import")
        return dados.get("aliases", [])

    def exportar_all(self, aliases: list[dict], callback = lambda x: logger.info(x)):

        def tarefa():
            try:

                payload = {
                    "aliases": aliases
                }

                resposta = self._post_json(
                    f"{self.api_url}/export",
                    json=payload
                )

                callback(resposta)

            except Exception as erro:
                logger.error(f"Erro export: {erro}")


        self._executar_thread(
            tarefa,
            "export-anydesk"
        )

    def enviar_aliases_para_exportacao(self, aliases: list[dict]) -> dict:
        """Exporta de forma síncrona a lista de aliases para a API.

        Args:
            aliases (list[dict]): Lista de aliases em formato dicionário.

        Returns:
            dict: Resposta da API parseada em formato JSON.
        """
        payload = {"aliases": aliases}
        return self._post_json(f"{self.api_url}/export", json=payload)


api = ApiAccess()
