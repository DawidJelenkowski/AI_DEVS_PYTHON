"""
Zastosuj wiedzę na temat działania modułu do moderacji treści i rozwiąż zadanie o nazwie “moderation” z użyciem naszego API do sprawdzania rozwiązań.
Zadanie polega na odebraniu tablicy zdań (4 sztuki), a następnie zwróceniu tablicy z informacją, które zdania nie przeszły moderacji. 
Jeśli moderacji nie przeszło pierwsze i ostatnie zdanie, to odpowiedź powinna brzmieć [1,0,0,1]. Pamiętaj, aby w polu  'answer' zwrócić tablicę w JSON, a nie czystego stringa.
"""
from typing import List

from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.solver import Solver


def moderation(input_data: dict):
    sentences: List[str] = input_data["input"]
    oai = OpenAIConnector()
    verdicts = [*map(int, oai.moderate_prompt(sentences))]
    prepared_answer = {"answer": verdicts}
    return prepared_answer


if __name__ == "__main__":
    sol = Solver("moderation")
    sol.solve(moderation)
