from openai import OpenAI

from config import (
    MIMO_API_KEY,
    MIMO_BASE_URL
)

from memory import (
    get_recent_messages,
    get_summary,
    get_memory
)

client = OpenAI(
    api_key=MIMO_API_KEY,
    base_url=MIMO_BASE_URL
)


def chat_with_ai(message: str):

    history = get_recent_messages(100)

    summary = get_summary()

    project_memory = get_memory(
        "project_memory"
    )

    if not project_memory:
        project_memory = "Belum ada project memory."

    messages = [
        {
            "role": "system",
            "content": (
                "Kamu adalah asisten pribadi owner.\n"
                "Jawab singkat, jelas, dan to the point.\n"
                "Anggap owner adalah pengguna utama yang harus kamu bantu.\n\n"
                f"PROJECT MEMORY:\n{project_memory}\n\n"
                f"PROJECT SUMMARY:\n{summary}"
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
