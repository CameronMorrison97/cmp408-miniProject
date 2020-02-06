import paho.mqtt.client as mqtt
import os
import sys
import ssl
# Port number Ip address
ip = "3.8.116.161"
port = 8883

def onerror():
  print("publishtest argument - username password message")
  exit()

try:
  uname = sys.argv[1]
  pword = sys.argv[2]
  message = sys.argv[3]
except:
  print("Too few arguments")
  onerror()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    if(rc==5):
      print("Auth Error")
      client.disconnect()
    else:
      client.publish("topic/test",message)
      client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect

# Someone can spoof the server
client.tls_set("ca.crt",tls_version=ssl.PROTOCOL_TLSv1)
client.tls_insecure_set(True)
client.username_pw_set(username=uname,password=pword)
client.connect(ip,port)
client.loop_forever()
