import time

from board import SCL, SDA # represents clock channel and data channel
import busio

from adafruit_motor.motor import DCMotor
from adafruit_pca9685 import PCA9685

from control.data import motors

freq = 50

class Motor:
	def __init__(self):
		# configure i2c connections
		i2c = busio.I2C(SCL, SDA)
		# create PCA9685 class instance and supply it with the i2c connections
		self.pca = PCA9685(i2c)
		self.pca.frequency = freq
		# Init refrence dict to servo objects so we can reference them later
		self.motor_dict = self._init_motors()
		
	def _init_motors(self):
		motor_dict = {}
		for motor in motors:
			motor_dict[motor] = DCMotor(self.pca.channels[motors[motor]["+"]], self.pca.channels[motors[motor]["-"]])
		return motor_dict

	def drive(self, power):
		# +ve for forward, -ve for backwards
		for motor in self.motor_dict:
			self.motor_dict[motor].throttle = power

			
	def left(self, power):
		for motor in self.motor_dict:
			# To turn left we need to apply throttle on the right wheels
			if 'R' in motor:
				self.motor_dict[motor].throttle = power
			else:
				# set the opposite side to reverse
				self.motor_dict[motor].throttle = -power
				
	def right(self, power):
		for motor in self.motor_dict:
			# To turn right we need to apply throttle on the left wheels
			if 'L' in motor:
				self.motor_dict[motor].throttle = power
			else:
				# set the opposite side to reverse
				self.motor_dict[motor].throttle = -power
				
	def stop(self):
		for motor in self.motor_dict:
			self.motor_dict[motor].throttle = 0


if __name__ == '__main__':
	print("Test driving.")
	motors = Motor()
	while True:
		try:
			motors.drive(0.5)
			time.sleep(1)
			motors.drive(-0.5)
			time.sleep(1)
			motors.left(0.5)
			time.sleep(1)
			motors.right(0.5)
			time.sleep(1)
			motors.stop()
			break
		except KeyboardInterrupt:
			print('\n Ended')
			break

