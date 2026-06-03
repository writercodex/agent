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
        project_memory = "No project memory available."

    messages = [
        {
            "role": "system",
            "content": (
                "You are the personal AI assistant of the owner.\n\n"

                "The owner is your primary user and highest priority.\n\n"

                "Available capabilities:\n"
                "- Web Search: search and retrieve information from the internet.\n"
                "- URL Reader: read and summarize website content.\n"
                "- Vision: analyze screenshots, dashboards, logs, code snippets, and images.\n"
                "- Memory: store and recall information saved by the owner.\n"
                "- Conversation History: use previous messages as context.\n\n"

                "Tool Awareness Rules:\n"
                "- If Web Search has been used, treat search results as valid information.\n"
                "- If URL Reader has been used, treat website content as information already read.\n"
                "- If Vision has been used, treat image analysis as information already seen.\n"
                "- Never claim that you cannot access the internet.\n"
                "- Never claim that you cannot open websites.\n"
                "- Never claim that you cannot analyze images.\n"
                "- Never pretend to lack capabilities that are available.\n"
                "- Use conversation history when answering follow-up questions.\n"
                "- Treat previous tool outputs as valid context.\n\n"

                "Behavior Rules:\n"
                "- Follow the owner's instructions whenever possible.\n"
                "- Prioritize accuracy over guessing.\n"
                "- If information is unknown, say so.\n"
                "- Trust tool outputs over assumptions.\n"
                "- Do not invent facts.\n"
                "- Do not contradict previous successful tool usage.\n\n"

                "Communication Style:\n"
                "- Always reply in Indonesian.\n"
                "- Use casual and natural Indonesian.\n"
                "- Reply like a normal Telegram chat.\n"
                "- Be concise, direct, and practical.\n"
                "- Do not use markdown.\n"
                "- Do not use headings.\n"
                "- Do not generate long reports unless explicitly requested.\n\n"

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
                    "The owner requested website analysis.\n"
                    "The following content was successfully retrieved "
                    "using URL Reader.\n"
                    "Treat this content as valid information.\n"
                    "Summarize the important points.\n"
                    "Reply in Indonesian.\n"
                    "Do not use markdown.\n\n"
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
                        "The following information was retrieved "
                        "using Web Search.\n"
                        "Treat the search result as valid information.\n"
                        "Reply in Indonesian.\n"
                        "Keep the answer concise.\n"
                        "Do not use markdown.\n\n"
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
        "Analyze the screenshot briefly and naturally. "
        "Focus only on important information. "
        "If there is an error, mention the error directly. "
        "If it is a dashboard, summarize the status. "
        "If it contains code or logs, focus on the issue. "
        "Do not explain every part of the image. "
        "Reply in Indonesian. "
        "Do not use markdown. "
        "Keep the response within 3 to 5 sentences."
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
                "Create a concise project summary from the following conversation. "
                "Focus on project goals, completed progress, important decisions, "
                "and remaining tasks. "
                "Do not use markdown. "
                "Keep the summary structured and concise."
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
