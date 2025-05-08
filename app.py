from flask import Flask, request, jsonify
import base64
from google.cloud import speech

app = Flask(__name__)
client = speech.SpeechClient()

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    audio_base64 = data.get("audio_base64")

    if not audio_base64:
        return jsonify({"error": "Missing 'audio_base64' field"}), 400

    try:
        audio_bytes = base64.b64decode(audio_base64)

        
        audio = speech.RecognitionAudio(content=audio_bytes)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=16000,
            language_code="en-US"
        )

        response = client.recognize(config=config, audio=audio)

        transcription = " ".join(
            [result.alternatives[0].transcript for result in response.results]
        )

        return jsonify({"transcription": transcription})

    except Exception as e:
        return jsonify({"error": "Transcription failed", "details": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True)
