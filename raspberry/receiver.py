import paho.mqtt.client as mqtt
import ssl
import json
from main import iot3  

broker = "b95ae3566650443f800f5a51749015d6.s1.eu.hivemq.cloud"
port = 8883
username = "testing2"
password = "Mf12345678"
topics = ["abs_persons", "co2_current", "mode", "state_windows", "permission_windows", "airing_now", "airing_quality"]



# Objekt der iot3-Klasse
iot_state = iot3()

# Dictionary für generischen Zugriff
variablen = {}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbindung hergestellt")
        for t in topics:
            client.subscribe(t)
            print(f"Abonniert: {t}")
    else:
        print(f"Verbindung fehlgeschlagen. Fehlercode: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()

        try:
            wert = json.loads(payload)
        except:
            try:
                wert = eval(payload)
            except:
                wert = payload

        topic = msg.topic.lower()
        variablen[topic] = wert

        # Automatische Zuordnung, wenn Attribut in Klasse existiert
        if hasattr(iot_state, topic):
            setattr(iot_state, topic, wert)
            print(f"{topic} = {wert} ({type(wert).__name__}) → in iot_state aktualisiert")
        else:
            print(f"{topic} = {wert} ({type(wert).__name__}) → kein Attribut in iot_state")

    except Exception as e:
        print(f"Fehler bei Nachricht: {e}")

def get_variable(topic):
    return variablen.get(topic, None)

client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
client.loop_forever()