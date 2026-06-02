from duckduckgo_search import DDGS


def web_search(
    query,
    max_results=5
):

    results_text = []

    try:

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    query,
                    max_results=max_results
                )
            )

        if not results:
            return "SEARCH_EMPTY"

        for item in results:

            title = item.get(
                "title",
                ""
            )

            body = item.get(
                "body",
                ""
            )

            link = item.get(
                "href",
                item.get(
                    "link",
                    ""
                )
            )

            results_text.append(
                f"Title: {title}\n"
                f"Content: {body}\n"
                f"URL: {link}"
            )

        return "\n\n".join(
            results_text
        )

    except Exception as e:

        return f"SEARCH_ERROR: {e}"
