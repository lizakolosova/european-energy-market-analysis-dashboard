"""Download the OWID energy dataset to data/raw/."""
import argparse
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import RAW_CSV_PATH

URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"


def download(force: bool = False) -> None:
    if RAW_CSV_PATH.exists() and not force:
        print(f"Already exists: {RAW_CSV_PATH}  (pass --force to re-download)")
        return

    RAW_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {URL} ...")

    try:
        response = requests.get(URL, timeout=60)
        response.raise_for_status()
    except requests.HTTPError as e:
        sys.exit(f"HTTP error: {e}")
    except requests.ConnectionError:
        sys.exit("Connection error — check your internet connection and try again.")
    except requests.Timeout:
        sys.exit("Request timed out after 60 s.")

    RAW_CSV_PATH.write_bytes(response.content)
    size_kb = RAW_CSV_PATH.stat().st_size / 1024
    print(f"Saved {size_kb:.0f} KB -> {RAW_CSV_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Re-download even if file exists")
    download(force=parser.parse_args().force)
