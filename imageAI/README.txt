Done
	1. Object detection on image(s)
	2. Extraction of images
	3. Calling of imageAI script
	4. getting output from script to autopsy
	5. Facial recognition
	6. Video analysis
	
To Do
	*Report + Video (7 Nov)
	1. Integrate video analysis
	2. 
	3. 
		
To Do Backlog
	1. remove useless code/comments
	2. test on a real disk image + duration
	3. additional module options (e.g image/video only or specify video cut intervals)
	4. user input error checks (e.g user specifying wrong target image)
	
Updates (01/11)
	- Added facial recognition
		1. User can choose to include this submodule/function? when analysing images (checkbox)
		2. User choose a target face image via autopsy GUI
		3. module will analyse all images in the temp folder for the face specified
		4. results is in the 'facial recognition' column as 'MATCH' or 'NIL'
	- Temp images are now extracted to os.tempDir/extracted_images (user's tmp folder might have his own img files)	
