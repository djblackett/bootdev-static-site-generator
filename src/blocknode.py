from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE_BLOCK = "code_block"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith("#") and block.count("#") <= 6:
        return BlockType.HEADING
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1.") and is_ascending(block):
        return BlockType.ORDERED_LIST
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE_BLOCK
    elif block.startswith(">") and check_first_chars(block, ">"):
        return BlockType.QUOTE
    else:
        return BlockType.PARAGRAPH


def check_first_chars(block, first_chars):
    valid = True
    for line in block.split("\n"):
        if not line.startswith(first_chars):
            valid = False
            break
    return valid


def is_ascending(block):
    valid = True
    for i, line in enumerate(block.split("\n")):
        if i == 0:
            continue
        if not line.startswith(f"{i + 1}."):
            valid = False
            break
    return valid
