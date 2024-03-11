import sys
import shutil

def copy_directory(source_dir, destination_dir):
    try:
        shutil.copytree(source_dir, destination_dir)
        print(f"Directory '{source_dir}' copied to '{destination_dir}' successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 copyPNGdirectory.py <source_directory> <destination_directory>")
        sys.exit(1)

    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]

    copy_directory(source_directory, destination_directory)

