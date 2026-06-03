from pathlib import Path


GENERATED_DIR = Path(
    "generated"
)

GENERATED_DIR.mkdir(
    exist_ok=True
)


def create_file(
    filename,
    content
):

    filepath = GENERATED_DIR / filename

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(content)

    return str(
        filepath
    )


def read_file(
    filename
):

    filepath = GENERATED_DIR / filename

    if not filepath.exists():
        return None

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


def list_files():

    return [
        str(f)
        for f in GENERATED_DIR.rglob("*")
        if f.is_file()
    ]


def delete_file(
    filename
):

    filepath = GENERATED_DIR / filename

    if not filepath.exists():
        return False

    filepath.unlink()

    return True
