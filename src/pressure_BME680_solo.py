"""
Código para validação do funcionamento do BME680 + OLED

Botão de chaveamento de informações do sensor

    O botão serve para chavear no display as diferentes grandezas capturadas pelo sensor:

        * Pressão Atmosférica
        * Temperatura
        * Umidade
        * Qualidade do ar
        * Altitude

LED RGB de indicação de funcionamento ou falha

    * LED em verde indica que o circuito está funcional
    * LED pisca em verde quando executa leitura do sensor
    * LED pisca em verde quando pressiona o botão
    * LED pisca em vermelho quando há falha de leitura do sensor
"""
import sys

from machine import Pin, I2C
from bme680 import BME680_I2C
from time import ticks_ms, sleep_ms
import ssd1306

# Definição dos valores de on/off para LED RGB:
# Anodo comum  => on=0, off=1
# Catodo comum => on=1, off=0
LED_ON = 1
LED_OFF = 0

NORMAL_STATE_READ = 10000
ERROR_STATE_READ = 5000

# Configuração I2C da Pico
# Usaremos I2C 0, GPIO 20 e 21 --> SDA e SCL
i2c = I2C(0, scl=Pin(21), sda=Pin(20))
bme = BME680_I2C(i2c=i2c)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Configuração das GPIOs para Botão e Leds
button = Pin(22, Pin.IN, Pin.PULL_UP)
led_R = Pin(27, Pin.OUT)
led_G = Pin(18, Pin.OUT)
led_B = Pin(19, Pin.OUT)

# Definindo estado inicial do LED RGB
led_R.value(LED_OFF)
led_G.value(LED_ON)
led_B.value(LED_OFF)

# Variáveis
state = -1
disp_prob = 0
relogio_bme = ticks_ms()
relogio_led = ticks_ms()
button_time = ticks_ms()

f_temperature = ''
f_humidity = ''
f_pressure = ''

def blink_alert():
    led_R.value(LED_OFF)
    sleep_ms(400)
    led_R.toggle()

def blink_functional():
    led_G.value(LED_OFF)
    sleep_ms(200)
    led_G.toggle()

def toggle_RGB(led_value):
    led_R.value(led_value)
    led_G.value(led_value)
    led_B.value(led_value)

def check_device_alert(device_id):
    if device_id == 60:
        blink_alert()
    elif end == 119:
        led_R.off()
        led_G.on()
    else:
        toggle_RGB(LED_OFF)

def set_error_state():
    led_G.value(LED_OFF)
    led_R.value(LED_ON)

def set_normal_state():
    led_G.value(LED_ON)
    led_R.value(LED_OFF)

while True:
    set_normal_state()

    # Leitura do botão com debounced
    if(button.value() == 0):
        # Debounced
        if(button.value() == 0) and (ticks_ms() - button_time > 100):
            button_time = ticks_ms()
            state = state + 1
            if state > 4:
                state = 0 
            blink_functional()
            print(f'button state: {state}')


    try:
        diff = ticks_ms() - relogio_bme
        # Obtenção dos parâmetros a cada 10 [s]
        if(diff > NORMAL_STATE_READ):
            print('reading data')
            blink_functional()
            f_temperature = "%0.1f C" % bme.temperature
            f_humidity = "%0.1f %%" % bme.humidity
            f_pressure = "%0.3f hPa" % bme.pressure
            temp = str(round(bme.temperature, 2)) + ' C'
            print(f'\nTemperatura: {f_temperature}')
            hum = str(round(bme.humidity, 2)) + ' %'
            print(f'Umidade: {f_humidity}')
            pres = str(round(bme.pressure, 2)) + ' hPa'
            print(f'Pressão: {f_pressure}\n')
            ar = str(round(bme.gas/1000, 2)) + ' KOhms'
            alt = str(round(bme.altitude, 2)) + ' m'
            relogio_bme = ticks_ms()

        if(state == 0):
            display.fill(0)
            display.text('Pressao: ', 0, 0)
            display.text(pres, 0, 24)
            display.show()
#             print(f'Pressao: {f_pressure}')
        elif(state == 1):
            display.fill(0)
            display.text('Temperatura: ', 0, 0)
            display.text(temp, 0, 24)
            display.show()
#             print(f'Temperatura: {f_temperature}')
        elif(state == 2):
            display.fill(0)
            display.text('Umidade Relativa: ', 0, 0)
            display.text(hum, 0, 24)
            display.show()
#             print(f'Umidade Relativa: {f_humidity}')
        elif(state == 3):
            display.fill(0)
            display.text('Altitude: ', 0, 0)
            display.text(alt, 0, 24)
            display.show()
#             print(f'Altitude: {alt}')
        elif(state == 4):
            display.fill(0)
            display.text('Qualidade do Ar: ', 0, 0)
            display.text(ar, 0, 24)
            display.show()
#             print(f'Qualidade do Ar: {ar}')

        disp_prob = 0
        led_G.value(LED_ON)

    except OSError as ose:
        set_error_state()
        print(f'OSError: {ose}')
        if(disp_prob == 0):
            devices = i2c.scan()
            print(f'Devices found: {devices}')
            if(len(devices) == 0 or devices[0] != 119):
                check_device_alert(119)
                disp_prob = 2
            elif(devices[0] != 60):
                check_device_alert(60)
                disp_prob = 1
        elif(disp_prob == 1):
            if(ticks_ms() - relogio_led > ERROR_STATE_READ):
                check_device_alert(60)
                relogio_led = ticks_ms()
        elif(disp_prob == 2):
            if(ticks_ms() - relogio_led > ERROR_STATE_READ):
                check_device_alert(119)
                relogio_led = ticks_ms()

    except KeyboardInterrupt as k:
        sys.exit()
    except BaseException as e:
        print(type(e))
        print(f'Unexpected {e}')


