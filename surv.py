#
# surv.py
# D. Gautier de Lahaut for a surveillance system


import RPi.GPIO as GPIO
import time
import wget
import os
import sys

# Configure the Pi to use the BCM (Broadcom) pin names, rather than the pin positions
GPIO.setmode(GPIO.BCM)

surv_state = 0 # etat initial du systeme de surveillance
sms_systeme_OK = 0 # flag pour gerer l'envoi d'un SMS journalier
yellow_pin = 23
led_pin = 24

GPIO.setup(yellow_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT)


def allume_led():
    GPIO.output(led_pin, True)

def eteint_led():
    GPIO.output(led_pin, False)

def clignote_led(nb_seconds):
    cpt = 0
    while (cpt < nb_seconds):
        GPIO.output(led_pin, True)
        time.sleep(0.2)
        GPIO.output(led_pin, False) 
        time.sleep(0.2)
        cpt = cpt + 0.4

def switch_ON_Cam1():
    urlCam1 = 'http://user:password@192.168.0.x/setSystemMotion?ReplySuccessPage=motion.htm&ReplyErrorPage=motion.htm&MotionDetectionEnable=1&MotionDetectionScheduleDay=0&MotionDetectionScheduleMode=0&MotionDetectionSensitivity=80&ConfigSystemMotion=Save'
    output = 'ON_CAM1_' + time.strftime("%d%m%Y_%H:%M:%S")
    wget.download(urlCam1,output)

def switch_ON_Cam2():
    urlCam2 = 'http://user:password@192.168.0.y/setSystemMotion?ReplySuccessPage=motion.htm&ReplyErrorPage=motion.htm&MotionDetectionEnable=1&MotionDetectionScheduleDay=0&MotionDetectionScheduleMode=0&MotionDetectionSensitivity=80&ConfigSystemMotion=Save'
    output = 'ON_CAM2_' + time.strftime("%d%m%Y_%H:%M:%S")
    wget.download(urlCam2,output)

def switch_OFF_Cam1():
    urlCam1 = 'http://user:password@192.168.0.x/setSystemMotion?ReplySuccessPage=motion.htm&ReplyErrorPage=motion.htm&MotionDetectionEnable=0&MotionDetectionScheduleDay=0&ConfigSystemMotion=Save'
    output = 'OFF_CAM1_' + time.strftime("%d%m%Y_%H:%M:%S")
    wget.download(urlCam1,output)

def switch_OFF_Cam2():
    urlCam2 = 'http://user:password@192.168.0.y/setSystemMotion?ReplySuccessPage=motion.htm&ReplyErrorPage=motion.htm&MotionDetectionEnable=0&MotionDetectionScheduleDay=0&ConfigSystemMotion=Save'
    output = 'OFF_CAM2_' + time.strftime("%d%m%Y_%H:%M:%S")
    wget.download(urlCam2,output)

#def envoi_sms_journalier():

sms_systeme_OK = 0
nb_files_before=-1   
timeref = time.time()
#print "Timeref = " + str(timeref)
while True:
    #print("Yellow button value: yellow=" + str(GPIO.input(yellow_pin)))
    if GPIO.input(yellow_pin):
        if surv_state == 0:
            clignote_led(20)
            if GPIO.input(yellow_pin): # entre temps on a pu eteindre le recepteur
                surv_state = 1
                allume_led()
                print("SURV: Activation du systeme de surveillance " + time.strftime("%d%m%Y_%H:%M:%S"))
                sys.stdout.flush()
                switch_ON_Cam1()
                switch_ON_Cam2()
    else: # GPIO de yellow_pin est a 0
        if surv_state == 1:
            surv_state = 0
            eteint_led()
            print("SURV: Desactivation du systeme de surveillance " + time.strftime("%d%m%Y_%H:%M:%S"))
            sys.stdout.flush()
            switch_OFF_Cam1()
            switch_OFF_Cam2()
    time.sleep(0.5)             # delay 0.5 seconds

    heure = time.localtime()
    #print "Heure =" + str(heure.tm_hour) + " minutes=" + str(heure.tm_min) + " sms_systeme_OK=" + str(sms_systeme_OK)
    if (sms_systeme_OK == 0 and heure.tm_hour == 15 and heure.tm_min == 7):
        print "SURV: Envoi de SMS a Damien pour dire que tout va bien"
        sys.stdout.flush()                    
        urlSMS = 'https://smsapi.free-mobile.fr/sendmsg?user=user_sms_chez_free&pass=pasword_sms_chez_free&msg=Systeme%20Camera%20OK'
        output = 'SEND_SMS_' + time.strftime("%d%m%Y_%H:%M:%S")
        wget.download(urlSMS,output)
        sms_systeme_OK = 1
    if (heure.tm_hour == 15 and heure.tm_min == 8):
        sms_systeme_OK = 0

    timenow = time.time()
    #print "TimeNow = " + str(timenow)
    if (surv_state == 1 and timenow > timeref + 20):
        timeref = timenow
        print "SURV: Test de presence de fichiers sur le NAS"
        sys.stdout.flush()

        pp = os.popen ("ssh 192.168.0.z ls -l /Partage/Cam1|wc -l","r") ; 
        for line in pp.readlines() : 
            nb_files = int(line)
        pp.close () ; 
             
        pp = os.popen ("ssh 192.168.0.z ls -l /Partage/Cam2|wc -l","r") ; 
        for line in pp.readlines() : 
            nb_files = nb_files + int(line)
        pp.close () ; 
        print "SURV: Nombre de lignes dans les repertoires Cam1 et Cam2 = " + str(nb_files) ;
        sys.stdout.flush()
                    
        if (nb_files_before != -1 and nb_files_before < nb_files):
            print "SURV: Envoi de SMS a Damien"
            sys.stdout.flush()

            urlSMS = 'https://smsapi.free-mobile.fr/sendmsg?user=user_sms_chez_free&pass=pasword_sms_chez_free&msg=Detection%20Camera'
            output = 'SEND_SMS_' + time.strftime("%d%m%Y_%H:%M:%S")
            wget.download(urlSMS,output)
            timeref = timenow + 60
                        
        nb_files_before = nb_files
        
