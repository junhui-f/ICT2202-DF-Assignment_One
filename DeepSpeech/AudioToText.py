from deepspeech import Model
from pydub import AudioSegment
import numpy as np
import os
import sys
import wave

# If additional file names are not provided
if len(sys.argv) == 1: 
	print("Usage: python AudioToText.py <filepath>")
	exit()

files = sys.argv[1:]
file_dir = os.path.dirname(os.path.abspath(__file__))

# Choose model and scorer, relative file path
model_file_path = 'models/deepspeech.pbmm'
lm_file_path = 'models/deepspeech.scorer'

beam_width = 100 # lower = faster, but less accurate. vice versa. 500 for accuracy, 100 for prod
lm_alpha = 0.93 # Language model weight; recommended values (as of v0.9.3 - en) 
lm_beta = 1.18 # Word insertion weight; recomended values (as of v0.9.3 - en)

# Class to redirect stderr to null, so that it doesn't print.
class SilenceStream():
    def __init__(self, stream):
        self.fd_to_silence = stream.fileno()

    def __enter__(self):
        self.stored_dup = os.dup(self.fd_to_silence)
        try: 
        	self.devnull = open('/dev/null', 'w') #on unix systems
        except:
        	self.devnull = open('nul', 'w') #on windows
        os.dup2(self.devnull.fileno(), self.fd_to_silence)

    def __exit__(self, exc_type, exc_value, tb):
        os.dup2(self.stored_dup, self.fd_to_silence)
        self.devnull = None
        self.stored_dup = None

def read_wav_file(filename):
	with wave.open(filename, 'rb') as w:
		rate = w.getframerate()
		frames = w.getnframes()
		buffer = w.readframes(frames)

	return buffer, rate 

def transcribe(audio_file):
	buffer, rate= read_wav_file(audio_file)
	data16 = np.frombuffer(buffer, dtype=np.int16)

	# REMOVES FILE - ONLY USE THIS IF REMOVING TEMPORARY FILES CREATED BY AUTOPSY.
	os.remove(audio_file)

	return model.stt(data16)

with SilenceStream(sys.stderr):
	model = Model(model_file_path)
	model.enableExternalScorer(lm_file_path)
	model.setScorerAlphaBeta(lm_alpha, lm_beta)
	model.setBeamWidth(beam_width)


# Iterate list of files
for file in files:

	# Convert MP3 / MP4 to WAV. REQUIRES FFMPEG
	if file.endswith('.mp3') or file.endswith('.mp4'):
		sound = AudioSegment.from_mp3(file)
		sound.export('temp.wav', format='wav')
		print(transcribe('temp.wav'))
		# f = open('transcribed.txt', "a+")
		# f.write('{"filename":"'+file+'", "text":"'+transcribe('temp.wav')+'"\n')
		# f.close()

	elif file.endswith('.wav'):
		print(transcribe(file))
		# f = open('transcribed.txt', 'a+')
		# f.write('{"filename":"'+file+'", "text":"'+transcribe(file)+'"}\n')
		# f.close()
	else:
		print("Error transcribing.")
