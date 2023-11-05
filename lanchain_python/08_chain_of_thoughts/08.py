from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

chat = ChatOpenAI(model='gpt-4')

zs_human_template = "{text}"

# Create a chat prompt template from system and human messages
zero_shot_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the question ultra-briefly:"),
    ("human", zs_human_template),
])

z_chain = zero_shot_prompt | chat

zero_shot_result = z_chain.invoke({"text": "48*62-9"})
zero_shot_content = int(zero_shot_result.content)

system_message = """
Take a deep breath and answer the question by carefully explaining your logic step by step.
Then add the separator: \n### and answer the question ultra-briefly with a single number:
"""

cot_human_template = "{text}"
cot_prompt = ChatPromptTemplate.from_messages([
    ("system", system_message),
    ("human", cot_human_template),
])

cot_chain = cot_prompt | chat

cot_result = cot_chain.invoke({"text": "48*62-9"})
cot_content = int(cot_result.content.split('\n###')[1])


print('Zero Shot:', zero_shot_content,
      "Passed" if zero_shot_content == 2967 else "Failed 🙁")
print('Chain of Thought:', cot_content,
      "Passed" if cot_content == 2967 else "Failed 🙁")
