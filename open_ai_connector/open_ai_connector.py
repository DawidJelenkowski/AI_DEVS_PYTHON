from open_ai_connector.const import OpenAiModels
from dotenv import load_dotenv, find_dotenv
import json
import os
from typing import List, BinaryIO, Tuple

from openai import OpenAI


class OpenAIConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OpenAIConnector, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.initialize_client()
        return cls._instance

    def initialize_client(self) -> None:
        load_dotenv(find_dotenv())
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_models(self) -> List[str]:
        models_page = self.client.models.list()
        models_name = [model.id for model in models_page.data]
        return models_name

    def moderate_prompt(self, sentences: List[str]) -> List[str]:
        verdicts = []
        for sentence in sentences:
            response = self.client.moderations.create(input=sentence)
            verdict = response.results[0].flagged
            verdicts.append(verdict)
        return verdicts

    def generate_answer(
        self,
        model: str,
        messages: List[dict],
        max_token: int = 150,
        variations: int = 1,
        temperature: float = 0.5,
    ) -> str:
        response = self.client.chat.completions.create(model=model,
                                                       temperature=temperature,
                                                       max_tokens=max_token,
                                                       n=variations,
                                                       messages=messages)
        return response.choices[0].message.content

    def function_calls(
        self,
        model: str,
        messages: List[dict],
        functions: List[dict],
        function_call: str = "auto",
        max_token: int = 150,
        variations: int = 1,
        temperature: float = 0.5,
    ) -> Tuple[str, dict]:
        response = self.client.chat.completions.create(model=model,
                                                       temperature=temperature,
                                                       max_tokens=max_token,
                                                       n=variations,
                                                       messages=messages,
                                                       functions=functions,
                                                       function_call=function_call)
        # === Return in structure [name_of_the_function, arguments]
        reply_content = response.choices[0].message.function_call
        return (
            reply_content.name,
            json.loads(reply_content.arguments),
        )

    def generate_embedding(self, text_to_embbeded: str) -> str:
        response = self.client.embeddings.create(
            input=text_to_embbeded, model=OpenAiModels.text_embedding_ada_002.value)
        embedding = response.data[0].embedding
        return embedding

    def use_whisperer(self, audio_file: BinaryIO) -> str:
        transcript = self.client.audio.transcriptions.create(
            model=OpenAiModels.whisper_1.value, file=audio_file, response_format="text")
        return transcript

    def use_vision(self, text, url, assistant_knowledge):
        response = (
            self.client.chat.completions.create(model=OpenAiModels.gpt4_vision.value,
                                                messages=[
                                                    {
                                                        "role": "user",
                                                        "content": [
                                                            {"type": "text",
                                                             "text": text},
                                                            {
                                                                "type": "image_url",
                                                                "image_url": {
                                                                    "url": url,
                                                                },
                                                            },
                                                        ],
                                                    },
                                                    {"role": "assistant",
                                                     "content": assistant_knowledge},
                                                ],
                                                max_tokens=300),
        )

        print(response[0]["choices"][0]["message"]["content"])
        return response[0]["choices"][0]["message"]["content"]


if __name__ == "__main__":
    pass
