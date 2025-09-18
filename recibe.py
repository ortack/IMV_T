import spidev
import lgpio
import time

# Pines según Waveshare SX1262 HAT
BUSY = 17
RESET = 27
DIO1 = 25  # Interrupción RX_DONE
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

def read_buffer():
    send_cmd(0x1E, [0x00, 0x00])  # SetBufferBaseAddress RX
    time.sleep(0.01)
    while lgpio.gpio_read(h, BUSY):
        time.sleep(0.001)
    spi.xfer2([0x1E, 0x00, 0x00])  # Dummy read
    time.sleep(0.01)
    spi.xfer2([0x1E])
    data = spi.readbytes(32)  # Ajusta tamaño según payload
    return data

# Configura modo de recepción
send_cmd(0x82)  # SetRxContinuous

print("Esperando mensaje LoRa...")

try:
    while True:
        if lgpio.gpio_read(h, DIO1) == 1:
            print("Mensaje recibido!")
            payload = read_buffer()
            print("Datos:", payload)
            time.sleep(0.5)
except KeyboardInterrupt:
    print("Interrumpido por el usuario.")
finally:
    spi.close()
    lgpio.gpiochip_close(h)
