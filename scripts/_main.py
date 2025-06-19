import os
import sys
import argparse
from datetime import datetime
from laravel_deployer import LaravelDeployer
from firebase_deployer import FirebaseDeployer


def parse_args():
    parser = argparse.ArgumentParser(description="🔥 Full deploy script for Laravel & Firebase client")
    parser.add_argument("--with-client", action="store_true", help="Also deploy the Firebase client app")
    parser.add_argument("--no-client", action="store_true", help="Skip client deploy")
    parser.add_argument("--create-firebase-site", action="store_true", help="Create Firebase site if not exists")
    return parser.parse_args()


def generate_site_id(app_id: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{app_id}-{timestamp}"


def main():
    args = parse_args()

    app_id = os.getenv("APP_ID")
    firebase_token = os.getenv("FIREBASE_TOKEN")

    if not app_id:
        raise EnvironmentError("❌ Missing required environment variable: APP_ID")

    print("🔨 Starting deployment process...")

    # Step 1: Laravel Deploy
    print("🚀 Step 1: Laravel Deploy")
    laravel = LaravelDeployer(app_id)
    laravel.deploy()

    # Step 2: Firebase Client Deploy (Optional)
    if args.with_client and not args.no_client:
        print("🌐 Step 2: Firebase Hosting Deploy")
        if not firebase_token:
            raise EnvironmentError("❌ Missing FIREBASE_TOKEN for Firebase deployment")

        site_id = generate_site_id(app_id)
        print(f"🆔 Generated Firebase site_id: {site_id}")

        firebase = FirebaseDeployer(site_id=site_id, firebase_token=firebase_token)
        firebase.deploy(create_if_needed=args.create_firebase_site)

    print("🎉 All deployment steps completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)
