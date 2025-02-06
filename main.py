from flask import Flask, request, jsonify, send_file, render_template
import os
from TTS.api import TTS

app = Flask(__name__)

# Directory to save generated audio
AUDIO_DIR = "generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Initialize TTS model
print("Loading TTS model...")
tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")
print("TTS model loaded.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_tts", methods=["POST"])
def generate_tts():
    data = request.json
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    file_path = os.path.join(AUDIO_DIR, "output.wav")
    
    # Generate speech from text
    tts.tts_to_file(text=text, file_path=file_path)

    return jsonify({"audio_url": f"/play_audio?file=output.wav"})

@app.route("/play_audio")
def play_audio():
    file = request.args.get("file")
    file_path = os.path.join(AUDIO_DIR, file)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run()
