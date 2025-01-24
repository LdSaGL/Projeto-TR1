from interface import ModulationApp
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import camada_fisica as cf
#import camada_enlace as ce

def ascii_to_binary(ascii_input):
    # Função que converte uma string ASCII para uma string binária
    binary_output = ""
    for char in ascii_input:
        binary_output += format(ord(char), "08b")
    return binary_output

def main():
    # Função de callback que será chamada ao dar submit na interface
    def handle_submit(digital_mod, analog_mod, framing, error_detection, ascii_input):
        
        bin_ascii = ascii_to_binary(ascii_input)
        
        #message = ce.main(framing, error_detection, bin_ascii)
        #message_to_transmit = cf.main(digital_mod, analog_mod, message)
        
        # Aqui você pode chamar outras funções de processamento com os parâmetros
        # process_modulations(digital_mod, analog_mod, framing, error_detection, ascii_input)
        return bin_ascii

    # Cria a instância da interface, passando a função de callback
    win = ModulationApp(handle_submit)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()