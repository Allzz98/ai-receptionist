from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# ElevenLabs Setup
ELEVENLABS_API_KEY = "sk_e79f59ee2c2faf2bbc6e459e1f8ca0fb09958b70f5b4766f"
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Default ElevenLabs voice

@app.route("/", methods=["GET"])
def home():
    return "AI receptionist is running"

@app.route("/voice", methods=["POST"])
def voice():
    # For now, speak a professional welcome message
    response = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="alice">Welcome to Hype Drip Creative Studio. How can I assist you today?</Say>
        <Pause length="10"/>
    </Response>
    """
    return Response(response, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
