import os
import gzip
import shutil
import subprocess
import re


def unzip_gz_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".gz"):
            file_path = os.path.join(directory, filename)
            output_file_path = os.path.join(directory, filename[:-3])
            try:
                with gzip.open(file_path, 'rb') as f_in:
                    with open(output_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                print(f"Unzipped: {file_path} to {output_file_path}")
            except Exception as e:
                print(f"Failed to unzip {file_path}: {e}")


def delete_gz_files(directory):
    deleted_count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".gz"):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    print(f"Total .gz files deleted: {deleted_count}")


def convert_crx_to_rnx(input_dir, crx2rnx_path):
    for filename in os.listdir(input_dir):
        if filename.endswith(".crx"):
            input_path = os.path.join(input_dir, filename)
            subprocess.run([crx2rnx_path, input_path])
            os.remove(input_path)
            print(f"Converted {filename} to RINEX format")


def process_rinex_files(input_dir, crx2rnx_path, output_dir, station, year):
    unzip_gz_files(input_dir)
    delete_gz_files(input_dir)
    convert_crx_to_rnx(input_dir, crx2rnx_path)

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".rnx"):
            input_file = os.path.join(input_dir, filename)

            # Extract date and hour from the filename
            match = re.search(r'(\d{3})(\d{2})00', filename)
            if match:
                date = match.group(1)
                hour = match.group(2)

                # Convert hour to alphabetic character (00=a, 01=b, ..., 23=x)
                hour_char = chr(97 + int(hour))

                # Create new filename format
                new_filename = f"{station.lower()}{date}{hour_char}.{year[2:]}o"
                output_file = os.path.join(output_dir, new_filename)

                command = [
                    "wine",
                    "gfzrnx_2.1.9_win10_64.exe",
                    "-finp", input_file,
                    "-fout", output_file,
                    "--version_out", "2"
                ]

                try:
                    result = subprocess.run(command, check=True, capture_output=True, text=True)
                    print(f"Processed: {input_file} -> {output_file}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {input_file}: {e}")
                    print(f"Error output: {e.stderr}")
            else:
                print(f"Couldn't extract date and hour from filename: {filename}")

    return output_dir