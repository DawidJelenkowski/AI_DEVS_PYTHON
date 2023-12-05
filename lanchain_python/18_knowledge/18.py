
from typing import List
import re
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.docstore.document import Document
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


loader = TextLoader(r"lanchain_python/18_knowledge/knowledge.md")
data = loader.load()
chat = ChatOpenAI()


def search_docs(docs: Document, keywords: List):
    filtered_docs = []
    for doc in docs:
        for keyword in keywords:
            # remove punctuation
            keyword = re.sub(r'[^\w\s]', '', keyword)
            if keyword.lower() in doc.page_content.lower() and len(keyword) > 3:
                print('Found:', keyword)
                filtered_docs.append(doc)
                print(filtered_docs)
                break
    return filtered_docs


documents = [Document(page_content=content)
             for content in data[0].page_content.split("\n\n")]
query = "Can you write me a function that will generate random number in range for easy?"
filtered = search_docs(documents, query.split(' '))

chat_template = ChatPromptTemplate.from_messages([
    ("system", """
    Answer questions as truthfully using the context below and nothing more.
    If you don't know the answer, say 'don't know'.\n\n
    context###
    '{filtered}'
    """),
    ("human", '{query}'),
])

messages = chat(chat_template.format_messages(
    filtered=filtered, query=query))
messages = messages.content
print(messages)
