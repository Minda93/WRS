#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import math
import numpy as np


# lib
from lib.nodehandle import NodeHandle
from lib.pidcontrol import PIDControl,PIDControl_Y,PIDControl_Yaw
from lib.fuzzycontrol import FUZZYControl
from lib.counter import TimeCounter

# rostopic msg
from geometry_msgs.msg import Twist


# define behavior 
MOBILE_ROBOT = 0
CORRECTION = 1
PLATFORM = 2
NEXT_POINT = 3
HOME = 4
MANUAL = 5
ROTATE = 6
GO_POINT = 7
RETURN_POINT = 8
CROSS = 9
INIT = 10

# FLAG 
CONTROL = 'PIDCONTROL'
# CONTROL = 'FUZZYCONTROL'
IMU_FLAG = True

'''
    HOME -> FIRST
        INIT -> MOBILE -> CORRECTION_0 -> ROTATE_90 -> CORRECTION_90 -> PLATFORM
    FIRST -> SECOND 
        NEXT -> ROTATE_0 -> CROSS -> MOBILE -> CORRECTION_0 -> ROTATE_90 -> CORRECTION_90 -> PLATFORM
    POINT -> HOME
        HOME -> ROTATE -> CROSS_FIRST -> MOBILE -> PLATFORM
'''

