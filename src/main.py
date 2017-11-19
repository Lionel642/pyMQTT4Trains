# pip install paho-mqtt pySerial
import paho.mqtt.client as mqtt
from lib import maestro

MQTT_TURNOUTS_TOPIC="/trains/track/turnout/#"

SERVO_ACC=5
SERVO_POS_CLOSED=7500
SERVO_POS_THROWN=4500

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT bus with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TURNOUTS_TOPIC)


# The callback for when a turnout message is received
def on_turnout_message(client, userdata, msg):
    try:
        toid = int( msg.topic[len(MQTT_TURNOUTS_TOPIC)-1::] )
        print("turnout id : "+str(toid))
        if (msg.payload=="THROWN"):
            servo.setAccel(toid, SERVO_ACC)
            servo.setTarget(toid,SERVO_POS_THROWN)
            print("  ...throwing")
        elif  (msg.payload=="CLOSED"):
            servo.setAccel(toid, SERVO_ACC)
            servo.setTarget(toid,SERVO_POS_CLOSED)
            print("  ...closing")
        else:
            raise Exception('Invalid turnout command')
    except:
        print("Invalid turnout command :")
        print("  topic :"+ str(msg.topic))
        print("  msg :"+ str(msg.payload))
        return









# Program

# init maestro
print("Openning servo connection...")
servo = maestro.Controller()
for i in range(0,12):
    print("Servo "+str(i))
    min = servo.getMin(i)
    max = servo.getMax(i)
    print("    limits "+str(min)+" - "+str(max))
    pos = servo.getPosition(i)
    print("    position "+str(pos))

# init mqtt
client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add(MQTT_TURNOUTS_TOPIC, on_turnout_message)
client.connect("leontu.local", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

print("Closing servo connection...")
servo.close
