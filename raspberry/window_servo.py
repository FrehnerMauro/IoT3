import RPi.GPIO as GPIO
import time

class FensterSteuerung:
    def __init__(self, servo_pin=18):
        self.servo_pin = servo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, 50)
        self.pwm.start(0)
        self.offen = False

    def set_angle(self, angle):
        duty = 2 + (angle / 18)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(0)

    def oeffnen(self):
        print("Fenster öffnen...")
        self.set_angle(150)
        self.offen = True

    def schliessen(self):
        print("Fenster schlie?^=en...")
        self.set_angle(50)
        self.offen = False

    def steuern(self, eco2):
        if eco2 > 1000 and not self.offen:
            self.oeffnen()
        elif eco2 < 800 and self.offen:
            self.schliessen()

    def stop(self):
        self.pwm.stop()
        GPIO.cleanup()


