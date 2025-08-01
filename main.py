from flask import Flask, request, Response
import requests
import openai
import os

app = Flask(__name__)

# OpenAI Whisper + GPT setup
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

@app.route("/", methods=["GET"])
def home():
    return "AI receptionist with transcription + GPT is running."

# Step 1: Greet the caller and record their voice
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

# Step 2: Transcribe the message and respond using ChatGPT
@app.route("/process", methods=["POST"])
def process():
    recording_url = request.form.get("RecordingUrl") + ".mp3"
    print(f"[Caller Audio] {recording_url}")

    # Step 1: Download the caller's recording
    audio = requests.get(recording_url)
    with open("caller.mp3", "wb") as f:
        f.write(audio.content)

    # Step 2: Transcribe using Whisper
    with open("caller.mp3", "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)

    caller_text = transcript["text"]
    print(f"[Caller said] {caller_text}")

    # Step 3: Generate a reply using ChatGPT
    prompt = f"You are a friendly and professional receptionist. A client just said: '{caller_text}'. How do you respond?"
    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI receptionist who helps book appointments and answer questions."},
            {"role": "user", "content": prompt}
        ]
    )

    reply_text = chat_response.choices[0].message.content
    print(f"[AI Reply] {reply_text}")

    # Step 4: Speak the reply using Twilio Say (ElevenLabs voice comes next)
    response = f"""
    <Response>
        <Say voice="alice">{reply_text}</Say>
        <Pause length="1"/>
        <Say>Goodbye!</Say>
    </Response>
    """
    return Response(response, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
