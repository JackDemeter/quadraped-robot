# test test

from adafruit_servokit import ServoKit
from enum import IntEnum
import time
import math


class Motor(IntEnum):
    # may be useful for tuning specific motors
    FR_SHOULDER = 0
    FR_ELBOW = 1
    FR_HIP = 2
    FL_SHOULDER = 3
    FL_ELBOW = 4
    FL_HIP = 5
    BR_SHOULDER = 6
    BR_ELBOW = 7
    BL_SHOULDER = 8
    BL_ELBOW = 9

class Quadruped:
    def __init__(self):
        self.kit = ServoKit(channels=16)
        self.upper_leg_length = 10
        self.lower_leg_length = 10
        for i in range(10):
            self.kit.servo[i].set_pulse_width_range(500,2500)
        
        
    def calibrate(self):
        # set the robot into the default "middle position" use this for attaching legs in right location
        self.kit.servo[Motor.FR_SHOULDER].angle = 60
        self.kit.servo[Motor.FR_ELBOW].angle = 90
        self.kit.servo[Motor.FR_HIP].angle = 90
        self.kit.servo[Motor.FL_SHOULDER].angle = 120
        self.kit.servo[Motor.FL_ELBOW].angle = 90
        self.kit.servo[Motor.FL_HIP].angle = 90
        self.kit.servo[Motor.BR_SHOULDER].angle = 60
        self.kit.servo[Motor.BR_ELBOW].angle = 90
        self.kit.servo[Motor.BL_SHOULDER].angle = 120
        self.kit.servo[Motor.BL_ELBOW].angle = 90

    def set_shoulders(self, offset, anti=[]):
        #TODO ADD MIN MAX POSITIONS!!!
        if not Motor.FR_SHOULDER in anti:
            self.kit.servo[Motor.FR_SHOULDER].angle = self.kit.servo[Motor.FR_SHOULDER].angle - offset
        if not Motor.BR_SHOULDER in anti:
            self.kit.servo[Motor.BR_SHOULDER].angle = self.kit.servo[Motor.BR_SHOULDER].angle - offset
        if not Motor.FL_SHOULDER in anti:
            self.kit.servo[Motor.FL_SHOULDER].angle = self.kit.servo[Motor.FL_SHOULDER].angle + offset
        if not Motor.BL_SHOULDER in anti:
            self.kit.servo[Motor.BL_SHOULDER].angle = self.kit.servo[Motor.BL_SHOULDER].angle + offset

    def forward_cycle(self, num_cycles=1):
        self.calibrate()
        time.sleep(3)
        self.set_shoulders(8)
        time.sleep(2)
        for i in range(num_cycles):  
            self.set_angle(Motor.FL_ELBOW,80)
            time.sleep(0.2)
            self.set_angle(Motor.FL_SHOULDER,110)
            time.sleep(0.2)
            self.set_shoulders(10,anti=[Motor.FL_SHOULDER])
            time.sleep(0.2)
            self.set_angle(Motor.FL_ELBOW,90)
            time.sleep(0.2)
            
            # BR
            self.set_angle(Motor.BR_ELBOW,100)
            time.sleep(0.2)
            self.set_angle(Motor.BR_SHOULDER,70)
            time.sleep(0.2)
            self.set_shoulders(10,anti=[Motor.BR_SHOULDER])
            time.sleep(0.2)
            self.set_angle(Motor.BR_ELBOW,90)
            time.sleep(0.2)
                
            # FR
            self.set_angle(Motor.FR_ELBOW,100)
            time.sleep(0.2)
            self.set_angle(Motor.FR_SHOULDER,70)
            time.sleep(0.2)
            self.set_shoulders(10,anti=[Motor.FR_SHOULDER])
            time.sleep(0.2)
            self.set_angle(Motor.FR_ELBOW,90)
            time.sleep(0.2)
        
            # BL
            self.set_angle(Motor.BL_ELBOW,80)
            time.sleep(0.2)
            self.set_angle(Motor.BL_SHOULDER,1100)
            time.sleep(0.2)
            self.set_shoulders(10,anti=[Motor.BL_SHOULDER])
            time.sleep(0.2)
            self.set_angle(Motor.BL_ELBOW,90)
            time.sleep(0.2)
            

    def set_angle(self,leg_id, degrees):
        self.kit.servo[leg_id].angle = degrees

    def test_pos(self,leg_id, x,y):
        a1 = self.upper_leg_length
        a2 = self.lower_leg_length

        c2 = (x**2+y**2-a1**2-a2**2)/(2*a1*a2)
        s2 = math.sqrt(1-c2**2)
        theta2 = math.atan2(s2,c2)
        c2 = math.cos(theta2)
        s2 = math.sin(theta2)

        c1 = (x*(a1+(a2*c2)) + y*(a2*s2))/(x**2+y**2)
        s1 = (y*(a1+(a2*c2)) - x*(a2*s2))/(x**2+y**2)
        theta1 = math.atan2(s1,c1)
        # generate positions with respect to robot motors
        theta_shoulder = -theta1
        theta_elbow = theta_shoulder - theta2
        theta_shoulder = 180 - self.rad_to_degree(theta_shoulder)
        theta_elbow = 130 - self.rad_to_degree(theta_elbow)
        self.kit.servo[Motor.FR_SHOULDER].angle = theta_shoulder
        self.kit.servo[Motor.FR_ELBOW].angle = theta_elbow
        print("theta shoulder:",theta_shoulder,"\ttheta_elbow:",theta_elbow)
        return [theta_shoulder, theta_elbow]

    def rad_to_degree(self,rad):
        return rad*180/math.pi


if __name__ == "__main__":
    r = Quadruped()
    r.forward_cycle()



