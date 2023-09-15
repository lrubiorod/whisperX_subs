# whisperX Subs

This repository provides utilities for processing audio files using the `whisperx` tool. The added functionalities include formatting subtitles based on a user-specified maximum size, downloading videos and audios from YouTube, and extracting audio from videos stored on Google Drive.

## Using the Notebooks

There are three Jupyter notebooks provided:

1. **whisperx_subs.ipynb**: This notebook focuses on processing audio files and generating well-formatted subtitles.
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lrubiorod/whisperX_subs/blob/main/whisperx_subs.ipynb)

2. **youtube_to_audio.ipynb**: This notebook allows you to download videos and audios from YouTube, which can then be processed using the `whisperx_subs.ipynb` notebook.

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lrubiorod/whisperX_subs/blob/main/youtube_to_audio.ipynb)

3. **video_to_audio.ipynb**: This notebook facilitates the extraction of audio from videos stored on Google Drive, saving the audio as a separate file back to Google Drive.

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lrubiorod/whisperX_subs/blob/main/video_to_audio.ipynb)

By launching these notebooks, you'll have a hands-on environment to run, modify, and experiment with the code in real-time.

## About the Tool

This utility builds upon the [whisperx repository](https://github.com/m-bain/whisperX) to process audio files and generate transcriptions. The added functionality in this repository allows for conditioning the generated subtitles so that they adhere to a maximum length, as specified by the user. This is particularly useful for ensuring that subtitles are easily readable and well-paced for viewers.

## Acknowledgements & License

Parts of this project utilize software developed by Max Bain. We would like to express our gratitude to Max Bain for his contribution.

Any use, redistribution, or modification of the software from the [whisperx repository](https://github.com/m-bain/whisperX) should adhere to the licensing terms provided by Max Bain. Please refer to the associated license file for detailed terms and conditions.


