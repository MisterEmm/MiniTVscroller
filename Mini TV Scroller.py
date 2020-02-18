#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
import time
from sys import exit
import numpy
from matrix11x7 import Matrix11x7

from Adafruit_IO import Client, Feed, RequestError

ADAFRUIT_IO_KEY = 'Your_Adafruit_Key'
ADAFRUIT_IO_USERNAME = 'Your_Adafruit_Username'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
incoming = aio.feeds('Your_Adafruit_Feed_Name')

prev_read = "sausages"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

matrix11x7 = Matrix11x7()
matrix11x7.clear()
matrix11x7.set_brightness(0.5)

matrix = numpy.zeros((7, 11), dtype=numpy.int)

matrix[0] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
matrix[1] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
matrix[2] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
matrix[3] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
matrix[4] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
matrix[5] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
matrix[6] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

matrix1 = numpy.zeros((7, 11), dtype=numpy.int)

matrix1[0] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
matrix1[1] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
matrix1[2] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
matrix1[3] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
matrix1[4] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
matrix1[5] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
matrix1[6] = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

def buzz():

    GPIO.output(16,True)
    sleep(0.4)
    GPIO.output(16,False)
    sleep(0.1)
    GPIO.output(16,True)
    sleep(0.4)
    GPIO.output(16,False)

def scroll_message(message):
    matrix11x7.clear()                         # Clear the display and reset scrolling to (0, 0)
    length = matrix11x7.write_string(message)  # Write out your message
    matrix11x7.show()                          # Show the result
    time.sleep(0.5)                              # Initial delay before scrolling

    length -= matrix11x7.width

    # Now for the scrolling loop...
    while length > 0:
        matrix11x7.scroll(1)                   # Scroll the buffer one place to the left
        matrix11x7.show()                      # Show the result
        length -= 1
        time.sleep(0.02)                         # Delay for each scrolling step

    time.sleep(0.5)                              # Delay at the end of scrolling
    matrix11x7.clear() 

def snow():

    matrix11x7.clear() 
    count = 0
    while (count < 10):

        for y in range(0, 7): 
            for x in range(0, 11):
                matrix11x7.pixel(x, y, matrix[y, x])

        matrix11x7.show()
        time.sleep(1)

        for y in range(0, 7): 
            for x in range(0, 11):
                matrix11x7.pixel(x, y, matrix1[y, x])


        matrix11x7.show()
        time.sleep(1)
        count = count +1
        matrix11x7.clear() 

buzz()
scroll_message(" Old Tech, New Spec    ")

while True:
    
    incoming_read = aio.receive(incoming.key)
    if incoming_read.value != prev_read:
        print(incoming_read.value)
        buzz()
        scroll_message(incoming_read.value)
        prev_read = incoming_read.value
        time.sleep(1)
    else:
        print("the same")
        snow()    
    


