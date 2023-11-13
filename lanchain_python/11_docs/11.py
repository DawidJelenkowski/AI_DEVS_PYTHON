import json
import logging
from typing import List, Dict
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, Document
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv, find_dotenv

# Configure logger for the application
logging.basicConfig(level=logging.INFO,
                    filename='lanchain_python/11_docs/text.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self, path: str, loader_kwargs: Dict, chat_model: ChatOpenAI):
        # Initialization of the DocumentProcessor class
        logger.info("Initializing Document Processor")
        self.path: str = path  # Path to the directory with documents
        # Additional arguments for loading documents
        self.loader_kwargs: Dict = loader_kwargs
        self.chat: ChatOpenAI = chat_model  # Chat model for document processing
        self.documents: List[str] = []  # List to store document contents
        # List to store descriptions of documents
        self.descriptions: List[str] = []

    def load_documents(self) -> None:
        # Method to load documents from a directory
        logger.info("Loading documents from directory: %s", self.path)
        try:
            # Create a DirectoryLoader instance
            loader = DirectoryLoader(self.path, **self.loader_kwargs)
            docs: List[Document] = loader.load()  # Load documents
            # Split each document's content into segments and store in self.documents
            self.documents = [
                content for doc in docs for content in doc.page_content.split("\n\n")]
            logger.info("Loaded %d documents", len(self.documents))
        except Exception as e:
            # Log any exceptions that occur
            logger.exception("Failed to load documents: %s", e)

    def describe_documents(self) -> None:
        # Method to describe documents using the chat model
        logger.info("Describing documents with concurrency")
        try:
            # Define the processing chain
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
            # Process documents in batch with concurrency
            self.descriptions = chain.batch(
                self.documents, {"max_concurrency": 5})
            logger.info("Document description completed")
        except Exception as e:
            # Log any exceptions that occur
            logger.exception("Failed to describe documents: %s", e)

    def save_to_json(self, output_path: str) -> None:
        # Method to save the results to a JSON file
        logger.info("Saving results to %s", output_path)
        try:
            # Prepare the data for JSON output
            result: List[Dict[str, Dict[str, str]]] = [{"page_content": doc, "metadata": {"source": desc}}
                                                       for doc, desc in zip(self.documents, self.descriptions)]
            # Write the data to a JSON file
            with open(output_path, 'w') as file:
                json.dump(result, file, indent=2)
            logger.info("Results successfully saved")
        except Exception as e:
            # Log any exceptions that occur
            logger.exception("Failed to save results: %s", e)


def main() -> None:
    # Main function to orchestrate the document processing
    logger.info("Starting document processing")
    load_dotenv(find_dotenv())  # Load environment variables
    chat_model = ChatOpenAI(streaming=True)  # Initialize the chat model
    path = "lanchain_python/11_docs/"
    loader_kwargs = {
        'glob': "**/*.md",  # Pattern to match markdown files in the path
        'show_progress': True,  # Display progress during loading
        'use_multithreading': True,  # Enable multithreading for faster processing
        # Suppress errors during loading (if there is error it moves on)
        'silent_errors': True,
        # Automatically detect file encoding
        'loader_kwargs': {'autodetect_encoding': True}
    }

    # Create an instance of DocumentProcessor and process the documents
    processor = DocumentProcessor(path, loader_kwargs, chat_model)
    processor.load_documents()  # Load documents
    processor.describe_documents()  # Describe documents
    # Save results to JSON
    processor.save_to_json("lanchain_python/11_docs/output.json")


if __name__ == "__main__":
    main()  # Execute the main function
