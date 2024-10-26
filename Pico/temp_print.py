
import machine
import time
import os

adcpin = 4
sensor = machine.ADC(adcpin)
pin = machine.Pin("LED", machine.Pin.OUT)
  
def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    # C
    temperature = 27 - (volt - 0.706)/0.001721
    # F
    temperature = (temperature * (9/5) )+ 32 
    # -20 for real temp estimate
    temperature-=20
    return round(temperature, 1)

def WriteTemperature(t):
    with open("temp.log","a") as l:
        l.write(str(t))
        l.write("\n")

WriteTemperature("boot")


while True:
    pin.toggle()
    temperature = ReadTemperature()
    print(temperature)
    WriteTemperature(temperature)
    time.sleep(1)

