from interface import ModulationApp
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import asyncio
import websockets
import numpy as np
import json
import camada_fisica as cf
import camada_enlace as ce
import Servidor.decode_camada_enlace as dce
import Servidor.decode_camada_fisica as dcf

async def enviar_quadro(quadro, digital_mod, analog_mod, framing, error_detection, error_correction):
    """
    Envia um quadro para o servidor WebSocket.

    :param quadro: O quadro a ser enviado (como array NumPy).
    """
    async with websockets.connect("ws://localhost:8765") as websocket:
        # Monta o JSON com o quadro e as configurações
        data = {
            "quadro": quadro.tolist(),  # Converte o array NumPy para lista
            "digital_mod": digital_mod,
            "analog_mod": analog_mod,
            "framing": framing,
            "error_detection": error_detection,
            "error_correction": error_correction
        }
        # Envia os dados para o servidor
        await websocket.send(json.dumps(data))
        
def main():
    # Função de callback que será chamada ao dar submit na interface
    def handle_submit(digital_mod, analog_mod, framing, error_detection, error_correction, ascii_input):
        
        message, bin_ascii = ce.main(framing, error_detection, error_correction, ascii_input)
        quadro = cf.main(digital_mod, analog_mod, message)
        
        # Realiza a demodulação
        demodulated_frame = dcf.main(digital_mod, analog_mod, quadro)

        # Realiza a decodificação de enlace
        final_message = dce.main(framing, error_detection, error_correction, demodulated_frame)

        # Monta a resposta
        print(final_message)
        
        #asyncio.run(enviar_quadro(quadro, digital_mod, analog_mod, framing, error_detection, error_correction))

        
        return ' '.join(bin_ascii[i:i+8] for i in range(0, len(bin_ascii), 8))

    # Cria a instância da interface, passando a função de callback
    win = ModulationApp(handle_submit)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()