import subprocess
import tempfile

class ApacheConfigurator:
    def __init__(self):
        pass

    def run_command(self, command: str):
        """Chạy lệnh hệ thống và in kết quả."""
        print(f"▶️ Running: {command}")
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e.stderr.decode()}")

    def update_apache_config(self, config_path: str, alias_path: str, alias_target: str, marker: str):
        """Thêm Alias vào Apache config nếu chưa tồn tại."""
        try:
            with open(config_path, 'r') as file:
                lines = file.readlines()

            if any(f"Alias {alias_path}" in line for line in lines):
                print("✅ Alias đã tồn tại.")
                return

            alias_block = (
                f"\nAlias {alias_path} {alias_target}\n"
                f"<Directory {alias_target}>\n"
                f"    Options Indexes FollowSymLinks\n"
                f"    AllowOverride All\n"
                f"    Require all granted\n"
                f"</Directory>\n"
            )

            inserted = False
            for i, line in enumerate(lines):
                if marker in line:
                    lines.insert(i, alias_block)
                    inserted = True
                    break

            if not inserted:
                print("⚠️ Marker not found in config. Appending block at end.")
                lines.append(alias_block)

            # Viết nội dung mới vào file tạm
            with tempfile.NamedTemporaryFile('w', delete=False) as tmpfile:
                tmpfile.writelines(lines)
                tmpfile_path = tmpfile.name

            # Ghi đè file config bằng sudo + tee
            self.run_command(f"sudo tee {config_path} < {tmpfile_path}")

            print("✅ Đã cập nhật Apache config.")

        except Exception as e:
            print(f"❌ Lỗi khi cập nhật Apache config: {e}")

    def restart_services(self):
        """Restart Apache và Supervisor services."""
        print("🔄 Restarting Apache và Supervisor...")
        self.run_command("sudo systemctl restart apache2")
        self.run_command("sudo supervisorctl reread")
        self.run_command("sudo supervisorctl update")
        self.run_command("sudo supervisorctl start laravel-worker:*")

    def add_supervisor_config(self, app_name: str):
        """Thêm Supervisor config cho ứng dụng Laravel."""
        source = f"/var/www/html/{app_name}/server/supervisor/laravel-worker.conf"
        dest = f"/etc/supervisor/conf.d/{app_name}.conf"
        self.run_command(f"sudo cp {source} {dest}")
        print(f"✅ Đã thêm Supervisor config cho {app_name}")
