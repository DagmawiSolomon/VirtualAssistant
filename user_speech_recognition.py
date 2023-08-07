import speech_recognition as sr
from textToSpeech import ReadNews

class SpeechRecognition:
    def __init__(self):
        self.news = ReadNews()
        self.recognizer = sr.Recognizer()
        

    def interpret_speech(self, text):
        if text.lower() == "can you read me the headlines":
            self.news.read_headlines()
        elif text.lower() == "what's the weather like today":
            self.news.read_weather()
        else:
            self.news.read_loud("Sorry, I could not understand what you said.")

    def recognize_speech(self, retries=4):
        for _ in range(retries):
            with sr.Microphone() as source:
                self.news.read_loud("Hi, Speak something")
                audio = self.recognizer.listen(source)

            try:
                recognized_text = self.recognizer.recognize_google(audio)
                print(f"You said: {recognized_text}")
                self.interpret_speech(recognized_text)
                break
            except sr.UnknownValueError:
                self.news.read_loud("Sorry, I could not understand what you said.")
                
            except sr.RequestError as e:
                print(f"Error fetching results from Google Web Speech API; {e}")
                print("Please check your internet connection and try again later.")
                break

