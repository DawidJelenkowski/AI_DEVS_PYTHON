import json
import logging
from typing import List, Dict
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, Document
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv, find_dotenv
# Configure basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class DocumentProcessor:
    def __init__(self, path: str, loader_kwargs: Dict, chat_model: ChatOpenAI):
        self.path: str = path
        self.loader_kwargs: Dict = loader_kwargs
        self.chat: ChatOpenAI = chat_model
        self.documents: List[str] = []
        self.descriptions: List[str] = []

    def load_documents(self) -> None:
        logging.info("Loading documents from directory")

        loader = DirectoryLoader(self.path, **self.loader_kwargs)
        docs: List[Document] = loader.load()
        self.documents = [
            content for doc in docs for content in doc.page_content.split("\n\n")]

    def describe_documents(self) -> None:
        logging.info("Describing documents with concurrency")

        chain = (
            {"doc": lambda x: x}
            | ChatPromptTemplate.from_template("""
                Describe the following document with one of the following keywords:
                Mateusz, Jakub, Adam. Return the keyword and nothing else.
                Document:{doc}
                """)
            | self.chat
            | StrOutputParser()
        )

        # Process the documents in batch with concurrency
        self.descriptions = chain.batch(self.documents, {"max_concurrency": 5})

    def save_to_json(self, output_path: str) -> None:
        logging.info(f"Saving results to {output_path}")

        result: List[Dict[str, Dict[str, str]]] = [{"page_content": doc, "metadata": {"source": desc}}
                                                   for doc, desc in zip(self.documents, self.descriptions)]
        with open(output_path, 'w') as file:
            json.dump(result, file, indent=2)


def main() -> None:
    logging.info("Starting document processing")
    load_dotenv(find_dotenv())
    chat_model = ChatOpenAI(streaming=True)
    path = "lanchain_python/11_docs/"
    loader_kwargs = {
        'glob': "**/*.md",
        'show_progress': True,
        'use_multithreading': True,
        'silent_errors': True,
        'loader_kwargs': {'autodetect_encoding': True}
    }

    processor = DocumentProcessor(path, loader_kwargs, chat_model)
    processor.load_documents()
    processor.describe_documents()
    processor.save_to_json("lanchain_python/11_docs/output.json")


if __name__ == "__main__":
    main()
