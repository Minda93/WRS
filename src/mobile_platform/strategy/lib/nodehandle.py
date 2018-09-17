#!/usr/bin/env python3
# -*- coding: utf-8 -*-+

import rospy
import rospkg
import subprocess

# rostopic msg
from mobile_platform.msg import scaninfo
from std_msgs.msg import Int32,Float32,Bool
from geometry_msgs.msg import Twist

# define behavior 
MOBILE_ROBOT = 0
CORRECTION = 1
PLATFORM = 2
HOME = 3
MANUAL = 4


class NodeHandle(object):
    '''
        scan infomation
            dis: 各點平均誤差(pixel)
            scanstate: 紅外線數位值
        strategy
            start: 策略執行
            behavior: 機器人行為狀態
            maxVel: 機器人最高速度
            minVel: 機器人最低速度
    '''
    def __init__(self):
        self.__dis = None
        self.__ang = None
        self.__scanState = None

        self.__start = 1
        self.__behavior = MOBILE_ROBOT
        self.__maxVel = 10.0
        self.__minVel = 15.0
        self.__velYaw = 15.0
        self.__errorAng = 1.2

        self.__qrang = None

        self.__loadParam = False

        self.pub_cmdvel = rospy.Publisher('motion/cmd_vel',Twist, queue_size = 1)
        self.pub_behavior = rospy.Publisher('scan_black/strategy_behavior',Int32, queue_size = 1)
        self.pub_behavior = rospy.Publisher('scan_black/qrcode_start',Bool, queue_size = 1)

        rospy.Subscriber("scan_black/scaninfo",scaninfo,self.Sub_ScanInfo)
        rospy.Subscriber("scan_black/strategy_start",Int32,self.Sub_Start)
        rospy.Subscriber("scan_black/strategy_behavior",Int32,self.Sub_Behavior)
        rospy.Subscriber("scan_black/qrcode_angle",Float32,self.Sub_QRAngle)
    
    def Sub_ScanInfo(self,msg):
        self.__dis = msg.dis
        self.__ang = msg.angle
        self.__scanState = msg.scanstate
    def Sub_Start(self,msg):
        self.__start = msg.data
    def Sub_Behavior(self,msg):
        self.__behavior = msg.data
        self.__loadParam = True
    def Sub_QRAngle(self,msg):
        self.__qrang = msg.data
        

    
    @property
    def dis(self):
        return self.__dis

    @dis.setter
    def dis(self, value):
        self.__dis = value
    
    @property
    def ang(self):
        return self.__ang

    @ang.setter
    def ang(self, value):
        self.__ang = value
    
    @property
    def scanState(self):
        return self.__scanState

    @scanState.setter
    def scanState(self, value):
        self.__scanState = value
    
    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value
    
    @property
    def behavior(self):
        return self.__behavior

    @behavior.setter
    def behavior(self, value):
        self.__behavior = value
    
    @property
    def maxVel(self):
        return self.__maxVel

    @maxVel.setter
    def maxVel(self, value):
        self.__maxVel = value
    
    @property
    def minVel(self):
        return self.__minVel

    @minVel.setter
    def minVel(self, value):
        self.__minVel = value
    
    @property
    def velYaw(self):
        return self.__velYaw

    @velYaw.setter
    def velYaw(self, value):
        self.__velYaw = value
    
    @property
    def errorAng(self):
        return self.__errorAng

    @errorAng.setter
    def errorAng(self, value):
        self.__errorAng = value
    
    @property
    def qrang(self):
        return self.__qrang

    @qrang.setter
    def qrang(self, value):
        self.__qrang = value
    
    @property
    def loadParam(self):
        return self.__loadParam

    @loadParam.setter
    def loadParam(self, value):
        self.__loadParam = value
    

        