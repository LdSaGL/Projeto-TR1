import binascii
import camada_enlace as ce

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def decode_hamming(binary_sequence):
    grouped_bytes = [binary_sequence[i:i + 12] for i in range(0, len(binary_sequence), 12)]
    
    for byte in grouped_bytes:
        # Cálculo dos bits de paridade
        t1 = (byte[0] + byte[2] + byte[4] + byte[6] + byte[8]+ byte[10]) % 2
        t2 = (byte[1] + byte[2] + byte[5] + byte[6] + byte[9] + byte[10]) % 2
        t4 = (byte[3] + byte[4] + byte[5] + byte[6] + byte[11]) % 2
        t8 = (byte[7] + byte[8] + byte[9] + byte[10] + byte[11]) % 2
        
        error = t1*1 + t2*2 + t4*4 + t8*8
        if error != 0:
            byte[error-1] = 1 - byte[error-1]
        
        original_byte = [byte[2], byte[4], byte[5], byte[6], byte[8], byte[9],  byte[10], byte[11]]
        
    return original_byte

def decode_crc(binary_sequence):
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
    
    if resto != [0,0,0]:
        raise Exception("Erro de transmissão detectado")
    return binary_sequence[:-3]

def decode_parity_bit(binary_sequence):
    # Cálculo do bit de paridade
    parity = sum(binary_sequence) % 2 
        
    if parity != 0:
        raise Exception("Erro de transmissão detectado")
        
    return binary_sequence[:-1]

def decode_char_insertion(binary_sequence):
    # Declaração da Flag
    flag = [0,1,1,1,1,1,1,0]
    trimmed_sequence = binary_sequence[8:-8]
    
    flag_inserted_char = [0,1,1,1,1,1,0,1,0]
    for bit in range(len(trimmed_sequence)):
        if trimmed_sequence[bit:bit+9] == flag_inserted_char:
            trimmed_sequence = trimmed_sequence[:bit] + flag + trimmed_sequence[bit+9:]
    return trimmed_sequence

def decode_byte_insertion(binary_sequence): ##
    # Declaração da Flag
    flag =   [0,1,1,1,1,1,1,0]
    escape = [0,1,1,1,1,0,1,1]
    trimmed_sequence = binary_sequence[8:-8]
    
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
    first_8_bits = text_from_bits(''.join(map(str,binary_sequence[:8])))
    second_8_bits = text_from_bits(''.join(map(str,binary_sequence[8:16])))
    
    data_sequence = binary_sequence[8:]
    char_number=first_8_bits
    if second_8_bits.isdecimal() and len(binary_sequence) > 16:
        char_number += second_8_bits
        data_sequence = binary_sequence[16:]
    
    if len(data_sequence) != int(char_number):
        raise Exception("Erro de transmissão detectado")
        
    return data_sequence