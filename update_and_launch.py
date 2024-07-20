import os
import requests
import zipfile
import io
import subprocess
import json

GITHUB_REPO = "https://api.github.com/repos/mrcafune/Quari"
LATEST_RELEASE_URL = f"{GITHUB_REPO}/releases/latest"
LOCAL_VERSION_FILE = "version.json"
MAIN_SCRIPT = "main.py"

def get_local_version():
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            version_info = json.load(f)
        return version_info.get("version", "0.0.0")
    except FileNotFoundError:
        return "0.0.0"

def get_latest_version():
    response = requests.get(LATEST_RELEASE_URL)
    response.raise_for_status()
    latest_release = response.json()
    return latest_release["tag_name"]

def download_and_extract_update(download_url):
    response = requests.get(download_url)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall()

def update_local_version(version):
    with open(LOCAL_VERSION_FILE, "w") as f:
        json.dump({"version": version}, f)

def main():
    local_version = get_local_version()
    latest_version = get_latest_version()

    if local_version < latest_version:
        print(f"Update available: {latest_version} (current version: {local_version})")
        update_choice = input("Do you want to update? (y/n): ").strip().lower()
        if update_choice == "y":
            # Fetch the latest release data
            response = requests.get(LATEST_RELEASE_URL)
            response.raise_for_status()
            latest_release = response.json()
            download_url = latest_release["zipball_url"]

            print("Downloading and installing update...")
            download_and_extract_update(download_url)
            update_local_version(latest_version)
            print("Update installed successfully.")
        else:
            print("Continuing with the current version.")
    else:
        print("No updates available.")

    # And we're off
    subprocess.run(["python", MAIN_SCRIPT])

if __name__ == "__main__":
    main()
