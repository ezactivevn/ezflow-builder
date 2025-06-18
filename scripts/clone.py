import subprocess
import os

class Clone:
    def __init__(self, repo_url: str, target_dir: str = "."):
        self.repo_url = repo_url
        self.target_dir = target_dir

    def check_git_installed(self) -> bool:
        """Check if Git is installed on the system."""
        try:
            subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False

    def clone_repo(self):
        """Clone the GitHub repository."""
        if not self.check_git_installed():
            print("Git is not installed. Please install Git first.")
            return

        try:
            print(f"Cloning {self.repo_url} into {self.target_dir}")
            subprocess.run(["git", "clone", self.repo_url, self.target_dir], check=True)
            print("Repository cloned successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}")
    
    def checkout_branch(self, app_id: str):
        """Checkout to the branch ezleague/{APP_ID}."""
        branch_name = f"ezleague/{app_id}"
        try:
            print(f"Checking out branch {branch_name}")
            subprocess.run(["git", "checkout", branch_name], check=True, cwd=self.target_dir)
            print(f"✅ Checked out to {branch_name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to checkout branch {branch_name}: {e}")
