"""
Korzystając z modelu Whisper wykonaj zadanie API (zgodnie z opisem na zadania.aidevs.pl) o nazwie whisper. 
W ramach zadania otrzymasz plik MP3 (15 sekund), 
który musisz wysłać do transkrypcji, a otrzymany z niej tekst odeślij jako rozwiązanie zadania.
"""
import os
import tempfile

import requests

from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.solver import Solver
from tasks.common import extract_url


def whisper(input_data: dict):
    # Extract the URL of the MP3 file from the input data
    url_with_mp3 = extract_url(input_data["msg"])

    # Make an HTTP request to download the MP3 file
    response = requests.get(url_with_mp3)

    # Create a temporary file to save the MP3 file
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".mp3", dir=tempfile.gettempdir()
    ) as temp_file:
        # Write the content of the downloaded file to the temporary file
        temp_file.write(response.content)

        # Open the temporary MP3 file in binary read mode
        audio_file = open(
            os.path.join(tempfile.gettempdir(),
                         os.path.basename(temp_file.name)), "rb"
        )

        # Create an instance of OpenAIConnector
        oai = OpenAIConnector()

        # Use the Whisper model (or similar) to transcribe the audio file
        transcript = oai.use_whisperer(audio_file)

        # Prepare the answer with the transcript
        prepared_answer = {"answer": transcript}
        return prepared_answer


if __name__ == "__main__":
    sol = Solver("whisper")
    sol.solve(whisper)
