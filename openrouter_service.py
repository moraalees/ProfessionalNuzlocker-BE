import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openrouter/free"

SYSTEM_PROMPT = """Eres NuzBot, asistente de Pokémon Black & White para partidas Nuzlocke.
Solo respondes preguntas sobre Pokémon. Si preguntan algo fuera de Pokémon, dilo amablemente.
Tienes acceso al estado de la partida del jugador. Sé breve y útil.
Responde siempre en español y terminando tu mensaje con 'Si necesitas algo más, dilo, xyz', donde xyz es el nombre del jugador que recibes."""


def ask_llm(game_context: str, user_message: str) -> str:
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY.startswith("sk-or-xxxx"):
        return f"[STUB - sin API key] Recibido contexto y pregunta: '{user_message}'"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"[Estado de mi partida]\n{game_context}\n\n[Pregunta]\n{user_message}",
            },
        ],
        "max_tokens": 250,
        "temperature": 0.7,
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if not response.ok:
        print(f"[openrouter error] {response.status_code}: {response.text}")
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
