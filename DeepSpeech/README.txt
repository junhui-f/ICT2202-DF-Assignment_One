Requirements:

pip install requirements.txt
deepspeech-0.9.3-models.pbmm
deepspeech-0.9.3-models.scorer
ffmpeg

Please install FFMPEG so that .mp3/.mp4 can be converted to .wav
ffmpeg can be downloaded from https://github.com/BtbN/FFmpeg-Builds/releases
Models can be downloaded from https://github.com/mozilla/DeepSpeech/releases

Models COULD BE RENAMED to:
deepspeech.pbmm
deepspeech.scorer

and placed in a folder named models

e.g: ~/DeepSpeech/models/deepspeech.pbmm

Output:
  Under Analysis Results, "Transcribed Text: <transcribed text>"
  Searchable using Keyword Ingest.

python AudioToText.py <Model(.pbmm) file path> <Scorer(.scorer) file path> <beam_width> <lm_alpha> <lm_beta> <EnableVAD?:1/0> <VADSTRICTNESS:0~3> <FilePath(s)>

Usage:
Model File: The file path of the model file (.pbmm). 
  By default, path of model file is set to 'models/deepspeech.pbmm'
  
Scorer File: The file path of the scorer file (.scorer). 
  By default, path of scorer file is set to 'models/deepspeech.scorer'
  
Beam_width: Value used by the model, a larger beam width value generates better results at the cost of decoding time. 
  By default, the value of Beam_width is set to 500.
  
lm_alpha: Language Model weight. 
  By default, the value of lm_alpha is set to 0.93.
  
lm_beta: Word insertion weight. 
  By default, the value of lm_beta is set to 1.18.
  
Enable VAD: Voice Activity Detection. When enabled, attempts to only transcribe audio files that might contain speech, rather than every audio file.
  By default, VAD is enabled, and strictness set to 3.
  Strictness value ranges from 0~3, a lower strictness value generates better results at the cost of decoding time.