class Strategy(object):
    def __init__(self):
        self._param = NodeHandle()
        if(CONTROL == 'PIDCONTROL'):
            self.control = PIDControl()
            self.controlY = PIDControl_Y()
            self.controlYaw = PIDControl_Yaw()
        elif(CONTROL == 'FUZZYCONTROL'):
            self.control = FUZZYControl()
        
        self.state = 0
        self.pre_state = 0
        self.prev_dis = 0
        self.prev_ang = 0
        self.prev_vel = []

        self.initPID = 0
        self.not_find = 0
        # self._kp = 6
        # self._ki = 0.1
        # self._kd = 4.0
        # self.prevIntegral = 0
        # self.lastError = 0
        
        ''' rotate  '''
        self.rotateAng = 0

        ''' go_point '''
        self.timer = TimeCounter(time = 0.8)

        ''' home '''
        self.homeFlag = 0
        self.homeTimes = 0

    def Process(self):
        if(self._param.behavior == MOBILE_ROBOT):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.Mobile_Strategy()

        elif(self._param.behavior == CORRECTION):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.Correction_Strategy()

        elif(self._param.behavior == PLATFORM):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.Platform_Strategy()

        elif(self._param.behavior == NEXT_POINT):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.Next_Point_Strategy()

        elif(self._param.behavior == HOME):
            if(self._param.loadParam):
                self.Change_Behavior()
            print('HOME')

        elif(self._param.behavior == MANUAL):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.state = 0
            self.initPID = 0
            self.controlYaw.Init()
            self.controlY.Init()
            print('MANUAL')

        elif(self._param.behavior == ROTATE):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.Rotate_Strategy()

        elif(self._param.behavior == GO_POINT):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.Go_Point_Strategy()
            print('GO_POINT')

        elif(self._param.behavior == RETURN_POINT):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.Return_Point_Strategy()
            print('RETURN_POINT')
        elif(self._param.behavior == CROSS):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.Cross_Strategy()
        elif(self._param.behavior == INIT):
            if(self._param.loadParam):
                self.Change_Behavior()
            self.Init_Strategy()
            print('Init')
        else:
            print("Don't have Behavior")
            self.Robot_Stop()

    def Mobile_Strategy(self):
        if(self._param.scanState):
            count = self._param.scanState.count(1)
            if(count):
                scanNum = len(self._param.scanState)
                if(count <= math.ceil((scanNum)*(1./3)) and self._param.stopPoint == 999):
                    self.state = 0
                    # Method 3
                    #if(CONTROL == 'PIDCONTROL'):
                    #    x,y,yaw = self.control.Process(self._param.dis,self._param.ang,self._param.maxVel,self._param.minVel,self._param.velYaw)
                    #elif(CONTROL == 'FUZZYCONTROL'):
                    #    x,y,yaw = self.control.Process(self._param.dis,self._param.ang)
                    # yaw = 0
                    #self.Robot_Vel([y,-x,yaw])
                    #print(y,-x,yaw)

                    # Method 4
                    # x,y,yaw = self.control.Process(self._param.dis,self._param.ang,self._param.maxVel,self._param.minVel,self._param.velYaw)
                    # if(abs(self._param.ang) > 10.0):
                    #     if(self._param.ang > 0):
                    #         x = -(self._param.minVel*math.cos(math.radians(self._param.ang)))*0.15
                    #         y = -(self._param.minVel*math.sin(math.radians(self._param.ang)))*0.15
                    #         # yaw = self._param.velYaw
                    #         yaw = (self._param.velYaw+abs(yaw))
                    #     else:
                    #         x = -(self._param.minVel*math.cos(math.radians(self._param.ang)))*0.15
                    #         y = (self._param.minVel*math.sin(math.radians(self._param.ang)))*0.15
                    #         # yaw = -self._param.velYaw
                    #         yaw = -(self._param.velYaw+abs(yaw))
                    # else:
                    #     x,y,_ = self.control.Process(self._param.dis,self._param.ang,self._param.maxVel,self._param.minVel,self._param.velYaw)
                    #     # x,y,_ = self.control.Process(self._param.dis,self._param.ang)
                    #     yaw = 0
                        
                    ''' Method 5 '''
                    y = self.controlY.Process(self._param.dis,self._param.ang,self._param.minVel)
                    x = (self._param.minVel - abs(y))*math.cos(math.radians(self._param.ang)) - y*math.sin(math.radians(self._param.ang))
                    
                    if(abs(self._param.dis) > 1000):
                        yaw = 0
                    else:       
                        if(abs(self._param.ang) > 3.0):
                            yaw = self.controlYaw.Process(self._param.ang,self._param.velYaw)
                        else:
                            yaw = 0

                    self.Robot_Vel([x,y,yaw])
                    print(x,y,yaw)
                    self.prev_dis = self._param.dis
                    self.prev_ang = self._param.ang
                    self.prev_vel = [x,y,yaw]
                elif(self._param.stopPoint):
                    print('STOP')
                    self.state = 1
                    self.Robot_Stop()

                    if(self.homeFlag == 1):
                        self._param.behavior = HOME
                    else:
                        self._param.behavior = CORRECTION
                        self.homeTimes += 1

                self._param.stopPoint = 999
                self.pre_state = self.state
            else:
                print('Offset track !!!!!!')
                if(len(self.prev_vel)):
                    if(self.prev_vel[2] == 0):
                        x = -(self.prev_vel[0])*0.8
                        y = -self.prev_vel[1]*1.5
                        yaw = 0
                    else:     
                        x = (self._param.minVel*math.cos(math.radians(self.prev_ang)))*0.5
                        y = self._param.minVel*math.sin(math.radians(self.prev_ang))
                        yaw = 0
                else:
                    x = 0
                    y = 0
                    yaw = 0
                    print('No scan line')
                # self.Robot_Vel([y,-x,yaw])
                self.Robot_Stop()
        else:
            print('No Scan Info !!!!!!')
            self.Robot_Stop()

    def Correction_Strategy(self):
        y = self.controlY.Process(self._param.dis,self._param.ang,self._param.minVel)
        if(self._param.dis < 600):
            if(self._param.qrang is not None and self._param.qrang != 999):
                RPang = self.Norm_Angle(self.rotateAng - self._param.qrang)
                if(abs(RPang) > self._param.errorAng):
                    if(RPang > 0):
                        x = 0
                        y = 0
                        # yaw = self._param.velYaw
                        yaw = self._param.rotateYaw
                    else:
                        x = 0
                        y = 0
                        # yaw = -self._param.velYaw
                        yaw = -self._param.rotateYaw

                    self.Robot_Vel([x,y,yaw])
                    print('CORRECTION','FRONT',self._param.qrang)
                else:
                    self.Robot_Stop()
                    self.Robot_Stop()
                    self.Robot_Stop()
                    if(self.rotateAng == 0):
                        self._param.behavior = ROTATE
                        self.rotateAng = self._param.errorRotate90
                    else:
                        self._param.behavior = PLATFORM
                        self.rotateAng = self._param.errorRotate0
                        self.initPID = 1
                    print('CORRECTION')
                self.not_find = 0
            else:
                print('CORRECTION not find')
                if(self.not_find < 100):
                    self.not_find += 1
                    self.Robot_Stop()
                else:
                    self.not_find = 0
                    if(self.rotateAng == 0):
                        self._param.behavior = ROTATE
                        self.rotateAng = self._param.errorRotate90
                    else:
                        self._param.behavior = PLATFORM
                        self.rotateAng = self._param.errorRotate0  
                        self.initPID = 1
            self._param.qrang = 999
        else:
            x = 0
            yaw = 0
            self.Robot_Vel([x,y,yaw])
            print('CORRECTION','dis',y)
    
    def Platform_Strategy(self):
        print('PLATFORM')
        self.state = 0
        if(self.initPID):
            self.controlYaw.Init()
            self.controlY.Init()
            self.initPID = 0
        self.Robot_Stop()
    
    def Next_Point_Strategy(self):
        print('NEXT_POINT')
        self.Robot_Stop()
        self._param.behavior = ROTATE
        self.rotateAng = 0
        
            
    def Rotate_Strategy(self):
        # yaw = self.controlYaw(self._param.qrang,self._param.velYaw)
        if(self._param.qrang is not None and self._param.qrang != 999):
            RPang = self.Norm_Angle(self.rotateAng - self._param.qrang)
            if(abs(RPang) > self._param.errorAng):
                if(RPang > 0):
                    x = 0
                    y = 0
                    # yaw = self._param.velYaw
                    yaw = self._param.rotateYaw
                else:
                    x = 0
                    y = 0
                    # yaw = -self._param.velYaw
                    yaw = -self._param.rotateYaw
                self.Robot_Vel([x,y,yaw])
                print('ROTATE','angle',self._param.qrang)
            else:
                self.Robot_Stop()
                self.Robot_Stop()
                self.Robot_Stop()
                if(self.rotateAng == self._param.errorRotate90):
                    self._param.behavior = CORRECTION
                    print('ROTATE COREECTION')
                else:
                    self._param.behavior = CROSS
                    print('ROTATE CROSS')
            self.not_find = 0
        else:
            print('ROTATE not find')
            if(self.not_find < 100):
                self.not_find += 1
                # self.Robot_Stop()
            else:
                self.not_find = 0
                if(self.rotateAng == self._param.errorRotate90):
                    self._param.behavior = CORRECTION
                    print('ROTATE COREECTION')
                else:
                    self._param.behavior = CROSS
                    print('ROTATE CROSS')
        self._param.qrang = 999
    
    def Go_Point_Strategy(self):
        time,state = self.timer.Process()

        if(state):
            self.Robot_Stop()
            self._param.behavior = CORRECTION
        else:
            x = self._param.minVel
            y = 0
            yaw = 0
            self.Robot_Vel([x,y,yaw])

    def Return_Point_Strategy(self):
        time,state = self.timer.Process()

        if(state):
            self.Robot_Stop()
            self._param.behavior = ROTATE
            self.rotateAng = 0
        else:
            x = -self._param.minVel
            y = 0
            yaw = 0
            self.Robot_Vel([x,y,yaw])
    
    def Cross_Strategy(self):
        print('CROSS')
        time,state = self.timer.Process()

        if(state):
            self.Robot_Stop()
            self._param.behavior = MOBILE_ROBOT
            self.rotateAng = 0
        else:
            x = self._param.minVel
            y = 0
            yaw = 0
            self.Robot_Vel([x,y,yaw])
        # if(self.pre_state == 1 and self.state == 0):
        #     if(self._param.scanState):
        #         if(self._param.qrang is not None and self._param.qrang != 999):
        #             x = self._param.minVel
        #             y = 0
        #             yaw = 0
        #             self.not_find = 0
        #             # self.Robot_Vel([y,-x,yaw])
        #             self.Robot_Vel([x,y,yaw])
        #         elif(self.not_find > 60):
        #             self.Robot_Stop()
        #             self._param.behavior = MOBILE_ROBOT
        #             self.not_find = 0
        #                 # print('next point not find line')
        #         else:
        #             self.not_find +=1
        #             x = self._param.minVel
        #             y = 0
        #             yaw = 0
        #             # self.Robot_Vel([y,-x,yaw])
        #             self.Robot_Vel([x,y,yaw])
        #         self._param.qrang = 999
        # else:
        #     self.Robot_Stop()
        #     print('fuck Cross')
    
    def Init_Strategy(self):
        self.rotateAng = 0
        self.homeFlag = 0
        self.homeTimes = 0
        self.Robot_Stop()
        self._param.behavior = MOBILE_ROBOT

    def Home_Strategy(self):
        if(self.homeFlag == 0):
            self.homeFlag = 1
            self.Robot_Stop()
            self._param.behavior = ROTATE
            self.rotateAng = 0
            self.homeTimes -= 1
        else:
            if(self.homeTimes == 0):
                print('home')
                self.Robot_Stop()
                self._param.behavior = PLATFORM
            else:
                if(self.homeTimes == self._param.stopPoint):
                    self.homeTimes -= 1
                    self._param.behavior = CROSS

            
    def Deg2Rad(self,deg):
        return deg*math.pi/180
    
    def Norm_Angle(self,angle):
        if(angle > 180):
            angle -= 360
        elif(angle < -180):
            angle +=360
        return angle

    def Robot_Stop(self):
        vel = Twist()
        vel.linear.x = 0
        vel.linear.y = 0
        vel.angular.z = 0
        self._param.pub_cmdvel.publish(vel)

    def Robot_Vel(self,vec):
        vel = Twist()
        vel.linear.x = vec[0]
        vel.linear.y = vec[1]
        vel.angular.z = vec[2]
        self._param.pub_cmdvel.publish(vel)
    
    def Change_Behavior(self):
        self.Robot_Stop()
        self.Robot_Stop()
        self._param.loadParam = False
    

