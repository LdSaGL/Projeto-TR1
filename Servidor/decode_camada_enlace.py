import binascii

# Funções auxiliares importadas dos questionários
def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def decode_hamming(binary_sequence):
    """
    Realiza a decodificação do método de Hamming.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Lista de bits com a sequência decodificada.
    """
    
    # Agrupa em grupos de 12 bits, uma vez que a função de Hamming é aplicada em grupos de 8 bits
    grouped_bytes = [binary_sequence[i:i + 12] for i in range(0, len(binary_sequence), 12)]
    
    decoded_list = []
    for byte in grouped_bytes:
        # Em casos em que o byte não é completo, ele é ignorado (possível melhoria - mais robustez)
        if len(byte) == 12:
            # Cálculo dos bits de paridade
            t1 = (byte[0] + byte[2] + byte[4] + byte[6] + byte[8]+ byte[10]) % 2
            t2 = (byte[1] + byte[2] + byte[5] + byte[6] + byte[9] + byte[10]) % 2
            t4 = (byte[3] + byte[4] + byte[5] + byte[6] + byte[11]) % 2
            t8 = (byte[7] + byte[8] + byte[9] + byte[10] + byte[11]) % 2
            
            # Cálculo do erro e correção
            error = t1*1 + t2*2 + t4*4 + t8*8
            if error != 0:
                byte[error-1] = 1 - byte[error-1]
            
            # Remoção dos bits de paridade e adição dos bits na lista        
            original_byte = [byte[2], byte[4], byte[5], byte[6], byte[8], byte[9],  byte[10], byte[11]]
            decoded_list.extend(original_byte)
        else:
            # Adição dos bits na lista
            decoded_list.extend(byte)
    
    return decoded_list

def decode_crc(binary_sequence):
    """
    Realiza a decodificação do método de CRC.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Lista de bits com a sequência decodificada (Sem o CRC).
    """
    # Dividendo
    dividendo = binary_sequence.copy()
    
    # Polinômio gerador
    polynomial = [1, 1, 0, 1]
    
    # Dividir o dividendo pelo polinômio gerador
    for i in range(len(dividendo)-3):
        if dividendo[i] == 1:  # Se o bit atual do CRC for 1
            for j in range(len(polynomial)):
                # Realiza a operação XOR com o polinômio gerador
                dividendo[i + j] ^= polynomial[j]
    resto = dividendo[-(len(polynomial) - 1):]
    
    # Verificação do resto
    if resto != [0,0,0]:
        raise Exception("Erro de transmissão detectado - CRC")
    return binary_sequence[:-3]

def decode_parity_bit(binary_sequence):
    """
    Realiza a decodificação do método de Bit de Paridade.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Lista de bits com a sequência decodificada (Sem o bit de paridade).
    """
    # Cálculo do bit de paridade
    parity = sum(binary_sequence) % 2 
    
    # Verificação do bit de paridade, retorna erro se o número de bits 1 for ímpar    
    if parity != 0:
        raise Exception("Erro de transmissão detectado - Bit de Paridade")
        
    return binary_sequence[:-1]

def decode_char_insertion(binary_sequence):
    """
    Realiza a decodificação do método de Inserção de Caracteres.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Lista de bits com a sequência decodificada (Sem a flag).
    """
    # Declaração da Flag
    flag = [0,1,1,1,1,1,1,0]
    trimmed_sequence = binary_sequence[8:-8]
    
    # Verifica se as flags de início e fim recebidas batem com a flag
    flag_inicial = binary_sequence[:8]
    flag_final = binary_sequence[-8:]
    if flag_inicial != flag or flag_final != flag:
        raise Exception("Erro de transmissão detectado - Inserção de Caracteres")
    
    flag_inserted_char = [0,1,1,1,1,1,0,1,0]
    for bit in range(len(trimmed_sequence)):
        if trimmed_sequence[bit:bit+9] == flag_inserted_char:
            trimmed_sequence = trimmed_sequence[:bit] + flag + trimmed_sequence[bit+9:]
    return trimmed_sequence

