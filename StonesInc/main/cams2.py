import io
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from django.conf import settings
import cv2
import os
import numpy as np


try:
    import RPi.GPIO as GPIO
except:
    pass

class VCam(object):
    def __init__(self, request) -> None:
        self.request = request
        self.imagenumber = 0
        print(0)
        self.picam2 = Picamera2()
        self.picam2.set_controls({"AfMode": 1 ,"AfTrigger": 0})
        # config = self.picam2.create_still_configuration(lores={"size": (320, 240)}, display="lores")
  # Set the resolution
        self.picam2.preview_config = self.picam2.create_preview_configuration()
        self.picam2.capture_config = self.picam2.create_still_configuration()
        print(1)
        # self.camera.framerate = 24  # Set the frame rate
        self.folder_name = None
        self.capture_frame = False  # flag to control image capture
        self.recording = False  # flag to control recording
        self.frames = []
        # video_config = self.picam2.create_video_configuration()
        # self.picam2.configure(video_config)
        self.picam2.start()
        print(2)
        # self.frame = self.picam2.capture_array('main')

    def __del__(self):
        self.picam2.close()

    def get_frame(self):
        image = 0
        return image
    
    def update(self):
        while True:
            self.frame = 0#self.picam2.capture_array('main')


import io
from PIL import Image

def gen(camera, imgarray):
    while True:
        # image = camera.get_frame()
        # frame = io.BytesIO()
        # image = camera.capture_image("main")
        print(1)
        # preview_config = camera.picam2.create_preview_configuration()
        print(2)
        # capture_config = camera.picam2.create_still_configuration()
        print(3)
        # camera.picam2.configure(preview_config)
        print(4)
        
        # time.sleep(2)
        print(5)
        image = camera.picam2.switch_mode_and_capture_image(camera.picam2.capture_config)
        print(6)
        image_np = np.array(image)  # Convert PIL.Image.Image to numpy array
        _, jpeg = cv2.imencode('.jpg', image_np)
        frame = jpeg.tobytes()
        # camera.picam2.capture_file(frame, format='jpeg')
        if camera.capture_frame:
            image_filename = f'{str(camera.folder_name)}_{camera.imagenumber:02d}.jpg'
            print(image_filename)
            # Assuming you have a folder named "StoredData" in your media root
            image_path = os.path.join(settings.MEDIA_ROOT, 'StoredData', camera.folder_name, image_filename)
            with open(image_path, 'wb') as f:
                f.write(frame)
            camera.capture_frame = False
        print(type(frame))
        if camera.recording:
            imgarray.append(frame)
            camera.frames = imgarray
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
