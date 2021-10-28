Requirements:

pip install requirements.txt
deepspeech-0.9.3-models.pbmm
deepspeech-0.9.3-models.scorer
ffmpeg

Please install FFMPEG so that .mp3/.mp4 can be converted to .wav
Models can be downloaded from https://github.com/mozilla/DeepSpeech/releases

Models MUST BE RENAMED to:
deepspeech.pbmm
deepspeech.scorer

and placed in a folder named models

e.g: ~/DeepSpeech/models/deepspeech.pbmm

Output:
output.txt:
  Debug statements
  
transcribed.txt
  json objects
  syntax: {"filename":"example.wav", "text":"hello world"}
  

