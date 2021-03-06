from imageai.Detection import VideoObjectDetection
import os,sys
from matplotlib import pyplot as plt

execution_path = os.getcwd()
video_detector = VideoObjectDetection()
video_detector.setModelTypeAsTinyYOLOv3()
video_detector.setModelPath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models\yolo-tiny.h5'))
video_detector.loadModel()

video_file_name = sys.argv[1]
detectedObjectsList = []

def forSecond(frame_number, output_arrays, count_arrays, average_count, returned_frame):
	#Detect object in the image, ignore duplicate objects
    for eachItem in average_count:
        if eachItem not in detectedObjectsList:
            detectedObjectsList.append(eachItem)
            print (eachItem + " ")

def VideoObject(video_file_name):
    video_detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, video_file_name), output_file_path=os.path.join(execution_path, "video_second_analysis") ,  frames_per_second=20, per_second_function=forSecond,  minimum_percentage_probability=30, return_detected_frame=True, log_progress=False)

VideoObject(video_file_name)
