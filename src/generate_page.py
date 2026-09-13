import os

from md_to_html_node import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        new_line = line.strip()
        if new_line.startswith("# "):
            return new_line.removeprefix("# ")

    raise ValueError("no h1 header present")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)
    template_string = template_content.replace("{{ Title }}", title)
    template_string = template_string.replace("{{ Content }}", html_string)

    dir_name = os.path.dirname(dest_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(template_string)
