from machine import Pin, I2C
from bme680 import BME680_I2C

class Pressure_BME680:

     def __init__(self, *, i2c_id, clk_pin, sda_pin):
        self.i2c = I2C(i2c_id, scl=Pin(clk_pin), sda=Pin(sda_pin))
        self.bme = BME680_I2C(i2c=self.i2c)


        # Criação da lista auxiliar para cálculo da média e contador
        valores_media_bme680 = []
        cont_media_bme = 0


    def read(self, state):

        # Obtenção dos parâmetros
        f_pressure = "%0.2f" % self.bme.pressure
        #f_temperature = "%0.2f" % self.bme.temperature
        #f_humidity = "%0.2f" % self.bme.humidity
        #alt = round(self.bme.altitude, 2)
        #ar = round(self.bme.gas/1000, 2)    # Transformação desta variável
        
        # Geração de código de erro, caso não consiga executar as ações anteriores

        # Retorno dos parâmetros
        '''
        return{ 'raw' : {'Press_BME680', 'Temp_BME680', 'Umid_BME680', 'Alt_BME680', 'Ar_BME680'},
                'value': {f_pressure, f_temperature, f_humidity, alt, ar},
                'unit': {'hPa', 'C', '%', 'm', 'kOhm'}  
        }
        '''
        
        # Adiciono na lista de valores
        valores_media_bme680.append(f_pressure)
        cont_media_bme += 1

        # Cálculo da média de 10 valores
        if(cont_media_bme >= 10):
            
            media_press = 0

            # trocar por macro de media do python --> mean --> tem que usar a lib Numpy
            for k in range(cont_media_bme): 
                media_press += valores_media_bme680[k]
            media_press/cont_media_bme
            cont_media_bme = 0

            return{'raw': 'Press_BME680', 'value': media_press, 'unit': 'hPa'}

