from geo_download import download
from pathlib import Path

geo_accession = "GSE84133"
download(geo_accession)
geo_data_dir = Path(f"geo_data/{geo_accession}/extracted")

human_files = []
for geo_file in geo_data_dir.iterdir():
    if geo_file.is_file():
        if "human" in geo_file.name.lower():
            human_files.append(geo_file)

human_files = sorted(human_files)

if len(human_files) == 0:
  raise RuntimeError(
      "No files matching 'human' were found in the extracted archive. "
      f"Files actually present: {human_files}. "
      "GEO occasionally changes file naming between dataset versions. "
      "Check the printed filenames above and adjust the filter if needed."
  )

print("Human sample files we'll use:")
for f in human_files:
  print(" -", f)