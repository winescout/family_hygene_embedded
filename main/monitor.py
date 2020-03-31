import urequests
import time
import array
from machine import Pin

def post_url():
    return 'http://insubstantial-squeaky-pupa.gigalixirapp.com/api/washings/sessions'

def update_url(id):
    return 'http://insubstantial-squeaky-pupa.gigalixirapp.com/api/washings/sessions/' + str(id) +'/end'

def wash_start(pir_pin):
    led_pin_numbers = [12, 13, 14, 25, 26, 32]
    led_pins = map(lambda number: Pin(number, Pin.OUT), led_pin_numbers)
    success_seconds = 20
    seconds_active = 0

    #Make sure all the pins are off
    for pin in led_pin_numbers:
        Pin(pin, Pin.OUT).off()

    #Notify server washing event is active
    response = urequests.post(post_url(), headers = {"content-type": "application/json", "content-length": "0"}).json()
    end_url = update_url(response['id'])

    #Monitor washing event
    v = pir_pin.value()
    while v == 1:
        seconds_active += 1

        #Lite LEDs
        pins_to_light = (seconds_active / success_seconds) * len(led_pin_numbers)
        if(pins_to_light <= len(led_pin_numbers)):
            for index in range(0, pins_to_light):
                Pin(led_pin_numbers[index], Pin.OUT).on()

        #Take a rest, then grab a new value
        time.sleep(1)
        v = pir_pin.value()

    #Washing complete, notify server
    urequests.put(end_url, headers = {"content-type": "application/json", "content-length": "0"}).json()

    #Turn off LED's
    for pin in led_pin_numbers:
        Pin(pin, Pin.OUT).off()

def monitor():
    pir_pin_number = 27
    pir_pin = Pin(pir_pin_number, Pin.IN)
    pir_pin.irq(trigger=Pin.IRQ_RISING, handler=wash_start)
