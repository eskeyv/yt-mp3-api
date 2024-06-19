from pytube import YouTube
from pydub import AudioSegment
import os
from flask import Flask, jsonify, request, redirect, send_from_directory
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/")
def index():
    return redirect("https://eskey.me")

@app.route("/api/convert", methods=["GET"])
def convert():
    
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        out_file = audio.download(output_path=DOWNLOAD_FOLDER)      
        base, ext = os.path.splitext(out_file)
        new_file = f"{base}_{uuid.uuid4()}" + '.mp3'
        os.rename(out_file, new_file)
        file_name = os.path.basename(new_file)
        return jsonify({'url': f'/api/download/{file_name}'})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
