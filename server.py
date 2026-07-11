import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 1. Grab the API key from Railway's environment variables
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable is not set!")
else:
    # Configure the Gemini SDK with your key
    genai.configure(api_key=API_KEY)

@app.route("/", methods=["GET"])
def home():
    """A simple health check endpoint to verify the server is live."""
    return jsonify({"status": "online", "message": "Server is running perfectly!"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    """
    The endpoint your hardware or app will send requests to.
    Expects JSON: {"prompt": "Your question here"}
    """
    try:
        # Get data sent to the server
        data = request.get_json()
        
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' in request body"}), 400
        
        user_prompt = data["prompt"]

        # 2. Call the Gemini API (using the standard gemini-1.5-flash model)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_prompt)
        
        # 3. Return Gemini's text response back to your hardware
        return jsonify({
            "success": True,
            "response": response.text
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 4. The dynamic Port configuration for Railway
if __name__ == "__main__":
    # Look for the port Railway assigns, default to 8080 if running locally
    port = int(os.environ.get("PORT", 8080))
    # host="0.0.0.0" allows external hardware to connect
    app.run(host="0.0.0.0", port=port)
