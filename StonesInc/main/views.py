from time import sleep
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip
from django.conf import settings
#from .funs import StepperMotor, create_options, capture_and_save_image, save_Video
import os
import cv2
import json
from .cams2 import *
from django.http import JsonResponse
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="cv2")



# initial code to for motor
GPIO_PIN_LIST = [5, 6, 13, 19]
Motor = StepperMotor(GPIO_PIN_LIST)
# Motor.rotate(direction=True, degrees=-180)

# Folder for storage
IMG_FOLDER = os.path.join('static', 'IMG')
capturedFolder = os.path.join(settings.MEDIA_ROOT, 'StoredData')
CurrentDir = capturedFolder
index = 0
currentFile = f'snap{index}.jpeg'

selected_folder = ""
streaming = True
global img_array
streaming = True
recording = False
global out

img_array = []


def at_home(request):
    options = create_options(capturedFolder)



@csrf_exempt
@gzip.gzip_page
def Home(request):
    FolderName = request.session.get('selectedFolder')
    global cam
    try:
        cam.__del__()
    except Exception:
        print('No yet started')
    options = create_options(capturedFolder)
    if request.method == "POST":
        # getting input with name = fname in HTML form
        FolderName = request.POST.get("FolderName")
        return HttpResponse(f"Your name is {FolderName}")

    return render(request,'start.html',  context = {"FolderN": FolderName, "options": options})


def selectfolder(request, folder):
    #selection = request.GET.get('folder')
    if folder == 'Create new folder':
        return render(request, 'select.html')
    else:
        global cam 
        cam.folder_name = folder
        request.session['selectedFolder'] = folder
        return HttpResponse(f'Selected folder is {folder}.')


from django.http import StreamingHttpResponse
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Condition
import io


import io
from django.http import StreamingHttpResponse
from django.views.decorators.http import condition
from threading import Condition
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


output = StreamingOutput()
picam2 = Picamera2()
picam2.set_controls({"AfMode": 1 ,"AfTrigger": 0, "LensPosition": 425})
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720)}))
picam2.start_recording(JpegEncoder(), FileOutput(output))


