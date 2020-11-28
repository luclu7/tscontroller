import serial
import io
import raildriver
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("comport", help="selects which COM port to use to speak to the Arduino")
args = parser.parse_args()

rd = raildriver.RailDriver()
rd.set_rail_driver_connected(True)  # start data exchange
loco_name = rd.get_loco_name()

if loco_name is None:
    print("Can't find any loco")
    os._exit(1)

ser = serial.serial_for_url(args.comport, timeout=1, baudrate=115200)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

sio.flush()  # it is buffering. required to get the data out *now*
while True:
    text = sio.readline()
    text = text.rstrip()
    args = text.split(",")
    print(args)

    try:
        rd.set_controller_value("Regulator", float(args[0]))
        rd.set_controller_value('Reverser', float(args[1]))
    except ValueError:
        print(args)
    except IndexError:
        print(args)
