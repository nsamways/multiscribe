'''
Created on 26 Jul 2023
Last updated 16 Apr 2024

@author: nsamways
'''

import os
import whisper
import ffmpeg
import argparse
import time
    
# Function to recursively search for media files in the current directory
def search_files(directory):
    
    media_files = []
    
    # create a list of filetypes to search for 
    media_types = ['.mp3','.mp4','.opus', '.mod', '.wma']
    
    for root, _, files in os.walk(directory):
        for file in files:
            if (os.path.splitext(file)[1].lower()) in media_types:
                media_files.append(os.path.join(root, file))
    
    return media_files

# Function to extract audio from media using python-ffmpeg
def extract_audio(media_file):
    
    c_durr = None
    # check if the file already exists. If not, create it
    audio_file = media_file[:-4] + ".wav"
    
    if not os.path.isfile(audio_file):
        
        # doesn't exist, so create
        print("Creating {} ... ".format(audio_file))
        
        c_start = time.perf_counter()
        
        stream = ffmpeg.input(media_file)
        stream = ffmpeg.output(stream, audio_file, loglevel="quiet")
        ffmpeg.run(stream)
        
        c_durr = time.perf_counter() - c_start

    return (c_durr, audio_file)


# Function to generate transcript using OpenAI's Whisper
def generate_transcript(audio_file, lang_model, processor):
    
    # check if model already exists
    try:
        model
    except NameError:
        # doesn't exist, so create it
        print("Loading model")
        model = whisper.load_model(lang_model, device=processor)
 
    print("Generating transcript")

    t_start = time.perf_counter()
    transcript = model.transcribe(audio_file, fp16=False, language='English')
    t_durr = time.perf_counter() - t_start
    
    return (t_durr, transcript)
    
def time_format(num_seconds):
    
    hours = num_seconds // 3600
    num_seconds %= 3600
    mins = num_seconds // 60   
    secs = num_seconds % 60
    
    hms_time = str('{:0>2.0f}'.format(hours)) + ":" + str('{:0>2.0f}'.format(mins)) + ":" + str('{:0>2.0f}'.format(secs))
    
    return (hms_time)
    ''' take a time in seconds as a float and return a string in H:M:S format. '''
        

def main():
       
    '''Uses OpenAI's whisper program to transcribe multiple video files.'''
    
    # use the arguments passed throught the command line to set variables/flags 
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--input", help="Folder root for video files.")
    parser.add_argument("-o", "--output", help="Output folder for transcripts. Default is same folder as video.")
    parser.add_argument("-m", "--model", help="Language model for Whisper. Default is 'tiny-en'.")
    parser.add_argument("-p", "--processor", help="Processor usage. If option 'g' try using GPU, if 'c' force CPU")

    args = parser.parse_args()

    input_path = args.input if args.input else "./"
    output_path = args.output if args.output else  "./"
    whisper_model = args.model if args.model else "base"
    proc_type = "cuda" if args.processor == "g" else "cpu" 

    # search for 
    media_files = search_files(input_path)

    # media file list

    if media_files:
        # there are some media files so set everything up
        if output_path:
            # create a new folder for the transcripts
            custom_output = True
   
            new_path = output_path
             
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            
            # create the ouptput file      
            f =  open((os.path.join(new_path, r'./log.txt')), 'w')
            f.write("\n Results")
      
            
        else:
            # just create the logfile

            f = open(r'./log.txt', 'w')
            f.write("\n Results2")
      
        # write the configuration to the log file
            
        f.write("\n Input root: " +  input_path)
        f.write("\n Output base: " +  output_path)
        f.write("\n Whisper model: " +  whisper_model)
        f.write("\n Processor: " +  proc_type)
        
        f.flush()    
        # generate base for transcript output    
        
        # process file list accordingly
        for media_file in media_files:
            
            (cv_duration, audio_file) = extract_audio(media_file)
            (tr_duration, transcript) = generate_transcript(audio_file, whisper_model, proc_type)
            
            # write details to log file
            if cv_duration:
                f.writelines("\n " + media_file + " Converstion time: " + time_format(cv_duration) + " Transcription time: " + time_format(tr_duration))
    
            else:
                f.writelines("\n " + media_file + " Transcription time: " + time_format(tr_duration))
                
            # output transcript
            segments = transcript["segments"]

            if custom_output:
                
                head_tail = os.path.split(media_file)
                new_head = head_tail[1][:-4] + ".txt"
                tr_out_path = os.path.join(new_path, new_head)
                    
            else:
                tr_out_path = media_file[:-4] + ".txt"
            
                        
            with open(tr_out_path ,'w') as g: 
                                
                for identifier_number in segments:
                    g.writelines(time_format(identifier_number["start"]) + " - " + time_format(identifier_number["end"]) + ": " + identifier_number["text"] + "\n")

        # close the log file
        f.close()
                
    else:
        
        print("No Media files found. Exiting.")        
        

    
    
if __name__ == '__main__':
    main()

