import os
import sys
import argparse
from datetime import datetime
from laravel_deployer import LaravelDeployer
from firebase_deployer import FirebaseDeployer


def parse_args():
    parser = argparse.ArgumentParser(description="🔥 Full deploy script for Laravel & Firebase client")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--laravel-only", action="store_true", help="Only deploy Laravel backend")
    group.add_argument("--client-only", action="store_true", help="Only deploy Firebase client")

    parser.add_argument("--create-firebase-site", action="store_true", help="Create Firebase site if not exists")

    args = parser.parse_args()

    flags = {
        "is_laravel": args.laravel_only or (not args.laravel_only and not args.client_only),
        "is_client": args.client_only or (not args.laravel_only and not args.client_only),
        "create_firebase_site": args.create_firebase_site
    }

    return flags


def generate_site_id(app_id: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{app_id}-{timestamp}"


def main():
    args = parse_args()

    app_id = os.getenv("APP_ID")
    firebase_token = os.getenv("FIREBASE_TOKEN")

    # if not app_id:
    #     raise EnvironmentError("❌ Missing required environment variable: APP_ID")

    print("🔨 Starting deployment process...")

    print(args["is_laravel"])

    if args["is_laravel"]:
        print("🚀 Step 1: Laravel Deploy")
        laravel = LaravelDeployer(app_id)
        laravel.deploy(skip_clone=True)

    elif args["is_client"]:
        if not firebase_token:
            raise EnvironmentError("❌ Missing FIREBASE_TOKEN for Firebase deployment")

        site_id = generate_site_id(app_id)
        print(f"🆔 Generated Firebase site_id: {site_id}")

        firebase = FirebaseDeployer(site_id=site_id, firebase_token=firebase_token)
        firebase.deploy(create_if_needed=args["create_firebase_site"])

    print("🎉 Deployment steps completed successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)
