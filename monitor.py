import urequests
import time
import array
from machine import Pin

def post_url():
    return 'http://insubstantial-squeaky-pupa.gigalixirapp.com/api/washings/sessions'

def update_url(id):
    return 'http://insubstantial-squeaky-pupa.gigalixirapp.com/api/washings/sessions/' + str(id) +'/end'

def monitor():
    active_request = False
    inactive_noticings = 0
    active_noticings = 0
    led_active = False
    pir_pin = 27
    led_pin_numbers = [12, 13, 14, 25, 26, 32]
    led_pins = map(lambda number: Pin(number, Pin.OUT), led_pin_numbers)
    success_seconds = 10
    per_second = 3

    Pin(12, Pin.OUT).off()
    for pin in led_pin_numbers:
        print("TURNING OFF %s" %pin)
        Pin(pin, Pin.OUT).off()



    while True:
        sensor_active = Pin(pir_pin, Pin.IN).value() > 0 
        # debounce activation
        if (sensor_active):
            active_noticings += 1

            seconds_active = active_noticings / per_second 
            print("Seconds Active %s" % seconds_active)
            pins_to_light = (seconds_active / success_seconds) * len(led_pin_numbers)

            if(pins_to_light <= len(led_pin_numbers)):
                for index in range(0, pins_to_light):
                    print("TURNING ON %s" % led_pin_numbers[index])
                    Pin(led_pin_numbers[index], Pin.OUT).on()

        #debounce inactivity
        if (not sensor_active and active_request and end_url):
            inactive_noticings += 1

        if active_noticings >= 3 and not active_request:
            response = urequests.post(post_url(), headers = {"content-type": "application/json", "content-length": "0"}).json()
            end_url = update_url(response['id'])
            active_request = True

        if inactive_noticings >= 2:
            response = urequests.put(end_url, headers = {"content-type": "application/json", "content-length": "0"}).json()
            active_request = False
            inactive_noticings = 0
            active_noticings = 0
            for pin in led_pin_numbers:
                print("TURNING OFF %s" %pin)
                Pin(pin, Pin.OUT).off()

        time.sleep(1 / per_second)
