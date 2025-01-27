import asyncio
import websockets
import numpy as np
import json
import decode_camada_fisica as dcf
import decode_camada_enlace as dce

async def handler(websocket):
    """
    Manipula conexões recebidas no servidor WebSocket.
    """
    try:
        # Recebe o JSON do cliente
        data_json = await websocket.recv()

        # Decodifica o JSON recebido
        data = json.loads(data_json)

        # Extrai os dados do JSON
        quadro_array = np.array(data.get("quadro", []))
        digital_modulation = data.get("digital_mod")
        analogical_modulation = data.get("analog_mod")
        framing = data.get("framing")
        error_detection = data.get("error_detection")
        error_correction = data.get("error_correction")

        # Realiza a demodulação
        demodulated_frame = dcf.main(digital_modulation, analogical_modulation, quadro_array)

        # Realiza a decodificação de enlace
        final_message = dce.main(framing, error_detection, error_correction, demodulated_frame)

        # Monta a resposta
        print(final_message)

    except Exception as e:
        # Envia o erro para o cliente
        error_response = {"error": str(e)}
        await websocket.send(json.dumps(error_response))
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
