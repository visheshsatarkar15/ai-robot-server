import os
from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
from io import BytesIO

app = Flask(__name__)

# Grab the API key from Railway's environment variables
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable is not set!")
else:
    genai.configure(api_key=API_KEY)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "message": "IRIS Robot Server is running!"}), 200

@app.route("/audio-chat", methods=["POST"])
def audio_chat():
    """
    Accepts an audio file from the robot, processes it with Gemini,
    and returns a spoken audio response.
    """
    try:
        # 1. Check if the robot actually sent an audio file
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file received"}), 400
            
        audio_file = request.files['audio']
        
        # Read the binary audio data into memory
        audio_data = audio_file.read()
        
        # 2. Setup Gemini Model with instructions to reply via Audio
        # We request an audio output from the model configuration
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={
                "response_mime_type": "audio/mp3"  # Tells Gemini to speak back
            }
        )
        
        # 3. Send the audio directly to Gemini
        # We specify the mime_type so Gemini knows how to read it (e.g., audio/wav or audio/mp3)
        mime_type = audio_file.content_type or "audio/wav"
        
        response = model.generate_content([
            {
                "mime_type": mime_type,
                "data": audio_data
            },
            "You are IRIS, a helpful robot companion. Listen to the user's audio query and reply back with short, conversational speech."
        ])
        
        # 4. Extract the spoken audio parts from Gemini's response
        audio_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("audio/"):
                audio_bytes = part.inline_data.data
                break
                
        if not audio_bytes:
            return jsonify({"error": "Gemini did not return an audio response"}), 500

        # 5. Send the raw audio bytes back to the robot's speaker
        return send_file(
            BytesIO(audio_bytes),
            mimetype="audio/mp3",
            as_attachment=False
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
