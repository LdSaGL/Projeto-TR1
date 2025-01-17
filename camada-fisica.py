import matplotlib.pyplot as plt
import numpy as np

def nrz_polar_modulation(binary_sequence):
    """
    Função para modulação NRZ-Polar.
    :param binary_sequence: Lista de bits (0 e 1) representando a sequência binária.
    :return: Sinal modulado e eixo do tempo.
    """
    # Definir parâmetros
    bit_duration = 1  # Duração de cada bit em segundos
    sampling_rate = 3  # Taxa de amostragem em Hz
    samples_per_bit = int(bit_duration * sampling_rate)

    # Geração do sinal NRZ-Polar
    signal = []
    for bit in binary_sequence:
        if bit == 1:
            signal.extend([1] * sampling_rate)   # +V para 1
        else:
            signal.extend([-1] * sampling_rate)  # -V para 0

    # Geração do eixo do tempo
    time = np.linspace(0, len(binary_sequence) * bit_duration, len(signal), endpoint=False)
    
    # Plotar o sinal modulado
    plt.figure(figsize=(10, 4))
    plt.plot(time, signal, drawstyle='steps-pre', label="Sinal NRZ-Polar")
    plt.title("Sinal Modulado NRZ-Polar")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.savefig("sinal_nrz_polar.png")
    
    return signal, time

def manchester_modulation(binary_sequence):
    """
    Função para modulação Manchester.
    :param binary_sequence: Lista de bits (0 e 1) representando a sequência binária.
    :return: Sinal modulado e eixo do tempo.
    """
    # Definir parâmetros
    bit_duration = 1  # Duração de cada bit em segundos
    sampling_rate = 3  # Taxa de amostragem em Hz
    samples_per_bit = int(bit_duration * sampling_rate)

    # Geração do sinal Manchester
    signal = []
    for bit in binary_sequence:
        if bit == 1:
            signal.extend([-1] * samples_per_bit // 2 + [1] * samples_per_bit // 2)  # Transição de -V para +V
        else:
            signal.extend([1] * samples_per_bit // 2 + [-1] * samples_per_bit // 2)  # Transição de +V para -V

    # Geração do eixo do tempo
    time = np.linspace(0, len(binary_sequence) * bit_duration, len(signal), endpoint=False)
    
    # Plotar o sinal modulado
    plt.figure(figsize=(10, 4))
    plt.plot(time, signal, drawstyle='steps-pre', label="Sinal Manchester")
    plt.title("Sinal Modulado Manchester")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.savefig("sinal_manchester.png")
    
    return signal, time	

def main():
    # Entrada de dados do usuário
    user_input = input("Digite a sequência binária: ")
    print("Tipos de modulação disponíveis:")
    print("1 - NRZ-Polar")
    print("2 - Manchester")
    print("3 - Bipolar")
    modulation_selected = input("Digite o número da modulação desejada: ")
    
    # Validação da entrada
    if not set(user_input).issubset({'0', '1'}):
        print("Entrada inválida! Certifique-se de digitar apenas 0s e 1s.")
        return
    
    # Converter a sequência de entrada para uma lista de inteiros
    binary_sequence = [int(bit) for bit in user_input]
    
    # Modulação selecionada
    if modulation_selected == "1":
        signal, time = nrz_polar_modulation(binary_sequence)
    elif modulation_selected == "2":
        signal, time = manchester_modulation(binary_sequence)
    else:
        print("Modulação não reconhecida!")
        return
    
    print("Sinal modulado:", signal)
    print("Eixo do tempo:", time)

if __name__ == "__main__":
    main()
