from imageai.Detection import VideoObjectDetection
import os,sys
from matplotlib import pyplot as plt

execution_path = os.getcwd()
video_detector = VideoObjectDetection()
video_detector.setModelTypeAsTinyYOLOv3()
video_detector.setModelPath(os.path.join(execution_path, "yolo-tiny.h5"))
video_detector.loadModel()

video_file_name = sys.argv[1]

def forSecond(frame_number, output_arrays, count_arrays, average_count, returned_frame):
    counter = 0
    for eachItem in average_count:
        counter += 1
        print (eachItem + " ")

def VideoObject(video_file_name):
    video_detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, video_file_name), output_file_path=os.path.join(execution_path, "video_second_analysis") ,  frames_per_second=20, per_second_function=forSecond,  minimum_percentage_probability=30, return_detected_frame=True, log_progress=False)

VideoObject(video_file_name)
