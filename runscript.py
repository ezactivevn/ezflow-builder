import sys
import os

def read_files_in_directory(directory):
    # Iterate over all the files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if it's a file (and not a directory)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as file:
                    content = file.read()
                    try:
                        content = content.decode('utf-8')
                    except UnicodeDecodeError:
                        content = content.decode('latin1')  # Or use another encoding
                    print(f"Contents of {filename}:")
                    print(content)
                    print("-" * 20)
            except Exception as e:
                print(f"Failed to read {filename}: {e}")

def main(cache_dir):
    # Read all files in the cache directory
    read_files_in_directory(cache_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python runscript.py <cache_dir>")
        sys.exit(1)
    cache_dir = sys.argv[1]
    main(cache_dir)
