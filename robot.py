"""
Main logic code
"""
import wpilib

from inits import Component
import helpers

from components.chassis import Chassis

from autonomous import Autonomous
from components.lights import Lights
from components.metabox import MetaBox
from components.winch import Winch
from components.pdb import Power

class Randy(wpilib.TimedRobot):
    def robotInit(self):
        self.C = Component() # Components inits all connected motors, sensors, and joysticks. See inits.py.

        # Setup subsystems
        self.driverStation = wpilib.DriverStation.getInstance()
        self.drive = Chassis(self.C.driveTrain, self.C.gyroS, self.C.driveYEncoderS)
        self.lights = Lights()
        self.metabox = MetaBox(self.C.elevatorEncoderS, self.C.elevatorLimitS, self.C.elevatorM, self.C.intakeM)
        self.winch = Winch(self.C.winchM)
        self.power = Power()

        self.autonomousRoutine = Autonomous(self.drive, self.driverStation)

        # Joysticks
        self.C.joystick = wpilib.XboxController(0)
        self.C.leftJ = wpilib.Joystick(1)

        # default to rainbow effect
        self.lights.run({'effect': 'rainbow'})


    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        '''Components'''
        # Drive
        self.drive.cartesian(self.C.joystick.getRawAxis(0), self.C.joystick.getRawAxis(1), self.C.joystick.getRawAxis(4))

        # MetaBox
        self.metabox.run(self.C.leftJ.getY(), self.C.leftJ.getRawButton(4), self.C.leftJ.getRawButton(5))

        # Winch
        if (self.C.leftJ.getRawButton(3)):
            self.winch.run(1)
        else:
            self.winch.run(0)

        # Lights
        self.lights.setColor(self.driverStation.getAlliance())

        if (self.driverStation.getMatchTime() < 30 and self.driverStation.getMatchTime() != -1):
            self.lights.run({'effect': 'flash', 'fade': True, 'speed': 255})
        elif (helpers.deadband(self.C.leftJ.getY(), 0.1) != 0):
            self.lights.run({'effect': 'stagger'})
        else:
            self.lights.run({'effect': 'rainbow'})

    def teleopInit(self):
        """This function is run once each time the robot enters teleop mode."""
        # reset gyro
        self.C.gyroS.reset()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.lights.run({'effect': 'flash', 'fade': True, 'speed': 400})
        self.autonomousRoutine.run() # see autonomous.py

if __name__ == "__main__":
    wpilib.run(Randy)
