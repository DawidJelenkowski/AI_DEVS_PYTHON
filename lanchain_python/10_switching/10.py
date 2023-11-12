from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

chat = ChatOpenAI()

query = "Where Jakub works?"
sources = [
    {"name": "Adam (overment)", "source": "adam.md"},
    {"name": "Jakub (unknow)", "source": "jakub.md"},
    {"name": "Mateusz (MC)", "source": "mateusz.md"}
]

sources_string = '\n'.join(
    [s['name'] + ' file:' + s['source'] for s in sources])

# Define a system template providing instructions to the model
system_template = """
Pick one of the following sources related to the query and return filename and nothing else.
Sources###
{sources_string}
###
Query: {query}\n\n
Source file name:
"""

# Create a chat prompt template from system and human messages
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
])

# Format the chat prompt with specific values for 'context' and 'role'
formatted_chat_prompt = chat_prompt.format_messages(
    sources_string=sources_string,
    query=query
)

# Create an instance of the ChatOpenAI model
chat = ChatOpenAI()

# Use the model to predict messages based on the formatted chat prompt
content = chat.predict_messages(formatted_chat_prompt)
content = content.content
print(content)
