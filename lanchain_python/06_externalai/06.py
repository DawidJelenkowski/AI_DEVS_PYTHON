"""
The prompt below doesn't work because chat GPT is not capable of solving datetime related problems. 
"""
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

system_template = """
You are given code in python how to count days, answer the question.
from datetime import datetime, timedelta
# Q: 2015 is coming in 36 hours. What is the date one week from today in MM/DD/YYYY?
# If 2015 is coming in 36 hours, then today is 36 hours before.
today = datetime(2015, 1, 1)
today -= timedelta(hours=36)
# One week from today,
one_week_from_today = today + timedelta(days=7)
# The answer formatted with MM/DD/YYYY is
one_week_from_today.strftime('%m/%d/%Y')

# Q: The first day of 2019 is a Tuesday, and today is the first Monday of 2019. What is the date today in MM/DD/YYYY?
# If the first day of 2019 is a Tuesday, and today is the first Monday of 2019, then today is 6 days later.
today = datetime(2019, 1, 1)
today += timedelta(days=6)
# The answer formatted with MM/DD/YYYY is
today.strftime('%m/%d/%Y')

# Q: The concert was scheduled to be on 06/01/1943, but was delayed by one day to today. What is the date 10 days ago in MM/DD/YYYY?
# If the concert was scheduled to be on 06/01/1943, but was delayed by one day to today, then today is one day later.
today = datetime(1943, 6, 1)
today += timedelta(days=1)
# 10 days ago,
ten_days_ago = today - timedelta(days=10)
# The answer formatted with MM/DD/YYYY is
ten_days_ago.strftime('%m/%d/%Y')

# Q: It is 4/19/1969 today. What is the date 24 hours later in MM/DD/YYYY?
# It is 4/19/1969 today.
today = datetime(1969, 4, 19)
# 24 hours later,
later = today + timedelta(days=1)
# The answer formatted with MM/DD/YYYY is
later.strftime('%m/%d/%Y')

# Q: Jane thought today is 3/11/2002, but today is in fact Mar 12, which is 1 day later. What is the date 24 hours later in MM/DD/YYYY?
# If Jane thought today is 3/11/2002, but today is in fact Mar 12, then today is 3/12/2002.
today = datetime(2002, 3, 12)
# 24 hours later,
later = today + timedelta(days=1)
# The answer formatted with MM/DD/YYYY is
later.strftime('%m/%d/%Y')

# Q: Jane was born on the last day of February in 2001. Today is her 16-year-old birthday. What is the date yesterday in MM/DD/YYYY?
# If Jane was born on the last day of February in 2001 and today is her 16-year-old birthday, then today is 16 years later.
today = datetime(2001, 2, 28)
today = today.replace(year=today.year + 16)
# Yesterday,
yesterday = today - timedelta(days=1)
# The answer formatted with MM/DD/YYYY is
yesterday.strftime('%m/%d/%Y')
"""

# Define a template for human messages where the actual question will be formatted in.
human_template = "Q: {question}"

# Construct a chat prompt using a system message and a human message.
# ChatPromptTemplate is likely a custom class that formats messages for a conversational AI.
chat_prompt = ChatPromptTemplate.from_messages([("system", system_template),
                                                ("human", human_template),])

# Format the chat prompt with a specific question about calculating a future date.
formatted_chat_prompt = chat_prompt.format_messages(
    question="Today is October 13, 2023. What will the date after 193 days from now in the format MM/DD/YYYY?")

# Create an instance of ChatOpenAI with a specified model (likely 'gpt-4' in this case).
chat = ChatOpenAI(model="gpt-4")

# Use the ChatOpenAI instance to predict a response to the formatted chat prompt.
# The predict_messages method will process the prompt and generate a response.
content = chat.predict_messages(formatted_chat_prompt)

print(content)
print("Actual Date:", content)
