import os
import re
import subprocess

def merge_rinex_files(input_dir, output_dir, station, year):
    os.makedirs(output_dir, exist_ok=True)

    station = station.lower()
    year_short = year[-2:]

    processed_dates = set()
    file_pattern = rf'{station}(\d{{3}})[a-x]\.{year_short}o'

    for file in os.listdir(input_dir):
        match = re.match(file_pattern, file)
        if match:
            date = match.group(1)
            if date not in processed_dates:
                input_pattern = os.path.join(input_dir, f"{station}{date}[a-x].{year_short}o")
                output_file = os.path.join(output_dir, f"{station}{date}0.{year_short}o")

                command = [
                    "wine",
                    "gfzrnx_2.1.9_win10_64.exe",
                    "-finp", input_pattern,
                    "-fout", output_file,
                    "--version_out", "2"
                ]

                try:
                    result = subprocess.run(command, check=True, capture_output=True, text=True)
                    print(f"Merged files for date {date}: {output_file}")
                    processed_dates.add(date)
                except subprocess.CalledProcessError as e:
                    print(f"Error merging files for date {date}: {e}")
                    print(f"Error output: {e.stderr}")

    return output_dir
