
import argparse
from lib import maestro as Mastreo


parser = argparse.ArgumentParser(description='Set servo s on Maestro device d plugged in tty t to position p with acceleration a.')

parser.add_argument('-t', '--tty',       type=str, help='tty',      default='/dev/ttyACM0')
parser.add_argument('-d', '--device',        type=int, help='Maestro device id', default=12)
parser.add_argument('-s', '--servo',        type=int, help='Servo id')
parser.add_argument('-a', '--acceleration', type=int, help='Acceleration')
parser.add_argument('-p', '--position',     type=int, help='Position')

args = parser.parse_args()
print("TTY : "+args.tty)
print("Device : "+str(args.device))
print("Servo : "+str(args.servo))
print("Acceleration : "+str(args.acceleration))
print("Position : "+str(args.position))

maestro = Mastreo.Controller( args.tty, args.device )

min = maestro.getMin(args.servo)
max = maestro.getMax(args.servo)
print("Servo limits "+str(min)+" - "+str(max))

pos = maestro.getPosition(args.servo)
print("Curent position "+str(pos))

print("Setting acceleration to "+str(args.acceleration)+"...")
maestro.setAccel(args.servo, args.acceleration)

print("Setting position to "+str(args.position)+"...")
maestro.setTarget(args.servo, args.position)

pos = maestro.getPosition(args.servo)
print("New position "+str(pos))
