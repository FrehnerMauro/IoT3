# receiver.py
import paho.mqtt.client as mqtt
import ssl

# MQTT-Verbindungseinstellungen
broker = "b95ae3566650443f800f5a51749015d6.s1.eu.hivemq.cloud"
port = 8883
username = "testing"
password = "Mf12345678"
topic = "test"

# Callback wenn verbunden
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Verbunden mit HiveMQ Cloud")
        client.subscribe(topic)
        print(f"📡 Warte auf Nachrichten auf Topic '{topic}' ...")
    else:
        print(f"❌ Verbindung fehlgeschlagen. Fehlercode: {rc}")

# Callback wenn Nachricht empfangen wird
def on_message(client, userdata, msg):
    print(f"📥 Nachricht empfangen: {msg.payload.decode()} (Topic: {msg.topic})")

# MQTT-Client einrichten
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message

# Verbindung herstellen und Nachrichten empfangen
client.connect(broker, port)
client.loop_forever()