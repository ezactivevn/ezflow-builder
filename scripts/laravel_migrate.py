import subprocess
import os
import shutil

class Laravel:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.env_file = os.path.join(project_path, '.env')
        self.env_example_file = os.path.join(project_path, 'env.txt')
        self.php_path = "php"  # adjust if using PHP 8.x or custom path

    def run_command(self, command: str):
        """Run shell command inside Laravel project folder."""
        print(f"▶️ Running: {command}")
        try:
            subprocess.run(command, shell=True, check=True, cwd=self.project_path)
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e}")

    def copy_env_file(self):
        """Copy .env.example to .env if it doesn't exist."""
        if os.path.exists(self.env_file):
            print("✅ .env file already exists.")
        elif os.path.exists(self.env_example_file):
            shutil.copyfile(self.env_example_file, self.env_file)
            print("✅ .env file copied from env.txt.")
        else:
            print("❌ .env.txt file not found.")

    def generate_app_key(self):
        """Run artisan key:generate."""
        self.run_command(f"{self.php_path} artisan key:generate")

    def migrate_database(self):
        """Run artisan migrate."""
        self.run_command(f"{self.php_path} artisan migrate --seed")

    def install_passport(self):
        """Install Laravel Passport (optional)."""
        self.run_command(f"{self.php_path} artisan migrate")
        self.run_command(f"{self.php_path} artisan passport:install")
        print("✅ Passport installed.")


    def full_setup(self, use_passport=False):
        print("🚀 Starting Laravel setup...")
        self.copy_env_file()
        self.generate_app_key()
        self.migrate_database()
        if use_passport:
            self.install_passport()
        print("✅ Laravel setup completed.")

