#!/usr/bin/env python

import wget
import time

urlCam1 = 'http://user:password@192.168.0.x/setSystemMotion?ReplySuccessPage=motion.htm&ReplyErrorPage=motion.htm&MotionDetectionEnable=0&MotionDetectionScheduleDay=0&ConfigSystemMotion=Save'

output = 'OFF_CAM1_' + time.strftime("%d%m%Y_%H:%M:%S")
wget.download(urlCam1,output)

urlCam2 = 'http://user:password@192.168.0.y/setSystemMotion?ReplySuccessPage=motion.htm&ReplyErrorPage=motion.htm&MotionDetectionEnable=0&MotionDetectionScheduleDay=0&ConfigSystemMotion=Save'

output = 'OFF_CAM2_' + time.strftime("%d%m%Y_%H:%M:%S")
wget.download(urlCam2,output)
