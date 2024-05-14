
#import inputs
from datetime import datetime, timedelta
from configs.robots.robots import base
import multiprocessing
import random

from evdev import InputDevice #, categorize, ecodes


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


def main():
    # Inizializza un oggetto gamepad per gestire l'input dal gamepad
    
    gamepad.grab()

    # Loop infinito per leggere gli eventi del gamepad
    for event in gamepad.read_loop():
        # Se l'evento è un evento di input valido
        if event.type == ecodes.EV_KEY:
            # Categorizza e ottiene il nome del tasto premuto
            key_event = categorize(event)
            key_name = key_event.keycode

            # Stampa il nome del tasto premuto
            print("Tasto premuto:", key_name)


 
