# ##############################################################################################
# # Project     : 28BYJ-48 Stepper Motor driver
# # File        : stepperMotor.py
# # Author      : remi-ma
# # Date        : 27/02/18
# # Description : Control 28BYJ-48 Stepper Motor for Raspberry Pi
# # License     : None
# ##############################################################################################
# import os
# import time
# import cv2
# import RPi.GPIO as GPIO
# import numpy as np
# import io
# from django.conf import settings
# #import picamera

# REVOLUTION_STEP_NUMBER = 2048

# GPIO_PIN_LIST = [5,6,13,19]

# def init_gpio(pinlist):
#     """
#     Initialize GPIO.

#     :param pinlist: GPIO list. Order is important...
#     :return: None
#     """
#     GPIO.setmode(GPIO.BCM)
#     for pin in pinlist:
#         GPIO.setup(pin, GPIO.OUT)
#         GPIO.output(pin, 0)



# class StepperMotor(object):
#     def __init__(self, gpio_pin_list):
#         """
#         Initialize GPIO and Step Motor status.

#         :param gpio_pin_list: GPIO list
#         """
#         self.gpio_list = gpio_pin_list
#         GPIO.setmode(GPIO.BCM)

#         #init_gpio(self.gpio_list)
#         self.phase = [1, 1, 0, 0]

#     def get_phase(self):
#         """
#         Get the phase of the 4 phases Stepper motor.

#         :return: phase of step motor
#         """
#         return self.phase

#     def rotate_segment(self, degrees):
#         """
#         Perform one step.

#         :param direction: (Boolean) Clockwise = True | Inverted = False
#         :return: None
#         """
#         if degrees >0:
#             direction = False
#         else:
#             direction = True
        
#         if direction:
#             self.phase = np.roll(self.phase, 1)
#         else:
#             self.phase = np.roll(self.phase, -1)

#         for pin_idx in range(len(self.gpio_list)):
#             GPIO.output(self.gpio_list[pin_idx], int(self.phase.astype(int)[pin_idx]))

#     def rotate(self,  degrees=0, delay=0.002):
#         """
#         Perform rotation with direction and angle info.

#         :param direction: (Boolean) Clockwise = True | Inverted = False
#         :param degrees: angle of rotation
#         :return: None
#         """
#         init_gpio(self.gpio_list)
#         step_number = int(REVOLUTION_STEP_NUMBER * abs(degrees)/ 360)
#         for i in range(0, step_number):
#             self.rotate_segment(degrees)
#             time.sleep(delay)
#         GPIO.cleanup()
        
# def create_options(folder_path):
#     static_folder =  os.path.join(settings.MEDIA_ROOT, 'StoredData')
#     # Get the path to the subfolder within the static folder
#     subfolder_path =  os.path.join(settings.MEDIA_ROOT, 'StoredData')
#     # Get a list of all files and directories in the subfolder
#     items = os.listdir(subfolder_path)
#     # Filter the list to only include directories
#     options = [item for item in items if os.path.isdir(os.path.join(subfolder_path, item))]
#     # Add the "create new folder" option to the list
#     options.insert(0,'Create new folder')
#     # Return the list of directories
#     return options

# def capture_image():
#     # Open the video capture device
#     cap = cv2.VideoCapture(0)
#     # Set the resolution of the capture device
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
#     # Capture a frame from the video stream
#     success, frame = cap.read()
#     # Check if the frame was successfully read
#     if not success:
#         print("Error: Unable to read frame from video stream")
#         return None
#     # Rotate the frame 180 degrees
#     frame = cv2.flip(frame, -1)
#     # Create a BytesIO object to store the image data
#     image_data = io.BytesIO()
#     # Encode the frame as JPEG
#     ret, jpeg = cv2.imencode('.jpg', frame)
#     # Write the JPEG data to the BytesIO object
#     image_data.write(jpeg.tobytes())
#     # Reset the position of the BytesIO object to the beginning
#     image_data.seek(0)
#     # Release the video capture device
#     cap.release()
#     return image_data

# """
# def capture_and_save_image(folder):
#     # Capture an image and get the image data as a BytesIO object
#     motor = StepperMotor(GPIO_PIN_LIST)
#     for i in range(1, 13):
#         image_data = capture_image()
#         motor.rotate(degrees=30)
#     # Generate a unique file name
#         file_name = str(folder) + f'_{i:02d}.jpg'

#     # Save the image to the static folder
#         file_path = os.path.join('static/StoredData/'+ folder, file_name)
#         with open(file_path, 'wb') as f:
#             f.write(image_data.getvalue())
# """
# def capture_and_save_image(folder):
#     # Capture an image and get the image data as a BytesIO object
#     motor = StepperMotor(GPIO_PIN_LIST)
#     for i in range(1, 13):
#         image_data = capture_image()
#         if image_data is None:
#             # Handle the error here
#             print("Error: Unable to capture image")
#             continue
#         motor.rotate(degrees=30)
#     # Generate a unique file name
#         file_name = str(folder) + f'_{i:02d}.jpg'

#     # Save the image to the static folder
#         file_path = os.path.join('static/StoredData/'+ folder, file_name)
#         # Load the image data from the BytesIO object
#         image = cv2.imdecode(np.frombuffer(image_data.getvalue(), np.uint8), -1)
#         # Save the image to the file
#         cv2.imwrite(file_path, image)

# def capture_video():
#     # Open the video capture device
#     cap = cv2.VideoCapture(0)
#     # Set the resolution and framerate of the video
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
#     cap.set(cv2.CAP_PROP_FPS, 90)
#     # Create a VideoWriter object to store the video
#     fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#     video_buffer = cv2.VideoWriter('video.avi', fourcc, 90, (1024,768))
#     print("Recording Started")
#     # Record for 10 seconds
#     start_time = time.time()
#     while time.time() - start_time < 1:
#         # Read a frame from the video stream
#         success, frame = cap.read()
#         # Rotate the frame 180 degrees
#         frame = cv2.flip(frame, -1)
#         # Write the frame to the VideoWriter object
#         video_buffer.write(frame)
#         # Rotate the motor
#         GPIO_PIN_LIST = [5, 6, 13, 19]
#         Motor = StepperMotor(GPIO_PIN_LIST)
#         Motor.rotate(degrees=360, delay=0.01)
#     # Release the video capture device and the VideoWriter object
#     cap.release()
#     video_buffer.release()
#     return video_buffer


# def save_Video(folder):
#     # Capture the video and get the VideoWriter object
#     video_buffer = capture_video()
#     # Save the video to the static folder
#     file_path = os.path.join('static/StoredData/' + folder, 'Video1.avi')
#     # Define the codec to be used for the video
#     fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#     # Load the video from the VideoWriter object
#     cap = cv2.VideoCapture(video_buffer)
#     # Save the video to the file
#     cv2.VideoWriter(file_path, fourcc, 90, (1024, 768)).write(cap)
#     # Release the video capture device
#     cap.release()

