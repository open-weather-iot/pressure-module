# MÓDULO DE PRESSÃO ATMOSFÉRICA

O módulo de pressão atmosférica faz parte do projeto de estação meteorológica no âmbito da disciplina de Laboratorio Experimental de Campus Inteligente (IE321K - 2S2022).

O sensor utilizado é o [BME680](https://br.mouser.com/datasheet/2/783/BST_BME680_DS001-1509608.pdf) que além da pressão atmosférica, realiza medição de outras grandezas como temperatura, umidade relativa do ar, altitude e qualidade do ar.

## Protótipo

Foi realizado um protótipo inicial para avaliar as medições do sensor e dinâmica de funcionamento do software.

![Skematics](./img/proto-skematic.png)

Para o circuito foram utilizados os seguintes componentes:

* RaspberryPi Pico 
* Módulo sensor BME680
* 1 Tela (_Display_ OLED 128x32)
* 1 LED RGB
* 1 Botão (_Push button_)

**Funcionamento:** O LED RGB informa a cor verde indicando funcionamento normal do sistema. A cada leitura do sensor e pressionamento do botão, o LED pisca.
O botão serve para alternar a exibição na tela das 5 grandezas exibidas pelo sensor, sendo que inicialmente é exibido primeiro o valor de pressão atmosférica.
As medições ocorrem a cada 10 segundos. Caso ocorra algum erro com a leitura I2C do sensor, o LED vai alternar para vermelho, piscando a cada 5 segundos. Ao restabelecer a conexão I2C, retorna ao estado normal (verde).




## Orientações gerais
### Import
Não importe módulos inteiros.

> ❌
> ```py
> from example import *
> ```

> ✅
> ```py
> from example import Example
> ```

---

### Variáveis e instruções globais
Evite utilizar variáveis e instruções globais para prover uma melhor modularização do código.

> ❌
> ```py
> # src/blink_led.py
> from time import sleep_ms
> from machine import Pin
>
> led_builtin = Pin(25, Pin.OUT)
> led_builtin.value(1)
> interval = 1000
>
> def blink():
>     while True:
>         led_builtin.toggle()
>         sleep_ms(interval)
>
> # test/main.py
> from src.blink_led import blink
>
> blink()
> ```

> ✅
> ```py
> # src/blink_led.py
> from time import sleep_ms
> from machine import Pin
>
> def blink():
>     led_builtin = Pin(25, Pin.OUT)
>     led_builtin.value(1)
>     interval = 1000
>
>     while True:
>         led_builtin.toggle()
>         sleep_ms(interval)
>
> # test/main.py
> from src.blink_led import blink
>
> if __name__ == "__main__":
>     blink()
> ```

> 💡 Note que com essa alteração, agora é possível parametrizar o pino do led e intervalo, deixando o código mais genérico e personalizável.
> ```py
> # src/blink_led.py
> from time import sleep_ms
> from machine import Pin
>
> def blink(*, led_pin=25, interval=1000):
>     led = Pin(led_pin, Pin.OUT)
>     led.value(1)
>
>     while True:
>         led.toggle()
>         sleep_ms(interval)
> ```

---

### Identação
Tome cuidado para identar o código com **4 espaços**.

> ❌ Exemplo: 3 espaços
> ```py
> def test():
>    return 42
> ```

> ✅
> ```py
> def test():
>     return 42
> ```

---

### Parâmetros nomeados
Quando uma classe ou função tem objetivo de comunicar com o usuário final, dê preferência a receber e passar parâmetros pelo nome, em vez de pela ordem de passagem de parâmetros, principalmente quando há muitos parâmetros.

Essa recomendação propõe que os nomes dos parâmetros sejam expostos ao usuário da classe ou função, assim, facilitando a leitura dos parâmetros sem a necessidade de abrir o código e analisar a ordem dos parâmetros.

> ❌
> ```py
> class Example:
>     # Inicialização da classe Example
>     # recebe os pinos utilizados para o SPI
>     def __init__(self, clk_pin, sdi_tx_pin, sdo_rx_pin, cs_pin, spi_id):
>         pass
>
> # ...
>
> ex = Example(10, 11, 12, 13, 1)
> ```

> ✅
> ```py
> class Example:
>     # Inicialização da classe Example
>     # recebe os pinos utilizados para o SPI
>     def __init__(self, *, clk_pin, sdi_tx_pin, sdo_rx_pin, cs_pin, spi_id):
>         pass
>
> # ...
>
> ex = Example(clk_pin=10, sdi_tx_pin=11, sdo_rx_pin=12, cs_pin=13, spi_id=1)
> ```

> 💡 Note que basta colocar `*` na posição a partir da qual deseja-se que os parâmetros seguintes sejam passados pelo nome, não por ordem

> 💡 Não é sempre necessário utilizar parâmetros nomeados, por exemplo, quando há poucos parâmetros e os valores são auto-descritivos
> ```py
> # src/max31865.py
> class MAX31865:
>     def __init__(self, spi_bus):
>         self.spi_bus = spi_bus
>
> # test/main.py
> from src.max31865 import MAX31865
> from util.bus import SPI
>
> def main():
>     sensors = {
>         "t1": MAX31865(SPI(port=1))
>     }
>
>     # ...
>
> if __name__ == "__main__":
>     main()
> ```

---

### Parâmetros de inicialização de classes
Valores padrão podem ser utilizados para parâmetros que definam comportamentos do módulo/função. Porém, não utilize valores padrão quando se refere ao hardware (por exemplo, um pino).

Essa recomendação facilita no momento de integração de códigos e resolução de conflito de pinagem.

> ❌
> ```py
> class Example:
>     # Inicialização da classe Example
>     # recebe os pinos utilizados para o SPI
>     def __init__(self, *, clk_pin=10, sdi_tx_pin=11, sdo_rx_pin=12, cs_pin=13, spi_id=1):
>         pass
> ```

> ✅
> ```py
> class Example:
>     # Inicialização da classe Example
>     # recebe os pinos utilizados para o SPI
>     def __init__(self, *, clk_pin, sdi_tx_pin, sdo_rx_pin, cs_pin, spi_id):
>         pass
> ```

> ✅
> ```py
> # interval: intervalo de envio de dados (em segundos)
> def send(interval=10):
>     pass
> ```
