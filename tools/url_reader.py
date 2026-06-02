import requests

from bs4 import BeautifulSoup


def read_url(url):

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup(
            [
                "script",
                "style",
                "noscript"
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        if not text:
            return "URL_ERROR: Halaman kosong."

        return text[:15000]

    except Exception as e:

        return f"URL_ERROR: {e}"
