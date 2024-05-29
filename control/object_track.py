import cv2

from control.config import package_root

haar = package_root / 'haar_face.xml'

class ObjectTrack():
    def __init__(self, haar=haar):
        # Initialise a haar face detector
        self.detector = cv2.CascadeClassifier(str(haar))

    # Update function that processes single frames
    def update(self, frame, prev_frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = self.detector.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=9,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(rects) > 0:
            # Extract bounding box co-ords of the face first face
            (x,y,w,h) = rects[0]
            centre_x = int(x + (w/2))
            centre_y = int(y + (w/2))

            return((centre_x, centre_y), rects[0])
        
        return (prev_frame, None)