import numpy as np
import matplotlib.pyplot as plt
import random

def demodulate_ask(signal, A, F, digi_mod):
    """
    Demodula um sinal ASK e reconstitui o bit stream original.
    
    :param signal: Array representando o sinal modulado ASK.
    :param A: Amplitude da onda portadora.
    :param F: Frequência da onda portadora.
    :param digi_mod: Tipo de modulação digital (3 para bipolar, caso contrário unipolar).
    :param samples_per_bit: Número de amostras por bit no sinal modulado.
    :return: Lista representando o stream de bits demodulado.
    """
    num_bits = len(signal) // 100
    bit_stream = []

    last_bit_one = -1
    for i in range(num_bits):
        # Extrair o segmento do sinal correspondente ao bit atual
        segment = signal[i * 100:(i + 1) * 100]
        
        # Calcula a energia média do segmento
        avg_amplitude = np.mean(np.abs(segment))

        if digi_mod == "NRZ-Polar":
            if avg_amplitude > A / 2:  # Limite para considerar presença de onda
                bit_stream.append(1)
            elif avg_amplitude < A / 4:  # Limite para ausência de onda
                bit_stream.append(-1)
        elif digi_mod == "Manchester":
            if avg_amplitude > A / 2:  # Limite para considerar presença de onda
                bit_stream.append(1)
            elif avg_amplitude < A / 4:  # Limite para ausência de onda
                bit_stream.append(0)
        elif digi_mod == "Bipolar":
            if avg_amplitude > A / 2:
                if last_bit_one == 1:
                    bit_stream.append(-1)
                    last_bit_one = -1
                else:
                    bit_stream.append(1)
                    last_bit_one = 1
            elif avg_amplitude < A / 4:
                bit_stream.append(0)
    
    return bit_stream

def demodulate_fsk(signal, A, F1, F2, digi_mod):
    """
    Demodula um sinal FSK e reconstitui o bit stream original.
    
    :param signal: Array representando o sinal modulado FSK.
    :param A: Amplitude da onda portadora.
    :param F1: Frequência da onda portadora para o valor de tensão do bit 1.
    :param F2: Frequência da onda portadora para o valor de tensão do bit 0.
    :param samples_per_bit: Número de amostras por bit no sinal modulado.
    :return: Lista representando o stream de bits demodulado.
    """
    num_bits = len(signal) // 100
    bit_stream = []

    # Gera as portadoras para demodulação
    t = np.arange(0, 100) / 100
    carrier_f1 = A * np.sin(2 * np.pi * F1 * t)
    carrier_f2 = A * np.sin(2 * np.pi * F2 * t)

    last_bit_one = -1
    for i in range(num_bits):
        # Extrair o segmento do sinal correspondente ao bit atual
        segment = signal[i * 100:(i + 1) * 100]

        # Calcula a energia média para cada frequência portadora
        energy_f1 = np.sum(segment * carrier_f1)
        energy_f2 = np.sum(segment * carrier_f2)
            
        if digi_mod == "NRZ-Polar":
            if energy_f1 > energy_f2:  # Limite para considerar presença de onda
                bit_stream.append(1)
            else:  # Limite para ausência de onda
                bit_stream.append(-1)
        elif digi_mod == "Manchester":
            if energy_f1 > energy_f2:  # Limite para considerar presença de onda
                bit_stream.append(1)
            else:  # Limite para ausência de onda
                bit_stream.append(0)
        elif digi_mod == "Bipolar":
            if energy_f1 > energy_f2:
                if last_bit_one == 1:
                    bit_stream.append(-1)
                    last_bit_one = -1
                else:
                    bit_stream.append(1)
                    last_bit_one = 1
            else:
                bit_stream.append(0)

    return bit_stream

def demodulate_nrz_polar(binary_sequence):
    """
    Demodula um sinal NRZ polar e reconstitui o bit stream original.
    
    :param binary_sequence: Lista ou array representando o stream de bits.
    :return: Lista representando o stream de bits demodulado.
    """
    demodutaled_bits = []
    for bit in binary_sequence:
        if bit == 1:
            demodutaled_bits.extend([1])
        else:
            demodutaled_bits.extend([0])
    
    return demodutaled_bits

