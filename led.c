#include <linux/init.h>
#include <linux/gpio.h>
#include <linux/module.h>
#include <linux/interrupt.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Cameron Morrison");
MODULE_DESCRIPTION("Kernel module that interacts with the HL69 soil moisture device.");
MODULE_VERSION("0.55");

// Inspired by piirq.c
// Green pin
static unsigned int led = 14;
// red pin
static unsigned int led2 = 4;
static unsigned int watch = 25;
static unsigned int Counter = 0;
static unsigned int Irqnum = 0;
static unsigned int state = 0;

static irq_handler_t led_handler(unsigned int irq, void *dev_id, struct pt_regs *regs){
	state=!state;
	printk(KERN_INFO "LED: Interrupt called\n");
	printk(KERN_INFO "LED: watch value is %d\n",gpio_get_value(watch));

	// Pin low if wet
	if(gpio_get_value(watch) == 0){
		gpio_set_value(led,1);
		gpio_set_value(led2,0);
	}else{
	// Pin high if dry
		gpio_set_value(led,0);
		gpio_set_value(led2,1);
	}

	Counter++;
	return (irq_handler_t) IRQ_HANDLED;
}

static int ledInit(void){
	int result = 0;	

	printk(KERN_INFO "Hello World\n");
	
	if(!gpio_is_valid(led)){
		printk(KERN_INFO "LED: invalid GPIO\n");
		return -ENODEV;
	}
	
	gpio_request(led,"LED");
	gpio_request(led2,"LED2");
	gpio_direction_output(led,1);
	gpio_direction_output(led2,1);
	gpio_export(led,false);
	gpio_export(led2,false);

	gpio_request(watch,"WATCH");
	gpio_direction_input(watch);
	gpio_set_debounce(watch,500);
	gpio_export(watch,true);

	Irqnum = gpio_to_irq(watch);
	printk(KERN_INFO "Led: The led is mapped to IRQ : %d\n", Irqnum);

	result = request_irq(Irqnum,
			(irq_handler_t) led_handler,
			IRQF_TRIGGER_RISING,
			"led_handler",
			NULL);

        return 0;
}

static void ledExit(void){
	printk(KERN_INFO "Goodbye\n");
	
	gpio_set_value(watch,0);
	gpio_set_value(led,0);
	gpio_set_value(led2,0);
	free_irq(Irqnum,NULL);
	gpio_unexport(led);
	gpio_unexport(led2);
	gpio_unexport(watch);
	gpio_free(led);
	gpio_free(led2);
	gpio_free(watch);
}

module_init(ledInit);
module_exit(ledExit);
