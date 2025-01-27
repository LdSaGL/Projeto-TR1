import binascii

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def char_count(binary_sequence):
    """
    Função para contagem de caracteres.
    Adiciona o tamanho da sequência em ASCII (convertido para bits) no início da sequência binária.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Lista de bits com o protocolo de enquadramento contagem de caracteres.
    """
    sequence_size = text_to_bits(str(len(binary_sequence))) # Converte o tamanho da sequência para ASCII representado em binário
    
    # Converte a string de contagem de caracteres para a forma de lista 
    sequence_size_ascii = []
    for bit in sequence_size:
        sequence_size_ascii.append(int(bit))
    return sequence_size_ascii + binary_sequence

def byte_insertion(binary_sequence):
    """
    Realiza a inserção de flags para delimitar quadros e trata flags e escapes acidentais nos dados.
    :param binary_sequence: Lista de bytes (dados do quadro).
    :return: Lista de bytes com as inserções de flag e escape realizadas.
    """
    # Declaração da Flag e do Escape padrão
    flag =   [0,1,1,1,1,1,1,0]
    escape = [0,1,1,1,1,0,1,1]
    
    for i in range(len(binary_sequence)):
        if binary_sequence[i:i+8] == flag or binary_sequence[i:i+8] == escape:
            binary_sequence = binary_sequence[:i] + escape + binary_sequence[i:] 
     
    return flag + binary_sequence + flag

def char_insertion(binary_sequence):
    """
    Realiza a inserção de flags para delimitar quadros e trata flags acidentais ao inserir caracteres nos dados.
    :param binary_sequence: Lista de bytes (dados do quadro).
    :return: Lista de bytes com as inserções de flag e caracteres realizadas.
    """
    
    # Declaração da Flag
    flag = [0,1,1,1,1,1,1,0]
    
    framed_data = [bit for bit in flag]  # Adiciona o byte de flag inicial
    
    char_insertion = [0,1,1,1,1,1,0,1,0]

    for bit in range(len(binary_sequence)):
        if binary_sequence[bit:bit+8] == flag:
            binary_sequence = binary_sequence[:bit]+ char_insertion + binary_sequence[bit+8:]
    
    framed_data.extend(binary_sequence)
            
    # Adiciona o byte de flag final    
    framed_data.extend(flag)  
    
    return framed_data

def parity_bit(binary_sequence):
    """
    Função para cálculo de bit de paridade.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Lista de bits com bit de paridade.
    """
    # Cálculo do bit de paridade
    binary_sequence.append(sum(binary_sequence) % 2)  # Soma os bits 1 e verifica se é par ou ímpar
    return binary_sequence

def crc(binary_sequence):
    """
    Calcula o CRC usando o polinômio gerador pré-determinado (1101).
    :param dividendo: lista de bits representando o dividendo.
    :return: lista de bits resultante que contém o dividendo concatenado ao CRC.
    """
    # Dividendo
    dividendo = binary_sequence
    
    # Polinômio gerador
    polynomial = [1, 1, 0, 1]
    
    # Adicionar zeros ao final do dividendo para o cálculo do CRC
    crc = dividendo + [0] * (len(polynomial) - 1)

    # Dividir o dividendo pelo polinômio gerador
    for i in range(len(dividendo)):
        if crc[i] == 1:  # Se o bit atual do CRC for 1
            for j in range(len(polynomial)):
                # Realiza a operação XOR com o polinômio gerador
                crc[i + j] ^= polynomial[j]

    # Retorna o dividendo concatenado ao CRC (os últimos 3 bits)
    return dividendo + crc[-(len(polynomial) - 1):]

def hamming(binary_sequence):
    """
    Função para cálculo de código de Hamming.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Lista de bits com código de Hamming.
    """
    # Dividir a sequência em grupos de 8 bits (1 byte)
    grouped_bytes = [binary_sequence[i:i + 8] for i in range(0, len(binary_sequence), 8)]
    hamming_sequence = ''

    for byte in grouped_bytes:
        # Garantir que o byte tenha exatamente 8 bits
        if len(byte) != 8:
            hamming_sequence += ''.join(map(str, byte))
        else:
            # Conversão dos bits de string para inteiros (caso necessário)
            byte = list(map(int, byte))

            # Cálculo dos bits de paridade
            p1 = (byte[0] + byte[1] + byte[3] + byte[4] + byte[6]) % 2
            p2 = (byte[0] + byte[2] + byte[3] + byte[5] + byte[6]) % 2
            p4 = (byte[1] + byte[2] + byte[3] + byte[7]) % 2
            p8 = (byte[4] + byte[5] + byte[6] + byte[7]) % 2

            # Construir o novo byte com os bits de Hamming
            hamming_byte = [p1, p2, byte[0], p4, byte[1], byte[2], byte[3], p8, byte[4], byte[5], byte[6], byte[7]]

            # Adicionar o byte codificado à sequência final
            hamming_sequence += ''.join(map(str, hamming_byte))

    return [int(bit) for bit in hamming_sequence]

def ascii_to_binary(ascii_input):
    # Função que converte uma string ASCII para uma string binária
    binary_output = ""
    for char in ascii_input:
        binary_output += format(ord(char), "08b")
    return binary_output

def main(framing, error_detection, error_correction, ascii_input):
    
    bin_ascii_input = ascii_to_binary(ascii_input)
    binary_sequence = [int(bit) for bit in bin_ascii_input]
  
    # Verifica o tipo de enquadramento a ser utilizado
    if framing == "Contagem de Caracteres":
        binary_sequence = char_count(binary_sequence)
    elif framing == "Inserção de Bytes":
        binary_sequence = byte_insertion(binary_sequence)
    elif framing == "Inserção de Bits":
        binary_sequence = char_insertion(binary_sequence)

    # Verifica o tipo de detecção de erros a ser utilizado
    if error_detection == "Bit de Paridade":
        binary_sequence = parity_bit(binary_sequence)
    elif error_detection == "CRC":
        binary_sequence = crc(binary_sequence)
        
    # Verifica o tipo de correção de erros a ser utilizada
    if error_correction == "Hamming":
        binary_sequence = hamming(binary_sequence)

    return binary_sequence, bin_ascii_input