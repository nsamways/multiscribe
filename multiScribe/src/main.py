'''
Created on 26 Jul 2023

@author: nsamways
'''

import sys
import os
import subprocess
import whisper

    
# Function to recursively search for MP4 files in the current directory
def search_files(directory):
    mp4_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4"):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

# Function to extract audio from MP4 using python-ffmpeg
# rewrite this to use native binding
def extract_audio(mp4_file):
    wav_file = mp4_file[:-4] + ".wav"
    ffmpeg.input(mp4_file)
    audio_file = ffmpeg.output()
#    subprocess.call(["ffmpeg", "-i", mp4_file, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_file])
    return audio_file


# Function to generate transcript using OpenAI's Whisper ASR API
def generate_transcript(audio_file):
    model = whisper.load_model("small.en")
    transcript = model.transcribe(audio_file)
    return transcript

# Main function to process MP4 files and generate transcripts
def process_files(directory):
    mp4_files = search_files(directory)
    for mp4_file in mp4_files:
        audio_file = extract_audio(mp4_file)
        transcript = generate_transcript(audio_file)
        print(f"Transcript for {mp4_file}:")
        print(transcript)
        print()

def main():

# Provide the directory path where you want to search for MP4 files

# use the info passed throught the command line, or use cwd as defauly
    
    directory_path = "./"
    process_files(directory_path)
    
if __name__ == '__main__':
    main()


