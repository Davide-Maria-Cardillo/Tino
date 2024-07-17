import serial
from datetime import datetime
import multiprocessing
from evdev import InputDevice, categorize, ecodes
import time

SERIAL_RATE = 0.5
TOT_MSG = 2
serial_base_port = "/dev/ttyUSB0_BASE"
ser_base = serial.Serial(serial_base_port, 115200, timeout=1)

time.sleep(2)  # Attendi che la connessione seriale si stabilisca

gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Logitech_Cordless_RumblePad_2-event-joystick')

_manager = multiprocessing.Manager()
_gamepadState = _manager.dict()

def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

def serial_writer(_gamepadState, write_queue):
    print("serial_writer started")
    prev_time = datetime.now()
    while True:
        if (datetime.now() - prev_time).total_seconds() < SERIAL_RATE:
            continue
        else:
            # send_base_str = ( "BF:%.2f"%_gamepadState["BF"] + "_BS:%.2f"%_gamepadState["BS"] + "_BB:%.2f"%_gamepadState["BB"])
            send_base_str = ( "BF:%.2f"%_gamepadState["BF"] + "_BB:%.2f"%_gamepadState["BB"])
            write_queue.put(send_base_str)
            prev_time = datetime.now()

def serial_reader(read_queue):
    print("serial_reader started")
    while True:
        if ser_base.in_waiting > 0:
            line = ser_base.readline().decode('utf-8').rstrip()
            read_queue.put(line)
            # time.sleep(0.3)  # Aggiungi un ritardo di 1 secondi


def serial_comm(write_queue, read_queue):
    print("serial_comm started")
    while True:
        if not write_queue.empty():
            send_base_str = write_queue.get()
            for _ in range(TOT_MSG):
                ser_base.write((send_base_str + "\n").encode('utf-8'))

        if not read_queue.empty():
            line = read_queue.get()
            print("[ARDUINO]" + line)
            # time.sleep(0.3)  # Aggiungi un ritardo di 1 secondi

class Controller:
    def loop(self):
        write_queue = multiprocessing.Queue()
        read_queue = multiprocessing.Queue()

        serial_writer_process = multiprocessing.Process(target=serial_writer, args=(_gamepadState, write_queue))
        serial_reader_process = multiprocessing.Process(target=serial_reader, args=(read_queue,))
        serial_comm_process = multiprocessing.Process(target=serial_comm, args=(write_queue, read_queue))

        serial_writer_process.start()
        serial_reader_process.start()
        serial_comm_process.start()

        gamepad.grab()

        _gamepadState["BF"] = 0
        # _gamepadState["BS"] = 0
        _gamepadState["BB"] = 0

        for event in gamepad.read_loop():
            if event.code == 0 and event.type == 0:
                pass
            else:
                print("--------------" + " | code:" + str(event.code) + " | type:" + str(event.type) + " | value:" + str(event.value))
                eventName = 0
                if event.code == 2:
                    eventName = "BB"
                elif event.code == 5:
                    eventName = "BF"
                # elif event.code == 0 and event.type == 3:
                #     eventName = "BS"
                
                #BF forward moovement
                if event.code == 5:
                    if event.value <= 130 and event.value >= 120:
                        new_val = 0
                    else:
                        if event.value > 130:
                            new_val = mapRange(event.value, 130, 255, 0, -10)
                        else:
                            new_val = mapRange(event.value, 0, 120, 10, 0)
                    _gamepadState[eventName if eventName else event.code] = new_val
                #BB turning in place moovement
                if event.code == 2:
                    if event.value <= 140 and event.value >= 110:
                        new_val = 0
                    else:
                        if event.value > 140:
                            new_val = mapRange(event.value, 140, 255, 0, 15)
                        else:
                            new_val = mapRange(event.value, 0, 110, -15, 0)
                    _gamepadState[eventName if eventName else event.code] = new_val
                # #BS lateral moovement
                # if event.code == 0 and event.type == 3:
                #     if event.value <= 130 and event.value >= 120:
                #         new_val = 0
                #     else:
                #         if event.value > 130:
                #             new_val = mapRange(event.value, 130, 255, 0, -10)
                #         else:
                #             new_val = mapRange(event.value, 0, 120, 10, 0)
                #     _gamepadState[eventName if eventName else event.code] = new_val

