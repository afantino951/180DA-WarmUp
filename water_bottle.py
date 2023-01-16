import cv2
import numpy as np


def main():
    """ The following code was copied from 
    https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html """
    low_hsv = [97, 159, 112]
    high_hsv = [120, 255, 255]

    low_rgb = [0, 50, 140]
    high_rgb = [100, 150, 255]
    
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
      
        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # mask = cv2.inRange(hsv, np.array(low_hsv), np.array(high_hsv))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(rgb, np.array(low_rgb), np.array(high_rgb))

        contours, hierarchy  = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Stolen from https://automaticaddison.com/real-time-object-tracking-using-opencv-and-a-webcam/
        areas = [cv2.contourArea(c) for c in contours]
 
        # If there are no countours
        if len(areas) > 1:
            max_index = np.argmax(areas)
        
            contour=contours[max_index]
            approx=cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
            x,y,w,h=cv2.boundingRect(approx)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),4)

        # Display the resulting frames
        cv2.imshow('frame', frame)
        # cv2.imshow('mask', mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()