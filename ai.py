from openai import OpenAI

from config import (
    MIMO_API_KEY,
    MIMO_BASE_URL
)

client = OpenAI(
    api_key=MIMO_API_KEY,
    base_url=MIMO_BASE_URL
)


def chat_with_ai(message: str):

    response = client.chat.completions.create(
        model="mimo-v2.5-pro",
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah asisten pribadi owner. "
                    "Jawab singkat, jelas, dan to the point."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content
