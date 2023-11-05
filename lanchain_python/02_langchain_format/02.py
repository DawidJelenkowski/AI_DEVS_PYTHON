from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from system_context import context
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Define a system template providing instructions to the model
system_template = """
As a {role} who answers questions ultra-concisely using CONTEXT below 
and truthfully says "don't know" when the CONTEXT is not enough to give an answer.

context###{context}###
"""

# Define a human template for the chat interaction
human_template = "{text}"

# Create a chat prompt template from system and human messages
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),  # System-level instructions with placeholders
    ("human", human_template),  # Represents the user's input
])

# Format the chat prompt with specific values for 'context' and 'role'
formatted_chat_prompt = chat_prompt.format_messages(
    context=context,  # Replace the 'context' placeholder with actual context
    role="Senior sentence Programmer",  # Define the role for the model
    text="What is Vercel AI?"  # User's input text
)

# Create an instance of the ChatOpenAI model
chat = ChatOpenAI()

# Use the model to predict messages based on the formatted chat prompt
content = chat.predict_messages(formatted_chat_prompt)

print(content)
