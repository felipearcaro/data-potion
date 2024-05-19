from openai import OpenAI
from decouple import config
import replicate


class ModelManager():

    def get_open_ai_response(self, content, **kwargs):
        """Send prompt to OpenAI's chat endpoint and return the response

        Args:
            content (str): User's prompt

        Returns:
            str: Model response
        """
        openai_api_key = config('OPENAI_API_KEY')
        client = OpenAI(
            api_key=openai_api_key,
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system",
                    "content": "You're a helpful assistant",
                 },
                {"role": "user", "content": content},
            ],
            model="gpt-3.5-turbo",
        )
        return chat_completion.choices[0].message.content

    def get_arctic_response(self, content, **kwargs):
        """Send prompt to Arctic's chat endpoint and return the response

            Args:
                content (str): User's prompt

            Returns:
                str: Model response
            """
        answer = ''
        replicate_api_token = config('REPLICATE_API_TOKEN')
        api = replicate.Client(api_token=replicate_api_token)
        for event in replicate.stream(
            "snowflake/snowflake-arctic-instruct",
            input={
                "top_k": 50,
                "top_p": 0.9,
                "prompt": content,
                "temperature": 0.2,
                "max_new_tokens": 512,
                "min_new_tokens": 0,
                "stop_sequences": "<|im_end|>",
                "prompt_template": "<|im_start|>system\nYou're a helpful assistant<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n\n<|im_start|>assistant\n",
                "presence_penalty": 1.15,
                "frequency_penalty": 0.2
            },
        ):
            answer += str(event)
        return answer
