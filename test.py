from operator import itemgetter

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

model = ChatOpenAI()

prompt1 = ChatPromptTemplate.from_template(
    "generate a {attribute} color. Return the name of the color and nothing else:"
)
prompt2 = ChatPromptTemplate.from_template(
    "what is a fruit of color: {color}. Return the name of the fruit and nothing else:"
)
prompt3 = ChatPromptTemplate.from_template(
    "what is a country with a flag that has the color: {color}. Return the name of the country and nothing else:"
)
prompt4 = ChatPromptTemplate.from_template(
    "What is the color of {fruit} and the flag of {country}?"
)

model_parser = model | StrOutputParser()

color_generator = (
    {"attribute": RunnablePassthrough()} | prompt1 | {"color": model_parser}
)
color_to_fruit = prompt2 | model_parser
color_to_country = prompt3 | model_parser
question_generator = (
    color_generator | {"fruit": color_to_fruit,
                       "country": color_to_country} | prompt4
)

question_generator.invoke("warm")
# if __name__ == "__main__":
