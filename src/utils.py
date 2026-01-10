from typing import Optional


class InvalidId(Exception):
    pass


class Id:
    @staticmethod
    def validate(id: int | str | None):
        if id is None:
            raise InvalidId()

        try:
            int(id)
        except Exception:
            raise InvalidId()


def parse_user_input(content: str, keys_to_extract: tuple) -> dict[str, str]:
    current_field: Optional[str | None] = None
    data: dict[str, list[str]] = {}

    for line in content.splitlines():
        if line == "---":
            current_field = None
            continue

        if line.endswith(":"):
            name = "_".join(line[:-1].split()).lower()
            if name in keys_to_extract:
                current_field = name
                data.setdefault(name, [])
                continue

        if current_field:
            data[current_field].append(line)

    result = {field: "\n".join(content).strip() for field, content in data.items()}

    return result
