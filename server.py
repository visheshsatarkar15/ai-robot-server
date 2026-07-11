import os
from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
from io import BytesIO

app = Flask(__name__)

# Grab the API key securely from Railway's environment variables
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable is not set!")
else:
    # Authenticate the official Google Generative AI SDK
    genai.configure(api_key=API_KEY)

@app.route("/", methods=["GET"])
def home():
    """Simple connection diagnostic endpoint."""
    return jsonify({
        "status": "online",
        "message": "IRIS Robot Server is running perfectly!"
    }), 200

@app.route("/audio-chat", methods=["POST"])
def audio_chat():
    """
    Accepts 16kHz WAV audio bytes from the ESP32, 
    processes it through Gemini 1.5 Flash, 
    and returns an audio voice tracking stream.
    """
    try:
        # Get raw PCM data sent directly as binary payload from ESP32
        audio_data = request.get_data()
        
        if not audio_data:
            return jsonify({"error": "No binary audio payload received"}), 400
            
        # Initialize Gemini Model to respond strictly in audio format
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={
                "response_mime_type": "audio/mp3"  # Instructs Gemini to output voice data
            }
        )
        
        # Pass the raw voice capture stream inline directly to Gemini
        response = model.generate_content([
            {
                "mime_type": "audio/wav", # Matches the ESP32 INMP441 configuration layout
                "data": audio_data
            },
            "You are IRIS, a helpful robot companion. Listen to the user's audio query and reply back with short, conversational speech. CRITICAL: Your voice output must sound deep and masculine."
        ])
        
        # Extract the spoken binary audio part from the generated response candidate
        audio_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("audio/"):
                audio_bytes = part.inline_data.data
                break
                
        if not audio_bytes:
            return jsonify({"error": "Gemini did not return a valid audio speech candidate"}), 500

        # Send raw audio bytes backward directly into the ESP32 MAX98357A decoder
        return send_file(
            BytesIO(audio_bytes),
            mimetype="audio/mp3",
            as_attachment=False
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Railway Dynamic Port Forwarding Routine
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
