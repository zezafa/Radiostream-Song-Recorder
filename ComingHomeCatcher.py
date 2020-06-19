"""
    song ripper
    remember to play audio in background
"""

import pyaudio 
import audioop
import sys
import math
import wave
import time
import glob, os
import urllib
from bs4 import BeautifulSoup
import re


# Insert url for a radio stream of your choice in order to scan for a hit tag
URL = "www.yourURLforRadioStream.com"

# Name of song to look after
HIT_TAG = "Coming"

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 300 # Assuming the song is shorter than 300 seconds

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print str(i)+'. '+dev['name']
        i += 1

def record_10min():
    WAVE_OUTPUT_FILENAME = "potentialSong_" + str(len(glob.glob("potentialSong*"))) + ".wav"

    # Use list_devices() to list all your input devices
    device = 2  
    
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
                    #,input_device_index = device)
    
    print "Recording..."
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        
    print "** Finished recording **"

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def check_comingHome():
    page = urllib.urlopen(URL)
    soup = BeautifulSoup(page.read(), "lxml")
    #print soup
    searchAfter = HIT_TAG
    
    if len(soup(text=re.compile(searchAfter))) > 0:
        print
        print "Potential Hit"
        record_10min()
    
if __name__ == '__main__':
    print
    print "Domain: " + URL + "\n"
    print "Searching for: " + HIT_TAG
    print
    while True:
        check_comingHome()
        spinner = spinning_cursor()
        for _ in range(50):
            _msg = spinner.next() + " Listening to background and scrapping domain for hit tag."
            sys.stdout.write(_msg)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b'*len(_msg))
        
    
