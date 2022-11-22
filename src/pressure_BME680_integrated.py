from machine import Pin, I2C
from bme680 import BME680_I2C

class Pressure_BME680:

     def __init__(self, *, i2c_id, clk_pin, sda_pin):
        self.i2c = I2C(i2c_id, scl=Pin(clk_pin), sda=Pin(sda_pin))
        self.bme = BME680_I2C(i2c=self.i2c)


    def read(self, state):

        # Obtenção dos parâmetros
        f_pressure = "%0.2f" % self.bme.pressure
        f_temperature = "%0.2f" % self.bme.temperature
        f_humidity = "%0.2f" % self.bme.humidity
        alt = round(self.bme.altitude, 2)
        ar = round(self.bme.gas/1000, 2)    # Transformação desta variável
        
        # Geração de código de erro, caso não consiga executar as ações anteriores

        # Retorno dos parâmetros
        return{ 'raw' : {'Press_BME680', 'Temp_BME680', 'Umid_BME680', 'Alt_BME680', 'Ar_BME680'},
                'value': {f_pressure, f_temperature, f_humidity, alt, ar},
                'unit': {'hPa', 'C', '%', 'm', 'kOhm'}  
        }
