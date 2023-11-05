from typing import List, Union
from tiktoken import get_encoding
from langchain.schema import BaseMessage


def count_tokens(messages: List[BaseMessage], model="gpt-3.5-turbo-0613") -> int:
    # Get the encoding for a specific model.
    encoding = get_encoding("cl100k_base")

    # Initialize variables to count tokens per message and tokens per name.
    tokens_per_message, tokens_per_name = 0, 0

    # Define token counts based on the specified model.
    if model in ["gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-4-0314", "gpt-4-32k-0314", "gpt-4-0613", "gpt-4-32k-0613"]:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4
        tokens_per_name = -1
    elif "gpt-3.5-turbo" in model:
        # Warn and assume gpt-3.5-turbo-0613 token counts if the model is not recognized.
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return count_tokens(messages, "gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        # Warn and assume gpt-4-0613 token counts if the model is not recognized.
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return count_tokens(messages, "gpt-4-0613")
    else:
        # Raise an exception for unsupported models.
        raise Exception(
            f"num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.")

    # Initialize the total token count.
    num_tokens = 0

    # Iterate through the list of messages and count tokens for each message and its attributes.
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.__dict__.items():
            if value is not None:  # Check if value is not None
                str_value = str(value)  # Convert value to string
                num_tokens += len(encoding.encode(str_value))
                if key == "name":
                    num_tokens += tokens_per_name

    # Add 3 tokens as a buffer (you can adjust this number based on your needs).
    num_tokens += 3
    return num_tokens
