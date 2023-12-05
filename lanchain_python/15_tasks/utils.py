from datetime import datetime
import json
from typing import Any, List, String
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


def convert_objects_to_json(objects: List[Any]) -> str:
    objects_as_dicts: list = [vars(obj) for obj in objects]
    return json.dumps(objects_as_dicts, indent=4)


def current_date():
    date = datetime.now()

    weekdays = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday = weekdays[date.weekday()]

    month = date.strftime('%m')  # months are 1-based in Python
    day = date.strftime('%D')
    year = date.strftime('%Y')

    hours = date.strftime('%H')
    minutes = date.strftime('%M')

    return f"{weekday}, {month}/{day}/{year} {hours}:{minutes}"


def rephrase(response: String, query: String):
    llm = ChatOpenAI(model="gpt-4", temperature=1)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """Answer the question ultra-briefly using casual, human-friendly tone:
        ###${query}###
        and act as if you just performed this action and confirming this fact to the user, using the following response: 
        ###{response}###
        """),
        ]
    )
