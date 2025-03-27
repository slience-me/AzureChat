import os
from openai import AzureOpenAI
from typing import List, Dict
from AzureChatServer import settings

class AzureOpenAIClient:
    def __init__(self, endpoint: str = None, api_key: str = None, api_version: str = '2024-02-01'):
        self.endpoint = endpoint or settings.AZURE_OPENAI_ENGINE
        self.api_key = api_key or settings.AZURE_OPENAI_KEY
        self.api_version = api_version

        if not all([self.endpoint, self.api_key, self.api_version]):
            raise ValueError("Azure configuration is missing. Please set environment variables or provide values.")

        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version
        )

    def get_chat_response(self, messages: List[Dict[str, str]], model: str = settings.AZURE_OPENAI_MODEL_DEPLOYMENT_NAME) -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during API call: {str(e)}"


def send_prompt(user_prompt):
    messages = [
        {"role": "system", "content": "你是一個名叫「OpenAI ChatGPT」的角色。你对各个领域都精通，博学多才！"},
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": ""}
    ]
    azure_client = AzureOpenAIClient()
    response = azure_client.get_chat_response(messages=messages)
    return response

def send_message(user_messages):
    azure_client = AzureOpenAIClient()
    response = azure_client.get_chat_response(messages=user_messages)
    return response
