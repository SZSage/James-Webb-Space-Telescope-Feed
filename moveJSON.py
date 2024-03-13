"""moveJSON.py copies contents from the metadata into the JS template file
testJSON.py
"""

import sys


def write_file_from_another(file_path, content_file):
    first_line = "const datav7 ="
    last_line = ";\nexport default datav7"
    with open(content_file, "r") as content:
        content_to_write = content.read()

    with open(file_path, "w") as file:
        file.write(first_line)
        file.write(content_to_write)
        file.write(last_line)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python moveJSON.py <file_path> <content_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    content_file = sys.argv[2]

    write_file_from_another(file_path, content_file)
