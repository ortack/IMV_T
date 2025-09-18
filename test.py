import lgpio
import time

h = lgpio.gpiochip_open(0)
BUSY_PIN = 17  # Ajusta si usas otro pin

while True:
    busy = lgpio.gpio_read(h, BUSY_PIN)
    print("BUSY:", "HIGH" if busy else "LOW")
    time.sleep(1)


