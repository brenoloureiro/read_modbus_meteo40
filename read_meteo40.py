#Script SCADA ler RJ485 datalogger
#Script SCADA ler datalogger via Modbus TCP

from pymodbus.client import ModbusTcpClient
import time
import struct

# Configurações do Modbus TCP
IP = '192.168.1.16'
PORT = 502
SLAVE_ID = 1           # ID do dispositivo Modbus (endereço)
START_ADDRESS = 0      # Endereço inicial do registrador
NUM_REGISTERS = 6      # Quantidade de registradores a ler

client = ModbusTcpClient(IP, port=PORT)

def regs_to_floats(registers):
    floats = []
    for i in range(0, len(registers), 2):
        bytes_ = registers[i].to_bytes(2, 'big') + registers[i+1].to_bytes(2, 'big')
        float_val = struct.unpack('>f', bytes_)[0]
        floats.append(float_val)
    return floats

if client.connect():
    print(f'Conectado ao Modbus TCP em {IP}:{PORT}.')
    try:
        while True:
            # Lê 4 registradores a partir do endereço 0 (pega os floats dos endereços 0 e 2)
            result = client.read_input_registers(address=0, count=12, slave=SLAVE_ID)
            if not result.isError():
                regs = result.registers
                print(f'Registradores lidos: {regs}')
                print(f'Registradores lidos (hex): {[hex(r) for r in regs]}')
                floats = regs_to_floats(regs)
                print(f'Valores float convertidos: {floats}')
            else:
                print('Erro na leitura Modbus:', result)
            time.sleep(2)  # Aguarda 2 segundos para próxima leitura
    except KeyboardInterrupt:
        print('Leitura interrompida pelo usuário.')
    finally:
        client.close()
        print('Conexão Modbus encerrada.')
else:
    print(f'Não foi possível conectar ao Modbus TCP em {IP}:{PORT}.')