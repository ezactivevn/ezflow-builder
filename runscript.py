import sys
import os

def list_directory_tree(directory):
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

def main(cache_dir):
    # List the directory tree of the cache directory
    list_directory_tree(cache_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python runscript.py <cache_dir>")
        sys.exit(1)
    cache_dir = sys.argv[1]
    main(cache_dir)
