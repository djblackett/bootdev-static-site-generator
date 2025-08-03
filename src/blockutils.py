import re


def markdown_to_blocks(markdown: str):
    sections = re.split(r"\n\s*\n", markdown.strip())
    cleaned = []
    for s in sections:
        trimmed = s.strip()
        if trimmed.count("\n") == 0:
            cleaned.append(trimmed)
        else:
            lines = trimmed.split("\n")
            clean_block = []
            for line in lines:
                if line.strip() != "":
                    clean_block.append(line.strip())
            if clean_block:
                cleaned.append("\n".join(clean_block))
    # Remove empty blocks
    cleaned = [block for block in cleaned if block.strip() != ""]
    # Remove trailing newlines
    cleaned = [block.rstrip("\n") for block in cleaned]
    return cleaned
