import os
import shutil
import sys

app_id = sys.argv[1]

def _replace_config_filepath(filepath, key, value):
        """ Find string @@key to replace"""

        # Find string @@key to replace

        with open(f"{filepath}", "r", encoding="utf-8") as f:
            content = f.read()
            new_content = content.replace("@@" + key, str(value))
            with open(f"{filepath}", "w", encoding="utf-8") as f:
                f.write(new_content)

def _copy_file_to_cache(file_path, project_dir):
    """Copy file to cache"""
    # if filename contains variables
    if "env.txt" in file_path:
        shutil.copy(file_path, f"{project_dir}/server/.env")

def replace_and_copy_files(self, cache_dir, app_info):

        test_cache_dir = os.path.join(cache_dir, 'replacefiles')
        try:
            # loop in test_cache_dir
            for filename in os.listdir(test_cache_dir):
                if filename.endswith(".txt"):
                    file_path = os.path.join(test_cache_dir, filename)
                    print("File path:", file_path)
                    for key, value in app_info.__dict__.items():
                        print(key, ":", value)  
                        _replace_config_filepath(file_path, key, value)
                        _copy_file_to_cache(file_path, cache_dir)
        except Exception as e:
            print(f"Error: {e}")


def main():
    zip_path = f"/var/www/html/server.zip"

    shutil.unpack_archive(zip_path, f"/var/www/html{app_id}")

    replace_and_copy_files(app_id, app_id)


# main
if __name__ == "__main__":
    main()
     
