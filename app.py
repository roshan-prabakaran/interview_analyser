from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from utils.audio_utils import save_audio, transcribe_audio, provide_feedback
import os
import json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    print("Upload endpoint hit")

    if "audio_data" not in request.files:
        print("No audio_data in request.files")
        return jsonify({"error": "Upload failed.", "feedback": "Error uploading audio."})

    audio_file = request.files["audio_data"]
    print(f"Received audio file: {audio_file.filename}")

    file_path = os.path.join(UPLOAD_FOLDER, "user_input.wav")
    try:
        audio_file.save(file_path)
    except Exception as e:
        print(f"Error saving file: {e}")
        return jsonify({"error": "Upload failed.", "feedback": "Error saving audio."})

    text = transcribe_audio(file_path)
    if "Speech not recognized" in text or "API error" in text:
        print(f"Transcription error: {text}")
        return jsonify({"error": text, "feedback": "Error: No feedback available."})

    feedback = provide_feedback(text, file_path)
    feedback["transcription"] = text

    with open("interview_feedback.json", "w") as f:
        f.write(json.dumps(feedback, indent=4))

    return jsonify(feedback)

if __name__ == "__main__":
    app.run(debug=True)
