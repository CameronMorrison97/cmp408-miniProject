import paho.mqtt.client as mqtt
import ssl
import sys
import os
import smtplib

# ip and port number
ip = "3.8.116.161"
port = 8883

# Code adapted from tutorialspoint https://www.tutorialspoint.com/python/python_sending_email.htm and https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
# username and password of gmail account that will send the email.
gmail_user = "testsysinternals@gmail.com"
gmail_password = "testsysinternals@12@"

def sendmail():
  sent_from = gmail_user
  to = "cameron.morrison1997@gmail.com"
  message = """From: test <testsysinternals@gmail.com>
  To: Cameron Morrison <cameron.morrison1997@gmail.com>
  Subject: Plant Management

  Please water your plant :)
  """

  # Starts the smtplib logs in as email address and password above sends the message and closes the smtp server.
  try:
      server = smtplib.SMTP_SSL('smtp.gmail.com',465)
      server.ehlo()
      server.login(gmail_user, gmail_password)
      print(message)
      print(to)
      print(sent_from)
      server.sendmail(sent_from, to, message)
      server.close()

      print("email sent")
  except:
      print("Something went wrong")

def onerror():
  print("pahotest.py arguments - username password")
  exit()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Returns 5 if auth error
    if(rc == 5):
      print("Auth Error")
      client.disconnect()
      GPIO.cleanup()
    elif(rc == 0):
      client.subscribe("topic/test")

def on_message(client, userdata, msg):
   message = str(msg.payload.decode("utf-8"))
   os.system("echo " + message + " > ~/test.txt")
   print(message)

   # Prevents the user from being spammed with messages by setting a file when the email is sent and not sending the email again until state change
   if message == str('0'):
     if os.path.isfile("lock"):
       os.remove("lock")
   elif message == str('1'):
     if os.path.isfile("lock"):
       print("not sending email until state change")
     else:
       f = open("lock","w+")
       f.close()
       sendmail()

def on_subscribe(client,userdata,mid,granted_qos):
    print("Subscribed")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.tls_set("ca.crt",tls_version=ssl.PROTOCOL_TLSv1)
# Someone can spoof the server
client.tls_insecure_set(True)

try:
  client.username_pw_set(username=sys.argv[1],password=sys.argv[2])
except:
  print("Not enough arguments supplied")
  onerror()

client.connect(ip,port)
client.loop_forever()
