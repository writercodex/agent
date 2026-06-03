from pathlib import Path


GENERATED_DIR = Path(
    "generated"
)

GENERATED_DIR.mkdir(
    exist_ok=True
)


def safe_path(filename):

    filename = str(filename).strip().replace("\\", "/")

    if not filename:
        filename = "output.txt"

    filepath = (GENERATED_DIR / filename).resolve()
    base = GENERATED_DIR.resolve()

    if base not in filepath.parents and filepath != base:
        raise ValueError("Invalid filename")

    return filepath


def create_file(
    filename,
    content
):

    filepath = safe_path(filename)

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

    filepath = safe_path(filename)

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

    filepath = safe_path(filename)

    if not filepath.exists():
        return False

    filepath.unlink()

    return True
