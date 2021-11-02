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



## Installation
Due to potential conflicts in dependency versions it is **highly** recommended that you install the following files in the provided sequence.

### 1. The basics
#### Python Dependencies
```
pip install --upgrade pip
```
```
pip install wheel cmake
```

### 2. Image Analyser
#### Python Dependencies
```
pip install tensorflow==2.4.0 keras==2.4.3 numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 opencv-python keras-resnet==0.2.0 imageai
```

### 3. Video Analyser
#### Python Dependencies
 ```
 pip install face_recognition
 ```
>If the install fails on **Windows** please install
>
>https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-160

### 4. AudioToText
#### Python Dependencies
```
pip install deepspeech pydub webrtcvad
```
#### Others
- ffmpeg https://www.ffmpeg.org/download.html
- deepspeech model https://github.com/mozilla/DeepSpeech/releases
