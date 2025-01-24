import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ModulationApp(Gtk.Window):
    def __init__(self, submit_callback):
        Gtk.Window.__init__(self, title="Seleção de Modulação e Enquadramento")
        self.set_border_width(10)
        self.set_default_size(800, 400)

        # Callback que será chamado ao dar submit
        self.submit_callback = submit_callback

        # Criando a divisão da janela
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(paned) 

        # ** Parte da esquerda (Resultados) **
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        left_box.set_border_width(10)

        self.binary_output_label = Gtk.Label(label="Mensagem ASCII em binário:")
        self.binary_output_label.set_xalign(0)  # Alinhamento à esquerda
        self.binary_output_display = Gtk.TextView()
        self.binary_output_display.set_editable(False)
        self.binary_output_display.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)  # Quebra por caractere

        left_box.pack_start(self.binary_output_label, False, False, 0)
        left_box.pack_start(self.binary_output_display, True, True, 0)

        # Adiciona a parte esquerda ao painel
        paned.pack1(left_box, resize=True, shrink=False)

        # ** Parte da direita (Seletores) **
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        right_box.set_border_width(10)

        # Campo de entrada para caracteres ASCII
        self.label_ascii_input = Gtk.Label(label="Entrada ASCII:")
        self.ascii_input_entry = Gtk.Entry()

        # Labels e Comboboxes
        self.label_digital_mod = Gtk.Label(label="Modulação Digital:")
        self.digital_mod_combo = Gtk.ComboBoxText()
        self.digital_mod_combo.append_text("NRZ-Polar")
        self.digital_mod_combo.append_text("Manchester")
        self.digital_mod_combo.append_text("Bipolar")

        self.label_analog_mod = Gtk.Label(label="Modulação Analógica:")
        self.analog_mod_combo = Gtk.ComboBoxText()
        self.analog_mod_combo.append_text("ASK")
        self.analog_mod_combo.append_text("FSK")
        self.analog_mod_combo.append_text("8-QAM")

        self.label_framing = Gtk.Label(label="Enquadramento:")
        self.framing_combo = Gtk.ComboBoxText()
        self.framing_combo.append_text("Contagem de Caracteres")
        self.framing_combo.append_text("Inserção de Bytes")
        self.framing_combo.append_text("Inserção de Bits")

        self.label_error_detection = Gtk.Label(label="Detecção de Erros:")
        self.error_detection_combo = Gtk.ComboBoxText()
        self.error_detection_combo.append_text("Bit de Paridade")
        self.error_detection_combo.append_text("CRC")
        self.error_detection_combo.append_text("Hamming")

        # Botão para enviar seleção
        self.submit_button = Gtk.Button(label="Selecionar")
        self.submit_button.connect("clicked", self.on_submit)

        # Adicionando widgets à caixa direita
        right_box.pack_start(self.label_ascii_input, False, False, 0)
        right_box.pack_start(self.ascii_input_entry, False, False, 0)

        right_box.pack_start(self.label_digital_mod, False, False, 0)
        right_box.pack_start(self.digital_mod_combo, False, False, 0)
        right_box.pack_start(self.label_analog_mod, False, False, 0)
        right_box.pack_start(self.analog_mod_combo, False, False, 0)
        right_box.pack_start(self.label_framing, False, False, 0)
        right_box.pack_start(self.framing_combo, False, False, 0)
        right_box.pack_start(self.label_error_detection, False, False, 0)
        right_box.pack_start(self.error_detection_combo, False, False, 0)
        right_box.pack_start(self.submit_button, False, False, 0)

        # Adiciona a parte direita ao painel
        paned.pack2(right_box, resize=False, shrink=False)

    def on_submit(self, widget):
        digital_mod = self.digital_mod_combo.get_active_text()
        analog_mod = self.analog_mod_combo.get_active_text()
        framing = self.framing_combo.get_active_text()
        error_detection = self.error_detection_combo.get_active_text()
        ascii_input = self.ascii_input_entry.get_text()

        # Chama a função de callback com os parâmetros
        binary_output = self.submit_callback(digital_mod, analog_mod, framing, error_detection, ascii_input)

        # Exibe o binário gerado na interface
        buffer = self.binary_output_display.get_buffer()
        buffer.set_text(binary_output if binary_output else "Nenhum binário gerado.")
