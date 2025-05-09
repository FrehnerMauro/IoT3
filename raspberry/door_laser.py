import RPi.GPIO as GPIO
import time
import threading

class PersonenZaehlerLaser:
    def __init__(self, laser_1=17, laser_2=27):
        self.laser_1 = laser_1
        self.laser_2 = laser_2
        self.personen_im_raum = 0
        self.running = True

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.laser_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.laser_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Start Hintergrund-Thread
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while self.running:
            # Checke zuerst Laser 1 (Person kommt rein)
            if GPIO.input(self.laser_1) == GPIO.HIGH:
                start_time = time.time()
                while time.time() - start_time < 2:
                    if GPIO.input(self.laser_2) == GPIO.HIGH:
                        self.personen_im_raum += 1
                        print(f"Person reingekommen! Personen im Raum: {self.personen_im_raum}")
                        time.sleep(0.5)
                        break
                time.sleep(0.1)

            # Checke Laser 2 (Person geht raus)
            if GPIO.input(self.laser_2) == GPIO.HIGH:
                start_time = time.time()
                while time.time() - start_time < 2:
                    if GPIO.input(self.laser_1) == GPIO.HIGH:
                        if self.personen_im_raum > 0:
                            self.personen_im_raum -= 1
                        print(f"Person rausgegangen! Personen im Raum: {self.personen_im_raum}")
                        time.sleep(0.5)
                        break
                time.sleep(0.1)

    def get_personen(self):
        return self.personen_im_raum

    def stop(self):
        self.running = False
        GPIO.cleanup()

