from imageai.Detection import ObjectDetection
import os,sys,time,re

tempDir = 'C:\\Users\\Kevin\\Desktop\\temp\\'
modelFilePath = "C:\\Users\\Kevin\\Desktop\\2202 project\\yolo-tiny.h5"
img_file_name = sys.argv[1]

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(modelFilePath)
detector.loadModel(detection_speed="fastest")

def detectObject(img_file_name):
	detections = detector.detectObjectsFromImage(input_image=os.path.join(tempDir , img_file_name), output_image_path=os.path.join(tempDir , img_file_name+"_output.jpg"))
	
	detectedObjects = ""
	detectedObjectsList = []

	for eachObject in detections:
		# print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
		if eachObject["name"] not in detectedObjectsList:
			detectedObjectsList.append(eachObject["name"])
			detectedObjects += eachObject["name"]

			if len(detections) > 1:
				detectedObjects += ' '

    #Rename the file to object detected
	print(detectedObjects)
	imageFileName = re.sub(r'.*\\', '',img_file_name)
	os.rename(os.path.join(tempDir , img_file_name+"_output.jpg"), tempDir+imageFileName+';'+detectedObjects+'.jpg')

detectObject(img_file_name)

