import paho.mqtt.client as mqtt
from lib import maestro 

MQTT_TURNOUTS_TOPIC="trains/track/turnouts/#"

SERVO_ACC=1
SERVO_POS_CLOSED=6000
SERVO_POS_OPENED=0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TURNOUTS_TOPIC)


# The callback for when a turnout message is received
def on_turnout_message(client, userdata, msg):
    try:
        toid = int( msg.topic[len(MQTT_TURNOUTS_TOPIC)-1::] )
        print("turnout id : "+str(toid))
        if (msg.topic=="OPEN"):
            servo.setAccel(toid, SERVO_ACC)
            servo.setTarget(toid,SERVO_POS_OPENED)
        elif  (msg.topic=="CLOSE"):
            servo.setAccel(toid, SERVO_ACC)
            servo.setTarget(toid,SERVO_POS_CLOSED)
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