def decode_byte_insertion(binary_sequence):
    """
    Função para decodificação do enquadramento Inserção de Bytes.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Lista de bits com a sequência decodificada e os escapes inseridos pela camada de enlace transmissora removidos.
    """
    # Declaração da Flag e Escape
    flag =   [0,1,1,1,1,1,1,0]
    escape = [0,1,1,1,1,0,1,1]
    
    # Sequência sem os bytes de flag
    trimmed_sequence = binary_sequence[8:-8]
    
    # Verifica se as flags de início e fim recebidas batem com a flag
    flag_inicial = binary_sequence[:8]
    flag_final = binary_sequence[-8:]
    if flag_inicial != flag or flag_final != flag:
        raise Exception("Erro de transmissão detectado - Inserção de Bytes")
    
    # Verifica se encontra um escape e remove-o
    ignore_next_flag_or_escape = False
    for i in range(len(trimmed_sequence)):
        if trimmed_sequence[i:i+8] == escape and not ignore_next_flag_or_escape:
            ignore_next_flag_or_escape = True
            trimmed_sequence = trimmed_sequence[:i] + trimmed_sequence[i+8:]
        else:
            if trimmed_sequence[i:i+8] == flag or trimmed_sequence[i:i+8] == escape:
                ignore_next_flag_or_escape = False
    return trimmed_sequence

def decode_char_count(binary_sequence):
    """
    Função para decodificação do enquadramento Contagem de Caracteres.
    :param binary_sequence: Lista de bits representando a sequência binária.
    :return: Lista de bits com a sequência decodificada.
    """
    # Separa os 8 primeiros bits para obter o número de caracteres
    first_8_bits = text_from_bits(''.join(map(str,binary_sequence[:8])))
    # Separa os próximos 8 bits para obter o número de caracteres (caso necessário)
    second_8_bits = text_from_bits(''.join(map(str,binary_sequence[8:16])))
    
    # Inicializa a sequência de dados
    data_sequence = binary_sequence[8:]
    char_number=first_8_bits
    # Verifica se o número de caracteres é um número decimal e se a sequência binária é maior que 16, ou seja, se o segundo byte também faz parte da contagem
    if second_8_bits.isdecimal() and len(binary_sequence) > 16:
        char_number += second_8_bits
        # Modifica a sequência de dados para a partir do 17º bit
        data_sequence = binary_sequence[16:]
    
    # Lança exceção caso o número de caracteres recebido não corresponda ao tamanho da sequência de dados
    if len(data_sequence) != int(char_number):
        raise Exception("Erro de transmissão detectado - Contagem de Caracteres")
        
    return data_sequence

def main(framing, error_detection, error_correction, binary_sequence):
    """
    Função principal para decodificação da camada de enlace.
    :param binary_sequence: Sequência binária de entrada.
    :param framing: Tipo de enquadramento selecionado.
    :param error_detection: Tipo de detecção de erros selecionado.
    :param error_correction: Tipo de correção de erros selecionado.
    :return: Mensagem decodificada e sequência binária.
    """
    # Correção de erros
    if error_correction == "Hamming":
        binary_sequence = decode_hamming(binary_sequence)
        
    # Decodificação de erros
    if error_detection == "Bit de Paridade":
        binary_sequence = decode_parity_bit(binary_sequence)
    elif error_detection == "CRC":
        binary_sequence = decode_crc(binary_sequence)
        
    # Decodificação do enquadramento
    if framing == "Contagem de Caracteres":
        binary_sequence = decode_char_count(binary_sequence)
    elif framing == "Inserção de Bytes":
        binary_sequence = decode_byte_insertion(binary_sequence)
    elif framing == "Inserção de Bits":
        binary_sequence = decode_char_insertion(binary_sequence)
    
    x = ''.join(map(str,binary_sequence))
    return text_from_bits(''.join(map(str,binary_sequence))), ' '.join(x[i:i+8] for i in range(0, len(x), 8))