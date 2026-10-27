import os
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
from pydub import AudioSegment

app = Flask(__name__, template_folder='templates', static_folder='.')
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_audio():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # ಆಡಿಯೋ ಲೂಪ್ / ಪ್ರೊಸೆಸಿಂಗ್
    song = AudioSegment.from_file(input_path)
    target_duration_ms = 5 * 60 * 1000  # 5 ನಿಮಿಷ
    extended_song = song
    while len(extended_song) < target_duration_ms:
        extended_song += song

    output_filename = 'remix_' + file.filename
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    extended_song.export(output_path, format="mp3")

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    # host='0.0.0.0' ಕೊಟ್ಟರೆ ನಿಮ್ಮ ವೈಫೈ ನೆಟ್‌ವರ್ಕ್‌ನಲ್ಲಿರುವ ಮೊಬೈಲ್‌ನಿಂದಲೂ ಕನೆಕ್ಟ್ ಆಗಬಹುದು
    app.run(host='0.0.0.0', port=5000, debug=True)