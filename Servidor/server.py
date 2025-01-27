import asyncio
import websockets
import gi
import json
import decode_camada_enlace as dce
import decode_camada_fisica as dcf
import numpy as np

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib
import os

class ReceiverInterface(Gtk.Window):
    def __init__(self):
        super().__init__(title="Receptor - Resultados")
        self.set_default_size(800, 600)
        self.set_border_width(10)

        # Layout principal
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(layout)

        # Imagem da demodulação analógica
        self.analog_img = Gtk.Image()
        analog_label = Gtk.Label(label="Demodulação Analógica")
        layout.pack_start(analog_label, False, False, 0)
        layout.pack_start(self.analog_img, True, True, 0)

        # Imagem da demodulação digital
        self.digital_img = Gtk.Image()
        digital_label = Gtk.Label(label="Demodulação Digital")
        layout.pack_start(digital_label, False, False, 0)
        layout.pack_start(self.digital_img, True, True, 0)

        # Resultados em binário
        self.binary_label = Gtk.Label(label="Resultado em Binário: ")
        layout.pack_start(self.binary_label, False, False, 0)

        # Resultado em ASCII
        self.ascii_label = Gtk.Label(label="Resultado em ASCII: ")
        layout.pack_start(self.ascii_label, False, False, 0)

        # Inicializar com imagens padrão
        self.load_default_images()

    def load_default_images(self):
        """
        Carrega imagens padrão (caso os arquivos ainda não existam).
        """
        placeholder_image = "placeholder.png"
        self.set_image(self.analog_img, placeholder_image)
        self.set_image(self.digital_img, placeholder_image)

    def set_image(self, image_widget, file_path):
        """
        Define uma imagem no widget fornecido.
        """
        if os.path.exists(file_path):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(file_path, 600, 300, True)
            image_widget.set_from_pixbuf(pixbuf)
        else:
            image_widget.set_from_stock(Gtk.STOCK_MISSING_IMAGE, Gtk.IconSize.DIALOG)

    def show_results(self, binary_result, ascii_result):
        """
        Mostra os resultados fornecidos pelo servidor.
        """
        analog_path = "demodulacao_analogica.png"
        digital_path = "demodulacao_digital.png"
        self.set_image(self.analog_img, analog_path)
        self.set_image(self.digital_img, digital_path)
        self.binary_label.set_text(f"Resultado em Binário: {binary_result}")
        self.ascii_label.set_text(f"Resultado em ASCII: {ascii_result}")


async def websocket_server(interface):
    """
    Servidor WebSocket que se comunica com a interface.
    """
    async def handler(websocket):
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
            final_message, final_message_bin = dce.main(framing, error_detection, error_correction, demodulated_frame)

            # Atualiza a interface pelo GLib
            GLib.idle_add(interface.show_results, final_message_bin, final_message)

        except Exception as e:
            print(f"Erro: {e}")

    # Inicializa o servidor
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()


def main():
    # Cria a interface
    interface = ReceiverInterface()
    interface.connect("destroy", Gtk.main_quit)
    interface.show_all()

    # Cria um loop para o servidor WebSocket
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, Gtk.main)
    loop.run_until_complete(websocket_server(interface))


if __name__ == "__main__":
    main()
