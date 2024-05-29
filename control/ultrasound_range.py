import time
import RPi.GPIO as GPIO

trigger = 27
echo = 22
pulse_time = 0.00001
timeout = 10000
speed_sound = 34300

class Ultrasound:
    def __init__(self):
        self.trigger_pin = trigger
        self.echo_pin = echo
        GPIO.setmode(GPIO.BCM)
        # Assign trigger pin and force to low
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.output(self.trigger_pin, False)
        # Assign echo pin
        GPIO.setup(self.echo_pin,GPIO.IN)

    def _trigger_pulse(self):
        # US Ranging module requires a 10ms trigger pulse
        # which causes it to send 8 x 40kHz pulses for ranging
        GPIO.output(self.trigger_pin, True)
        time.sleep(pulse_time)
        GPIO.output(self.trigger_pin, False)

    def _echo(self, timeout):
        count = timeout
        start, echo = (time.time(), time.time())
        # The US modules sets the Echo pin to high(True) when it triggers
        # So we record the last low timestamp
        while GPIO.input(self.echo_pin) == False and count > 0:
            count -= 1
        start = time.time()
        
        count = timeout
        # When the pulse returns it sets the pin to low, so we want to 
        # record the last high time stamp
        while GPIO.input(self.echo_pin) == True and count > 0:
            count -= 1
        echo = time.time()

        return (echo - start)
    
    def calculate_distance(self):
        distance = []
        for i in range(4):
            self._trigger_pulse()
            pulse_len = self._echo(timeout)
            distance.append((pulse_len * speed_sound) / 2)

        avg_dist = sum(distance) / len(distance)
        return avg_dist
    
    def destroy(self):
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        us = Ultrasound()
        while True:
            dist = us.calculate_distance()
            time.sleep(1)
            print(f'Distance to object {dist:.0f}cm')
    except KeyboardInterrupt:
        us.destroy()