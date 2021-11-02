<h1 align="center"> Trying Hardest - Autopsy Media Analyser </h1>

The project aims to create plug-ins for the **Autopsy - Digital Forensics** platform.

### Image Analyser
- Object Detection and Identification for still images.
- Optional Facial Recognition.
- Based on ImageAI

### Video Analyser
- Object detection and identification on video files.
- Based on ImageAI

### AudioToText
- Audio to text transcription.
- Based on DeepSpeech

#### Project Folder Structure 
```
.
├── DeepSpeech/         # AudioToText plugin
├── Java/               # Scrapped Java plugin
├── VideoAI/            # Video Analyser plugin
│   └── models/         # imageAI pretrained model
├── imageAI/            # Image Analyser plugin
│   └── models/         # imageAI pretrained model
├── sample/             # Sample test data
└── README.md
```
## Platform Requirements
#### Tested and developed on
- Microsoft Windows 10
- Autopsy `4.19.1`
- Java `1.8` 64-bit
- Python `3.7`

#### Key validated Python libraries
> Versions and dependencies are listed within the installation guide
- Tensorflow `2.4.0`
- ImageAI `2.1.6`
- Face_recognition `1.3.0`
- DeepSpeech `0.9.3`

#### Validated Models
- ImageAI v1.0
  - [yolo-tiny.h5](https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0)
- DeepSpeech v0.9.3
  - [deepspeech-0.9.3-models.pbmm](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3)
  - [deepspeech-0.9.3-models.scorer](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3)

## Prerequisites - Installing the support files
Due to potential conflicts in dependency versions it is **highly** recommended that you install the following files in the provided sequence.

### 1. The basics
#### Python Dependencies
```
pip install --upgrade pip
```
```
pip install wheel cmake
```

### 2. Image Analyser / Video Analyser
#### Python Dependencies
```
pip install tensorflow==2.4.0 keras==2.4.3 numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 opencv-python keras-resnet==0.2.0 imageai
```
#### Others
- The ImageAI model has been **pre-bundled**
- If you wish to replace the bundled model you can do so at the plugin sub-directory `./imageAI/models/yolo-tiny.h5` and `./VideoAI/models/yolo-tiny.h5`

### 3. Facial Recognition for Image Analyser
#### Python Dependencies
 ```
 pip install face_recognition
 ```
> If the install fails on **Windows** when installing `dlib` please install [Microsoft C++ (MSVC) compiler toolset](https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-160)
 
### 4. AudioToText
#### Python Dependencies
```
pip install deepspeech pydub webrtcvad
```
#### Others
- [**FFMPEG**](https://www.ffmpeg.org/download.html) to support conversion between `.mp3` to `.wav` for processing
- **DeepSpeech** Model to be downloaded and selected when prompted
  - [deepspeech-0.9.3-models.pbmm](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3)
  - [deepspeech-0.9.3-models.scorer](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3)

## Installation & Getting Started
1. Either download via
    - The release bundle [INSERT LINK HERE](http://github.com)
    - Or any other method e.g `git`
    
2. Move the following folders into the **Autopsy Python plugin directory**
    - `DeepSpeech`
    - `VideoAI`
    - `imageAI`
    > Plugin directory on **Windows** is `%appdata%\autopsy\python_modules\`
  
    Your directory tree should now look like
  
    ```
    python_modules\
    ├── DeepSpeech\         # AudioToText plugin
    ├── VideoAI\            # Video Analyser plugin
    └── imageAI\            # Image Analyser plugin
    ```

3. Ensure **DeepSpeech** Models have been downloaded as per [Prerequisites - 4. AudioToText](https://github.com/junhui-f/ICT2202-DF-Assignment_One#others)

4. Launch Autopsy!
