from asyncio import wait
import datetime
import os
import time
import cv2
import threading

import numpy as np
from django.conf import settings

try:
    import RPi.GPIO as GPIO
except:
    pass

class VideoCam(object):
    def __init__(self, request):
        self.request = request
        self.imagenumber = 0
        self.video = cv2.VideoCapture(0)
        self.capture_frame = False  # flag to control image capture
        self.recording = False  # flag to control recording
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()


    def __del__(self):
        self.video.release()

    def get_frame(self):
        image= self.frame
        # _, jpeg = cv2.imencode('.jpg', image)
        # return jpeg.tobytes()
        return image
    
    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()


def gen(camera, imgarray):
    while True:
        image = camera.get_frame()
        _, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        if camera.capture_frame:
        # Save the image
            image_filename = str(camera.request.session.get('selectedFolder')) + f'_{camera.imagenumber:02d}.jpg'
            cv2.imwrite(os.path.join(settings.MEDIA_ROOT, 'StoredData', camera.request.session.get('selectedFolder'), image_filename), image)
            camera.capture_frame = False
        if camera.recording:
            imgarray.append(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def capture_and_save_image(request, GPIO_PIN_LIST, cam):
    # Capture an image and get the image data as a BytesIO object
    try :
        motor = StepperMotor(GPIO_PIN_LIST)
    except:
        print("No motor hardware")
    for i in range(1, 13):
        while cam.capture_frame:
            pass  # wait until capture_frame is False
        cam.imagenumber= i
        cam.capture_frame = True
        try:
            motor.rotate(degrees=30)
        except:
            print("No motor hardware")


   
def create_options(folder_path):
    static_folder =  os.path.join(settings.MEDIA_ROOT, 'StoredData')
    # Get the path to the subfolder within the static folder
    subfolder_path =  os.path.join(settings.MEDIA_ROOT, 'StoredData')
    # Get a list of all files and directories in the subfolder
    items = os.listdir(subfolder_path)
    # Filter the list to only include directories
    options = [item for item in items if os.path.isdir(os.path.join(subfolder_path, item))]
    # Add the "create new folder" option to the list
    options.insert(0,'Create new folder')
    # Return the list of directories
    return options

def init_gpio(pinlist):
    """
    Initialize GPIO.

    :param pinlist: GPIO list. Order is important...
    :return: None
    """
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    for pin in pinlist:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)


class StepperMotor(object):
    def __init__(self, gpio_pin_list):
        """
        Initialize GPIO and Step Motor status.

        :param gpio_pin_list: GPIO list
        """

        self.gpio_list = gpio_pin_list
        try:
            GPIO.setmode(GPIO.BCM)
        except:
            pass
        #init_gpio(self.gpio_list)
        self.phase = [1, 1, 0, 0]
        self.REVOLUTION_STEP_NUMBER = 2048

    def get_phase(self):
        """
        Get the phase of the 4 phases Stepper motor.

        :return: phase of step motor
        """
        return self.phase

    def rotate_segment(self, degrees):
        """
        Perform one step.

        :param direction: (Boolean) Clockwise = True | Inverted = False
        :return: None
        """
        if degrees >0:
            direction = False
        else:
            direction = True
        
        if direction:
            self.phase = np.roll(self.phase, 1)
        else:
            self.phase = np.roll(self.phase, -1)

        for pin_idx in range(len(self.gpio_list)):
            GPIO.output(self.gpio_list[pin_idx], int(self.phase.astype(int)[pin_idx]))

    def rotate(self,  degrees=0, delay=0.002):
        
        """
        Perform rotation with direction and angle info.

        :param direction: (Boolean) Clockwise = True | Inverted = False
        :param degrees: angle of rotation
        :return: None
        """
        init_gpio(self.gpio_list)
        step_number = int(self.REVOLUTION_STEP_NUMBER * abs(degrees)/ 360)
        for i in range(0, step_number):
            self.rotate_segment(degrees)
            time.sleep(delay)
        GPIO.cleanup()


#rewrite gen function so that there will also be option for recording images to array and then convert it to videos
