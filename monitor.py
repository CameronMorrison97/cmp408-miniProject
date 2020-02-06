import time
import os

# Read sysfs file get the value and then pass that value to pub script
def main():
  file = "/sys/class/gpio/gpio4/value"

  while 1==1:
    file_open = open(file,"r")
    status = int(file_open.read(1))
    # if the soil is dry
    if status == 1:
      os.system("python3 miniprojectpub.py cam securepassword123! 1")
    else:
      os.system("python3 miniprojectpub.py cam securepassword123! 0")
    time.sleep(1)


main()
