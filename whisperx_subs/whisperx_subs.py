import json

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

def convert_json_to_srt(json_str, max_char):
    """
    Convert a given JSON string to SRT format.
    
    Parameters:
    - json_str (str): The JSON string containing segments and words data.
    - max_char (int): The maximum number of characters for each SRT segment.
    
    Returns:
    - str: The formatted SRT string.
    """
    
    # Parse the input JSON string.
    data = json.loads(json_str)

    srt_output = ""
    index = 1 
    start_word = 0
    end_word = 0

    # Iterate over each segment in the data.
    for segment in data["segments"]:
        words = segment['words']
        segment_text = segment['text']

        # Determine the number of segments needed based on the max_char limit.
        n_segments = (len(segment_text) // max_char) + 1
        len_segment = len(segment_text) // n_segments
        text = ""

        # Get the start time of the segment or use the end time of the last word if not available.
        start_time = segment.get('start', end_word)

        # Iterate over each word in the segment.
        for word in words:
            start_word = word.get('start', end_word)
            end_word = word.get('end', start_word)

            # If adding the current word exceeds the character limit or it's the last word, finalize the segment.
            if len(text + word['word']) > len_segment or word == words[-1]:
                text += word['word']
                end_time = end_word
                srt_output += format_segment_to_srt(index, start_time, end_time, text)
                index += 1
                text = ""
            else:
                if len(text) == 0:
                    start_time = start_word
                text += word['word'] + " "

    return srt_output
    
