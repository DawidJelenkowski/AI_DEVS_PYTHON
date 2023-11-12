from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

loader = TextLoader(r"lanchain_python/09_context/memory.md")
data = loader.load()
data = data[0].page_content
chat = ChatOpenAI()

# Create a chat prompt template from system and human messages
chat_template = ChatPromptTemplate.from_messages([
    ("system", """
    Answer questions as truthfully using the context below and nothing more. 
    If you don't know the answer, say "don't know".
    context###${data}###
    """),
    ('human', '{text}'),
])

messages = chat(chat_template.format_messages(
    data=data, text="Who is overment?"))
messages = messages.content
print(messages)
