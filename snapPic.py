from picamera import PiCamera, Color
import time
import datetime as dt

def snap():
        try:
                camera = PiCamera()
                #camera.resolution = (1280, 720)
                camera.resolution = (640, 480)
                camera.vflip = True
                camera.contrast = 10
                #camera.image_effect = "watercolor"
                #camera.image_effect = "sketch"
                #camera.image_effect = "hatch"
                camera.annotate_background = Color('black')
                camera.annotate_foreground = Color('white')
                camera.annotate_text_size = 15 # (values 6 to 160, default is 32)
                camera.annotate_text = dt.datetime.now().strftime('%A %I:%M %p')
                time.sleep(2)
                camera.capture("/home/pi/Scripts/pic.jpg")
                time.sleep(2)
                camera.close()
        except:
                print("snap() in snapPic() fail")
