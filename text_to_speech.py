import azure.cognitiveservices.speech as speechsdk
import os
# Creates an instance of a speech config with specified subscription key and service region.

class TTS:

    def __init__(self) -> None: 
        self.speech_config = speechsdk.SpeechConfig(subscription=os.environ.get("AZURE_SPEECH_API_KEY"), region=os.environ.get("AZURE_SPEECH_REGION"))
        self.speech_config.speech_synthesis_voice_name = "en-US-EvelynMultilingualNeural" #change later to a selection of voices, possibly

    def get_speech_synthesiser(self, audio_device_name=None):
        if audio_device_name:
            return speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_device_name)
        else:
            return speechsdk.SpeechSynthesizer(speech_config=self.speech_config)     
    
    
    def play_audio(self, text: str, audio_device_name=None):
        if not text:
            text = "Rowan why are you so fucking massive and strong? Also, please write for the prompt something next time"

        speech_synthesizer = self.get_speech_synthesiser(audio_device_name)
    
        return speech_synthesizer.speak_text_async(text).get()

    def result_handle(self, result, text):
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
    
    def convert_text_to_ssml(self, text):
        ssml_text = (
            "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"
            "<voice name='en-US-EvelynMultilingualNeural'>"
        )
        for token in text.split():
            if token.startswith("*") and token.endswith("*"):
                action_text = token.strip("*")
                ssml_text += f'<prosody rate="fast" volume="x-loud" emphasis="strong" pitch="+5%">>{action_text}</prosody>'
                print("biden")
            else:
                ssml_text += f'<prosody rate="medium" volume="loud" pitch="+5%">{token}</prosody> '
        ssml_text += "</voice></speak>"
        return ssml_text
    
    def get_audio_onto_file(self, text: str, file_path: str):
        if not text:
            text = "Rowan why are you so fucking massive and strong? Also, please write for the prompt something next time"
        audio_output_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
        speech_synthesizer = self.get_speech_synthesiser(audio_device_name=audio_output_config)
        ssml_text = self.convert_text_to_ssml(text)
        result = speech_synthesizer.speak_ssml_async(ssml_text).get()
        self.result_handle(result, text)
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_stream = speechsdk.AudioDataStream(result)
            audio_stream.save_to_wav_file(file_path)
            return True
        else:
            print("Error synthesizing speech:", result.cancellation_details.reason)
            if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details:", result.cancellation_details.error_details)
            return False