import os
import whisper
from whisper.utils import get_writer
from transcribe_audio.chosen_model_parameters import MODEL, DEVICE

INPUT_AUDIO="eleven_labs.mp3"
OUTPUT_DIR="./" # Eg. ./
OUTPUT_FILENAME_W_EXT="eleven_labs.srt"

try:
    print("Load Whisper model:", )
    whisper_model = whisper.load_model(MODEL, device=DEVICE)  # For CPU processing
    # Detailed timestamps for when each word was spoken in the audio to help DaVinci timeline with syncing
    print(f"Read {INPUT_AUDIO} and create the subtitles file {OUTPUT_DIR}{OUTPUT_FILENAME_W_EXT}")
    transcription_result = whisper_model.transcribe(audio=INPUT_AUDIO, initial_prompt="prompt", word_timestamps=True)

    # Word formatting options
    # highlight_words: Underline each word as it is spoken in srt and vtt
    # More options at: https://github.com/openai/whisper/blob/main/whisper/transcribe.py
    word_formatting = {
        "highlight_words": False,
        "max_line_count": 2,
        "max_line_width": 15
    }

    write_to_dir = get_writer("srt", os.path.dirname(OUTPUT_DIR))
    write_to_dir(transcription_result, os.path.basename(OUTPUT_FILENAME_W_EXT), word_formatting)

except Exception as e:
    print("Error transcribing audio:", e)
else:
    print(f"Transcription completed. Check the output file: {OUTPUT_DIR}{OUTPUT_FILENAME_W_EXT}")
