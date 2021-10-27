from imageai.Detection import ObjectDetection
import os,sys

execution_path = 'C:\\Users\\Kevin\\Desktop\\temp'
img_file_name = sys.argv[1]

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath("C:\\Users\\Kevin\\Desktop\\2202 project\\yolo-tiny.h5")
detector.loadModel(detection_speed="fastest")

def detectObject(img_file_name):
	print("Detecting: " + img_file_name)	
	detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , img_file_name), output_image_path=os.path.join(execution_path , img_file_name+"_output.jpg"))
	for eachObject in detections:
	    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )

# img_file_names = 

# for img_file_name in img_file_names:
detectObject(img_file_name)


# from imageai.Classification import ImageClassification
# import os

# execution_path = os.getcwd()

# prediction = ImageClassification()
# prediction.setModelTypeAsDenseNet()
# prediction.setModelPath( os.path.join(execution_path , "DenseNet-BC-121-32.h5"))
# prediction.loadModel()

# predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, "kitchen.jpg"), result_count=5 )
# for eachPrediction, eachProbability in zip(predictions, probabilities):
#     print(eachPrediction , " : " , eachProbability)

