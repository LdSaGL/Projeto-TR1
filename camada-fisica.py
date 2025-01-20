import matplotlib.pyplot as plt
import numpy as np

def nrz_polar_modulation(binary_sequence):
    """
    Função para modulação NRZ-Polar.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Sinal modulado e eixo do tempo.
    """   
    # Geração do sinal NRZ-Polar
    signal = []
    for bit in binary_sequence:
        if bit == 1:
            signal.extend([1])   # +V para 1
        else:
            signal.extend([-1])  # -V para 0

    # Geração do eixo do tempo
    time = np.linspace(0, len(signal), len(signal), endpoint=False)
    
    return signal, time

def manchester_modulation(binary_sequence):
    """
    Função para modulação Manchester.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Sinal modulado e eixo do tempo.
    """
    # Clock Manchester
    clock = 0, 1
    
    # Geração do sinal Manchester
    signal = []
    for bit in binary_sequence:  
        signal.extend([bit ^ clock[0], bit ^ clock[1]]) # bit XOR com o clock
        
     # Gerar o eixo de tempo correspondente ao sinal
    time = np.linspace(0, len(signal), len(signal), endpoint=False)  # Cada bit gera 2 valores

    return signal, time	

def bipolar_modulation(binary_sequence):
    """
    Função para modulação bipolar.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Sinal modulado e eixo do tempo.
    """
    # Geração do sinal bipolar
    signal = []
    last_bit_one = -1 # Variável de alternância de polaridade
    for bit in binary_sequence:
        if bit == 1:
            if last_bit_one == 1:
                signal.extend([-1]) # -V para 1
                last_bit_one = -1
            else:
                signal.extend([1])   # +V para 1
                last_bit_one = 1
        else:
            signal.extend([0])  # 0 para 0

    # Geração do eixo do tempo
    time = np.linspace(0, len(signal), len(signal), endpoint=False)
    
    return signal, time

def ask_modulation(A, F, bit_stream, digi_mod):
    """
    Realiza modulação ASK (Amplitude Shift Keying) em um stream de bits.
    :param A: Amplitude da onda portadora.
    :param F: Frequência da onda portadora.
    :param bit_stream: Lista ou array representando o stream de bits.
    :param digi_mod: Tipo de modulação digital.
    :return: Array representando o sinal modulado ASK.
    """
    sig_size = len(bit_stream)
    signal = np.zeros(sig_size * 100)  # Inicializa o array para o sinal modulado
    
    for i in range(sig_size):
        if digi_mod == 3: # Se for bipolar
            if bit_stream[i] in (1, -1): # Inclui a tensão -1 V como bit 1 
                for j in range(100):
                    signal[(i * 100) + j] = A * np.sin(2 * np.pi * F * j / 100)
            else:
                for j in range(100):
                    signal[(i * 100) + j] = 0
        else:
            if bit_stream[i] == 1:
                for j in range(100):
                    signal[(i * 100) + j] = A * np.sin(2 * np.pi * F * j / 100)
            else:
                for j in range(100):
                    signal[(i * 100) + j] = 0

    return signal

def fsk_modulation(A, F1, F2, bit_stream, digi_mod):
    """
    Realiza modulação FSK (Frequency Shift Keying) em um stream de bits.
    :param A: Amplitude da onda portadora.
    :param F1: Frequência da onda portadora para o valor de tensão do bit 1.
    :param F2: Frequência da onda portadora para o valor de tensão do bit 0.
    :param bit_stream: Lista ou array representando o stream de bits.
    :param digi_mod: Tipo de modulação digital.
    :return: Array representando o sinal modulado FSK.
    """
    sig_size = len(bit_stream)
    signal = np.zeros(sig_size * 100)  # Inicializa o array para o sinal modulado
    
    for i in range(sig_size):
        if digi_mod == 3: # Se for bipolar
            if bit_stream[i] in (1, -1): # Inclui a tensão -1 V como bit 1 
                for j in range(100):
                    signal[(i * 100) + j] = A * np.sin(2 * np.pi * F1 * j / 100)
            else:
                for j in range(100):
                    signal[(i * 100) + j] = A * np.sin(2 * np.pi * F2 * j / 100)
        else:
            if bit_stream[i] == 1:
                for j in range(100):
                    signal[(i * 100) + j] = A * np.sin(2 * np.pi * F1 * j / 100)
            else:
                for j in range(100):
                    signal[(i * 100) + j] = A * np.sin(2 * np.pi * F2 * j / 100)

    return signal
    
def main():
    # Entrada de dados do usuário
    user_input = input("Digite a sequência binária: ")
    
    # Seleção da modulação digital
    print("Tipos de modulação digital disponíveis:")
    print("1 - NRZ-Polar")
    print("2 - Manchester")
    print("3 - Bipolar")
    digital_modulation_selected = input("Digite o número da modulação digital desejada: ")
    digital_modulation_name = ""
    
    # Validação da entrada
    if not set(user_input).issubset({'0', '1'}):
        print("Entrada inválida! Certifique-se de digitar apenas 0s e 1s.")
        return
    
    # Converter a sequência de entrada para uma lista de inteiros
    binary_sequence = [int(bit) for bit in user_input]
    
    # Modulação digital selecionada
    if digital_modulation_selected == "1":
        signal, time = nrz_polar_modulation(binary_sequence)
        digital_modulation_name = "NRZ-Polar"
    elif digital_modulation_selected == "2":
        signal, time = manchester_modulation(binary_sequence)
        digital_modulation_name = "Manchester"
    elif digital_modulation_selected == "3":
        signal, time = bipolar_modulation(binary_sequence)
        digital_modulation_name = "Bipolar"
    else:
        print("Modulação inválida!")
        return
    
    # Seleção da modulação analógica
    print("Tipos de modulação analógica disponíveis:")
    print("1 - ASK")
    print("2 - FSK")
    print("3 - 8QAM")
    analogical_modulation_selected = input("Digite o número da modulação analógica desejada: ")
    analogical_modulation_name = ""
    
    # Modulação analógica selecionada
    if analogical_modulation_selected == "1":
        signal2 = ask_modulation(1, 1, signal, int(digital_modulation_selected))
        analogical_modulation_name = "ASK"
    elif analogical_modulation_selected == "2":
        signal2 = fsk_modulation(1, 1, 3, signal, int(digital_modulation_selected))
        analogical_modulation_name = "FSK"
    else:
        print("Modulação inválida!")
        return
    
    # Exibir no terminal
    print("Sinal modulado:", signal)
    print("Eixo do tempo:", time)
    
    # Correção do eixo x para plotagem
    time_extended = np.append(time, time[-1] + (time[1] - time[0]))
    signal_extended = np.append(signal, signal[-1])
    
    # Plotar o sinal digital modulado
    plt.figure(figsize=(10, 4))
    plt.plot(time_extended, signal_extended, drawstyle='steps-post', label="Sinal")
    plt.title(f"Modulação {digital_modulation_name}")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    #plt.savefig(f"sinal_{modulation_name}.png")
    plt.show()
    
    print(signal2)
    # Plotar o sinal analogico modulado
    plt.figure(figsize=(12, 4))
    plt.plot(signal2)
    plt.title(f"Sinal {analogical_modulation_name} Modulado")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()
    
    
if __name__ == "__main__":
    main()
