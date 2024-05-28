from gtts import gTTS
import os
import io
import speech_recognition as sr
import scipy.io.wavfile as wavfile
import soundfile as sf
import numpy as np
from speech_recognition.exceptions import UnknownValueError, WaitTimeoutError
import tempfile


def audio_to_text(audio):
    # Gradio's audio component returns audio as a tuple
    # first element is metadata, second is actual audio as ndarray
    sample_rate, audio_data = audio

    # Create a temporary file to save the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        # Write the audio data to the temporary file
        wavfile.write(temp_audio_file.name, sample_rate, audio_data.astype(np.int16))

    # Create a speech recognition object
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_audio_file.name) as source:
        # Adjust for ambient noise in the audio
        recognizer.adjust_for_ambient_noise(source)
        # Record the audio
        audio = recognizer.record(source)
    try:
        # Recognize the speech in the audio using Google speech recognition API
        text = recognizer.recognize_google(audio, language='en')
    except UnknownValueError:
        raise UnknownValueError('Sorry, I did not understand what you just said, may you repeat please.')
    except Exception as e:
        raise RuntimeError(f'Sorry an error occured')
    finally:
        # Remove the temporary audio file
        os.remove(temp_audio_file.name)
    return text


def str_to_audio(text: str):
    # Convert text to speech using Google Text-To-Speech API
    myobj = gTTS(text=text, lang='en', slow=False)
    # Save the audio to a bytes stream
    audio_data = io.BytesIO()
    myobj.write_to_fp(audio_data)

    # Ensure the pointer is at the start of the stream
    audio_data.seek(0)
    # Load the audio data using soundfile
    audio_segment, sample_rate = sf.read(audio_data)

    # Convert the audio segment to a NumPy array
    audio_data_np = np.array(audio_segment, dtype=np.float32)

    # Return audio in the format gradio's Audio component needs
    return sample_rate, audio_data_np
