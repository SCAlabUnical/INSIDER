import os
from openai import OpenAI
from ..utils import log_method_call

"""
    This class is responsible for calling the OpenAI API using the GPT_KEY environment variable and accepting the
    type of model to be used as a parameter.
"""
class GptCaller:
    @log_method_call
    def __init__(self, model: str="gpt-3.5-turbo", temperature: float=1.0):
        self.key = os.getenv("GPT_KEY")
        if not self.key:
            raise ValueError("No API key found. Please set the GPT_KEY environment variable.")

        self.model = model
        self.temperature = temperature
        
        self.client = OpenAI(api_key=self.key)

    """
        Sends the text argument to the OpenAI API and returns the response.
    """
    @log_method_call
    def call(self, developer_text: str, user_text: str):
        # The o1-mini model can't have a temperature of 0
        DEFAULT_TEMPERATURE= 1.0
        temp = self.temperature if self.model != "o1-mini" else DEFAULT_TEMPERATURE
        # Because the o1-mini model doesn't support the developer role, we need to send the developer and user text in the same message
        messages = [
            {
                "role": "user",
                "content": developer_text + user_text
            }
        ] if self.model == "o1-mini" else [
            {
                "role": "developer",
                "content": developer_text
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
        
        response = self.client.chat.completions.create(
            messages=messages,
            model = self.model,
            temperature=temp)

        return response