### Description

This script takes in an audio file and outputs a subtitle file in the SRT format. Your SRT format could be imported as a subtitle track in DaVinci. In the future, you can have the subtitles programmatically inserted at key timeframes as Text+ elements which allows for more dramatic text.

## Installation

To install the required package, run:
```bash
pip install openai-whisper
```

Also make sure ffmpeg is installed on your machine.

## Usage (Adjustment)

You can choose the model and device to use in the `chosen_processor.py` file.

| Size      | Parameters | English-only | Multilingual |
|-----------|------------|--------------|--------------|
| tiny      | 39 M       | ✓            | ✓            |
| base      | 74 M       | ✓            | ✓            |
| small     | 244 M      | ✓            | ✓            |
| medium    | 769 M      | ✓            | ✓            |
| large     | 1550 M     | x            | ✓            |
| large-v2  | 1550 M     | x            | ✓            |

Then add where the wav or mp3 file with speech is at. Then add where you want to save the SRT file to. For example, adjust in `transcribe_audio/generate.py`:

```
INPUT_AUDIO="eleven_labs.mp3"
OUTPUT_DIR="./" # Eg. ./
OUTPUT_FILENAME_W_EXT="eleven_labs.srt"
```

## Usage

To transcribe audio, use the following command:
```bash
python generate.py
```

Then look for the srt file in the output folder you've set in the script.

### FAQ

Q: Since Whisper is made by OpenAI, do I need an OpenAI API Key?
A: No.

Q: What are alternatives to OpenAI Whisper?
A: Hugging Face's Transformers, Mozilla DeepSpeech, Google Speech-to-Text, IBM Watson Speech to Text, Microsoft Azure Speech to Text, and Amazon Transcribe.