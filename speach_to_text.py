import os
import azure.cognitiveservices.speech as speechsdk
import threading
import time

class SpeechRecognition:
    def __init__(self, language="en-US") -> None:
        self.lock = threading.Lock()
        self.speech_config = speechsdk.SpeechConfig(subscription=os.environ.get("AZURE_SPEECH_API_KEY"), region=os.environ.get("AZURE_SPEECH_REGION"))
        self.speech_config.speech_recognition_language=language
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recogniser = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)
        self.is_listening = False
        self.listen_thread = None
        self.results = []
        self.stop_event = threading.Event()

    def start_listening(self):
        with self.lock:
            if not self.is_listening:
                self.is_listening = True
                self.results = []
                self.stop_event.clear()
                threading.Thread(target=self._listen_continuously).start()
                
    def stop_listening(self):
        with self.lock:
            if self.is_listening:
                self.is_listening = False
                time.sleep(.1)
                self.stop_event.wait()
                return self.results
            
    def _listen_continuously(self):
        print("Start listeing")
        while self.is_listening:
            try:
                speech_recognition_result = self.speech_recogniser.recognize_once_async().get() 
                if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    print("Recgnised: {}".format(speech_recognition_result.text))
                    self.results.append(speech_recognition_result.text)
                elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                    print("No speech could be recognised: {}".format(speech_recognition_result.no_match_details))
                elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = speech_recognition_result.concellation_details
                    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print("Error details: {}".format(cancellation_details.error_details))
                        print("Did you set the speech resource key and region values?")
            except RuntimeError as e:
                print(f"Runtime error occurred: {str(e)}")
                break
        print("listening stopped.")
        self.stop_event.set()