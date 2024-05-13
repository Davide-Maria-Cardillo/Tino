
#import inputs
import serial
from datetime import datetime, timedelta
from classes.serial_channel import SerialChannel
from configs.robots.robots import base
from utils.constants import serial_default_port, default_rasp_port, serial_base_port
import multiprocessing
import random
# Trova il joystick Logitech
#devices = inputs.devices

#devices = inputs.devices.gamepads
#print(devices)

# -----------------------------------------
from evdev import InputDevice, categorize, ecodes

SERIAL_RATE = 0.5
TOT_MSG = 5
ser_base = serial.Serial(serial_base_port, 115200)

#gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Wireless_Gamepad_F710_653595B3-event-joystick') # Cambia il percorso del dispositivo a seconda del tuo Raspberry Pi
#gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Wireless_Gamepad_F710_7B579A4E-event-joystick')
gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Wireless_Gamepad_F710_D68D96DF-event-joystick')
robot = base.base

_joystickDeadzone = 1000

#in main start this with
"""
if CONTROLLER_ENABLED:
    import Controller
    controller_process = multiprocessing.Process(target=Controller.main, args=[])
    controller_process.start()
"""

import serial
from classes.serial_channel import SerialChannel
import time

def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

def mapValue_RT_LT(val):
    new_val = (val * 100) / 200
    new_val = (new_val * 2) / 100
    new_val = new_val - 1

    return new_val

def mapValue_JOY(val):
    new_val = val + 32768
    new_val = (new_val * 100) / (32768*2)
    new_val = (new_val * 2) / 100
    new_val = new_val - 1
    

    return new_val

def format_str(val):
    return "%.2f"%val if type(val) == float else str(val)


_gamepadState = dict()
_manager = multiprocessing.Manager()
_gamepadState = _manager.dict()
val_RT = 0

def serial_writer(_gamepadState):
    print("serial_started")
    prev_time = datetime.now()
    while True:
        if (datetime.now() - prev_time).total_seconds() < SERIAL_RATE:
            continue
        else:
            #key = random between TBF: TUD: HUD:
            #key = random.choice(["TBF:", "HBF:", "HUD:"])
            #send_str = ("TBF:"+ send_str)
            #split gamestate to format "TBF:0.00_TUD:0.00_TLR:0.00_HBF:0.00_HUD:0.00_HLR:0.00_BF:0_BS:0_BA:0" with appropriate value from gamepadstate[key]
            send_base_str = ( "BF:%.2f"%_gamepadState["BF"] + "_BB:%.2f"%_gamepadState["BB"])
            
            print(send_base_str)
            i=0
            while i < TOT_MSG:
                ser_base.write((send_base_str+"\n").encode('utf-8'))
                i+=1
            i=0
            prev_time = datetime.now()
   
def serial_writer_non_blocking():
    #key = random between TBF: TUD: HUD:
    #key = random.choice(["TBF:", "HBF:", "HUD:"])
    #send_str = ("TBF:"+ send_str)
    #split gamestate to format "TBF:0.00_TUD:0.00_TLR:0.00_HBF:0.00_HUD:0.00_HLR:0.00_BF:0_BS:0_BA:0" with appropriate value from gamepadstate[key]
    send_base_str = ( "BF:%.2f"%_gamepadState["BF"] + "_BS:%.2f"%_gamepadState["BS"] + "_BB:%.2f"%_gamepadState["BB"])
    print(send_base_str)

    ser_base.write((send_base_str+"\n").encode('utf-8'))
             
def main():

    #parallel thread to send on serial
    serial_writer_sync = multiprocessing.Process(target=serial_writer, args=(_gamepadState,))
    serial_writer_sync.start()
    #sr = SerialChannel()
    #sr.setup_serial()
    gamepad.grab()
    
    
    #init all keys to zero
    
    _gamepadState["BF"] = 0
    _gamepadState["BS"] = 0
    _gamepadState["BB"] = 0

    for event in gamepad.read_loop():
        if(event.code == 0 and event.type == 0):
            pass
        else:
            print("---------------------------------------------------------------" + " | code:" + str(event.code) + " | type:" + str(event.type) + " | value:" + str(event.value))
            eventName = 0
            #check codes from if elif below
            
            if(event.code == 16):
                eventName = "BB"
            elif(event.code == 17):
                eventName = "BF"
            #elif(event.code == 1):
                #eventName = "BS"
            
            
            print(_gamepadState)
        
        if(event.code == 17):
                new_val = event.value*(-60)
                _gamepadState[eventName if eventName else event.code] = new_val

        if(event.code == 16):
                new_val = event.value*30
                _gamepadState[eventName if eventName else event.code] = new_val

        #elif(event.code == 1):
                #new_val = mapValue_RT_LT(event.value)
                #_gamepadState[eventName if eventName else event.code] = new_val

        

               
#digital --------------------------------------------    
        

    
    
    ##sr.write_key_value_serial("BB", 0)

if __name__ == "__main__":
    main()



 
