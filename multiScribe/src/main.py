'''
Created on 26 Jul 2023

@author: nsamways
'''

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
def generate_transcript(audio_file, lang_model, processor):
    
    # check if model already exists
    model = whisper.load_model(lang_model)
    transcript = model.transcribe(audio_file, fp16=False, language='English')
    return transcript


def main():
    
    '''Uses OpenAI's whisper program to transcribe multiple video files.'''

    # use the arguments passed throught the command line to set variables/flags 
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--input", help="Folder root for video files.")
    parser.add_argument("-o", "--output", help="Output folder for transcripts. Default is same folder as video.")
    parser.add_argument("-m", "--model", help="Language model for Whisper. Default is 'tiny-en'.")
    parser.add_argument("-p", "--processor", help="Processor usage. If option 'g' try using GPU, if 'c' force CPU")

    args = parser.parse_args()

    input_path = args.input if args.input else input_path = "./"
    output_path = args.output if args.output else output_path = None
    whisper_model = args.model if args.model else whisper_model = "tiny-en"
    proc_type = "cuda" if args.processor == "g" else proc_type = "cpu" 

    print( "input {} output {} model  ".format(
        args.input,
        args.output,
        args.model,
        args.proc_type
        ))
    
    # get file list
    mp4_files = search_files(input_path)
    
    # process file list accordingly
    for mp4_file in mp4_files:
        audio_file = extract_audio(mp4_file)
        transcript = generate_transcript(audio_file, whisper_model, proc_type)
        
        print(f"Transcript for {mp4_file}:")
        print(transcript)

    
if __name__ == '__main__':
    main()


