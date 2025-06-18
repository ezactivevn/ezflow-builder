import subprocess
import os
import shutil

class Laravel:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.env_file = os.path.join(project_path, '.env')
        self.env_example_file = os.path.join(project_path, 'env.txt')
        self.php_path = "php"  # Change if using a custom path

    def run_command(self, command: str) -> bool:
        """Run shell command inside Laravel project folder."""
        if "artisan" in command and "--force" not in command:
            command += " --force"

        print(f"▶️ Running: {command}")
        try:
            subprocess.run(command, shell=True, check=True, cwd=self.project_path)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e}")
            return False

    def install_dependencies(self):
        """Install Laravel PHP dependencies via Composer."""
        self.run_command("composer install --ignore-platform-reqs")

    def copy_env_file(self):
        """Copy env.txt to .env if it doesn't exist."""
        if os.path.exists(self.env_file):
            print("✅ .env file already exists.")
        elif os.path.exists(self.env_example_file):
            shutil.copyfile(self.env_example_file, self.env_file)
            print("✅ .env file copied from env.txt.")
        else:
            print("❌ env.txt file not found.")

    def generate_app_key(self):
        """Generate Laravel APP_KEY."""
        self.run_command(f"{self.php_path} artisan key:generate")

    def migrate_database(self):
        """Run database migrations (fresh)."""
        self.run_command(f"{self.php_path} artisan migrate:fresh")

    def seed_database(self):
        """Seed the database."""
        self.run_command(f"{self.php_path} artisan db:seed")

    def install_passport(self):
        """Install Laravel Passport."""
        self.run_command(f"{self.php_path} artisan passport:install")
        print("✅ Passport installed.")

    def storage_link(self):
        """Create storage symbolic link."""
        self.run_command(f"{self.php_path} artisan storage:link")
        print("✅ Storage link created.")

    def setup_permissions(self):
        """Set correct permissions and ownership for Laravel directories."""
        paths = [
            os.path.join(self.project_path, 'storage'),
            os.path.join(self.project_path, 'bootstrap', 'cache'),
            os.path.join(self.project_path, 'public'),
        ]

        try:
            for path in paths:
                if os.path.exists(path):
                    os.chmod(path, 0o775)
                    subprocess.run(f"chown -R www-data:www-data {path}", shell=True, check=True)
            print("✅ Permissions and ownership set to www-data:www-data.")
        except Exception as e:
            print(f"❌ Failed to set permissions or ownership: {e}")

    def full_setup(self, use_passport: bool = False) -> None:
        """Run full Laravel project setup."""
        print("🚀 Starting Laravel setup...")

        self.copy_env_file()
        self.install_dependencies()
        self.generate_app_key()
        self.migrate_database()

        if use_passport:
            self.install_passport()

        self.seed_database()
        self.storage_link()
        self.setup_permissions()

        print("✅ Laravel setup completed.")
