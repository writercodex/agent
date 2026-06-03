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
from tools.file_manager import (
    create_file,
    read_file,
    list_files,
    delete_file
)

import json


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
                "- File Manager: create, read, list, and delete files when requested.\n"
                "- Memory: store and recall information saved by the owner.\n"
                "- Conversation History: use previous messages as context.\n\n"

                "File Rules:\n"
                "- When the owner asks you to create, make, generate, write, save, or export a file, use create_file.\n"
                "- Do not only describe the file. Actually call the file tool.\n"
                "- Use the filename requested by the owner.\n"
                "- If no filename is provided, choose a clear filename with the right extension.\n"
                "- For text files use .txt, markdown use .md, HTML use .html, CSV use .csv, JSON use .json, Python use .py.\n"
                "- Put the complete final content inside the file.\n\n"

                "Tool Awareness Rules:\n"
                "- If Web Search has been used, treat search results as valid information.\n"
                "- If URL Reader has been used, treat website content as information already read.\n"
                "- If Vision has been used, treat image analysis as information already seen.\n"
                "- If File Manager has been used, treat created/read files as real files.\n"
                "- Never claim that you cannot access the internet.\n"
                "- Never claim that you cannot open websites.\n"
                "- Never claim that you cannot analyze images.\n"
                "- Never claim that you cannot create files.\n"
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


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "max_results": {
                        "type": "integer",
                        "default": 5
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_url",
            "description": "Read and extract text content from a URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string"
                    }
                },
                "required": [
                    "url"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Create a file with the exact filename and content requested by the owner.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "File name including extension, e.g. notes.txt, report.md, index.html, data.csv"
                    },
                    "content": {
                        "type": "string",
                        "description": "Complete file content to write."
                    }
                },
                "required": [
                    "filename",
                    "content"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a previously generated file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string"
                    }
                },
                "required": [
                    "filename"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List generated files.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a previously generated file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string"
                    }
                },
                "required": [
                    "filename"
                ]
            }
        }
    }
]


def run_tool(
    name,
    arguments
):

    if name == "web_search":
        return web_search(
            arguments.get(
                "query",
                ""
            ),
            max_results=arguments.get(
                "max_results",
                5
            )
        )

    if name == "read_url":
        return read_url(
            arguments.get(
                "url",
                ""
            )
        )

    if name == "create_file":
        path = create_file(
            arguments.get(
                "filename",
                "output.txt"
            ),
            arguments.get(
                "content",
                ""
            )
        )

        return {
            "status": "created",
            "path": path
        }

    if name == "read_file":
        content = read_file(
            arguments.get(
                "filename",
                ""
            )
        )

        return {
            "status": "found" if content is not None else "not_found",
            "content": content
        }

    if name == "list_files":
        return {
            "files": list_files()
        }

    if name == "delete_file":
        deleted = delete_file(
            arguments.get(
                "filename",
                ""
            )
        )

        return {
            "status": "deleted" if deleted else "not_found"
        }

    return {
        "error": f"Unknown tool: {name}"
    }


def chat_with_ai(
    message: str
):

    messages = build_context()

    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    created_files = []

    try:
        response = client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

    except Exception:
        response = client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=messages
        )

        reply = response.choices[0].message.content

        return {
            "text": clean_response(
                reply
            ),
            "files": []
        }

    assistant_message = response.choices[0].message

    tool_calls = getattr(
        assistant_message,
        "tool_calls",
        None
    )

    loops = 0

    while tool_calls and loops < 5:

        loops += 1

        messages.append(
            assistant_message
        )

        for tool_call in tool_calls:

            name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments or "{}"
                )

            except Exception:
                arguments = {}

            result = run_tool(
                name,
                arguments
            )

            if name == "create_file" and isinstance(
                result,
                dict
            ):

                path = result.get(
                    "path"
                )

                if path:
                    created_files.append(
                        path
                    )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False
                    )
                }
            )

        response = client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        tool_calls = getattr(
            assistant_message,
            "tool_calls",
            None
        )

    reply = assistant_message.content or "Selesai."

    if created_files:

        reply = clean_response(
            reply
        )

        if "file" not in reply.lower():
            reply = f"File berhasil dibuat: {', '.join(created_files)}"

    return {
        "text": clean_response(
            reply
        ),
        "files": created_files
    }


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
