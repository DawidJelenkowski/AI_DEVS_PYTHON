"""
Korzystając z modelu text-embedding-ada-002 wygeneruj embedding dla frazy Hawaiian pizza — upewnij się, że to dokładnie to zdanie. 
Następnie prześlij wygenerowany embedding na endpoint /answer. 
Konkretnie musi być to format 
{"answer": [0.003750941, 0.0038711438, 0.0082909055, -0.008753223, -0.02073651, -0.018862579, -0.010596331, -0.022425512, ..., -0.026950065]}. 
Lista musi zawierać dokładnie 1536 elementów.
"""
from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.solver import Solver


def embedding(to_embedded: str):
    oai = OpenAIConnector()
    embedding = oai.generate_embedding(to_embedded)
    prepared_answer = {"answer": embedding}
    return prepared_answer


if __name__ == "__main__":
    text_for_embedding = "Hawaiian pizza"
    sol = Solver("embedding")
    sol.solve(embedding, additional_data=text_for_embedding)
