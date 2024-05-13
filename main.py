import os

from classes.control import Control

from configs.robots.dof import DofName
from configs.robots.robots import base
import multiprocessing

# ______________________________________________________________________________________________GLOBALS

# directory of the file. It's the same dicrectory of the RESTART.SH file
abs_path = os.path.dirname(os.path.abspath(__file__))
restart_file_name = "restart.sh"
path_to_restart = "./" + restart_file_name  # abs_path + "/restart.sh"

# TODO resolve controller and camera conflict, they should all run in the main thread.
# Test this by running camera alone, it will be smoother
CONTROLLER_ENABLED = 1

# ______________________________________________________________________________________________ VALUES

# STRING IPS

#VR_ip = "192.168.0.101"

# ______________________________________________________________________________________________ CREATE VIRTUAL ObJECTS

# INITIALIZE CONTROLS

# -- this variable contains the ROBOT config. Just comment out the robot you are coding for
#    and all the setup will be already implemented in it

robot = base.base
# robot_base = base.base
# robot = blackwing.blackwing

# -- this is the MAIN CLASS, the one handling all the logic
control = Control(robot, path_to_restart)


# control_base = Control(robot_base, path_to_restart)


#def add_esp_channels():
#    global control
#    # global control_base
#    from configs.esps.esp_types import ESP_VALUE_TYPE_KEYS
#    from configs.robots.dof import DofName

    
    # control.on_new_config_rcv(joystick_ip, ESP_VALUE_TYPE_KEYS.UP.value, DofName.FORWARD.value.key, True)
    # control.on_new_config_rcv(joystick_ip, ESP_VALUE_TYPE_KEYS.DOWN.value, DofName.STRAFE.value.key, True)
    # control.on_new_config_rcv(joystick_ip, ESP_VALUE_TYPE_KEYS.RIGHT.value, DofName.ANGULAR.value.key, True)


# ______________________________________________________________________________________________ MAIN


def setup():
    print("[SETUP] --------------------------------------------- BEGIN")

    # ADD REMOTE ESP CONTROLLERS TO STRING CONTROL OBJECT
#    add_esp_channels()

    # SETUP STRING CONTROL OBJECT
    control.setup()
    # control_base.setup()

    print("[SETUP] --------------------------------------------- COMPLETE\n")


def main_body():
    # main setup
    setup()
    if CONTROLLER_ENABLED:
        import classes.Controller as Controller
        controller_process = multiprocessing.Process(target=Controller.main, args=[])
        controller_process.start()

    # main loop
    print("[MAIN LOOP] --------------------------------------------- STARTING MAIN LOOP\n")
    while True:
        # execute CONTROLLERS loop
        control.loop()
        # control_base.loop()

def main():
    main_body()

    print("end")

    control.cleanup()
    # control_base.cleanup()


if __name__ == "__main__":
    main()
