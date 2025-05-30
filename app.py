import streamlit as st
from voice_recorder import VoiceRecorder
from stt_service import STTService
from command_agent import CommandAgent
import os



class VoiceCommandApp:
    def __init__(self):
        self.recorder = None
        self.stt = None
        self.agent = None
        
        try:
            st.set_page_config(page_title="Persian Voice Commander", layout="wide")
            
            # Initialize components with progress indicators
            with st.spinner("Initializing voice recorder..."):
                self.recorder = VoiceRecorder()
                
            with st.spinner("Loading speech recognition model..."):
                self.stt = STTService()
                
            with st.spinner("Starting command processor..."):
                self.agent = CommandAgent()
                
        except Exception as e:
            st.error(f"Initialization failed: {str(e)}")
            st.stop()

    def run(self):
        st.title("Persian Voice Command System")
        st.write("Speak commands in Persian to control your computer")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎤 Record Command (5 seconds)", key="record"):
                try:
                    audio_file = self.recorder.record(duration=5)
                    if audio_file and os.path.exists(audio_file):
                        st.session_state.audio_file = audio_file
                        st.audio(audio_file)
                    else:
                        st.error("Recording failed - no audio file created")
                except Exception as e:
                    st.error(f"Recording error: {str(e)}")
        
        with col2:
            # In your app.py, update the processing section:
            if 'audio_file' in st.session_state and st.button("🚀 Process Command"):
                try:
                    with st.spinner("Converting speech to text..."):
                        transcription = self.stt.transcribe(st.session_state.audio_file)
                        st.text_area("Recognized Text", value=transcription, height=100)
                        
                    with st.spinner("Executing command..."):
                        result = self.agent.process_command(transcription)
                        
                        if "output" in result:
                            if "Error" in result["output"]:
                                st.error(result["output"])
                            else:
                                st.success(result["output"])
                        else:
                            st.error("Unexpected agent response")
                            
                except Exception as e:
                    st.error(f"Processing error: {str(e)}")
                finally:
                    if 'audio_file' in st.session_state:
                        if os.path.exists(st.session_state.audio_file):
                            os.remove(st.session_state.audio_file)
                        st.session_state.pop('audio_file')

if __name__ == "__main__":
    try:
        app = VoiceCommandApp()
        app.run()
    except Exception as e:
        st.error(f"Fatal application error: {str(e)}")
        st.stop()