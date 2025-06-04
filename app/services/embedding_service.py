import requests
import os

CLOVA_API_URL = os.getenv("CLOVA_EMBEDDING_URL")
CLOVA_API_KEY = os.getenv("CLOVA_EMBEDDING_KEY")

def get_embedding_from_clova(text: str) -> list[float]:
    response = requests.post(
        CLOVA_API_URL,
        headers={
            "Authorization": f"Bearer {CLOVA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={"text": text}
    )
    response.raise_for_status()
    return response.json()["embedding"]
