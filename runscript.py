import sys
import os

def read_files_in_directory(directory):
    # Iterate over all the files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if it's a file (and not a directory)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                print(f"Contents of {filename}:")
                print(content)
                print("-" * 20)

def main(cache_dir):
    # Read all files in the cache directory
    read_files_in_directory(cache_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <cache_dir>")
        sys.exit(1)
    cache_dir = sys.argv[1]
    main(cache_dir)
