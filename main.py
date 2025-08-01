from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "AI receptionist is running"

@app.route("/voice", methods=["POST"])
def voice():
    response = """
    <Response>
        <Say voice="alice">Hello! This is your AI receptionist. Please hold while we connect you.</Say>
    </Response>
    """
    return Response(response, mimetype='text/xml')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
