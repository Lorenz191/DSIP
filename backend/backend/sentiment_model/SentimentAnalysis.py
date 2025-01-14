import logging

from pathlib import Path
from dotenv import load_dotenv
import deepl
import os
import requests


auth_key = os.getenv("DEEPL_KEY")


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(Path(BASE_DIR).parent / ".env")


class SeAn:

    def __init__(self):
        pass

    def contains_swearwords(self, title, content):
        translator = deepl.Translator(auth_key)
        combined_text = translator.translate_text(
            f"{title}\n{content}", target_lang="EN-GB"
        ).text
        logging.info(f"Combined text: {combined_text}")
        response = requests.post(
            "https://vector.profanity.dev", json={"message": combined_text}
        )
        response_data = response.json()
        logging.info(f"Response: {response_data}")
        flagged = response_data["isProfanity"]

        if flagged:
            return True, "Profanity or inappropriate content detected."
        return False, "Content is clean."
