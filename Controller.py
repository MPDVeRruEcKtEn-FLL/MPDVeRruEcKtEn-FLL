# LEGO slot:0

import hub # type: ignore
import motor  # type: ignore
import time


from DriveBase import DriveBase
from Logger import Logger

"""

Our Personal Main Code

Here you can also find our specific exercises and also some examples.

Those are the ports we used for the specific tasks:
MotorPorts:
    A = 0: MotorRight
    B = 1: Unused
    C = 2: Unused
    D = 3: Addition
    E = 4: MotorLeft
    F = 5: AbilityRight

"""
print()
print("-" * 50)
print()

class Controller:
    def __init__(self):
        self._kill_ = False

        self.driveBase = DriveBase()

        Logger.info("Started Program", code = 0)

    #############
    # Internals #
    #############

    def __button_check__(self, button: int) -> bool:
        """"""
        if button == 0:
            return bool(
                hub.button.pressed(hub.button.LEFT)
                or hub.button.pressed(hub.button.RIGHT)
            )
        elif button == 1:
            return bool(hub.button.pressed(hub.button.LEFT))
        elif button == 2:
            return bool(hub.button.pressed(hub.button.RIGHT))
        else:
            Logger.exception(message = "UNKNOWN WHICH BUTTON", code = 303)
            return False

    def __connect_addition__(self):
        self.driveBase.attach_addition(False)
        Logger.info("WAITING", code = "START")
        while not self.__button_check__(0):
            pass
        self.driveBase.attach_addition(True)
        time.sleep(0.5)

    ##################
    # MAIN FUNCTIONS #
    ##################

    def kill(self):
        Logger.info("Killed program", code = -1)
        self._kill_ = True

    ###############
    # RUN PROGRAM #
    ###############

    def run_program(self, dive: int = 0):
        if dive == 0 or dive == 1:
            # Put here programs
            pass

        if dive not in range(1):
            Logger.exception(99, "Unknown Dive Number: {}".format(dive))

    ########################
    # Tasks for Robot Game #
    ########################

    ###

    ###########
    # TESTING #
    ###########
    
    
    def drive_forward(self):
        self.driveBase.turn_to_angle(90, maxspeed=1110, minspeed=800)
        # self.driveBase.drive_distance(10, 900, 800)
    ###


ctrl = Controller()

ctrl.driveBase.configure_pid(1, 1, 1)


def main():
    ctrl.drive_forward()
    ctrl.kill()


# Start the main async function
if __name__ == "__main__":
    main()
    raise Exception("Program Ended")
