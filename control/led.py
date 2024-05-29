import time
import rpi_ws281x as ws

# LED strip configuration:
LED_COUNT      = 8
LED_PIN        = 18     # PWM GPIO pin
LED_FREQ_HZ    = 800000 
LED_DMA        = 10     # DMA channel
LED_BRIGHTNESS = 255
LED_INVERT     = False
LED_CHANNEL    = 0

class LED:
    def __init__(self):
        self.ps = ws.PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.ps.begin()

    def block_colour(self, colour):
        for i in range(self.ps.numPixels()):
            self.ps.setPixelColor(i, colour)
            self.ps.show()
    
    def turn_off(self):
        colour = ws.Color(0,0,0)
        self.block_colour(colour)

    def rainbow(self, wait=0.2, repeat=2):
        for i in range(repeat):
            for j in range(256):
                for k in range(self.ps.numPixels()):
                    self.ps.setPixelColor(k, colour_wheel(j & 255))
                    self.ps.show()
            time.sleep(wait)

    def rainbow_chase(self, wait=0.1, repeat=2):
        for i in range(repeat):
            for j in range(256):
                for k in range(self.ps.numPixels()):
                    self.ps.setPixelColor(k, colour_wheel((int(k * 256 / self.ps.numPixels()) + j) & 255))
                    self.ps.show()
            time.sleep(wait)
    
def colour_wheel(pos, m=255):
    if pos < m//3:
        r=pos * 3
        g=255 - pos * 3
        b=0
    elif pos < 2*m//3:
        pos -= m//3
        r=255 - pos * 3
        g=0
        b=pos * 3
    else:
        pos -= 2*m//3
        r=0
        g=pos * 3
        b=255 - pos * 3
    return ws.Color(r,g,b)

if __name__ == '__main__':
    try:
        led = LED()
        while True:
            led.rainbow_chase()
    except KeyboardInterrupt:
        led.turn_off()