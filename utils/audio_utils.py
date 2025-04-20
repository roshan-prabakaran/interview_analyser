import os
import speech_recognition as sr
from pydub import AudioSegment

def save_audio(audio_file, file_path):
    audio_file.save(file_path)

def convert_to_wav(source_path, target_path):
    try:
        audio = AudioSegment.from_file(source_path)
        audio = audio.set_frame_rate(16000).set_channels(1)  # mono, 16kHz is ideal for transcription
        audio.export(target_path, format="wav")
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {e}")

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        # Convert file to proper WAV format
        base, _ = os.path.splitext(file_path)
        converted_path = base + "_converted.wav"
        convert_to_wav(file_path, converted_path)

        with sr.AudioFile(converted_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Speech not recognized"
    except sr.RequestError:
        return "API error"
    except Exception as e:
        return f"Error during transcription: {e}"

def provide_feedback(transcription, file_path=None):
    feedback = {}

    if not transcription.strip() or "Error" in transcription:
        feedback["feedback"] = "No speech detected or there was an error."
        return feedback

    feedback_points = []
    word_count = len(transcription.split())

    if word_count < 20:
        feedback_points.append("Try to elaborate more on your answers.")
    if any(filler in transcription.lower() for filler in ["um", "uh", "like", "you know"]):
        feedback_points.append("Avoid filler words like 'um', 'uh', or 'like'.")

    if word_count >= 20 and not feedback_points:
        feedback["feedback"] = "Good job! Your speech was clear and well-paced."
    else:
        feedback["feedback"] = " ".join(feedback_points)

    return feedback
