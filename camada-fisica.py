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

def main():
    # Entrada de dados do usuário
    user_input = input("Digite a sequência binária: ")
    print("Tipos de modulação disponíveis:")
    print("1 - NRZ-Polar")
    print("2 - Manchester")
    print("3 - Bipolar")
    modulation_selected = input("Digite o número da modulação desejada: ")
    modulation_name = ""
    
    # Validação da entrada
    if not set(user_input).issubset({'0', '1'}):
        print("Entrada inválida! Certifique-se de digitar apenas 0s e 1s.")
        return
    
    # Converter a sequência de entrada para uma lista de inteiros
    binary_sequence = [int(bit) for bit in user_input]
    
    # Modulação selecionada
    if modulation_selected == "1":
        signal, time = nrz_polar_modulation(binary_sequence)
        modulation_name = "NRZ-Polar"
    elif modulation_selected == "2":
        signal, time = manchester_modulation(binary_sequence)
        modulation_name = "Manchester"
    elif modulation_selected == "3":
        signal, time = bipolar_modulation(binary_sequence)
        modulation_name = "Bipolar"
    else:
        print("Modulação inválida!")
        return
    
    # Exibir no terminal
    print("Sinal modulado:", signal)
    print("Eixo do tempo:", time)
    
    # Correção do eixo x para plotagem
    time_extended = np.append(time, time[-1] + (time[1] - time[0]))
    signal_extended = np.append(signal, signal[-1])
    
    # Plotar o sinal modulado
    plt.figure(figsize=(10, 4))
    plt.plot(time_extended, signal_extended, drawstyle='steps-post', label="Sinal")
    plt.title(f"Modulação {modulation_name}")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"sinal_{modulation_name}.png")

if __name__ == "__main__":
    main()
