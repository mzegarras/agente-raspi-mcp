import RPi.GPIO as GPIO
import time

class ServoController:
    def __init__(self):
        self.servo_pin = 14
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin,GPIO.OUT)

        # 50 Hz or 20 ms PWM period
        self.pwm = GPIO.PWM(self.servo_pin,50)
    
    def start(self):
        print("Starting at zero...")
        self.pwm.start(7.5) 

    def open(self):
        self.pwm.ChangeDutyCycle(10) 
        print("abierto")
    
    def close(self):
        self.pwm.ChangeDutyCycle(7.5) 
        print("cerrado")