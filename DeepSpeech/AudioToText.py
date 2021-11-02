from deepspeech import Model
from pydub import AudioSegment
import numpy as np
import os
import sys
import wave
import webrtcvad
import contextlib

# If additional file names are not provided, or not all arguments are provided
if len(sys.argv) < 9:
    print("Usage: python AudioToText.py <Model(.pbmm) file path> <Scorer(.scorer) file path> <beam_width> <lm_alpha> <lm_beta> <EnableVAD?:[1/0]> <VADSTRICTNESS:[0-3]> <FilePath(s)>")
    exit()


""" 
    Arguments - Command Line

    sys.argv[0]: AudioToText.py
    sys.argv[1]: Model File Path
    sys.argv[2]: Scorer File Path
    sys.argv[3]: beam_width
    sys.argv[4]: lm_alpha
    sys.argv[5]: lm_beta
    sys.argv[6]: Enable Voice Activity Detection (VAD)
    sys.argv[7]: Voice Activity Detection Strictness 
    sys.argv[8]: File Path(s)

"""

files = sys.argv[8:]
file_dir = os.path.dirname(os.path.abspath(__file__))

# Model and Scorer file paths
model_file_path = sys.argv[1]
lm_file_path = sys.argv[2]

beam_width = int(sys.argv[3]) # lower = faster, but less accurate, vice versa.
lm_alpha = float(sys.argv[4]) # Language model weight; recommended values: 0.93 (as of v0.9.3 - en) 
lm_beta = float(sys.argv[5]) # Word insertion weight; recomended values: 1.18 (as of v0.9.3 - en)

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

class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.
    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.
    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n

def read_wav_file(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        sample_rate = wf.getframerate()
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate

def write_wave(path, audio, sample_rate):
    """Writes a .wav file.
    Takes path, PCM audio data, and sample rate.
    """
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)

def transcribe(buffer):
    """ 
    Reads Audio Buffer and transcribes
    """
    data16 = np.frombuffer(buffer, dtype=np.int16)
    
    return model.stt(data16)

with SilenceStream(sys.stderr):
    model = Model(model_file_path)
    model.enableExternalScorer(lm_file_path)
    model.setScorerAlphaBeta(lm_alpha, lm_beta)
    model.setBeamWidth(beam_width)

# The purpose of VAD is to save time from transcibing audio files that do not even have text in the first place.
vad = webrtcvad.Vad(3) # Integer 0-3; 0 least aggressive, 3 most.

# Iterate list of files
for file in files:

    # Initial Check: Are any of the files non mp3/wav?
    if not file.endswith('.mp3') and not file.endswith('.wav'):
        print("Invalid File type.")
        continue

    # Check file type. If its mp3, we need to convert it to wav for further processing
    if file.endswith('.mp3'):
        sound = AudioSegment.from_mp3(file)
        silence = AudioSegment.silent(duration=1000) # Silence padding to prevent cutoffs
        sound = silence + sound + silence
        sound.export('temp.wav', format='wav')
        file = 'temp.wav'
    
    containsSpeech = 0
    buffer, rate= read_wav_file(file)

    # VAD - To check if the audio file contains any speech for further processing.
    # The purpose of VAD is to not transcribe audio files that do not even have text in the first place.
    if int(sys.argv[6]) == 1:
        # Check Sample rate. We need it to be 8000/16000/32000/48000 for VAD. Convert to a wav with specific sample rate otherwise.
        if rate not in (8000, 16000, 32000, 48000):
            write_wave(os.path.join(file_dir,'temp2.wav'), buffer, 16000)
            buffer, rate = read_wav_file(os.path.join(file_dir,'temp2.wav'))

        vad = webrtcvad.Vad(int(sys.argv[7])) # Integer 0-3; 0 least strict, 3 most strict.
        frames = frame_generator(30, buffer, rate)
        frames = list(frames)
        for frame in frames:
            if vad.is_speech(frame.bytes, rate):
                containsSpeech = 1
                break

    if containsSpeech or int(sys.argv[6]) == 0:
        print(transcribe(buffer))
    else:
        print("Does not contain any speech.")

    # Clean Up
    try:
        os.remove('temp.wav')
    except:
        pass
    try:
        os.remove('temp2.wav')
    except:
        pass
