import os
from clone import Clone
from apache_config import ApacheConfigurator
from mysql_manager import MySQLManager
from laravel_migrate import Laravel

class LaravelDeployer:
    def __init__(self, app_id=None):
        self.app_id = app_id or os.getenv("APP_ID")
        if not self.app_id:
            raise ValueError("APP_ID is required for deployment.")

        self.repo_url = "https://github.com/ezactivevn/ezleague-core.git"
        self.target_dir = f"/var/www/html/{self.app_id}"
        self.project_path = os.path.join(self.target_dir, "server")

        self.db_host = os.getenv("DB_HOST")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASS")

    def clone_repository(self):
        print(f"📦 Cloning repo into {self.target_dir}...")
        clone = Clone(repo_url=self.repo_url, target_dir=self.target_dir)
        clone.clone_repo()
        clone.checkout_branch(self.app_id)
        print("✅ Repository cloned and branch checked out.")

    def update_apache_config(self):
        print("🔧 Updating Apache config...")
        config = ApacheConfigurator()
        config.update_apache_config(
            config_path="/etc/apache2/sites-available/ezleague.app-ssl.conf",
            alias_path=f"/{self.app_id}",
            alias_target=f"{self.target_dir}/server/public",
            marker="#Add alias here above"
        )
        config.add_supervisor_config(self.app_id)
        config.restart_services()
        print("✅ Apache & Supervisor config updated.")

    def create_database_and_user(self):
        if not self.db_host or not self.db_user or not self.db_password:
            raise EnvironmentError("DB credentials missing in environment variables.")

        print("🛢️ Creating MySQL database and user...")
        manager = MySQLManager(
            root_user=self.db_user,
            root_password=self.db_password,
            host=self.db_host
        )

        manager.create_database(
            db_name=f"ezleague_{self.app_id}",
            user=f"ezleague.{self.app_id}",
            host_ip="34.150.91.16",
            password="KhanhHoa79@"
        )
        print("✅ Database and user created.")

    def migrate_and_seed(self):
        print("📂 Running Laravel setup (migrate + seed + passport)...")
        laravel = Laravel(self.project_path)
        laravel.full_setup(use_passport=True)
        print("✅ Laravel setup complete.")

    def deploy(self, skip_clone=False):
        print(f"🚀 Starting deployment for app: {self.app_id}")

        if not skip_clone:
            self.clone_repository()

        self.update_apache_config()
        self.create_database_and_user()
        self.migrate_and_seed()
        print(f"🎉 Deployment for {self.app_id} completed successfully.")

