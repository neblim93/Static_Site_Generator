from block_conversion import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from textnode_splitter import text_to_textnodes


def block_type_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    if block_type == BlockType.HEADING:
        i = 0
        for character in block:
            if character == "#":
                i += 1
            else:
                break
        tag = f"h{i}"
        text = block[i + 1:]
        children_nodes = text_to_children(text)
        return ParentNode(tag, children_nodes)

    if block_type == BlockType.CODE:
        text = block[4:]
        text = text[:-3]
        code_node = TextNode(text, TextType.CODE)
        leaf_node = text_node_to_html_node(code_node)
        return ParentNode("pre", [leaf_node])

    if block_type == BlockType.QUOTE:
        tag = "blockquote"
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            line = line.removeprefix(">")
            line = line.strip()
            new_lines.append(line)
        children_nodes = text_to_children("\n".join(new_lines))
        return ParentNode(tag, children_nodes)

    if block_type == BlockType.UNORDERED_LIST:
        outer_tag = "ul"
        inner_tag = "li"
        lines = block.split("\n")
        children_nodes = []

        for line in lines:
            line = line.removeprefix("-")
            line = line.strip()
            child_node = text_to_children(line)
            children_nodes.append(ParentNode(inner_tag, child_node))

        return ParentNode(outer_tag, children_nodes)

    if block_type == BlockType.ORDERED_LIST:
        outer_tag = "ol"
        inner_tag = "li"
        lines = block.split("\n")
        children_nodes = []
        i = 1

        for line in lines:
            line = line.removeprefix(f"{i}.")
            line = line.strip()
            i += 1
            child_node = text_to_children(line)
            children_nodes.append(ParentNode(inner_tag, child_node))

        return ParentNode(outer_tag, children_nodes)

    if block_type == BlockType.PARAGRAPH:
        tag = "p"
        new_text = block.replace("\n", " ")
        child_node = text_to_children(new_text)
        return ParentNode(tag, child_node)

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []

    for text_node in text_nodes:
        leaf_node = text_node_to_html_node(text_node)
        leaf_nodes.append(leaf_node)

    return leaf_nodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    child_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_type_to_html_node(block, block_type)
        child_nodes.append(block_node)

    div_node = ParentNode("div", child_nodes)
    return div_node
