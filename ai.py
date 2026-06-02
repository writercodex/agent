from openai import OpenAI

from config import (
    MIMO_API_KEY,
    MIMO_BASE_URL
)

from memory import (
    get_recent_messages,
    get_summary,
    get_memory,
    save_summary
)

client = OpenAI(
    api_key=MIMO_API_KEY,
    base_url=MIMO_BASE_URL
)


def build_context():

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
                "Jawab singkat, jelas, natural, dan to the point.\n"
                "Anggap owner adalah pengguna utama yang harus kamu bantu.\n"
                "Jangan menggunakan markdown berlebihan.\n"
                "Jangan membuat heading.\n"
                "Jangan membuat laporan panjang kecuali diminta.\n"
                "Jawab seperti chat biasa.\n\n"
                f"PROJECT MEMORY:\n{project_memory}\n\n"
                f"PROJECT SUMMARY:\n{summary}"
            )
        }
    ]

    messages.extend(history)

    return messages


def chat_with_ai(message: str):

    messages = build_context()

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


def chat_with_image(
    base64_image: str,
    mime_type: str = "image/jpeg",
    prompt: str = (
        "Analisa screenshot secara singkat dan natural. "
        "Fokus pada informasi penting. "
        "Jika ada error langsung sebutkan errornya. "
        "Jika dashboard langsung simpulkan statusnya. "
        "Jika kode atau log langsung fokus ke masalahnya. "
        "Jangan menjelaskan semua bagian gambar. "
        "Jawab seperti chat biasa maksimal 3-5 kalimat."
    )
):

    messages = build_context()

    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": (
                            f"data:{mime_type};base64,"
                            f"{base64_image}"
                        )
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    )

    response = client.chat.completions.create(
        model="mimo-v2-omni",
        messages=messages
    )

    return response.choices[0].message.content


def update_project_summary():

    history = get_recent_messages(100)

    messages = [
        {
            "role": "system",
            "content": (
                "Buat ringkasan project dari percakapan berikut. "
                "Fokus pada tujuan project, progress yang sudah selesai, "
                "keputusan penting, dan task yang belum selesai. "
                "Tulis ringkas dan terstruktur."
            )
        }
    ]

    messages.extend(history)

    response = client.chat.completions.create(
        model="mimo-v2.5-pro",
        messages=messages
    )

    summary = response.choices[0].message.content

    save_summary(summary)

    return summary
