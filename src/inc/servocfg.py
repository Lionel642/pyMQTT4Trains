MQTT_TOPIC="/trains/servo/" # setpos/id setacc/id setclosed/id setthrown/id

# The callback for when a servo message is received
def on_message(client, userdata, msg):
    try:
        toid = int( msg.topic[len(MQTT_TURNOUTS_TOPIC)-1::] )
        print("turnout id : "+str(toid))
        todo = msg.payload.decode('utf-8')
        if (todo=="THROWN"):
            servo.setAccel(toid, SERVO_ACC)
            servo.setTarget(toid,SERVO_POS_THROWN)
            print("  ...throwing")
        elif  (todo=="CLOSED"):
            servo.setAccel(toid, SERVO_ACC)
            servo.setTarget(toid,SERVO_POS_CLOSED)
            print("  ...closing")
        else:
            raise Exception('Invalid turnout command')
    except:
        print("Invalid turnout command :")
        print("  topic :"+ str(msg.topic))
        print("  msg :"+ str(todo) +"(" +str(msg.payload) +")")
        return
