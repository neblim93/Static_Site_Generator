from markdown_extraction import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        conversion_nodes = []

        split_text = old_node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError("Invalid markdown syntax")

        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                conversion_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                conversion_nodes.append(TextNode(split_text[i], text_type))

        new_nodes.extend(conversion_nodes)

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        conversion_nodes = []

        extracted_images = extract_markdown_images(old_node.text)
        if len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue

        reference_text = old_node.text
        for image_alt, image_url in extracted_images:
            sections = reference_text.split(f"![{image_alt}]({image_url})", 1)
            if sections[0] != "":
                conversion_nodes.append(TextNode(sections[0], TextType.TEXT))
            conversion_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            reference_text = sections[1]

        if len(reference_text) > 0:
            conversion_nodes.append(TextNode(reference_text, TextType.TEXT))

        new_nodes.extend(conversion_nodes)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        conversion_nodes = []

        extracted_links = extract_markdown_links(old_node.text)
        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue

        reference_text = old_node.text
        for anchor_text, link in extracted_links:
            sections = reference_text.split(f"[{anchor_text}]({link})", 1)
            if sections[0] != "":
                conversion_nodes.append(TextNode(sections[0], TextType.TEXT))
            conversion_nodes.append(TextNode(anchor_text, TextType.LINK, link))
            reference_text = sections[1]

        if len(reference_text) > 0:
            conversion_nodes.append(TextNode(reference_text, TextType.TEXT))

        new_nodes.extend(conversion_nodes)

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes = []
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes
