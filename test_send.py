
import paho.mqtt.client as mqtt
import ssl

# MQTT-Broker-Informationen
broker = "b95ae3566650443f800f5a51749015d6.s1.eu.hivemq.cloud"
port = 8883
username = "testing"
password = "Mf12345678"
topic = "test"

# Callback-Funktion bei erfolgreicher Verbindung
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Verbunden mit HiveMQ Cloud")
        client.subscribe(topic)
    else:
        print(f"❌ Verbindung fehlgeschlagen. Fehlercode: {rc}")

# Callback-Funktion bei empfangener Nachricht
def on_message(client, userdata, msg):
    print(f"📥 Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")

# MQTT-Client einrichten
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message

# Verbindung herstellen
client.connect(broker, port)
client.loop_start()

# Nachrichten senden
try:
    while True:
        message = input("🔹 Nachricht eingeben: ")
        client.publish(topic, message)
except KeyboardInterrupt:
    print("⛔ Verbindung wird beendet.")
    client.loop_stop()
    client.disconnect()

# Callback-Funktion bei erfolgreicher Verbindung
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Verbunden mit HiveMQ Cloud")
        client.subscribe(topic)
    else:
        print(f"❌ Verbindung fehlgeschlagen. Fehlercode: {rc}")

# Callback-Funktion bei empfangener Nachricht
def on_message(client, userdata, msg):
    print(f"📥 Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")

# MQTT-Client einrichten
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message

# Verbindung herstellen
client.connect(broker, port)
client.loop_start()

# Nachrichten senden
try:
    while True:
        message = input("🔹 Nachricht eingeben: ")
        client.publish(topic, message)
except KeyboardInterrupt:
    print("⛔ Verbindung wird beendet.")
    client.loop_stop()
    client.disconnect()