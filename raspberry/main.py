from door_buttons import PersonenZaehler
from SGP30_csv import CO2Sensor
from window_servo import FensterSteuerung
from sender import sende_nachricht
import time

class iot3:
    def __init__(self, co2_current=None, abs_persons=None, mode="auto", state_windows="close", permission_windows=False, airing_quality="good", airing_now=False):
        self.co2_current = co2_current
        self.abs_persons = abs_persons
        self.mode = mode
        self.state_windows = state_windows
        self.permission_windows = permission_windows
        self.airing_quality = airing_quality
        self.airing_now = airing_now




if __name__ == "__main__":
    try:
        zaehler = PersonenZaehler()
        sensor = CO2Sensor()
        fenster = FensterSteuerung()

        while True:
            iot3.abs_persons = zaehler.get_personen()
            iot3.co2_current, tvoc = sensor.get_werte()
            
            sende_nachricht("abs_persons", str(iot3.abs_persons))
            sende_nachricht("co2_current", str(iot3.co2_current))

            if iot3.mode == "auto":
                fenster.steuern(iot3.co2_current)
                
        
            elif iot3.mode == "manual":
                if iot3.airing_now:
                    fenster.oeffnen()                         
                else:
                    fenster.schliessen()
                        
            time.sleep(20)

    except KeyboardInterrupt:
        print("Beende Hauptprogramm...")
        #zaehler.stop()
        #fenster.stop()



