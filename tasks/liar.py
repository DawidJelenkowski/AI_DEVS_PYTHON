"""
API: wykonaj zadanie o nazwie liar. Jest to mechanizm, który mówi nie na temat w 1/3 przypadków. 
Twoje zadanie polega na tym, aby do endpointa /task/ wysłać swoje pytanie w języku angielskim (dowolne, np "What is capital of Poland?") 
w polu o nazwie 'question' (metoda POST, jako zwykłe pole formularza, NIE JSON). 
System API odpowie na to pytanie (w polu 'answer') lub zacznie opowiadać o czymś zupełnie innym, zmieniając temat. 
Twoim zadaniem jest napisanie systemu filtrującego (Guardrails), który określi (YES/NO), czy odpowiedź jest na temat. 
Następnie swój werdykt zwróć do systemu sprawdzającego jako pojedyncze słowo YES/NO. 
Jeśli pobierzesz treść zadania przez API bez wysyłania żadnych dodatkowych parametrów, otrzymasz komplet podpowiedzi. 
Skąd wiedzieć, czy odpowiedź jest 'na temat'? 
Jeśli Twoje pytanie dotyczyło stolicy Polski, a w odpowiedzi otrzymasz spis zabytków w Rzymie, to odpowiedź, którą należy wysłać do API to NO.
"""
from pprint import pprint

from open_ai_connector.const import OpenAiModels
from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.solver import Solver
from tasks.blogger import prepare_prompt

ASSISTANT_CONTENT = "You need to verify the answer to a question. If the answer is correct return YES, if not return NO"
USER_CONTENT = "Question: {question}. Answer: {answer}"


def liar(question: str, answer_from_api: dict):
    answer = answer_from_api["answer"]
    oai = OpenAIConnector()
    prompt = prepare_prompt(
        ASSISTANT_CONTENT, USER_CONTENT.format(
            question=question, answer=answer)
    )
    verification_result = oai.generate_answer(
        model=OpenAiModels.gpt3_5_turbo.value, messages=prompt
    )
    prepared_answer = {"answer": verification_result}
    return prepared_answer


if __name__ == "__main__":
    question = "Is overment a bio-robot?"
    sol = Solver("liar")
    sol.solve(liar, question=question)
