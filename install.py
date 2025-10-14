import argparse
import os
import sys
import tempfile
import urllib.request
from pathlib import Path
from zipfile import ZipFile, BadZipFile

DEFAULT_URL = "https://files.consumerfinance.gov/hmda-historic-loan-data/hmda_2017_ca_all-records_labels.zip"

def parse_args():
    p = argparse.ArgumentParser(description="Download and unpack HMDA zip.")
    p.add_argument("--url", default=DEFAULT_URL, help="ZIP URL")
    p.add_argument("--data-dir", default="data", help="Destination directory")
    p.add_argument("--force", action="store_true", help="Redownload even if ZIP exists")
    return p.parse_args()

def download(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading:\n  {url}\n→ {dest}")
    # временный файл, чтобы не оставить полубитый архив при сбое
    with tempfile.NamedTemporaryFile(delete=False, dir=str(dest.parent), suffix=".part") as tmp:
        tmp_path = Path(tmp.name)
        with urllib.request.urlopen(url) as resp, open(tmp_path, "wb") as out:
            # потоково пишем
            chunk = 1024 * 1024
            total = 0
            while True:
                buf = resp.read(chunk)
                if not buf:
                    break
                out.write(buf)
                total += len(buf)
                print(f"\r  downloaded {total/1024/1024:.1f} MB", end="", flush=True)
        print()
    tmp_path.replace(dest)
    if dest.stat().st_size == 0:
        dest.unlink(missing_ok=True)
        raise RuntimeError("Downloaded file is empty")
    print("✓ Downloaded")

def unzip(zip_path: Path, data_dir: Path):
    print(f"Unpacking into: {data_dir}")
    data_dir.mkdir(parents=True, exist_ok=True)
    try:
        with ZipFile(zip_path) as z:
            z.extractall(data_dir)
    except BadZipFile as e:
        raise RuntimeError(f"Bad ZIP file: {e}")
    print("✓ Unpacked")

def main():
    a = parse_args()
    data_dir = Path(a.data_dir)
    zip_name = Path(urllib.request.urlparse(a.url).path).name or "archive.zip"
    zip_path = data_dir / zip_name
    stamp = data_dir / ".hmda_2017_ca_unpacked.stamp"

    try:
        if not zip_path.exists() or a.force:
            if zip_path.exists() and a.force:
                zip_path.unlink()
            download(a.url, zip_path)
        else:
            print(f"ZIP already exists: {zip_path} (use --force to redownload)")

        unzip(zip_path, data_dir)
        stamp.touch()
        print(f"Done. Data ready in: {data_dir}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
