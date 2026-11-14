import os

import requests
from dotenv import load_dotenv

load_dotenv()


class NvidiaAssistant:
    """Cliente opcional para endpoints NVIDIA NIM compativeis com Chat Completions."""

    def __init__(self) -> None:
        self.api_key = os.getenv("NVIDIA_API_KEY", "").strip()
        self.model = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3.5-bolt-e4b").strip()
        self.base_url = os.getenv(
            "NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"
        ).rstrip("/")

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def ask(self, prompt: str) -> str:
        if not self.configured:
            return "NVIDIA ainda não configurada. Preencha NVIDIA_API_KEY no arquivo .env."
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "Você é o Jarvis, assistente do RollOS. Responda em "
                                "português brasileiro. Não afirme controlar hardware "
                                "que ainda não esteja conectado."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                    "max_tokens": 900,
                },
                timeout=90,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except requests.Timeout:
            return "A NVIDIA demorou para responder. Tente novamente."
        except requests.RequestException as exc:
            detail = str(exc)
            if exc.response is not None:
                detail = f"HTTP {exc.response.status_code}: {exc.response.text[:400]}"
            return f"Falha ao consultar NVIDIA: {detail}"
        except (KeyError, IndexError, ValueError):
            return "A NVIDIA retornou uma resposta em formato inesperado."
