from openai import OpenAI

from config import (
    MIMO_API_KEY,
    MIMO_BASE_URL
)

from memory import (
    get_recent_messages,
    get_summary,
    get_memory,
    get_all_memories,
    save_summary
)

from search import web_search

client = OpenAI(
    api_key=MIMO_API_KEY,
    base_url=MIMO_BASE_URL
)


def build_context():

    history = get_recent_messages(100)

    summary = get_summary()

    memories = get_all_memories()

    memory_text = ""

    for key, value in memories:
        memory_text += f"{key}: {value}\n"

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
                "Gunakan bahasa Indonesia santai dan natural.\n"
                "Jawab seperti percakapan chat biasa.\n"
                "Jangan gunakan markdown.\n"
                "Jangan gunakan tanda **.\n"
                "Jangan gunakan heading.\n"
                "Jangan gunakan bullet point kecuali diminta.\n"
                "Jangan membuat laporan panjang kecuali diminta.\n"
                "Anggap owner adalah pengguna utama yang harus kamu bantu.\n\n"
                f"OWNER MEMORY:\n{memory_text}\n\n"
                f"PROJECT MEMORY:\n{project_memory}\n\n"
                f"PROJECT SUMMARY:\n{summary}"
            )
        }
    ]

    messages.extend(history)

    return messages


def chat_with_ai(message: str):

    messages = build_context()

    lower_message = message.lower()

    search_triggers = [
        "search ",
        "cari ",
        "google ",
        "berita "
    ]

    should_search = False

    for trigger in search_triggers:
        if lower_message.startswith(trigger):
            should_search = True
            break

    if should_search:

        try:

            search_result = web_search(
                message,
                max_results=5
            )

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "Gunakan hasil pencarian berikut "
                        "untuk menjawab pertanyaan owner.\n\n"
                        f"{search_result}"
                    )
                }
            )

        except Exception as e:

            messages.append(
                {
                    "role": "system",
                    "content": (
                        f"Search error: {e}"
                    )
                }
            )

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
        "Fokus pada informasi penting saja. "
        "Jika ada error langsung sebutkan errornya. "
        "Jika dashboard langsung simpulkan statusnya. "
        "Jika kode atau log langsung fokus ke masalahnya. "
        "Jangan menjelaskan semua bagian gambar. "
        "Jangan gunakan markdown. "
        "Jangan gunakan tanda **. "
        "Jawab seperti chat biasa maksimal 3 sampai 5 kalimat."
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
                "Jangan gunakan markdown. "
                "Jangan gunakan tanda **. "
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
