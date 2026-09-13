import os
import shutil

from generate_page import generate_page


def static_to_public():
    if os.path.exists("public"):
        shutil.rmtree("public")

    os.mkdir("public")

    static_copy_recursion("static", "public")

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
    static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")


main()
