import requests
import threading
import time


API_URL = "https://ids-connect.onrender.com/alias"


def buscar_computadores(texto, callback):
    def tarefa():
        inicio = time.time()

        try:
            resposta = requests.get(
                API_URL,
                params={"texto": texto},
                timeout=10
            )

            print("Tempo API:", time.time() - inicio)

            resultado = resposta.json().get("aliases", [])

        except Exception as erro:
            print(erro)
            resultado = []

        callback(resultado)

    threading.Thread(target=tarefa, daemon=True).start()
