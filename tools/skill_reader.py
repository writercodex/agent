import requests


ACTIVE_SKILL = {
    "url": None,
    "content": None
}


def read_skill_from_url(url):

    try:
        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        content = response.text.strip()

        if not content:
            return {
                "status": "error",
                "output": "Skill kosong."
            }

        ACTIVE_SKILL["url"] = url
        ACTIVE_SKILL["content"] = content[:30000]

        return {
            "status": "success",
            "url": url,
            "content": ACTIVE_SKILL["content"]
        }

    except Exception as e:
        return {
            "status": "error",
            "output": str(e)
        }


def get_active_skill():

    return ACTIVE_SKILL
