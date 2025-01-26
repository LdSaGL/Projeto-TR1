import camada_enlace as ce

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

x = ce.parity_bit([0,1,0,0,1,0,0,0])
print(x)
print(decode_parity_bit([0,1,0,0,1,0,0,0]))