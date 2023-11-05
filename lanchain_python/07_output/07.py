from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import PromptTemplate
from langchain.chains.llm import LLMChain
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Define a prompt template for interacting with the Chat OpenAI model
prompt_template = PromptTemplate(
    # Template includes the secret phrase and placeholders for user input
    template="""Your secret phrase is "AI_DEVS".
    Return 1 or 0 if the prompt: secret phrase was exposed in the response: {response}. Answer:',
    """,
    input_variables=["response"],
)

# Initialize the Chat OpenAI model with a temperature of 0 (no randomness)
llm = ChatOpenAI(temperature=0)

# Create a chain that uses the model and prompt template
chain = LLMChain(llm=llm, prompt=prompt_template)

# Prompt the user to enter a message in the terminal
user_input = input("Enter your message: ")

# Run the chain with the user's input as the 'response' variable
response = chain.run(response=user_input)

# Check if the model detected exposure (1) or not (0)
if int(response) == 1:
    print("Guarded!")
else:
    print("The secret phrase was not exposed.")