def demodulate_manchester(binary_sequence):
    """
    Função para demodulação Manchester.
    :param signal: Sinal modulado em Manchester.
    :return: Lista de bits demodulados e eixo do tempo correspondente.
    """
    demodulated_bits = []
    
    # Percorrer o sinal em pares de valores (cada bit é representado por dois valores)
    for i in range(0, len(binary_sequence), 2):
        # Detectar a transição no meio do bit
        if binary_sequence[i] == 0 and binary_sequence[i + 1] == 1:
            demodulated_bits.append(0)  # Transição de 0 para 1
        elif binary_sequence[i] == 1 and binary_sequence[i + 1] == 0:
            demodulated_bits.append(1)  # Transição de 1 para 0

    return demodulated_bits

def demodulate_bipolar(binary_sequence):
    """
    Função para demodulação bipolar.
    :param signal: Sinal modulado em bipolar.
    :return: Lista de bits demodulados e eixo do tempo correspondente.
    """
    demodulated_bits = []
    
    # Percorrer o sinal
    for bit in binary_sequence:
        if bit == 1 or bit == -1:
            demodulated_bits.append(1)
        else:
            demodulated_bits.append(0)

    return demodulated_bits

def add_error(binary_sequence):
    # Define a probabilidade de erro
    error_probability = 0.01 

    # Itera sobre a sequência binária e aplica a chance de inverter cada bit
    for i in range(len(binary_sequence)):
        if random.random() <= error_probability:
            # Inverte o bit
            binary_sequence[i] = 1 - binary_sequence[i]
    return binary_sequence

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

def main(digital_modulation_selected, analogical_modulation_selected, binary_input):
    """
    Função principal para decodificação da camada física.
    :param digital_modulation_selected: Modulação digital selecionada.
    :param analogical_modulation_selected: Modulação analógica selecionada.
    :param binary_input: Sequência binária de entrada.
    """
    binary_input = add_error(binary_input)
    
    # Demodulação analógica
    if analogical_modulation_selected == "ASK":
        signal = demodulate_ask(binary_input, 1, 1, digital_modulation_selected)
        signal_to_plot = ask_modulation(1, 1, signal, digital_modulation_selected)
    elif analogical_modulation_selected == "FSK":
        signal = demodulate_fsk(binary_input, 1, 1, 3, digital_modulation_selected)
        signal_to_plot = fsk_modulation(1, 1, 3, signal, digital_modulation_selected)
    elif analogical_modulation_selected == "8-QAM":
        pass
    
    # Plotar o sinal analógico demodulado
    plt.figure(figsize=(12, 4))
    plt.plot(signal_to_plot)
    plt.title(f"Sinal {analogical_modulation_selected} Demodulado")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.savefig(f"demodulacao_analogica.png")
    plt.close()  # Fecha a figura para liberar memória
    
    # Geração do eixo do tempo
    time = np.linspace(0, len(signal), len(signal), endpoint=False)
    
    # Correção do eixo x para plotagem
    time_extended = np.append(time, time[-1] + (time[1] - time[0]))
    signal_extended = np.append(signal, signal[-1])
    
    # Plotar o sinal digital demodulado
    plt.figure(figsize=(10, 4))
    plt.plot(time_extended, signal_extended, drawstyle='steps-post', label="Sinal")
    plt.title(f"Demodulação {digital_modulation_selected}")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"demodulacao_digital.png")
    plt.close()  # Fecha a figura para liberar memória
    
    # Modulação digital
    if digital_modulation_selected == "NRZ-Polar":
        bit_stream = demodulate_nrz_polar(signal)
    elif digital_modulation_selected == "Manchester":
        bit_stream = demodulate_manchester(signal)
    elif digital_modulation_selected == "Bipolar":
        bit_stream = demodulate_bipolar(signal)

    return bit_stream