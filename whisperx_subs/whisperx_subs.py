import json
from transformers import pipeline
from tqdm import tqdm

def format_time_to_srt(time_value):
    """
    Converts a time value (in seconds) into SRT format string.
    """
    return "{:02}:{:02}:{:02},{:03}".format(
        int(time_value // 3600),
        int((time_value % 3600) // 60),
        int(time_value % 60),
        int((time_value % 1) * 1000)
    )

def format_segment_to_srt(index, start_time, end_time, text):
    """
    Converts given segment data into SRT format string using the format_time_to_srt function.
    """
    start_time_srt = format_time_to_srt(start_time)
    end_time_srt = format_time_to_srt(end_time)

    return "{}\n{} --> {}\n{}\n\n".format(index, start_time_srt, end_time_srt, text.strip())

def split_text_into_equal_segments(segment_text, n_segments):
    """
    Split the given text into a specific number of segments of roughly equal character length, 
    without splitting words.
    
    Parameters:
    - segment_text (str): The input text to split.
    - n_segments (int): The number of segments to split the text into.
    
    Returns:
    - list: A list of strings, each being a segment of the original text.
    """
    segments = []
    avg_segment_length = len(segment_text) // n_segments
    start_idx = 0
    end_idx = 0

    for _ in range(n_segments):
        end_idx = start_idx + avg_segment_length
        
        # If not the last segment, adjust end_idx to not split a word
        if _ < n_segments - 1:
            while end_idx < len(segment_text) and segment_text[end_idx] != ' ':
                end_idx += 1
        
        segments.append(segment_text[start_idx:end_idx].strip())
        start_idx = end_idx

    return segments

def convert_json_to_srt(json_str, max_char, translator_model=None):
    """
    Convert a given JSON string to SRT format.
    
    Parameters:
    - json_str (str): The JSON string containing segments and words data.
    - max_char (int): The maximum number of characters for each SRT segment.
    - translate (str): Language pair for translation, e.g., 'en-es'. Default is None.

    Returns:
    - str: The formatted SRT string.
    """

    # Parse the input JSON string.
    data = json.loads(json_str)
    
    srt_output = ""
    index = 1 
    start_word = 0
    end_word = 0
    source_lang = data["language"]

    # If translation is required, initialize the translation pipeline
    translator = None
    if translator_model:
        translator = pipeline('translation', model=translator_model)

    # Iterate over each segment in the data.
    for segment in tqdm(data["segments"], desc="Converting segments", ncols=100):
        words = segment['words']
        segment_text = segment['text']
        len_text = len(segment_text)

        # Determine the number of segments needed based on the max_char limit.
        n_segments = (len_text // max_char) + 1
        len_segment = len_text // n_segments
        text = ""

        # Translate the segment_text if required
        translated_segments = None
        if translator:
            translated_text = translator(segment_text, max_length=10000)[0]['translation_text']
            translated_segments = split_text_into_equal_segments(translated_text, n_segments)

        # Get the start time of the segment or use the end time of the last word if not available.
        start_time = segment.get('start', end_word)

        i_translated_segment = 0
        # Iterate over each word in the segment.
        for word_index, word in enumerate(words):
            start_word = word.get('start', end_word)
            end_word = word.get('end', start_word)

            # If adding the current word exceeds the character limit or it's the last word, finalize the segment.
            if len(text + word['word']) > len_segment or word_index == len(words) - 1:
                text += word['word']
                end_time = end_word
                
                if translated_segments:
                    srt_output += format_segment_to_srt(index, start_time, end_time, translated_segments[i_translated_segment])
                    i_translated_segment += 1
                else:
                    srt_output += format_segment_to_srt(index, start_time, end_time, text)
                
                index += 1
                text = ""
            else:
                if len(text) == 0:
                    start_time = start_word
                    
                if source_lang == "ja" or source_lang == "zh":
                    text += word['word']
                else:
                    text += word['word'] + " "

    return srt_output

