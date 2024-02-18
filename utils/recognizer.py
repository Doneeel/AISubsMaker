import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, Pipeline, pipeline
from typing import Literal


class Recognizer:
    """
    Implements a speech recognizer.

    It uses a pretrained model Whisper large v3 from OpenAI.
    """

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "openai/whisper-large-v3"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _get_model(
        self, model_id: str, torch_dtype: torch.dtype,
        device: Literal["cuda:0", "cpu"]
    ) -> any:
        """
        Returns the model from the model_id.
        It uses the torch_dtype and device.
        """
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True,
        )
        model.to(device)

        return model

    def _get_processor(self, model_id: str) -> any:
        """
        Returns the processor for the model.
        """
        return AutoProcessor.from_pretrained(model_id)

    def _get_pipeline(
        self,
        model: any,
        processor: any,
        torch_dtype: torch.dtype,
        device: Literal["cuda:0", "cpu"],
    ) -> Pipeline:
        """
        Returns a pipeline for the given model and processor.
        The pipeline is a wrapper around the model.
        """
        return pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )

    def recognize(self, audio: str = None) -> str:
        """
        Main method of the recognizer.
        It uses the pipeline to recognize the audio.
        """
        recognizer = self._get_pipeline(
            self._get_model(
                model_id=self.model_id,
                torch_dtype=self.torch_dtype, device=self.device
            ),
            self._get_processor(model_id=self.model_id),
            self.torch_dtype,
            self.device,
        )

        result = recognizer(audio, return_timestamps=True)
        return result["chunks"]