@condition(etag_func=None)
def stream_video(request):
    def stream():
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                yield (b'--FRAME\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except GeneratorExit:
            picam2.stop_recording()

    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=FRAME')




def start_Photos(request):
    global cam
    try:
        # Use the global cam object to capture and save an image
        capture_and_save_image(request, GPIO_PIN_LIST=GPIO_PIN_LIST, cam=cam)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def record_view(request):
    try:
        folder = request.session.get('selectedFolder')
        record(folder)
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    
def record(folder):
    global cam
    global img_array
    try:
        cam.recording = True      
        img_array = []
        print("Recording Started")
        try:
            Motor.rotate(degrees=360, delay=0.01)  
        except Exception:
            print("No motor hardware connected")
        sleep(3)
        print("Recording Stopped")
        cam.recording = False
        
        # Define the output video file name and codec
        output_file = "Video.mp4"
        # Define the output file path
        output_path = os.path.join(settings.MEDIA_ROOT, 'StoredData',folder, output_file)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v") #*"XVID")

        # Set the video frame size to match the size of the input frames
        frame_size = (3840, 2160)

        # Create a VideoWriter object to write the frames to a video file
        out = cv2.VideoWriter(output_path, fourcc, 30.0, frame_size)
        print(f"Length of image array is {len(cam.frames)}")
        # Iterate over each JPEG-encoded image in the list and decode it using OpenCV
        for img_bytes in cam.frames:
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Resize the image to match the output video frame size
            img = cv2.resize(img, frame_size)

            # Write the image to the video file
            out.write(img)

        # Release the VideoWriter object and close the video file
        out.release()
        img_array = []
        print('Recording complete')
    except:
        pass

@csrf_exempt
def create_folder(request):
    response_data = {}
    # Parse the request body as JSON
    request_data = json.loads(request.body)
    
    # Extract the folder name and selection data from the JSON data
    
    # Get the selected option from the form
    selected_option = request_data.get('selection')
    print("New folder -", selected_option)

    # Check if the "create new folder" option was selected
    if selected_option == 'Create new folder':
        # Get the name of the new folder from the form
        folder_name = request_data.get('folderName')

        # Get the path to the static folder
        media_folder = settings.MEDIA_ROOT
        print("MEDIA_ROOT:", media_folder)

        # Get the path to the subfolder within the static folder
        subfolder_path = os.path.join(media_folder, 'StoredData')
        print("subfolder_path:", subfolder_path)

        # Check if folder already exists
        folder_path = os.path.join(subfolder_path, folder_name)
        print("Created folder_path:", folder_path)

        if os.path.isdir(folder_path):
            print("Folder already exists")
            request.session['selectedFolder'] = folder_name
            response_data['success'] = False
        else:
            # Create the new folder in the subfolder
            os.makedirs(folder_path)
            print("New folder created")
            request.session['selectedFolder'] = folder_name
            response_data['success'] = True

    else:
        request.session['selectedFolder'] = selected_option
        response_data['success'] = True

    # Set the response data
    response_data['selectedFolder'] = request.session['selectedFolder']

    # Return a JSON response
    return JsonResponse(response_data)



def stop_cam():
    global cam
    if cam:
        cam.video.release()
        cam = None

def redirect_to_Gallery(request):
    stop_cam()
    return redirect('folder_list')

@csrf_exempt
def update_zoom_factor(request):
    if request.method == 'POST':
        zoom_factor = request.POST.get('zoom_factor')
        view_factor = request.POST.get('view_factor')
        if zoom_factor:
            try:
                cam.zoom_factor = float(zoom_factor)
            except ValueError:
                pass
        if view_factor:
            try:
                cam.view_factor = float(view_factor)
            except ValueError:
                pass
    return HttpResponse()

# def browse_folder(request):
#     folder = 'static/StoredData'
#     files = os.listdir(folder)
#     return render(request, 'browse.html', {"files": files})


# def view_media(request, path):
#     directory = '/static/StoredData'
#     imgfiles = os.listdir(f"static/StoredData/{path}")
#     imgfiles.sort()
#     return render(request, 'view_media.html', {"files": imgfiles, "path": path})


# def take_Video(request):
#     FolderName = request.session.get('selectedFolder')
#     save_Video(FolderName)
#     return redirect("home")

# def gen(rec):
#     # Open the video stream
#     global cap
#     cap = cv2.VideoCapture(0)

#     while True:
#         # Check the status of the streaming
#         if not streaming:
#             cap.release()
#             print("Not streaming")
#             break

#         # Read a frame from the video stream
#         success, frame = cap.read()
#         if not success:
#             print("Error reading video stream")
#             break
#         frame = cv2.flip(frame, -1)

#         # Encode the frame as JPEG
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         if jpeg is None:
#             print("Error encoding frame as JPEG")
#             break
#         rec = recording
#         # If the recording is on, add the frame to the video
#         if rec:
#             img_array.append(frame)
#             #out.write(frame)
#             print(f"Recording {streaming} {len(img_array)}")
#         #print(streaming, recording, rec)
#         # Yield the JPEG frame
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

# @gzip.gzip_page
# def video_feed(request):
#     return StreamingHttpResponse(gen(recording), content_type='multipart/x-mixed-replace; boundary=frame')

# def start_stream(request):
#   global streaming
#   streaming = True
#   print("Streaming started")
#   return HttpResponse('Stream started')

# def stop_stream(request):
#   global streaming
#   streaming = False
#   print("Streaming Stopped")
#   return HttpResponse('Stream stopped')

# def rec_on(request):
#   global recording
#   recording = True
#   print("Recording Started")
#   Motor.rotate(degrees=360, delay=0.01)
#   # Set the timer for 5 seconds
#   sleep(5)
#   recording = False
#   # Redirect to the rec_stop route to stop the recording
#   return redirect('rec_off')

# def rec_off(request):
#   global recording
#   recording = False
#   FolderName = request.session.get('selectedFolder')
#   out = cv2.VideoWriter(f"static/StoredData/{FolderName}/exam1.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 24, (640, 480))
  
#   for i, img in enumerate(img_array):
#     out.write(img)
#   out.release()
#   print(len(img_array))
#   img_array.clear()
#   print("Recording Stopped")
#   return HttpResponse('Recording stopped')
