import os
import shutil
import subprocess

class FirebaseDeployer:
    def __init__(self, site_id=None, firebase_token=None):
        self.site_id = site_id or os.getenv("APP_ID")  # fallback từ APP_ID nếu site_id không truyền vào
        self.firebase_token = firebase_token or os.getenv("FIREBASE_TOKEN")

        if not self.firebase_token:
            raise ValueError("❌ Missing FIREBASE_TOKEN environment variable.")
        if not self.site_id:
            raise ValueError("❌ Missing site_id or APP_ID.")

        self.client_path = "client"

    def check_node_modules(self):
        return os.path.isdir(os.path.join(self.client_path, "node_modules")) and \
               os.path.exists(os.path.expanduser("~/.npm"))

    def check_firebase_tools(self):
        return shutil.which("firebase") is not None

    def install_dependencies(self):
        if not self.check_node_modules():
            print("📦 Installing client dependencies...")
            subprocess.run(f"cd {self.client_path} && npm install --legacy-peer-deps", shell=True, check=True)
        else:
            print("✅ Dependencies already installed.")

    def install_firebase_tools(self):
        if not self.check_firebase_tools():
            print("🛠️ Installing Firebase CLI...")
            subprocess.run("npm install -g firebase-tools", shell=True, check=True)
        else:
            print("✅ Firebase CLI already installed.")

    def build_client(self):
        npm_path = shutil.which("npm")
        if not npm_path:
            raise FileNotFoundError("❌ npm not found in PATH.")

        print("🔧 Building client app...")
        log_file_path = os.path.join(self.client_path, "build_log.txt")
        with open(log_file_path, 'w') as log_file:
            process = subprocess.Popen(
                [npm_path, 'run', 'build'],
                cwd=self.client_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    log_file.write(output)
                    print(output.strip())

            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, process.args)
        print("✅ Client build completed.")

    def create_site(self):
        print(f"🌐 Creating Firebase site `{self.site_id}` if not exists...")
        try:
            command = f"cd {self.client_path} && firebase hosting:sites:create {self.site_id} --token {self.firebase_token}"
            subprocess.run(command, shell=True, check=True)
            print("✅ Site created.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Site may already exist: {e}")

    def apply_hosting_target(self):
        print(f"🎯 Applying hosting target `{self.site_id}`...")
        try:
            command = f"cd {self.client_path} && firebase target:apply hosting {self.site_id} {self.site_id} --token {self.firebase_token}"
            subprocess.run(command, shell=True, check=True)
            print("✅ Hosting target applied.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error applying hosting target: {e}")
            raise

    def deploy_hosting(self):
        print(f"🚀 Deploying Firebase hosting for site `{self.site_id}`...")
        try:
            command = f"cd {self.client_path} && firebase deploy --only hosting:{self.site_id} --token {self.firebase_token}"
            subprocess.run(command, shell=True, check=True)
            print("🎉 Firebase hosting deployed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Firebase deployment failed: {e}")
            raise

    def deploy(self, create_if_needed=False):
        print(f"📡 Starting Firebase deployment for: {self.site_id}")
        self.install_firebase_tools()
        self.install_dependencies()
        self.build_client()

        if create_if_needed:
            self.create_site()

        self.apply_hosting_target()
        self.deploy_hosting()
        print(f"✅ All done for `{self.site_id}`.")
