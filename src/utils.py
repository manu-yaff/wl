from typing import Optional


def parse_user_input(content: str) -> dict[str, str]:
    current_field: Optional[str | None] = None
    data: dict[str, list[str]] = {}

    for line in content.splitlines():
        if line == "---":
            current_field = None
            continue

        if line.endswith(":"):
            name = line[:-1].strip()
            if name in ("Name", "Context"):
                current_field = name
                data.setdefault(name, [])
                continue

        if current_field:
            data[current_field].append(line)

    result = {field: "\n".join(content).strip() for field, content in data.items()}

    return result
