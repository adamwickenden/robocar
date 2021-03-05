from multiprocessing import Manager
from multiprocessing import Process

from imutils.video import VideoStream

from control.servo import Servo
from control.object_track import ObjectTrack
from control.pid import PID

import argparse
import signal
import time
import sys
import cv2

# We use var.value as we need to acces variables like this for threading

# Connect to servo control
servos = Servo()

def signal_handler(sig, frame):
    # sig is the signal process e.g ctrl + c
    # frame is the execution frame of the process
    print("Exiting program")
    servos.destroy()
    sys.exit()


# Thread 1 object tracking
def track_object(obj_x, obj_y, centre_x, centre_y):
    """
    Controls the facial inference and returns a rectangle to draw on a cv2 frame
    """
    # Init the exit handler
    signal.signal(signal.SIGINT, signal_handler)

    # Set up video stream
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    tracker = ObjectTrack()

    # Loop forever
    while True:
        # extract frame from video stream
        img = vs.read()

        # get centre of img, we focus here if nobody is in frame
        (h, w) = img.shape[:2]
        centre_x.value = w // 2
        centre_y.value = h // 2

        # find object location
        ((obj_x.value, obj_y.value), rect) = tracker.update(img, (centre_x.value, centre_y.value))

        # draw rectangle on image if it exists
        if rect is not None:
            (x,y,w,h) = rect
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        
        cv2.imshow("Object Tracking", img)
        cv2.waitKey(1)


def pid_feed(out, p, i, d, obj, centre):
    """
    PID Process will be instantiated twice, one for panning, one for tilting.

    args:
        out = servo angle we are going to control
        p,i,d = PID constants
        obj = co-ordinate of object in specific axis (x/y etc)
        centre = centre of frame in specific axis. Used to calculate error in axis
    """
    # Init the exit handler
    signal.signal(signal.SIGINT, signal_handler)

    # Create a PID at given start values
    p = PID(p.value, i.value, d.value)
    p.start()

    while True:
        # Error term
        error = centre.value - obj.value
        # Calculate PID
        out.value =  90 + p.update(error)
        print(out.value)


def pan_in_range(val, servo_range=[0, 180]):
    return (val > servo_range[0] and val < servo_range[1])


def tilt_in_range(val, servo_range=[90, 180]):
    return (val > servo_range[0] and val < servo_range[1])


def aim_servos(pan, tilt):
    """
    accepts an pan and a tilt variable which are being updated by a PID each
    """
    # Init the exit handler
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        pan_val = pan.value
        tilt_val = tilt.value
        if pan_in_range(pan_val):
            servos.set_servo_angle(0, pan_val)
        if tilt_in_range(tilt_val):
            servos.set_servo_angle(1, tilt_val)


if __name__ == '__main__':
    # Start a manager to control the processes
    # This is a multithreading tool that allows us to globally share variables
    with Manager() as mgr:
        # set values for the image centre
        centre_x = mgr.Value("i", 0)
        centre_y = mgr.Value("i", 0)
        # set values for the object co-ords
        obj_x = mgr.Value("i", 0)
        obj_y = mgr.Value("i", 0)
        # set values for the pan/tilt vals
        pan = mgr.Value("i", 90)
        tilt = mgr.Value("i", 90)

        # These have been pre-tuned. Tune myself afterwards.
        # Init pan PID manager vars
        panP = mgr.Value("f", 0.09)
        panI = mgr.Value("f", 0.08)
        panD = mgr.Value("f", 0.002)
        # Init tilt PID manager vars
        tiltP = mgr.Value("f", 0.11)
        tiltI = mgr.Value("f", 0.10)
        tiltD = mgr.Value("f", 0.002)

        # Init 4 independent processes
        # Object Tracker
        # PID panning
        # PID tilting
        # aim servos
        process_track_object = Process(target=track_object, args=(obj_x, obj_y, centre_x, centre_y))
        process_PID_pan = Process(target=pid_feed, args=(pan, panP, panI, panD, obj_x, centre_x))
        process_PID_tilt = Process(target=pid_feed, args=(tilt, tiltP, tiltI, tiltD, obj_y, centre_y))
        process_aim_servos = Process(target=aim_servos, args=(pan, tilt))

        # Start all processes
        process_track_object.start()
        time.sleep(5)
        process_PID_pan.start()
        process_PID_tilt.start()
        process_aim_servos.start()

        # Join all processes
        process_track_object.join()
        process_PID_pan.join()
        process_PID_tilt.join()
        process_aim_servos.join()
