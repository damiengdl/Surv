import os
import time
import wget

try:    
  nb_files_before=-1
  while 1 :
    pp = os.popen ("ls -l /mnt/nas/Cam1|wc -l","r") ; 
    for line in pp.readlines() : 
      nb_files = int(line)
    pp.close () ; 

    pp = os.popen ("ls -l /mnt/nas/Cam2|wc -l","r") ; 
    for line in pp.readlines() : 
      nb_files = nb_files + int(line)
    pp.close () ; 

    print "Nombre de lignes dans les repertoires Cam1 et Cam2 = " + str(nb_files) ;
        
    if (nb_files_before != -1 and nb_files_before < nb_files):
      print "Envoi de SMS a Damien"
      urlSMS = 'https://smsapi.free-mobile.fr/sendmsg?user=user_sms_chez_free&pass=pasword_sms_chez_free&msg=Detection%20Camera'
      output = 'SEND_SMS_' + time.strftime("%d%m%Y_%H:%M:%S")
      wget.download(urlSMS,output)

    nb_files_before = nb_files

    time.sleep(20)             # delay 20 seconds
finally:  
  print("Cleaning up supervision")
  pp.close()
