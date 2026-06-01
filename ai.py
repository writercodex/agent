from openai import OpenAI

from config import (
    MIMO_API_KEY,
    MIMO_BASE_URL
)

from memory import (
    get_recent_messages
)

client = OpenAI(
    api_key=MIMO_API_KEY,
    base_url=MIMO_BASE_URL
)


def chat_with_ai(message: str):

    history = get_recent_messages(20)

    messages = [
        {
            "role": "system",
            "content": (
                "Kamu adalah asisten pribadi owner. "
                "Jawab singkat, jelas, to the point. "
                "Ingat konteks percakapan sebelumnya."
            )
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    response = client.chat.completions.create(
        model="mimo-v2.5-pro",
        messages=messages
    )

    return response.choices[0].message.content
