from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torchaudio
import torch
import os

class STTService:
    def __init__(self):
        try:
            # Use a Persian-fine-tuned model for better accuracy
            model_name = "m3hrdadfi/wav2vec2-large-xlsr-persian"
            
            # Verify model files exist
            from transformers.utils import cached_file
            try:
                cached_file(model_name, "preprocessor_config.json")
            except Exception as e:
                raise ValueError(f"Model files not found: {str(e)}")
            
            # Initialize with explicit config
            self.processor = Wav2Vec2Processor.from_pretrained(
                model_name,
                tokenizer_type="wav2vec2",
                unk_token="[UNK]",
                pad_token="[PAD]",
                word_delimiter_token="|"
            )
            
            self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
            self.model.to("cuda" if torch.cuda.is_available() else "cpu")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize STT service: {str(e)}")

    def transcribe(self, audio_path):
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            waveform, sample_rate = torchaudio.load(audio_path)
            
            # Convert stereo to mono if needed
            if waveform.shape[0] > 1:
                waveform = torch.mean(waveform, dim=0, keepdim=True)
                
            # Resample to 16kHz
            if sample_rate != 16000:
                resampler = torchaudio.transforms.Resample(sample_rate, 16000)
                waveform = resampler(waveform)
            
            # Normalize audio
            waveform = (waveform - waveform.mean()) / (waveform.std() + 1e-8)
            
            # Process input
            input_values = self.processor(
                waveform.squeeze().numpy(),
                return_tensors="pt",
                sampling_rate=16000
            ).input_values.to(self.model.device)
            
            # Inference
            with torch.no_grad():
                logits = self.model(input_values).logits
                
            # Decode
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]
            
            return transcription
            
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")