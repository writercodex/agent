from ddgs import DDGS


def web_search(
    query,
    max_results=5
):

    try:

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

                link = item.get(
                    "href",
                    item.get(
                        "url",
                        ""
                    )
                )

                results_text.append(
                    f"Title: {title}\n"
                    f"Content: {body}\n"
                    f"URL: {link}"
                )

        if not results_text:
            return "Tidak ada hasil pencarian."

        return "\n\n".join(
            results_text
        )

    except Exception as e:

        return f"Search error: {e}"
