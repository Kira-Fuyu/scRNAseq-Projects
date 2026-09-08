from pathlib import Path
import requests
import tarfile

def download(geo_accession):
    download_url = (
        f"https://www.ncbi.nlm.nih.gov/geo/download/"
        f"?acc={geo_accession}&format=file"
    )

    output_dir = Path("geo_data")
    output_dir.mkdir(parents=True, exist_ok=True)

    tar_path = output_dir / f"{geo_accession}_RAW.tar"
    extract_dir = output_dir / geo_accession / "extracted"


    # Download only if the TAR file does not already exist
    if tar_path.exists() and tar_path.stat().st_size >= 10_000:
        print(f"{tar_path} already exists. Skipping download.")

    else:
        print(f"Downloading {geo_accession}...")
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