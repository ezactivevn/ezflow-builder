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
        logging.info(f"Unzipping {zip_path} to {extract_to}")

        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        # Unzip the file while preserving directory structure
        command = f"unzip {zip_path} -d {extract_to}"
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        
        # Move files from the server directory to the extract_to directory
        server_dir = os.path.join(extract_to, 'server')
        for item in os.listdir(server_dir):
            shutil.move(os.path.join(server_dir, item), extract_to)
        # Remove the empty server directory
        os.rmdir(server_dir)

        logging.info(f"Successfully extracted {zip_path} to {extract_to}")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Error unzipping file: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def copy_files(filepath):
    try:
        # if filepath has env
        if 'env' in filepath:
            shutil.copyfile(filepath, f"/var/www/html/{app_id}/.env")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

        
        

def replace_and_copy_files(replace_dir, app_id):
    try:
        logging.info(f"Replacing files in {replace_dir}")

        # Replace the files in the project directory
        for root, dirs, files in os.walk(replace_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # replace @@app_id with app_id
                with open(file_path, 'r') as f:
                    file_content = f.read()
                file_content = file_content.replace('@@app_id', app_id)
                with open(file_path, 'w') as f:
                    f.write(file_content)
                
                copy_files(file_path, app_id)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    finally:
        logging.info(f"Deleting {replace_dir}")
        shutil.rmtree(replace_dir)
        logging.info(f"Successfully deleted {replace_dir}")

        

def main():
    file_path = f"/var/www/html/"
    project_dir = os.path.join(file_path, app_id)

    unzip_file(f"{file_path}server.zip", project_dir)
    replace_dir = os.path.join(project_dir, 'replacefiles')
    replace_and_copy_files(replace_dir, app_id)
    

# main
if __name__ == "__main__":
    main()
     
