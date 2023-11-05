from message import Message
from count_tokens import count_tokens
from tiktoken import get_encoding
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Create a list of Message objects.
# In this case, it contains a single system message.
messages = [Message(role="system", content="Hey, you!")]

# Count the number of tokens required to encode the messages
# Expected output is 11 tokens, but this depends on the implementation of count_tokens
num = count_tokens(messages, model='gpt-4')
print("Token Count: ", num)

# Get the encoding object for the 'cl100k_base' model.
encoding = get_encoding("cl100k_base")

# Print the token IDs for the content of the first message in the list.
# The encode function is expected to convert the text into a list of token IDs.
print("Token IDs: ", encoding.encode(messages[0].content))
