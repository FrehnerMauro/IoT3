import time
import threading
import board
import busio
import adafruit_sgp30
import csv
from datetime import datetime

class CO2Sensor:
    def __init__(self, csv_dateiname="sgp30_messwerte.csv"):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(self.i2c)
        self.sgp30.iaq_init()
        #self.sgp30.set_iaq_baseline(0x8973, 0x8aae)
        self.csv_dateiname = csv_dateiname
        self.eco2 = 400
        self.tvoc = 0
        threading.Thread(target=self._run, daemon=True).start()

        with open(self.csv_dateiname, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Zeit", "eCO2 (ppm)", "TVOC (ppb)"])

    def _run(self):
        while True:
            self.eco2 = self.sgp30.eCO2
            self.tvoc = self.sgp30.TVOC
            zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"{zeit}  eCO2: {self.eco2} ppm | TVOC: {self.tvoc} ppb")

            with open(self.csv_dateiname, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([zeit, self.eco2, self.tvoc])

            time.sleep(2)

    def get_werte(self):
        return self.eco2, self.tvoc

