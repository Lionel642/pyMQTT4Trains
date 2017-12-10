
# pip install paho-mqtt pySerial
# pip install sqlalchemy

import paho.mqtt.client as mqtt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib import maestro as Mastreo
from inc import turnout
from inc import servocfg
from inc import DB

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT bus with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(turnout.MQTT_TOPIC)
    client.subscribe(servocfg.MQTT_TOPIC)

# init DB
Engine = create_engine('sqlite:///pyMQTT4Trains.db')
Session = sessionmaker(bind=Engine)

# init maestro(s)
maestros = {}
session = Session()
for m in session.query(DB.Controler):
    maestros[m.id] = Mastreo.Controller( m.tty, m.device )
    print("Openning servo connection...")
    for i in range(0,12):
        print("Servo "+str(i))
        min = maestros[m.id].getMin(i)
        max = maestros[m.id].getMax(i)
        print("    limits "+str(min)+" - "+str(max))
        pos = maestros[m.id].getPosition(i)
        print("    position "+str(pos))

turnout.session = session
turnout.maestros = maestros

# init mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add( turnout.MQTT_TOPIC, turnout.on_message )
client.message_callback_add( servocfg.MQTT_TOPIC, servocfg.on_message )
client.connect("leontu.local", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

print("Closing connections...")
for m in mastreos:
    m.close
