import spidev
import lgpio
import time
import json

# Pines según Waveshare SX1262 HAT
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

# Espera a que BUSY esté en LOW
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

def read_rx_buffer():
    # Set RX buffer base address
    send_cmd(0x1E, [0x00, 0x00])
    time.sleep(0.01)
    # Read RX buffer
    spi.xfer2([0x1E])
    time.sleep(0.01)
    payload = spi.readbytes(32)  # Ajusta tamaño según tu payload
    return payload

# Configura frecuencia a 868.1 MHz
send_cmd(0x86, freq_to_bytes(868.1))
print("Frecuencia configurada a 868.1 MHz")

# Configura potencia de transmisión (ej. 14 dBm)
send_cmd(0x8E, [0x0E])  # 0x0E = 14 dBm

# Configura modo LoRa
send_cmd(0x80, [0x00])  # SetStandby
send_cmd(0x8A, [0x70])  # SetPacketType: LoRa
send_cmd(0x8B, [0x00])  # SetRegulatorMode: LDO
send_cmd(0x82)          # SetRxContinuous

print("Modo recepción activado. Esperando mensajes...")

try:
    while True:
        if lgpio.gpio_read(h, DIO1) == 1:
            print("📨 Mensaje recibido")
            payload = read_rx_buffer()
            try:
                text = bytes(payload).decode('utf-8').strip('\x00')
                print("Texto:", text)
                try:
                    data = json.loads(text)
                    print("JSON:", json.dumps(data, indent=2))
                except json.JSONDecodeError:
                    pass
            except UnicodeDecodeError:
                print("Payload binario:", payload)
            time.sleep(0.5)
except KeyboardInterrupt:
    print("Interrumpido por el usuario.")
finally:
    spi.close()
    lgpio.gpiochip_close(h)
