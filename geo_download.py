from pathlib import Path
import requests
import tarfile

GEO_ACCESSION = "GSE84133"

download_url = (
    f"https://www.ncbi.nlm.nih.gov/geo/download/"
    f"?acc={GEO_ACCESSION}&format=file"
)

output_dir = Path("geo_data")
output_dir.mkdir(parents=True, exist_ok=True)

tar_path = output_dir / f"{GEO_ACCESSION}_RAW.tar"
extract_dir = output_dir / GEO_ACCESSION / "extracted"


# Download only if the TAR file does not already exist
if tar_path.exists() and tar_path.stat().st_size >= 10_000:
    print(f"{tar_path} already exists. Skipping download.")

else:
    print(f"Downloading {GEO_ACCESSION}...")
    print(f"URL: {download_url}")

    response = requests.get(download_url, stream=True)
    response.raise_for_status()

    with open(tar_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    if tar_path.stat().st_size < 10_000:
        raise RuntimeError(
            "The downloaded file is too small "
            "(possible NCBI server error)."
        )

    print("Download completed.")


# Extract only if the directory does not exist or is empty
if extract_dir.exists() and any(extract_dir.iterdir()):
    print(f"{extract_dir} already contains files. Skipping extraction.")

else:
    extract_dir.mkdir(parents=True, exist_ok=True)

    print("Extracting files...")

    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(extract_dir)

    print("Extraction completed.")


# Show a preview of the extracted files
files = list(extract_dir.rglob("*"))

print("\nFiles currently available:")
for file in files[:10]:
    print(file)