import face_recognition
import os, sys

# python face_recog.py C:/users/Kevin/Desktop/psb.jpg C:/Users/Kevin/Desktop/faces

targetImgPath = sys.argv[1]
imageFolderPath = sys.argv[2]
imageName = sys.argv[3]

# print(targetImgPath, imageFolderPath)

known_image = face_recognition.load_image_file(targetImgPath)
unknown_image = face_recognition.load_image_file(imageFolderPath+'/'+imageName)

known_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([known_encoding], unknown_encoding,tolerance=0.45)

if results[0] == True:
	print('MATCH')
else:
	print('NIL')

