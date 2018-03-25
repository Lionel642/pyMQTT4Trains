import traceback
from . import DB

MQTT_TOPIC="/trains/track/turnout/#"

# The callback for when a turnout message is received
def on_message(client, userdata, msg):
    try:
        toid = int( msg.topic[len(MQTT_TOPIC)-1::] )
        servo = session.query(DB.Servo).filter( DB.Servo.id == toid ).first()
        if (servo == None):
            raise Exception('No such turnout in DB: '+str(toid)+', topic : '+ str(msg.topic))
        todo = msg.payload.decode('utf-8')
        if (todo == "THROWN"):
            maestros[servo.controler_id].setAccel(servo.address, servo.accel)
            maestros[servo.controler_id].setTarget(servo.address, servo.posThrown)
            print("  ...throwing "+str(toid))
        elif (todo == "CLOSED"):
            maestros[servo.controler_id].setAccel(servo.address, servo.accel)
            maestros[servo.controler_id].setTarget(servo.address, servo.posClosed)
            print("  ...closing "+str(toid))
        else:
            raise Exception('Invalid turnout command, topic : '+ str(msg.topic)+', msg : '+ str(todo) +'(' +str(msg.payload) +')')
    except Exception as ex:
        print(ex)
