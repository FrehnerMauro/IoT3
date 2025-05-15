import paho.mqtt.client as mqtt
import ssl

broker = "b95ae3566650443f800f5a51749015d6.s1.eu.hivemq.cloud"
port = 8883
username = "testing"
password = "Mf12345678"

client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.connect(broker, port)
client.loop_start()

def sende_nachricht(topic: str, nachricht: str):
    result = client.publish(topic, nachricht)
    if result.rc == 0:
        print(f"Nachricht gesendet: {nachricht} -> {topic}")
    else:
        print(f"Fehler beim Senden an Topic {topic}")