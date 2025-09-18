import spidev
import lgpio
import time
import serial
import pynmea2
import json

# Pines SX1262
BUSY = 17
RESET = 27
CS = 8

# Inicializa GPIO
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, RESET, 1)
lgpio.gpio_claim_input(h, BUSY)

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

def transmit():
    send_cmd(0x83, [0x00, 0x00, 0x00])  # SetTx with timeout
    print("Mensaje transmitido")

# Configura LoRa
send_cmd(0x86, freq_to_bytes(868.1))  # Frecuencia
send_cmd(0x8E, [0x0E])                # Potencia: 14 dBm
send_cmd(0x80, [0x00])                # Standby
send_cmd(0x8A, [0x70])                # PacketType: LoRa
send_cmd(0x8B, [0x00])                # Regulator: LDO

# Inicializa GNSS
gnss = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

print("Esperando datos GNSS...")

try:
    while True:
        line = gnss.readline().decode("utf-8", errors="ignore")
        if line.startswith("$GNGGA"):
            try:
                msg = pynmea2.parse(line)
                lat = msg.latitude
                lon = msg.longitude
                alt = msg.altitude
                payload = {
                    "lat": round(lat, 6),
                    "lon": round(lon, 6),
                    "alt": round(alt, 1)
                }
                json_str = json.dumps(payload)
                print("Enviando:", json_str)
                data_bytes = list(json_str.encode("utf-8"))
                write_tx_buffer(data_bytes)
                transmit()
                time.sleep(10)  # Intervalo entre envíos
            except pynmea2.ParseError:
                continue
except KeyboardInterrupt:
    print("Interrumpido por el usuario.")
finally:
    spi.close()
    lgpio.gpiochip_close(h)
    gnss.close()
