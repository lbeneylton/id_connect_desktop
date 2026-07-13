import requests
import threading
import time


API_URL = "https://ids-connect.onrender.com"


class Api:
    def __init__(self, api_url=API_URL):
        self.api_url = api_url

    def buscar_computadores(self, texto: str, callback):
        def tarefa():
            inicio = time.time()

            try:
                resposta = requests.get(
                    f"{self.api_url}/alias",
                    params={"texto": texto}
                )

                print("Tempo API:", time.time() - inicio)

                resultado = resposta.json().get("aliases", [])

            except Exception as erro:
                print(erro)
                resultado = []

            callback(resultado)

        threading.Thread(target=tarefa, daemon=True).start()

    def importar_all(self):
        def tarefa():
            inicio = time.time()

            try:
                resposta = requests.get("/anydesk/import")

                print("Tempo API:", time.time() - inicio)
            except Exception as erro:
                print(str(erro))

        threading.Thread(target=tarefa, daemon=True).start()

    def exportar_all(self, pcs: list):
        def tarefa():
            inicio = time.time()

            try:
                resposta = requests.post(
                    "/anydesk/export",
                    params={"hosts": pcs}
                )

                print("Tempo API:", time.time() - inicio)

                return True

            except Exception as erro:
                print(str(erro))

        threading.Thread(target=tarefa, daemon=True).start()


api = Api()
