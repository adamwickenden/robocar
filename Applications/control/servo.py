from board import SCL, SDA # represents clock channel and data channel
import busio

from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

from .data import servos

freq = 50
active_servos = [0, 1]
servo_range = [0, 180] # not needed as adafruit library handles this

class Servo:
	def __init__(self):
		# configure i2c connections
		i2c = busio.I2C(SCL, SDA)
		# create PCA9685 class instance and supply it with the i2c connections
		self.pca = PCA9685(i2c)
		self.pca.frequency = freq
		# Init refrence dict to servo objects so we can reference them later
		self.servo_dict = self._init_servos()
		
	def _init_servos(self):
		# Create dict of servo objects for easy access
		servo_dict = {}
		for channel in active_servos:
			servo_dict[channel] = servo.Servo(self.pca.channels[servos[channel]], min_pulse=580, max_pulse=2480)
		return servo_dict
		
	def set_servo_angle(self, channel, angle):
		channel = int(channel)
		if channel in active_servos:
			# print(f"setting servo {channel} using pca channel {servos[channel]} to {angle} degrees")
			self.servo_dict[channel].angle = angle
		else:
			print(f"Incorrect servo channel passed, use {active_servos[0]}-{active_servos[1]}")

	def destroy(self):
		for i in active_servos:
			self.servo_dict[i].angle = 90


if __name__ == '__main__':
	print("Aligning all servos to 90°.")
	pwm = Servo()
	while True:
		try:
			pwm.set_servo_angle(0, 120)
			pwm.set_servo_angle(1, 120)
		except KeyboardInterrupt:
			pwm.destroy()
			print('\n Ended')
			break
