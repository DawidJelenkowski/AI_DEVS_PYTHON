from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "query_enrichment",
            "description": "Describe users query with semantic tags and classify with type",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "boolean",
                        "description": "Set to 'true' when query is direct command for AI. Set to 'false' when queries asks for saying/writing/translating/explaining something and all other."
                    },
                    "type": {
                        "type": "string",
                        "description": "memory (queries about the user and/or AI), notes|links (queries about user's notes|links). By default pick 'memory'.",
                        "enum": ["memory", "notes", "links"]
                    },
                    "tags": {
                        "type": "array",
                        "description": "Multiple semantic tags/keywords that enriches query for search purposes (similar words, meanings). When query refers to the user, add 'overment' tag, and when refers to 'you' add tag 'Alice'",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["type", "tags", "command"]
            }
        }
    }
]


messages = [{"role": "user", "content": "Hi there!"}]
completion = client.chat.completions.create(
    model="gpt-4-0613",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

content = completion.choices[0].message.content
print(content)
