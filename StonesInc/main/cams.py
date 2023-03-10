import datetime
import os
import cv2
import threading

from django.conf import settings

class VideoCam(object):
    def __init__(self, request):
        self.request = request
        self.video = cv2.VideoCapture(0)
        self.capture_frame = False  # flag to control image capture
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()


    def __del__(self):
        self.video.release()

    def get_frame(self):
        image= self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        if camera.capture_frame:
            # Save the image
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            image_filename = f"{timestamp}.jpg"
            cv2.imwrite(os.path.join(settings.MEDIA_ROOT, 'StoredData', camera.request.session.get('selectedFolder'), image_filename), frame)
            camera.capture_frame = False
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
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