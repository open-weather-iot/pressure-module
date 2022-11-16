from machine import Pin, I2C
from bme680 import BME680_I2C

class Pressure_BME680:

    # deve receber os parâmetros nomeados necessários e o barramento utilizado (seja SPI, Serial ou I2C)
    def __init__(self, *, i2c_id, clk_pin, sda_pin):
        self.i2c = I2C(i2c_id, scl=Pin(clk_pin), sda=Pin(sda_pin))
        self.bme = BME680_I2C(i2c=self.i2c)
        # self.led_R = Pin(r_pin, Pin.OUT)
        # self.led_G = Pin(g_pin, Pin.OUT)
        # self.led_B = Pin(b_pin, Pin.OUT)


    # método **OPCIONAL** da classe que realiza a inicialização do sensor
    def setup(self):
        pass

    # método **OBRIGATÓRIO** da classe que realiza leituras do sensor
    def read(self, state):
        if(state == 0):
            f_pressure = "%0.3f hPa" % self.bme.pressure
            pres = round(self.bme.pressure, 2)
            print(f'Pressao: {f_pressure}\n')
            return { 'raw': self.bme.pressure, 'value': pres, 'unit': 'hPa' }
        elif(state == 1):
            f_temperature = "%0.1f C" % self.bme.temperature
            temp = round(self.bme.temperature, 2)
            print(f'\nTemperatura: {f_temperature}')
            return { 'raw': self.bme.temperature, 'value': temp, 'unit': 'C' }
        elif(state == 2):
            f_humidity = "%0.1f %%" % self.bme.humidity
            hum = round(self.bme.humidity, 2)
            print(f'Umidade: {f_humidity}')
            return { 'raw': self.bme.humidity, 'value': hum, 'unit': '%' }
        elif(state == 3):
            alt = round(self.bme.altitude, 2)
            print(f'Altitude: {alt}')
            return { 'raw': self.bme.altitude, 'value': alt, 'unit': 'm' }
        elif(state == 4):
            ar = round(self.bme.gas/1000, 2)
            print(f'Qualidade do Ar: {ar}')
            return { 'raw': self.bme.gas, 'value': ar, 'unit': 'KOhms' }
        # raw: os valores puros que foram lidos do sensor que se está trabalhando
        # value: representa o valor após conversão de unidades para ser apresentado diretamente ao usuário final
        # unit: unidade de medida
        return { 'raw': {}, 'value': 0.0, 'unit': '' }
