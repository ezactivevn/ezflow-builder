import os
import shutil
import sys
import subprocess

app_id = sys.argv[1]

def unzip_file_to_dir(file_path, project_dir):
    """Unzip file to dir"""
    zip_file = os.path.join(file_path, 'server.zip')
    
    # Ensure the project directory exists
    os.makedirs(project_dir, exist_ok=True)
    
    # Construct the command
    command = ['unzip', zip_file, '-d', project_dir]
    
    # Execute the command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error unzipping file: {e.stderr}")



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

def replace_and_copy_files( cache_dir, app_info):

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
    file_path = f"/var/www/html/"
    project_dir = os.path.join(file_path, app_id)
    unzip_file_to_dir(file_path, project_dir)
    replace_and_copy_files(project_dir, app_id)
    

# main
if __name__ == "__main__":
    main()
     
