from time import sleep
import pifacedigitalio
import getopt
import sys
import random
import json
from paho.mqtt import client as mqtt_client

pifacedigital = pifacedigitalio.PiFaceDigital()

#MqttBrokerIp id
#MqttBrokerIp="localhost"
MqttBrokerIp = 'b95ae3566650443f800f5a51749015d6.s1.eu.hivemq.cloud'
#MqttBrokerIp="127.0.0.1"
MqttBrokerPort=8883
# generate client ID with pub prefix randomly
CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
MqttUserName = 'testroom'
MqttPassword = 'Mf648349'
#topics
TOPIC_LED = 'hauser/led'
TOPIC_STATE = 'hauser/state'
TOPIC_RELAIS = 'hauser/relais'

client = mqtt_client.Client(CLIENT_ID)

def  usage():
    print("options:")
    print("-b MqttBrokerIp-ip: The ip of the MQTT MqttBrokerIp (default: localhost)")
    print("-h: get help")
    print("-p MqttMqttBrokerIpPort: The MqttMqttBrokerIpPort of the MQTT MqttBrokerIp (default: 1883)")

def sendmqtt(client,topic,payload):
    result = client.publish(topic, payload)
    status = result[0]
    if status == 0:
        print(f"Sent via `{topic}`: `{payload}`")
    else:
        print(f"Failed to send message to topic {topic}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected")
    else:
        print("Failed to connect, return code %d\n", rc)
        sys.exit(2)
    client.subscribe(TOPIC_LED)
    client.subscribe(TOPIC_RELAIS)
    client.subscribe(TOPIC_STATE)
    client.on_message = on_message

def on_message(client, userdata, msg):
    try:
        payloadDecoded=json.loads(msg.payload)
        print(f"Received via `{msg.topic}`: `{msg.payload.decode()}`")
        if(TOPIC_LED==msg.topic and 2==len(payloadDecoded)):
            set_led(client,payloadDecoded[0],payloadDecoded[1])
            return
        elif (TOPIC_RELAIS==msg.topic and 2==len(payloadDecoded)):
            set_led(client,payloadDecoded[0],payloadDecoded[1])
            return
        elif (TOPIC_STATE==msg.topic):
            if(1==len(payloadDecoded) and "get"==payloadDecoded[0]):
                for index in range(0,8):
                    payload = '["led",'+str(index)+','+str(pifacedigital.leds[index].value)+']'
                    sendmqtt(client,TOPIC_STATE,payload)
                for index in range(0,2):
                    payload = '["relais",'+str(index)+','+str(pifacedigital.leds[index].value)+']'
                    sendmqtt(client,TOPIC_STATE,payload)
                for index in range(0,4):
                    payload = '["switch",'+str(index)+','+str(pifacedigital.switches[index].value)+']'
                    sendmqtt(client,TOPIC_STATE,payload)
            else:
                print(f"irrelevant message via `{msg.topic}`: `{msg.payload.decode()}`")
            return
    except ValueError as e:
        print(f"invalid message via `{msg.topic}`: `{msg.payload.decode()}`, error: `{e}`")
        return
    print(f"invalid message via `{msg.topic}`: `{msg.payload.decode()}`")
    return

def connect_mqtt(MqttBrokerIp,MqttBrokerPort,MqttUserName,MqttPassword):
    print(f"Connect to `{MqttBrokerIp}`:`{MqttBrokerPort}`)")
    client.username_pw_set(MqttUserName, MqttPassword)
    client.on_connect = on_connect
    client.connect(MqttBrokerIp, MqttBrokerPort)
    return client

def eval_args():    
    argv = sys.argv[1:]
    global MqttBrokerIp
    global MqttBrokerPort
    try:
        opts, args = getopt.getopt(argv, 'b:hp:', ['help'])
    except getopt.GetoptError:
        # Print a message or do something useful
        print('Something went wrong!')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-b'):
            MqttBrokerIp = arg
        elif opt in ('-p'):
            MqttBrokerPort = arg
        else:
            usage()
            sys.exit(2)
    print("MqttBrokerIp: "+str(MqttBrokerIp)+":"+str(MqttBrokerPort))

def set_led(client,index,value):
    index=int(index)
    value=int(value)
    if((7<index) or (0>index)):
        print(f"index(`{index}`,`{value}`) out of range")
        return
    try:
        if (1==value):
            pifacedigital.leds[index].turn_on()
        else:
            pifacedigital.leds[index].turn_off()
        payload = '["led",'+str(index)+','+str(value)+']'
        sendmqtt(client,TOPIC_STATE,payload)
        if (2 > index):# index to high to trigger a relais
            payload = '["relais",'+str(index)+','+str(value)+']'
            sendmqtt(client,TOPIC_STATE,payload)
    except ValueError as e:
        print(f"illegal values(`{index}`,`{value}`), error `{e}`")

def switch_pressed(event):
    payload = '["switch",'+str(event.pin_num)+',1]'
    sendmqtt(client,TOPIC_STATE,payload)

def switch_unpressed(event):
    payload = '["switch",'+str(event.pin_num)+',0]'
    sendmqtt(client,TOPIC_STATE,payload)

def run():
    global client
    eval_args()
    client = connect_mqtt(MqttBrokerIp,MqttBrokerPort,MqttUserName,MqttPassword)
    client.loop_start()
    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    for i in range(4):
        listener.register(i, pifacedigitalio.IODIR_ON, switch_pressed)
        listener.register(i, pifacedigitalio.IODIR_OFF, switch_unpressed)
    listener.activate()

    while(True):
        sleep(0.01)

if __name__ == '__main__':
    run()
    
