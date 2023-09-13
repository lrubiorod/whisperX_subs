# whisperX Subs

This repository provides utilities for processing audio files using the `whisperx` tool, with added functionalities that include formatting subtitles based on a user-specified maximum size, and downloading videos and audios from YouTube.

## Using the Notebooks

There are two Jupyter notebooks provided:

1. **whisperx_subs.ipynb**: This notebook focuses on processing audio files and generating well-formatted subtitles.
   
   To easily run and interact with the code, you can access the notebook via Google Colab:
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lrubiorod/whisperX_subs/blob/main/whisperx_subs.ipynb)

2. **youtube_to_audio.ipynb**: This notebook allows you to download videos and audios from YouTube, which can then be processed using the `whisperx_subs.ipynb` notebook.

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lrubiorod/whisperX_subs/blob/main/youtube_to_audio.ipynb)

By launching these notebooks, you'll have a hands-on environment to run, modify, and experiment with the code in real-time.

## About the Tool

This utility builds upon the [whisperx repository](https://github.com/m-bain/whisperX) to process audio files and generate transcriptions. The added functionality in this repository allows for conditioning the generated subtitles so that they adhere to a maximum length, as specified by the user. This is particularly useful for ensuring that subtitles are easily readable and well-paced for viewers.

