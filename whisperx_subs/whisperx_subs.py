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

def convert_json_to_srt(json_str, max_char, langs=[], model_name='Helsinki-NLP/opus-mt'):
    """
    Convert a given JSON string to SRT format.
    
    Parameters:
    - json_str (str): The JSON string containing segments and words data.
    - max_char (int): The maximum number of characters for each SRT segment.
    - langs (list): List of target languages for translation.
    - model_name (str): Base model name for translation.

    Returns:
    - tuple: A tuple containing a list with the original SRT and its translations, 
             and a dictionary with the complete texts for each language.
    """
    
    # Load the JSON content
    data = json.loads(json_str)
    source_lang = data["language"]

    # Create translator models for each target language
    translators = {}
    for lang in langs:
        translators[lang] = pipeline('translation', model=f'{model_name}-{source_lang}-{lang}')

    # Initialize the srt outputs and complete texts for each language (source + target languages)
    srt_outputs = {lang: "" for lang in [source_lang] + langs}
    txt_outputs = {lang: [] for lang in [source_lang] + langs}

    index = 1 
    start_word = 0
    end_word = 0
    
    # Iterate over each segment to create the srt content
    for segment in tqdm(data["segments"], desc="Converting segments", ncols=100):
        words = segment['words']
        segment_text = segment['text']
        len_text = len(segment_text)

        # Append the original segment text to txt_outputs
        txt_outputs[source_lang].append(segment_text)

        # Calculate number of srt segments needed based on max_char limit
        n_segments = (len_text // max_char) + 1
        len_segment = len_text // n_segments
        texts = {lang: "" for lang in srt_outputs.keys()}

        # Translate and split translations into segments
        translated_texts_segments = {}
        for lang in langs:
            translated_text = translators[lang](segment_text, max_length=10000)[0]['translation_text']
            translated_texts_segments[lang] = split_text_into_equal_segments(translated_text, n_segments)
            
            # Append the translated text to txt_outputs
            txt_outputs[lang].append(translated_text)

        start_time = segment.get('start', end_word)
        i_translated_segment = {lang: 0 for lang in langs}
        
        # Process each word in the segment
        for word_index, word in enumerate(words):
            start_word = word.get('start', end_word)
            end_word = word.get('end', start_word)

            # Check if the current srt segment is full or it's the last word
            if len(texts[source_lang] + word['word']) > len_segment or word_index == len(words) - 1:
                for lang, text in texts.items():
                    end_time = end_word

                    # If it's the source language, append the word, else append the translated segment
                    if lang == source_lang:
                        text += word['word']
                        srt_outputs[lang] += format_segment_to_srt(index, start_time, end_time, text)
                    else:
                        translated_segment = translated_texts_segments[lang][i_translated_segment[lang]]
                        srt_outputs[lang] += format_segment_to_srt(index, start_time, end_time, translated_segment)
                        i_translated_segment[lang] += 1
                        
                index += 1
                texts = {lang: "" for lang in srt_outputs.keys()}
            else:
                if len(texts[source_lang]) == 0:
                    start_time = start_word
                    
                # Handle cases for languages like Japanese and Chinese differently
                if source_lang == "ja" or source_lang == "zh":
                    texts[source_lang] += word['word']
                else:
                    texts[source_lang] += word['word'] + " "


    return srt_outputs, txt_outputs

