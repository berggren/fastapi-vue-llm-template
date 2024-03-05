"""Vertex AI LLM provider."""

from . import interface
from . import manager

from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models


class VertexAI(interface.LLMProvider):
    """Vertex AI LLM provider."""

    NAME = "vertexai"

    def generate(self, prompt: str) -> str:
        """
        Generate text using the Vertex AI service.

        Args:
            prompt: The prompt to use for the generation.
            temperature: The temperature to use for the generation.
            stream: Whether to stream the generation or not.

        Returns:
            The generated text as a string.
        """
        aiplatform.init(
            project=self.config.get("project_id"),
        )
        model = GenerativeModel(self.config.get("model"))

        # Safety config
        safety_config = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": self.config.get("max_output_tokens"),
                "temperature": self.config.get("temperature"),
            },
            safety_settings=safety_config,
            stream=self.config.get("stream"),
        )

        return response.text


manager.LLMManager.register_provider(VertexAI)
