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

from tools.search import web_search
from tools.url_reader import read_url

import re

client = OpenAI(
    api_key=MIMO_API_KEY,
    base_url=MIMO_BASE_URL
)


def clean_response(text):

    if not text:
        return ""

    replacements = [
        "**",
        "__",
        "###",
        "##",
        "#",
        "```"
    ]

    for item in replacements:
        text = text.replace(
            item,
            ""
        )

    return text.strip()


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
                "Gunakan bahasa Indonesia santai.\n"
                "Jawab seperti chat Telegram biasa.\n"
                "Jawab singkat, jelas dan natural.\n"
                "Jangan menggunakan markdown.\n"
                "Jangan menggunakan tanda **.\n"
                "Jangan membuat heading.\n"
                "Jangan membuat artikel.\n"
                "Jangan membuat laporan panjang kecuali diminta.\n"
                "Kalau pertanyaan sederhana jawab sederhana.\n"
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

    url_match = re.search(
        r'https?://\S+',
        message
    )

    if url_match:

        url = url_match.group(0)

        url_content = read_url(
            url
        )

        messages.append(
            {
                "role": "system",
                "content": (
                    "Berikut isi website yang diminta owner.\n"
                    "Ringkas isi website secara singkat.\n"
                    "Fokus pada informasi penting.\n"
                    "Jawab seperti chat biasa.\n"
                    "Jangan gunakan markdown.\n\n"
                    f"{url_content}"
                )
            }
        )

    else:

        search_triggers = [
            "search ",
            "cari ",
            "google ",
            "berita ",
            "news ",
            "terbaru "
        ]

        should_search = False

        for trigger in search_triggers:
            if lower_message.startswith(trigger):
                should_search = True
                break

        if should_search:

            search_result = web_search(
                message,
                max_results=5
            )

            messages.append(
                {
                    "role": "system",
                    "content": (
                        "Berikut hasil pencarian internet.\n"
                        "Gunakan hasil ini untuk menjawab.\n"
                        "Jangan membuat daftar panjang.\n"
                        "Jangan membuat artikel.\n"
                        "Ringkas hasil pencarian dalam gaya chat biasa.\n"
                        "Jika hasil kosong atau error, katakan apa adanya.\n\n"
                        f"{search_result}"
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

    reply = response.choices[0].message.content

    return clean_response(
        reply
    )


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

    reply = response.choices[0].message.content

    return clean_response(
        reply
    )


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

    save_summary(
        clean_response(summary)
    )

    return clean_response(
        summary
    )
