import sys
import time
import urllib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import RPi.GPIO as GPIO
import Adafruit_DHT
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, False)
GPIO.output(2, False)
global alert
alert=1
def start():
 global alert
 try:
  while 1:
   if(alert==120):
    alert=1
   htmlfile=urllib.urlopen("https://myotpsend.000webhostapp.com/index2.php")
   htmltext=htmlfile.read()
   if(htmltext=="<meta http-equiv=\"refresh\" content=\"3\">ON"):
    GPIO.output(3, True)
   else:
    GPIO.output(3, False)
   GPIO.output(2, False)
   humidity, temperature = Adafruit_DHT.read_retry(11, 4)
   if humidity is not None and temperature is not None:
    htmlfile=urllib.urlopen("https://myotpsend.000webhostapp.com/temp.php?temp="+str(temperature))
    htmltext=htmlfile.read()
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    if(temperature>40):
     GPIO.output(2, True)
     if(alert==1):
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.starttls()
      s.login('scscoe.feedback.system@gmail.com','scscoe123')
      body=MIMEMultipart('alternative')
      sub="Subject:ALERT FROM HOME AUTOMATION\n"
      part1=MIMEText(sub,'plain')
      part2=MIMEText("<html><body>ALERT YOUR ROOM TEMPERATURE IS HIGH TAKE ACTION PLEASE<br>YOUR ROOM TEMPERATURE IS "+str(temperature)+"*C<br>FROM HOME AUTOMATION SYSTEM.</body></html>",'html')
      body.attach(part1)
      body.attach(part2)
      s.sendmail('scscoe.feedback.system@gmail.com','jagdaleganesh9545@gmail.com','Subject:ALERT FROM HOME AUTOMATION\n'+body.as_string())
     alert=alert+1
     i=5
     while(i>=1):
      #print(i)
      time.sleep(1)
      i=i-1
 except:
  #print("error")
  start() 
start()
