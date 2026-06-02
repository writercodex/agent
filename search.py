from duckduckgo_search import DDGS


def web_search(query, max_results=5):

    results_text = []

    with DDGS() as ddgs:

        results = ddgs.text(
            query,
            max_results=max_results
        )

        for item in results:

            title = item.get(
                "title",
                ""
            )

            body = item.get(
                "body",
                ""
            )

            href = item.get(
                "href",
                ""
            )

            results_text.append(
                f"Title: {title}\n"
                f"Content: {body}\n"
                f"URL: {href}"
            )

    return "\n\n".join(
        results_text
    )
