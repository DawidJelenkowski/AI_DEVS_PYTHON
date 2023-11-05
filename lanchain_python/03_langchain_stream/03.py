from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Initialize an instance of ChatOpenAI configured for streaming
# Streaming allows for real-time interaction with the model, with responses being processed
# as they are generated. A callback handler is set up to handle these streaming responses.
chat = ChatOpenAI(streaming=True,
                  # Callback to handle output
                  callbacks=[StreamingStdOutCallbackHandler()],
                  temperature=0.5)  # Set the creativity of the model's responses

# Send a message to the ChatOpenAI instance asking it to write a song.
# The message is wrapped in a HumanMessage object, which indicates that this is a message
# from a human user rather than a system message.
resp = chat([HumanMessage(content="Write me a song about sparkling water.")])
