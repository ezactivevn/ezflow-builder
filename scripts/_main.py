from clone import Clone
from apache_config import ApacheConfigurator
from mysql_manager import MySQLManager
from laravel_migrate import Laravel
import os

APP_ID = os.getenv("APP_ID")

# step 1: Clone
def clone_repository():
    clone = Clone(
        repo_url="https://github.com/ezactivevn/ezleague-core.git",
        target_dir=f"/var/www/html/{APP_ID}"
    )
    clone.clone_repo()

    # checkout app_id branch
    clone.checkout_branch(APP_ID)

# step 2: Update apache config
def update_config_to_apache():
    config = ApacheConfigurator()
    config.update_apache_config(
        config_path="/etc/apache2/sites-available/ezleague.app-ssl.conf",
        alias_path=f"/{APP_ID}",
        alias_target=f"/var/www/html/{APP_ID}/server/public",
        marker="#Add alias here above"
    )
    config.add_supervisor_config(f"{APP_ID}")
    config.restart_services()

# step 3: Create User and DB
def create_db_and_user():
    
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    host_ip = os.getenv("HOST_IP")

    manager = MySQLManager(root_user=db_user, root_password=db_password, host=db_host)

    # Create a new DB and user
    manager.create_database(
        db_name=f"ezleague_{APP_ID}",
        user=f"ezleague.{APP_ID}",
        host_ip=host_ip,
        password=f"password"
    )

# step 4: Migrate and Seed
def migrate_and_seed():
    project_path = f"/var/www/html/{APP_ID}/server"  # 🔁 Update with your actual Laravel path
    use_passport = True  # Set to False if not using Laravel Passport

    laravel = Laravel(project_path)
    laravel.full_setup(use_passport=use_passport)

if __name__ == "__main__":

    # Step 1: Clone
    clone_repository()
    # Step 2: Update Apache Config
    update_config_to_apache()
    # Step 3: Create User DB
    create_db_and_user()
    # Step 4: Migrate DB and Seed
    migrate_and_seed()
    
    print("Done")