from flask import Flask, request, jsonify
import os
from google import genai

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

@app.route("/")
def home():
    return "AI Robot Server Running"

@app.route("/ask", methods=["GET"])
def ask():
    message = request.args.get("message")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=message
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
