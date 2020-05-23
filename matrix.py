
from luma.core.interface.serial import spi, noop
import time

def demo():
    DISPLAYTEST = 0x0F
    SHUTDOWN = 0x0C
    INTENSITY = 0x0A
    DECODEMODE = 0x09
    SCANLIMIT = 0x0B

    # Create an spi instance
    serial = spi(port=0, device=0, gpio=noop()) 
    # Change the brightness
    serial.data([INTENSITY, 0x70 >> 4] * 64)
    # Not sure what this does
    serial.data([SCANLIMIT, 7] * 32)
    # Select how the data will be decoded
    serial.data([DECODEMODE, 0] * 64)
    # hide each light
    serial.data([SHUTDOWN, 0] * 64)

    time.sleep(1)
    serial.data([0x01, 0b11111111])
    serial.data([0x02, 0b00000111])
    # serial.data([0x03, 0b00000001])
    # serial.data([0x04, 0b10000000])
    # serial.data([0x05, 0b10000000])
    # serial.data([0x06, 0b10000000])
    # serial.data([0x07, 0b00000001])
    # serial.data([0x08, 0b11100000])
    # show each light
    time.sleep(1)
    serial.data([SHUTDOWN, 1] * 64)


demo()
