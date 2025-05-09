import RPi.GPIO as GPIO
import threading
import time

class PersonenZaehler:
    def __init__(self, taster_plus=23, taster_minus=24):
        self.taster_plus = taster_plus
        self.taster_minus = taster_minus
        self.personen_im_raum = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.taster_plus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.taster_minus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while self.running:
            if GPIO.input(self.taster_plus) == GPIO.LOW:
                self.personen_im_raum += 1
                print(f"+1 Personen im Raum: {self.personen_im_raum}")
                time.sleep(0.3)

            if GPIO.input(self.taster_minus) == GPIO.LOW:
                if self.personen_im_raum > 0:
                    self.personen_im_raum -= 1
                    print(f"-1 Personen im Raum: {self.personen_im_raum}")
                else:
                    print("Niemand im Raum kann nicht weniger als 0 zählen.")
                time.sleep(0.3)

    def get_personen(self):
        return self.personen_im_raum

    def stop(self):
        self.running = False
        GPIO.cleanup()

