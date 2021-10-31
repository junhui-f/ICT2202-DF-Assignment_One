from imageai.Detection import VideoObjectDetection
import os,sys
from matplotlib import pyplot as plt

execution_path = os.getcwd()
color_index = {'bus': 'red', 'handbag': 'steelblue', 'giraffe': 'orange', 'spoon': 'gray', 'cup': 'yellow', 'chair': 'green', 'elephant': 'pink', 'truck': 'indigo', 'motorcycle': 'azure', 'refrigerator': 'gold', 'keyboard': 'violet', 'cow': 'magenta', 'mouse': 'crimson', 'sports ball': 'raspberry', 'horse': 'maroon', 'cat': 'orchid', 'boat': 'slateblue', 'hot dog': 'navy', 'apple': 'cobalt', 'parking meter': 'aliceblue', 'sandwich': 'skyblue', 'skis': 'deepskyblue', 'microwave': 'peacock', 'knife': 'cadetblue', 'baseball bat': 'cyan', 'oven': 'lightcyan', 'carrot': 'coldgrey', 'scissors': 'seagreen', 'sheep': 'deepgreen', 'toothbrush': 'cobaltgreen', 'fire hydrant': 'limegreen', 'remote': 'forestgreen', 'bicycle': 'olivedrab', 'toilet': 'ivory', 'tv': 'khaki', 'skateboard': 'palegoldenrod', 'train': 'cornsilk', 'zebra': 'wheat', 'tie': 'burlywood', 'orange': 'melon', 'bird': 'bisque', 'dining table': 'chocolate', 'hair drier': 'sandybrown', 'cell phone': 'sienna', 'sink': 'coral', 'bench': 'salmon', 'bottle': 'brown', 'car': 'silver', 'bowl': 'maroon', 'tennis racket': 'palevilotered', 'airplane': 'lavenderblush', 'pizza': 'hotpink', 'umbrella': 'deeppink', 'bear': 'plum', 'fork': 'purple', 'laptop': 'indigo', 'vase': 'mediumpurple', 'baseball glove': 'slateblue', 'traffic light': 'mediumblue', 'bed': 'navy', 'broccoli': 'royalblue', 'backpack': 'slategray', 'snowboard': 'skyblue', 'kite': 'cadetblue', 'teddy bear': 'peacock', 'clock': 'lightcyan', 'wine glass': 'teal', 'frisbee': 'aquamarine', 'donut': 'mincream', 'suitcase': 'seagreen', 'dog': 'springgreen', 'banana': 'emeraldgreen', 'person': 'honeydew', 'surfboard': 'palegreen', 'cake': 'sapgreen', 'book': 'lawngreen', 'potted plant': 'greenyellow', 'toaster': 'ivory', 'stop sign': 'beige', 'couch': 'khaki'}

resized = False
video_detector = VideoObjectDetection()
video_detector.setModelTypeAsTinyYOLOv3()
video_detector.setModelPath(os.path.join(execution_path, "yolo-tiny.h5"))
video_detector.loadModel()

video_file_name = sys.argv[1]
result = sys.argv[2]

def forSecond(frame_number, output_arrays, count_arrays, average_count, returned_frame):

    plt.clf()
    this_colors = []
    labels = []
    sizes = []
    counter = 0
    # This part onward is to find the number of objects in the frame and save it in textfile
    for eachItem in average_count:
        counter += 1
        labels.append(eachItem + " = " + str(average_count[eachItem]))
        print (eachItem + " = " + str(average_count[eachItem]))
        sizes.append(average_count[eachItem])
        this_colors.append(color_index[eachItem])
        with open( result+".txt", "a") as file_object:
            file_object.write(eachItem + " = " + str(average_count[eachItem]) + "\n")
            file_object.close()
    #####################################################################################

    # This part onward is to dislay chart in image
    global resized
    if (resized == False):
        manager = plt.get_current_fig_manager()
        manager.resize(width=1000, height=500)
        resized = True

    plt.subplot(1, 2, 1)
    plt.title("Second : " + str(frame_number))
    plt.axis("off")
    plt.imshow(returned_frame, interpolation="none")

    plt.subplot(1, 2, 2)
    plt.title("Analysis: " + str(frame_number))
    plt.pie(sizes, labels=labels, colors=this_colors, shadow=True, startangle=140, autopct="%1.1f%%")

    plt.pause(0.01)
    plt.savefig(result+".png")
    #############################################

def VideoObject(video_file_name):
    video_detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "traffic-minix.mp4"), output_file_path=os.path.join(execution_path, "video_second_analysis") ,  frames_per_second=20, per_second_function=forSecond,  minimum_percentage_probability=30, return_detected_frame=True, log_progress=True)

VideoObject(video_file_name)
plt.show()

#first argument = video
#second argument = result of filename to be save