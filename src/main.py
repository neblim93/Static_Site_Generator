import os
import shutil
import sys

from generate_page import generate_pages_recursive


def static_to_public():
    if os.path.exists("docs"):
        shutil.rmtree("docs")

    os.mkdir("docs")

    static_copy_recursion("static", "docs")

def static_copy_recursion(source_path, destination_path):
    directory_names = os.listdir(source_path)
    for name in directory_names:
        directory_path = os.path.join(source_path, name)
        destination_directory_path = os.path.join(destination_path, name)

        if os.path.isfile(directory_path):
            shutil.copy(directory_path, destination_directory_path)
            print(destination_directory_path)
        else:
            os.mkdir(destination_directory_path)
            static_copy_recursion(directory_path, destination_directory_path)


def main():
    if len(sys.argv) >= 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    static_to_public()
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
