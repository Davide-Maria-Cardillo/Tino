
#import inputs
import serial
from datetime import datetime
import multiprocessing
# import classes.serial_channel as serial_channel

# -----------------------------------------
from evdev import InputDevice, categorize, ecodes

SERIAL_RATE = 0.5
TOT_MSG = 2
serial_base_port = "/dev/ttyUSB_LEG"
ser_base = serial.Serial(serial_base_port, 115200)

gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Logitech_Cordless_RumblePad_2-event-joystick')

_gamepadState = dict()
_manager = multiprocessing.Manager()
_gamepadState = _manager.dict()
# read_serial=serial_channel.SerialChannel(serial_base_port)


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
            send_base_str = ( "BF:%.2f"%_gamepadState["BF"] + "_BS:%.2f"%_gamepadState["BS"] + "_BB:%.2f"%_gamepadState["BB"])
                
            print(send_base_str)
            # print(read_serial.read_serial_blocking())
            print("[ARDUIRNOOOOO]" + ser_base.readline().decode('utf-8').rstrip())
            i=0
            while i < TOT_MSG:
                ser_base.write((send_base_str+"\n").encode('utf-8'))
                i+=1
            i=0
            prev_time = datetime.now()



class Controller(object):
    # def __init__(self):
    #     self
                   
    def loop(self):

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
                
                if(event.code == 2):
                    eventName = "BB"
                elif(event.code == 5):
                    eventName = "BF"
                elif(event.code == 0 and event.type == 3):
                    eventName = "BS"
                
                
                print(_gamepadState)
            
            if(event.code == 5):
                    if(event.value <= 130 and event.value>=120):
                        new_val = 0
                    else:
                        if(event.value>130):
                            new_val = mapRange(event.value, 130, 255, 0, -1)
                        else:
                            new_val = mapRange(event.value, 0, 120, 1, 0)

                    _gamepadState[eventName if eventName else event.code] = new_val

            if(event.code == 2):
                    if(event.value <= 140 and event.value>=110):
                        new_val = 0
                    else:
                        if(event.value>140):
                            new_val = mapRange(event.value, 140, 255, 0, 0.1)
                        else:
                            new_val = mapRange(event.value, 0, 110, -0.1, 0)
                    _gamepadState[eventName if eventName else event.code] = new_val

            if(event.code == 0 and event.type == 3):
                    if(event.value <= 160 and event.value>=100):
                        new_val = 0
                    else:
                        if(event.value>160):
                            new_val = mapRange(event.value, 160, 255, -0.5, -0.7)
                        else:
                            new_val = mapRange(event.value, 0, 100, 0.7, 0.5)
                    _gamepadState[eventName if eventName else event.code] = new_val

