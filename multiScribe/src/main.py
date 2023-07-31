'''
Created on 26 Jul 2023

@author: nsamways
'''

import sys
import os
import whisper
import json
import ffmpeg
import argparse
    
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
    
    if not os.path.isfile(audio_file):
        
        # doesn't exist, so create
        stream = ffmpeg.input(mp4_file)
        stream = ffmpeg.output(stream, audio_file)
        ffmpeg.run(stream)

    return audio_file


# Function to generate transcript using OpenAI's Whisper
def generate_transcript(audio_file, lang_model):
    model = whisper.load_model(lang_model)
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

# use the info passed throught the command line, or use cwd as defauly
    

    parser = argparse.ArgumentParser()

    #-db DATABSE -u USERNAME -p PASSWORD -size 20
    parser.add_argument("-i", "--input", help="Folder root for video files.")
    parser.add_argument("-o", "--output", help="Output folder for transcripts. Default is same folder as video.")
    parser.add_argument("-m", "--model", help="Language model for Whisper. Default is 'tiny-en'.")

    args = parser.parse_args()

    print( "input {} output {} model  ".format(
        args.input,
        args.output,
        args.model
        ))
            
    
    directory_path = "./"
    process_files(directory_path)

    

    
if __name__ == '__main__':
    main()


