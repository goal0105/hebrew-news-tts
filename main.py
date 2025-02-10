from flask import Flask, request, jsonify, send_file, render_template
import os
from TTS.api import TTS
import tweepy

API_KEY = "your_api_key"
API_KEY_SECRET = "your_api_key_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAHPkygEAAAAAUGRfTB4mR772w9YjC9NMwFyRLS0%3DK1NRkWhDTX3I98ZsxUHp5YGsdjriKyesKZTvbOjGODJ50BPsCa"

app = Flask(__name__)

# Directory to save generated audio
AUDIO_DIR = "generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Initialize TTS model
print("Loading TTS model...")
# tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")
print("TTS model loaded.")

# Authenticate with Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_tweets", methods=["GET"])
def update_tweets():
    try:
        # Fetch recent tweets in Hebrew about Israel
        query = "ישראל חדשות"
        tweets = client.search_recent_tweets(query=query, max_results=10)

        print("Return tweets data")
        # Return tweets as JSON
        return jsonify({"tweets": tweets.data})

        # test code
        # tweets =["Tweet 1", "Tweet 2", "Tweet 3"]  # Mock data
        # return jsonify({"tweets": tweets}) 
    
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/generate_tts", methods=["POST"])
def generate_tts():
    data = request.json
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    file_path = os.path.join(AUDIO_DIR, "output.wav")
    
    # Generate speech from text
    # tts.tts_to_file(text=text, file_path=file_path)

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
