'''
Created on 26 Jul 2023

@author: nsamways
'''

import sys
import os
import whisper
import json
import ffmpeg

    
# Function to recursively search for MP4 files in the current directory
def search_files(directory):
    mp4_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4"):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

# Function to extract audio from MP4 using python-ffmpeg
def extract_audio(mp4_file):
    
    # check if the file already exists. If not, create it
    audio_file = mp4_file[:-4] + ".wav"
    
    if os.path.isfile(audio_file):
    
        stream = ffmpeg.input(mp4_file)
        stream = ffmpeg.output(stream, audio_file)
        ffmpeg.run(stream)

    return audio_file


# Function to generate transcript using OpenAI's Whisper
def generate_transcript(audio_file, lang_model):
    model = whisper.load_model("small.en")
    transcript = model.transcribe(audio_file, fp16=False, language='English')
    return transcript

# Main function to process MP4 files and generate transcripts
def process_files(directory):
    mp4_files = search_files(directory)
    for mp4_file in mp4_files:
        audio_file = extract_audio(mp4_file)
        transcript = generate_transcript(audio_file, w_model)
        print(f"Transcript for {mp4_file}:")
        print(transcript)
        print()

def main():

# Provide the directory path where you want to search for MP4 files

# use the info passed throught the command line, or use cwd as defauly
    for arg in (len(sys.argv):
        
        if cl_arg = "-m":
            
    
    directory_path = "./"
    process_files(directory_path)

    

    
if __name__ == '__main__':
    main()


