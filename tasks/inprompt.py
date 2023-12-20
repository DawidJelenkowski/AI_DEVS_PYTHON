"""
Skorzystaj z API zadania.aidevs.pl, aby pobrać dane zadania inprompt. 
Znajdziesz w niej dwie właściwości — input, czyli tablicę / listę zdań na temat różnych osób 
(każde z nich zawiera imię jakiejś osoby) oraz question będące pytaniem na temat jednej z tych osób. 
Lista jest zbyt duża, aby móc ją wykorzystać w jednym zapytaniu, więc dowolną techniką odfiltruj te zdania, 
które zawierają wzmiankę na temat osoby wspomnianej w pytaniu. 
Ostatnim krokiem jest wykorzystanie odfiltrowanych danych jako kontekst na podstawie którego model ma udzielić odpowiedzi na pytanie. 
Zatem: pobierz listę zdań oraz pytanie, skorzystaj z LLM, aby odnaleźć w pytaniu imię, 
programistycznie lub z pomocą no-code odfiltruj zdania zawierające to imię. 
Ostatecznie spraw by model odpowiedział na pytanie, a jego odpowiedź prześlij do naszego API w obiekcie JSON zawierającym jedną właściwość “answer”.
"""
import re

from open_ai_connector.const import OpenAiModels
from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.solver import Solver
from tasks.blogger import prepare_prompt

ASSISTANT_CONTENT = "Based on this information: {context}, answer to the question"
USER_CONTENT = "Question: {question}"

def inprompt(input_data: dict) -> dict:
    input_list = input_data["input"]
    question = input_data["question"]
    name = re.search(r"\b[A-Z][a-z]*\b", question).group()
    filtered_list = [sentence for sentence in input_list if name in sentence]
    oai = OpenAIConnector()
    prompt = prepare_prompt(
        ASSISTANT_CONTENT.format(context="".join(filtered_list)),
        USER_CONTENT.format(question=question),
    )
    verification_result = oai.generate_answer(
        model=OpenAiModels.gpt3_5_turbo.value, messages=prompt
    )
    prepared_answer = {"answer": verification_result}
    return prepared_answer


if __name__ == "__main__":
    sol = Solver("inprompt")
    sol.solve(inprompt)
