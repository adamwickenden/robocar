import time

class PID:
    def __init__(self, P=0, I=0, D=0):
        # init PID constants
        self.P = P
        self.I = I
        self.D = D

    def start(self):
        # Init times
        self.t_now = time.time()
        self.t_prev = self.t_now
        # Init error
        self.e_prev = 0
        # Init PID deltas
        self.dP = 0
        self.dI = 0
        self.dD = 0

    def update(self, error, sleep=0.2):
        # Pause interation so we aren't over calculating
        time.sleep(sleep)

        # Calculate time delta
        self.t_now = time.time()
        dt = self.t_now - self.t_prev

        # calculate delta error
        de = error - self.e_prev

        # Proportinal change term
        self.dP = error
        # Integral change term
        self.dI += error * dt
        # Deriv chnage term
        self.dD = (de/dt) if dt > 0 else 0

        # Save time and eror
        self.t_prev = self.t_now
        self.e_prev = error

        output = sum([self.P * self.dP, self.I * self.dI, self.D * self.dD])

        return output