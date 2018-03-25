
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

min = maestro.getMin(args.s)
max = maestro.getMax(args.s)
print("Servo limits "+str(min)+" - "+str(max))

pos = maestro.getPosition(args.s)
print("Curent position "+str(pos))

print("Setting acceleration to "+str(args.a))
maestro.setAccel(args.s, args.a)

print("Setting position to "+str(args.p))
maestro.setTarget(args.s, args.p)

pos = maestro.getPosition(args.s)
print("New position "+str(pos))
