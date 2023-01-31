from djitellopy import tello
import KeyPressModule as kp
import pygame

from time import sleep
import time, cv2
from threading import Thread
from djitellopy import Tello

kp.init()

me = tello.Tello()

me.connect()
keepRecording = True
me.streamon()
battery=me.get_battery()


def videoRecorder():
    
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (960,720))

    while keepRecording:
        frame_read = me.get_frame_read().frame
        frame_read = cv2.resize(frame_read, (960, 720))
        video.write(frame_read)
        cv2.putText(frame_read, str(battery),(20,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
        cv2.imshow("windowName", frame_read)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
            

    

recorder = Thread(target=videoRecorder)
recorder.start()

print(me.get_battery())

def getKeyboardInput():

    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 50

    if kp.getKey("LEFT"): lr = -speed

    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed

    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"):ud = speed

    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"):yv = -speed

    elif kp.getKey("d"): yv = speed

    if kp.getKey("x"): 
        me.land(); 
        sleep(1)
        pygame.quit()
        

    if kp.getKey("e"): me.takeoff()

    return [lr, fb, ud, yv]

while True:

    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)
    
keepRecording = False
recorder.join()