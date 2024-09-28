import os
import whisper
from whisper.utils import get_writer
from chosen_model_parameters import MODEL, DEVICE

# _ADJUST relative input audio, desired output directory, and desired output basename with file extension 1 of 2
INPUT_AUDIO="eleven_labs.mp3"
OUTPUT_DIR="./" # Eg. ./
OUTPUT_FILENAME_W_EXT="drop_subtitle_media.srt"

try:
    print("Load Whisper model:", )
    whisper_model = whisper.load_model(MODEL, device=DEVICE)  # For CPU processing
    # Detailed timestamps for when each word was spoken in the audio to help DaVinci timeline with syncing
    print(f"Read {INPUT_AUDIO} and create the subtitle file {OUTPUT_DIR}{OUTPUT_FILENAME_W_EXT}")
    transcription_result = whisper_model.transcribe(audio=INPUT_AUDIO, initial_prompt="prompt", word_timestamps=True)

    # _ADJUST 2 of 2: max_line_count and max_line_width
    # Word formatting options
    # highlight_words: Underline each word as it is spoken in srt and vtt
    # More options at: https://github.com/openai/whisper/blob/main/whisper/transcribe.py
    
    # 1/15 = 0-1 secs per subtitle screen
    # 2/15 = 1 secs per subtitle screen
    # 3/15 = 1-2 secs per subtitle screen
    # 1/30 = 1-2 secs per subtitle screen # /30 is reasonable for Text+ with OpenSans Size .09
    # 2/30 = 2-3 secs per subtitle screen # /35 is widest for Text+ with OpenSans Size .09
    # 3/30 = 3-4 secs per subtitle screen
    # 1/40 = 1-2 secs per subtitle screen
    # 2/40 = 3-4 secs per subtitle screen
    # 3/40 = 6 secs per subtitle screen
    # 1/45 = 1-2 secs per subtitle screen
    # 2/45 = 3-4 secs per subtitle screen
    # 3/45 = 6 secs per subtitle screen
    # 1/50 = 2 secs per subtitle screen
    # 2/50 = 4 secs per subtitle screen
    # 3/50 = 6-7 secs per subtitle screen
    # 1/55 = 2-3 secs per subtitle screen
    # 2/55 = 4-5 secs per subtitle screen
    # 3/55 = 7-8 secs per subtitle screen
    # 1/60 = 2-3 secs per subtitle screen
    # 2/60 = 6-7 secs per subtitle screen
    # 3/60 = 10-13 secs per subtitle screen
    # 1/65 = 3-4 secs per subtitle screen
    # 2/65 = 7-9 secs per subtitle screen
    # 3/65 = 11-13 secs per subtitle screen
    word_formatting = {
        "highlight_words": False,
        "max_line_count": 1,
        "max_line_width": 30
    }

    write_to_dir = get_writer("srt", os.path.dirname(OUTPUT_DIR))
    write_to_dir(transcription_result, os.path.basename(OUTPUT_FILENAME_W_EXT), word_formatting)

except Exception as e:
    print("Error transcribing audio:", e)
else:
    print(f"\nTranscription completed. Check the output file: {OUTPUT_DIR}{OUTPUT_FILENAME_W_EXT}")
