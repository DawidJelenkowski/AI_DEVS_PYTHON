"""
source [https://python.langchain.com/docs/get_started/quickstart]
There are two types of language models, which in LangChain are called:

- LLMs: this is a language model which takes a string as input and returns a string
- ChatModels: this is a language model which takes a list of messages as input and returns a message
"""
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

template = """
You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
ONLY return a comma separated list, and nothing more.
"""

# Define a human template for the chat interaction
human_template = "{text}"

# Create a chat prompt template from system and human messages
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),   # Provides system-level instructions
    ("human", human_template),  # Represents the user's input
])

# Combine the chat prompt template with the Chat OpenAI model using the '|' operator
chain = chat_prompt | ChatOpenAI()

# Invoke the model with the user's input data (in this case, "colors")
output = chain.invoke({"text": "colors"})

print(output)
