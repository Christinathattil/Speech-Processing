'''After installing 'brew install portaudio' in mac terminal, 
type 'python3 -m pip install --upgrade numpy scipy sounddevice SpeechRecognition' in vs code terminal after the environment is activated.'''

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import speech_recognition as sr
import wave  # used for writing the WAV file.

# Initialize the recognizer
recognizer = sr.Recognizer()

def record_speech(duration=5, fs=44100):
    """
    Record audio for a specified duration using sounddevice and save it as 16-bit PCM WAV.
    """
    try:
        print("Recording...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')  # Save as 16-bit PCM
        sd.wait()  # Wait until recording is finished
        print("Recording finished.")
        
        # Save the recorded audio as a 16-bit PCM WAV file
        with wave.open('YourAudio.wav', 'wb') as wf:
            wf.setnchannels(1)  # Mono channel
            wf.setsampwidth(2)  # 2 bytes = 16 bits
            wf.setframerate(fs)
            wf.writeframes(audio.tobytes())  # Convert to bytes and write to file
        return 'YourAudio.wav'  # Return the filename for further processing

    except sd.PortAudioError as e:
        print(f"Error recording audio: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error occurred during recording: {e}")
        return None

def convert_speech_to_text(audio_file):
    """
    Convert recorded audio file to text using Google's Web Speech API.
    """
    try:
        # Use recognizer to open and recognize the speech in the wav file
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)  # Record the audio from the file
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"Speech recognized: {text}")
        return text

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio. Please try speaking more clearly.")
        return None

    except sr.RequestError:
        print("Could not connect to the recognition service. Please check your internet connection.")
        return None

    except FileNotFoundError:
        print("The recorded audio file could not be found.")
        return None

    except Exception as e:
        print(f"An unexpected error occurred during speech recognition: {e}")
        return None

def display_text(text):
    if text:
        print(f'Speech successfully converted to text: "{text}"')
    else:
        print("Speech conversion failed.")

def main():
    # Step 1: Record the speech
    audio_file = record_speech(duration=5)  # Record 5 seconds of audio
    
    if audio_file:
        # Step 2: Convert the recorded audio to text
        text = convert_speech_to_text(audio_file)
        
        # Step 3: Display the converted text
        display_text(text)
    else:
        print("Audio recording failed, cannot proceed with speech recognition.")

if __name__ == "__main__":
    main()
