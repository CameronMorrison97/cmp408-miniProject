KERNEL := ../linux
PWD := $(shell pwd)
CROSS := /root/tools/arm-bcm2708/arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
obj-m += led.o

all:
	make ARCH=arm CROSS_COMPILE=$(CROSS) -C $(KERNEL) SUBDIRS=$(PWD) modules
clean:
	make -C $(KERNEL) SUBDIRS=$(PWD) clean
