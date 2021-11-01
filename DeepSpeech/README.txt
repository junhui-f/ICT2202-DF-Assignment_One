Requirements:

pip install requirements.txt
deepspeech-0.9.3-models.pbmm
deepspeech-0.9.3-models.scorer
ffmpeg

Please install FFMPEG so that .mp3/.mp4 can be converted to .wav
ffmpeg can be downloaded from https://github.com/BtbN/FFmpeg-Builds/releases
Models can be downloaded from https://github.com/mozilla/DeepSpeech/releases

Models MUST BE RENAMED to:
deepspeech.pbmm
deepspeech.scorer

and placed in a folder named models

e.g: ~/DeepSpeech/models/deepspeech.pbmm

Output:
  Under Analysis Results, "Transcribed Text: <transcribed text>"
  Searchable using Keyword Ingest.


TODO:

Allow user to set verbosity (see: AudioToText.py vars [
Allow user to choose model, scorer locations
Allow user to choose ffmpeg++ locations (tentative)
