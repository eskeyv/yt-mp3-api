from pytube import YouTube
from pydub import AudioSegment
import os

def convert(url):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        out_file = audio.download()
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        print('Done!')
        return new_file
    except Exception as e:
        print(e)

url = input("Enter YouTube URL: ")
new_file = convert(url)