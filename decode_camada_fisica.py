import numpy as np
import camada_fisica as cf

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