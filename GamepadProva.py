import serial
from datetime import datetime, timedelta
from classes.serial_channel import SerialChannel
from configs.robots.robots import base
from utils.constants import serial_default_port, default_rasp_port, serial_base_port
import multiprocessing
from evdev import InputDevice, categorize, ecodes

SERIAL_RATE = 0.5
TOT_MSG = 5
ser_base = serial.Serial('/dev/ttyUSB0_BASE', 115200)

gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Logitech_Cordless_RumblePad_2-event-joystick')
robot = base.base

_gamepadState = dict()
_manager = multiprocessing.Manager()
_gamepadState = _manager.dict()

def serial_writer(_gamepadState):
    print("serial_started")
    prev_time = datetime.now()
    while True:
        if (datetime.now() - prev_time).total_seconds() < SERIAL_RATE:
            continue
        else:
            send_base_str = ( "BF:%.2f"%_gamepadState["BF"] + "_BB:%.2f"%_gamepadState["BB"]) 
            print(send_base_str)
            i=0
            while i < TOT_MSG:
                ser_base.write((send_base_str+"\n").encode('utf-8'))
                i+=1
            i=0
            prev_time = datetime.now()
            
def main():
    
    #parallel thread to send on serial
    serial_writer_sync = multiprocessing.Process(target=serial_writer, args=(_gamepadState,))
    serial_writer_sync.start()
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

      
if __name__ == "__main__":
    main()