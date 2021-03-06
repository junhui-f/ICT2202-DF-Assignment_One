from imageai.Detection import ObjectDetection
import os,sys,time,re

img_file_name = sys.argv[1]
tempDir = sys.argv[2]
modelFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models\yolo-tiny.h5')

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(modelFilePath)
detector.loadModel(detection_speed="fastest")

def detectObject(img_file_name):
	detections = detector.detectObjectsFromImage(input_image=os.path.join(tempDir , img_file_name), output_image_path=os.path.join(tempDir , img_file_name+"_output.jpg"))

	detectedObjects = ""
	detectedObjectsList = []
	
	#Detect object in the image, ignore duplicate objects
	for eachObject in detections:
		if eachObject["name"] not in detectedObjectsList:
			detectedObjectsList.append(eachObject["name"])
			detectedObjects += eachObject["name"]

			if len(detections) > 1:
				detectedObjects += ' '
				
	#If no objects detected, mark it as unknown
	if len(detections) == 0:		
		detectedObjects = 'Unknown'	

	print(detectedObjects)
	#Rename the file to object detected
	imageFileName = re.sub(r'.*\\', '',img_file_name)
	os.rename(os.path.join(tempDir , img_file_name+"_output.jpg"), tempDir+imageFileName+';'+detectedObjects+'.jpg')

detectObject(img_file_name)
