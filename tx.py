import asyncio
import websockets
import numpy as np
import json

async def enviar_quadro(quadro):
    """
    Envia um quadro para o servidor WebSocket.

    :param quadro: O quadro a ser enviado (como array NumPy).
    """
    async with websockets.connect("ws://localhost:8765") as websocket:
        # Convertendo o array NumPy para uma lista e, em seguida, para JSON
        quadro_json = json.dumps(quadro.tolist())
        await websocket.send(quadro_json)  # Enviando o quadro como string JSON
        print(f"Quadro enviado: {quadro_json}")

def enviar_quadro_sync(quadro):
    """
    Função para enviar um quadro de forma síncrona.

    :param quadro: O quadro a ser enviado (como array NumPy).
    """
    asyncio.run(enviar_quadro(quadro))