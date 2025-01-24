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
    if len(binary_sequence) % 8 != 0: # Verifica se os bits estão alinhados corretamente
        raise ValueError('Os bits não estão alinhados corretamente')
    sequence_size = text_to_bits(str(len(binary_sequence))) # Converte o tamanho da sequência para ASCII representado em binário
    
    # Converte a string de contagem de caracteres a forma de lista 
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
    flag = [0,1,1,1,1,1,1,0]
    escape = [0,1,1,1,1,1,0,1]
    
    framed_data = [bit for bit in flag]  # Adiciona o byte de flag inicial

    # Dividir em grupos de 8 bits
    grouped_bytes = [binary_sequence[i:i+8] for i in range(0, len(binary_sequence), 8)]
    
    # Insere o byte de escape quando encontra uma flag ou um escape
    for byte in grouped_bytes:
        if byte == flag or byte == escape:  # Verifica se o byte é uma flag ou um escape
            framed_data.extend(escape) 
            
        # Adiciona o byte atual
        framed_data.extend(byte)    
             
    # Adiciona o byte de flag final        
    framed_data.extend(flag)   
     
    return framed_data

def char_insertion(binary_sequence):
    """
    Realiza a inserção de flags para delimitar quadros e trata flags acidentais ao inserir caracteres nos dados.
    :param binary_sequence: Lista de bytes (dados do quadro).
    :return: Lista de bytes com as inserções de flag e caracteres realizadas.
    """
    
    # Declaração da Flag
    flag = [0,1,1,1,1,1,1,0]
    
    framed_data = [bit for bit in flag]  # Adiciona o byte de flag inicial

    # Dividir em grupos de 8 bits
    grouped_bytes = [binary_sequence[i:i+8] for i in range(0, len(binary_sequence), 8)]

    # Insere o byte de carga útil que tem o mesmo valor que a flag adicionando um 0 no lugar do sexto 1
    for byte in grouped_bytes:
        if byte == flag:  # Verifica se o byte é uma flag
            framed_data.extend([0, 1, 1, 1, 1, 1, 0, 1, 0]) 
        else:
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
