from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# ElevenLabs setup
ELEVENLABS_API_KEY = "sk_e79f59ee2c2faf2bbc6e459e1f8ca0fb09958b70f5b4766f"
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

@app.route("/", methods=["GET"])
def home():
    return "AI receptionist with ElevenLabs is live"

# Step 1: Greet the caller and record their message
@app.route("/voice", methods=["POST"])
def voice():
    response = """
    <Response>
        <Say voice="alice">Welcome to Hype Drip Creative Studio. Please tell me how I can help you today after the beep.</Say>
        <Record action="/process" method="POST" maxLength="10" playBeep="true" />
        <Say>I didn't catch that. Goodbye!</Say>
    </Response>
    """
    return Response(response, mimetype="text/xml")

# Step 2: Process the recording
@app.route("/process", methods=["POST"])
def process():
    recording_url = request.form.get("RecordingUrl")
    print(f"Caller audio: {recording_url}")

    # Use a placeholder reply for now
    reply_text = "Thanks for calling. We'll get back to you shortly."

    # Send reply_text to ElevenLabs and get mp3 audio
    audio_url = elevenlabs_tts(reply_text)

    # Respond with audio playback
    response = f"""
    <Response>
        <Play>{audio_url}</Play>
        <Pause length="1"/>
        <Say>Goodbye!</Say>
    </Response>
    """
    return Response(response, mimetype="text/xml")

# ElevenLabs text-to-speech
def elevenlabs_tts(text):
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    response = requests.post(url, headers=headers, json=data)
    
    # Save audio locally
    audio_path = "response.mp3"
    with open(audio_path, "wb") as f:
        f.write(response.content)
    
    # Upload to a public location (Render doesn't support this out-of-the-box)
    # For now, return a dummy hosted MP3 or use Twilio's <Say> fallback
    return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
