import asyncio
import websockets
import numpy as np
import json
import matplotlib.pyplot as plt

async def handler(websocket):
    """
    Manipula conexões recebidas no servidor WebSocket.
    """
    try:
        # Recebe a string JSON do cliente
        quadro_json = await websocket.recv()
        print(f"Quadro recebido (JSON): {quadro_json}")

        # Converte de JSON para lista e depois para array NumPy
        quadro_array = np.array(json.loads(quadro_json))
        print(f"Quadro convertido para array NumPy:\n{quadro_array}")

        # Exibe o gráfico do sinal
        plt.figure(figsize=(12, 4))
        plt.plot(quadro_array)
        plt.title("Sinal Modulado")
        plt.xlabel("Amostras")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()

        # Opcional: Enviar uma resposta ao cliente
        await websocket.send("Quadro recebido e processado com sucesso!")
    except Exception as e:
        print(f"Erro ao processar o quadro: {e}")

async def main():
    """
    Inicia o servidor WebSocket.
    """
    async with websockets.serve(handler, "localhost", 8765):
        print("Servidor WebSocket rodando em ws://localhost:8765")
        await asyncio.Future()  # Mantém o servidor rodando

# Executa o servidor
asyncio.run(main())
