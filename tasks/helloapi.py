"""
API zawsze odpowiada w formacie JSON
Kod błedu 0 (zero) oznacza zaliczone zadanie
Ujemne kody błędów to errory (ich wyjaśnienie jest w polu 'msg')
Od pobrania pytania, na udzielenie odpowiedzi masz 120 sekund
"""
from solver.solver import Solver


def hello_api(input_data: dict) -> dict:
    processed_data = input_data["cookie"]
    prepared_answer = {"answer": processed_data}
    return prepared_answer


if __name__ == "__main__":
    sol = Solver("helloapi")
    sol.solve(hello_api)
