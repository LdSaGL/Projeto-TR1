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
        if digi_mod == "Bipolar": # Se for bipolar
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
        if digi_mod == "Bipolar": # Se for bipolar
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

def qam8_modulation(A, F, bit_stream, digi_mod):
    """
    Realiza modulação 8-QAM (Quadrature Amplitude Modulation com 8 estados) em um stream de bits.
    :param A: Amplitude base da onda portadora.
    :param F: Frequência da onda portadora.
    :param bit_stream: Lista ou array representando o stream de bits (deve ter múltiplos de 3).
    :return: Array representando o sinal modulado 8-QAM.
    """
    # Modificações para satisfazer a constelação 8-QAM
    bit_zero=0
    if digi_mod == "NRZ-Polar": # Se for bipolar
        bit_zero = -1
    elif digi_mod == "Bipolar":
        for i in range(len(bit_stream)):
            if bit_stream[i] == -1:
                bit_stream[i] = 1
    
    # Adiciona zeros ao bit_stream até que seu comprimento seja múltiplo de 3
    while len(bit_stream) % 3 != 0:
        bit_stream.append(bit_zero)

    sig_size = len(bit_stream) // 3  # Cada símbolo 8-QAM representa 3 bits
    signal = np.zeros(sig_size * 100)  # Inicializa o array para o sinal modulado
    t = np.linspace(0, 1, 100, endpoint=False)  # Intervalo de tempo para um símbolo
    
    # Constelação 8-QAM (amplitude e fase para cada combinação de bits)
    constellation = {
        (bit_zero, bit_zero, bit_zero): (A / 2, 0),
        (bit_zero, bit_zero, 1): (A / 2, np.pi / 4),
        (bit_zero, 1, bit_zero): (A / 2, np.pi / 2),
        (bit_zero, 1, 1): (A / 2, 3 * np.pi / 4),
        (1, bit_zero,bit_zero): (A, 0),
        (1, bit_zero, 1): (A, np.pi / 4),
        (1, 1, bit_zero): (A, np.pi / 2),
        (1, 1, 1): (A, 3 * np.pi / 4),
    }

    for i in range(sig_size):
        # Extrair os 3 bits que formam o símbolo
        bits = tuple(bit_stream[i * 3:(i + 1) * 3])
        if bits not in constellation:
            raise ValueError(f"Bits inválidos na constelação: {bits}")
        
        # Obter amplitude e fase do símbolo na constelação
        amp, phase = constellation[bits]
        
        # Gerar o sinal para o símbolo atual
        for j in range(100):
            signal[(i * 100) + j] = amp * np.sin(2 * np.pi * F * t[j] + phase)

    
    return signal
    
def main(digital_modulation_selected, analogical_modulation_selected, binary_output):
    """
    Executa a modulação digital e analógica selecionada, além de plotar os gráficos.
    :param digital_modulation_selected: Modulação digital selecionada.
    :param analogical_modulation_selected: Modulação analógica selecionada.
    :param binary_output: Sequência de bits a ser modulada.
    :return: Sinal modulado.
    """
    # Garantir que a sequência de bits é uma lista de inteiros
    binary_sequence = []
    for bit in binary_output:
        binary_sequence.append(int(bit))
    
    if digital_modulation_selected == "NRZ-Polar":
        signal,time = nrz_polar_modulation(binary_sequence) 
    elif digital_modulation_selected == "Manchester":
        signal, time = manchester_modulation(binary_sequence)
    elif digital_modulation_selected == "Bipolar":
        signal, time = bipolar_modulation(binary_sequence)
    
    # Correção do eixo x para plotagem
    time_extended = np.append(time, time[-1] + (time[1] - time[0]))
    signal_extended = np.append(signal, signal[-1])
    
    # Plotar o sinal digital modulado
    plt.figure(figsize=(10, 4))
    plt.plot(time_extended, signal_extended, drawstyle='steps-post', label="Sinal")
    plt.title(f"Modulação {digital_modulation_selected}")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"modulacao_digital.png")
    plt.close()  # Fecha a figura para liberar memória

       
    if analogical_modulation_selected == "ASK":
        signal2 = ask_modulation(1, 1, signal, digital_modulation_selected)
    elif analogical_modulation_selected == "FSK":
        signal2 = fsk_modulation(1, 1, 3, signal, digital_modulation_selected)
    elif analogical_modulation_selected == "8-QAM":
        signal2 = qam8_modulation(1, 1, signal, digital_modulation_selected)
    
    # Plotar o sinal analógico modulado
    plt.figure(figsize=(12, 4))
    plt.plot(signal2)
    plt.title(f"Sinal {analogical_modulation_selected} Modulado")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.savefig(f"modulacao_analogica.png")
    plt.close()  # Fecha a figura para liberar memória
    
    return signal2