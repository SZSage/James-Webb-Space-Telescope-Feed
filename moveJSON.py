import sys

def insert_file_at_line(original_file, insert_file, line_number):
    with open(original_file, 'r') as original:
        original_lines = original.readlines()

    with open(insert_file, 'r') as insert:
        insert_lines = insert.readlines()

    # Insert insert_file contents into original_file at specified line number
    original_lines[line_number:line_number] = insert_lines

    with open(original_file, 'w') as output:
        output.writelines(original_lines)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <original_file> <insert_file> <line_number>")
        sys.exit(1)

    original_file = sys.argv[1]
    insert_file = sys.argv[2]
    line_number = int(sys.argv[3])

    insert_file_at_line(original_file, insert_file, line_number)

