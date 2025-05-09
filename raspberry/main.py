from door_buttons import PersonenZaehler
from SGP30_csv import CO2Sensor
from window_servo import FensterSteuerung
import time

if __name__ == "__main__":
    try:
        zaehler = PersonenZaehler()
        sensor = CO2Sensor()
        fenster = FensterSteuerung()

        while True:
            personen = zaehler.get_personen()
            eco2, tvoc = sensor.get_werte()
            print(f"[Main] Personen: {personen} | CO2: {eco2} ppm | TVOC: {tvoc} ppb")
            fenster.steuern(eco2)
            time.sleep(2)

    except KeyboardInterrupt:
        print("Beende Hauptprogramm...")
        zaehler.stop()
        fenster.stop()



