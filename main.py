@app.route("/voice", methods=["POST"])
def voice():
    response = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="alice">Welcome to Hype Drip Creative Studio. How can I assist you today?</Say>
        <Pause length="10"/>
    </Response>
    """
    return Response(response, mimetype="text/xml")
