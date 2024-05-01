# Multiscribe

**Last updated 01 May 2024**

**Author:** nsamways

This script utilizes OpenAI's Whisper to transcribe specific media files within a specified directory. It can handle various media formats, including mp3, mp4, opus, mod, and wma.

## Getting Started

To run the application locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required Python dependencies listed in `requirements.txt` using `pip install -r requirements.txt`.
3. Run from the command line using the following syntax: `python scribe.py [options]`


**Options**

* `-i`, `--input`: (Optional) Specify the directory containing the media files you want to transcribe. Defaults to the current directory (./).
* `-o`, `--output`: (Optional) Specify the directory to store the generated transcripts. Defaults to the same directory as the media files.
* `-m`, `--model`: (Optional) Specify the Whisper language model to use for transcription. Defaults to "base". Available models include "tiny-en", "base", and "large".
* `-p`, `--processor`: (Optional) Specify the processor to use for Whisper. Defaults to "CPU". Will try to use cuda (GPU) if "g" specified.

**Example Usage**

To transcribe media files in the current directory using the "base" model and write the transcripts to a new folder named "transcripts", use the following command:

```
python scribe.py -o transcripts -m base
```

**Output**

The script generates two outputs:

1. **Transcript Files:** For each media file, a transcript file with a `.txt` extension is created in the specified output directory (or the same directory as the media file if no output directory is provided). The transcript file contains timestamps and the corresponding transcribed text for each segment in the audio.
2. **Log File:** A log file named "log.txt" is created in the output directory (or the current directory if no output directory is specified). This file logs details about the configuration used (input directory, output directory, Whisper model, processor) and the processing time for each media file.


**Further Notes**

* This script relies on ffmpeg for audio extraction. Ensure ffmpeg is installed and accessible from the command line. 
* By default, the script uses the CPU for processing. You can attempt to use GPU usage with the `-p g` option.
