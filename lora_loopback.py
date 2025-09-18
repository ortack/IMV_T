import spidev
import lgpio
import time
import json

# Pines SX1262
BUSY = 17
RESET = 27
DIO1 = 25  # RX_DONE interrupt
CS = 8     # CE0 → spidev0.0

# Inicializa GPIO
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, RESET, 1)
lgpio.gpio_claim_input(h, BUSY)
lgpio.gpio_claim_input(h, DIO1)

# Pulso de RESET
lgpio.gpio_write(h, RESET, 0)
time.sleep(0.01)
lgpio.gpio_write(h, RESET, 1)
time.sleep(0.01)

while lgpio.gpio_read(h, BUSY):
    time.sleep(0.01)

# Inicializa SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
spi.mode = 0b00

def send_cmd(cmd, data=[]):
    while lgpio.gpio_read(h, BUSY):
        time.sleep(0.001)
    spi.xfer2([cmd] + data)
    while lgpio.gpio_read(h, BUSY):
        time.sleep(0.001)

def freq_to_bytes(freq_mhz):
    freq = int((freq_mhz * 1_000_000) / 1.953125)
    return [(freq >> 24) & 0xFF, (freq >> 16) & 0xFF, (freq >> 8) & 0xFF, freq & 0xFF]

def write_tx_buffer(data_bytes):
    send_cmd(0x0E, [0x00])  # SetBufferBaseAddress TX
    time.sleep(0.01)
    spi.xfer2([0x0E] + data_bytes)

def read_rx_buffer():
    send_cmd(0x1E, [0x00, 0x00])  # SetBufferBaseAddress RX
    time.sleep(0.01)
    spi.xfer2([0x1E])
    time.sleep(0.01)
    return spi.readbytes(32)

def transmit():
    send_cmd(0x83, [0x00, 0x00, 0x00])  # SetTx
    print("Mensaje transmitido")

def receive():
    send_cmd(0x82)  # SetRxContinuous
    print("Escuchando...")

# Configura LoRa
send_cmd(0x86, freq_to_bytes(868.1))  # Frecuencia
send_cmd(0x8E, [0x0E])                # Potencia: 14 dBm
send_cmd(0x80, [0x00])                # Standby
send_cmd(0x8A, [0x70])                # PacketType: LoRa
send_cmd(0x8B, [0x00])                # Regulator: LDO

# Mensaje de prueba
payload = {
    "lat": 40.543135,
    "lon": -3.641709,
    "alt": 734.7
}
json_str = json.dumps(payload)
data_bytes = list(json_str.encode("utf-8"))

# Transmitir
write_tx_buffer(data_bytes)
transmit()
time.sleep(0.5)

# Cambiar a recepción
receive()

# Esperar mensaje
timeout = time.time() + 5
while time.time() < timeout:
    if lgpio.gpio_read(h, DIO1) == 1:
        print("Mensaje recibido")
        rx_data = read_rx_buffer()
        try:
            text = bytes(rx_data).decode("utf-8").strip('\x00')
            print("Texto:", text)
            try:
                parsed = json.loads(text)
                print("JSON:", json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                pass
        except UnicodeDecodeError:
            print("Payload binario:", rx_data)
        break
    time.sleep(0.1)
else:
    print(" No se recibió ningún mensaje")

# Cierre
spi.close()
lgpio.gpiochip_close(h)
