import logging
import os
import zipfile
import shutil
import subprocess

app_id = os.environ.get('APP_ID')
sudo_password = os.environ.get('GCLOUD_PASSWORD')

logging.basicConfig(level=logging.DEBUG)

def unzip_file(zip_path, extract_to):
    try:
        
        # Unzipping requires sudo
        command = f"echo {sudo_password} | sudo -S unzip -o {zip_path} -d {extract_to}"
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        logging.info(f"Successfully extracted {zip_path} to {extract_to}")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Error unzipping file with sudo: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")



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

    unzip_file(f"{file_path}server.zip", project_dir)
    replace_and_copy_files(project_dir, app_id)
    

# main
if __name__ == "__main__":
    main()
     
