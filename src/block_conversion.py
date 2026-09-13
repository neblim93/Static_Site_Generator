from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    lines = markdown.split("\n\n")

    for line in lines:
        new_line = line.strip()
        if new_line == "":
            continue
        blocks.append(new_line)

    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    for line in lines:
        if not line.startswith(">"):
            break
    else:
        return BlockType.QUOTE

    for line in lines:
        if not line.startswith("- "):
            break
    else:
        return BlockType.UNORDERED_LIST

    i = 1

    for line in lines:
        if not line.startswith(f"{i}. "):
            break
        i += 1
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
