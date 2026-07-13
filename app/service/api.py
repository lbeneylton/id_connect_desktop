import requests
import threading
import json
import time


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

    def buscar_computadores(self, texto: str, callback):

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

            except Exception as erro:

                print(
                    "Erro busca:",
                    erro
                )

                resultado = []

            print(
                f"Tempo API {time.time() - inicio:.2f}s"
            )

            # descarta resposta velha
            if id_atual != self.busca_id:
                print(
                    "Busca ignorada:",
                    texto
                )
                return

            callback(resultado)

        self._executar_thread(
            tarefa,
            "busca-alias"
        )

    def importar_all(self, callback):

        def tarefa():

            try:

                dados = self._get_json(
                    f"{self.api_url}/anydesk/import"
                )

                aliases = dados.get("aliases", [])

                callback(True, aliases)

            except Exception as erro:

                print("Erro import:", erro)

                callback(False, [])

        self._executar_thread(
            tarefa,
            "import-anydesk"
        )

    def exportar_all(self, aliases: list[dict], callback):

        def tarefa():

            try:

                self._post_json(
                    f"{self.api_url}/anydesk/export",
                    params={
                        "aliases": json.dumps(aliases)
                    }
                )

                callback(True)

            except Exception as erro:

                print("Erro export:", erro)

                callback(False)

        self._executar_thread(
            tarefa,
            "export-anydesk"
        )

# --------------------------
# Exemplo de uso
# --------------------------


api = ApiAccess()


# computadores = [
#     {
#         "alias": "STRING",
#         "id_connect": 1235,
#         "provider": "ANY"
#     },
#     {
#         "alias": "STRINGS",
#         "id_connect": 1235435,
#         "provider": "ANY"
#     },
#     {
#         "alias": "STRINGSGT",
#         "id_connect": 12354356,
#         "provider": "ANY"
#     }
# ]


# def retorno_export(resultado):
#     print(
#         "Resposta export:",
#         resultado
#     )


# api.exportar_all(
#     computadores,
#     retorno_export
# )


# def retorno_import(lista):

#     print(
#         "Computadores importados:"
#     )

#     for pc in lista:
#         print(pc)


# api.importar_all(
#     retorno_import
# )


# # apenas para teste em script puro
# # evita que o programa termine antes das threads
# time.sleep(5)
