import os
from pathlib import Path

from md_to_html_node import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        new_line = line.strip()
        if new_line.startswith("# "):
            return new_line.removeprefix("# ")

    raise ValueError("no h1 header present")


def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)
    template_string = template_content.replace("{{ Title }}", title)
    template_string = template_string.replace("{{ Content }}", html_string)
    template_string = template_string.replace('href="/', f'href="{base_path}')
    template_string = template_string.replace('src="/', f'src="{base_path}')

    dir_name = os.path.dirname(dest_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template_string)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str
):
    directory_names = os.listdir(dir_path_content)

    for name in directory_names:
        directory_path = os.path.join(dir_path_content, name)
        destination_directory_path = os.path.join(dest_dir_path, name)

        if os.path.isfile(directory_path):
            new_name = Path(name).with_suffix(".html")
            destination_directory_path = os.path.join(dest_dir_path, new_name)
            generate_page(directory_path, template_path, destination_directory_path, base_path)
        else:
            generate_pages_recursive(
                directory_path, template_path, destination_directory_path, base_path
            )
