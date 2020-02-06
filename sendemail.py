import smtplib

gmail_user = "testsysinternals@gmail.com"
gmail_password = "testsysinternals@12@"

def sendmail():
  sent_from = gmail_user
  to = ['cameron.morrison1997@gmail.com']
  message = "Please water your plant :)"

  try:
      server = smtplib.SMTP_SSL('smtp.gmail.com',465)
      server.ehlo()
      server.login(gmail_user, gmail_password)
      server.sendmail(sent_from, to, message)
      server.close()

      print("email sent")
  except:
      print("Something went wrong")

sendmail()
