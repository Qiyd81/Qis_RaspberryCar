#!/usr/bin/python
#coding: utf8
import sys
import RPi.GPIO as GPIO
import time
# import sys
# import tornado.ioloop
# import tornado.web
# import tornado.httpserver
# import tornado.options
# from tornado.options import define,options
# define("port",default=80,type=int)
IN1 = 11
IN2 = 12
IN3 = 13
IN4 = 15
def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)
# import os
# import time
# os.system("echo 14 > /sys/class/gpio/export")
# os.system("echo out > /sys/class/gpio/gpio14/direction")
# os.system("echo 1 > /sys/class/gpio/gpio14/value")
# os.system("echo 0 > /sys/class/gpio/gpio14/value")
# os.system("echo 14 > /sys/class/gpio/unexport")

# 前进
def forward(tf):
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()

# 后退
def reverse(tf):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(tf)
    GPIO.cleanup()

# 左转弯
def left(tf):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()

# 右转弯
def right(tf):
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()

# 后左转弯
def pivot_left(tf):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()

# 后右转弯
def pivot_right(tf):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(tf)
    GPIO.cleanup()

# 原地左转
def p_left(tf):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()

# 原地右转
def p_right(tf):
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(tf)
    GPIO.cleanup()

# stop
def stop(tf):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(tf)
    GPIO.cleanup()

class RunCar(object):
    def __init__(self):

        rospy.init_node('run_car')
        self.init()        
        sleep_time = 0.02		

        # TODO: Subscribe to all the topics you need to
        rospy.Subscriber('/vehicle/steering_cmd', SteeringCmd, self.steer_cb)
        rospy.Subscriber('/vehicle/throttle_cmd', ThrottleCmd, self.trottle_cb)
        rospy.Subscriber('/vehicle/brake_cmd', BrakeCmd, self.brake_cb)

        self.throttle = self.steering = self.brake = 0

        self.post()
        # rospy.spin()

    def steer_cb(self, msg):
	   self.steering = msg.steering_wheel_angle_cmd

    def throttle_cb(self, msg):
	   self.throttle = msg.pedal_cmd

    def brake_cb(self, msg):
	   self.brake = msg.pedal_cmd

    # def get(self):
    #         self.render("index.html")
    def post(self):
        # init()
        # sleep_time = 0.1
        # arg = self.get_argument('k')
        rate = rospy.Rate(50)
        while not rospy.is_shutdown():
            forward(sleep_time)
            if(self.throttle > 0 and self.steering == 0 and self.brake == 0):
        	   forward(sleep_time)
            # if(arg=='w'):
            #         forward(sleep_time)
            elif(self.throttle > 0 and self.steering > 0 and self.brake ==0):
        	   left(sleep_time)
            elif(self.throttle > 0 and self.steering < 0 and self.brake ==0):
        	   right(sleep_time)
            elif(self.throttle == 0 and self.steering > 0 and self.brake ==0):
        	   p_left(sleep_time)
            elif(self.throttle == 0 and self.steering < 0 and self.brake ==0):
        	   p_right(sleep_time)

            else:
        	   stop()

            rate.sleep()
        # elif(arg=='s'):
        #         reverse(sleep_time)
        # elif(arg=='a'):
        #         left(sleep_time)
        # elif(arg=='d'):
        #         right(sleep_time)
        # elif(arg=='q'):
        #         pivot_left(sleep_time)
        # elif(arg=='e'):
        #         pivot_right(sleep_time)
        # elif(arg=='z'):
        #         p_left(sleep_time)
        # elif(arg=='x'):
        #         p_right(sleep_time)
        # else:
        #         return False
        # self.write(arg)
if __name__ == '__main__':
    try:
	   RunCar()
    except rospy.ROSInterruptException:
	   pass
        # tornado.options.parse_command_line()
        # app = tornado.web.Application(handlers=[(r"/",IndexHandler)])
        # http_server = tornado.httpserver.HTTPServer(app)
        # http_server.listen(options.port)
        # tornado.ioloop.IOLoop.instance().start()