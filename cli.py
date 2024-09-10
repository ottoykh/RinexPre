import argparse
from datetime import datetime
from RinexPre.rinex_download.downloader import download_rinex_files
from RinexPre.rinex_download.processor import process_rinex_files
from RinexPre.rinex_download.merger import merge_rinex_files

def main():
    parser = argparse.ArgumentParser(description="Download and process RINEX files.")
    parser.add_argument("start_date", type=lambda d: datetime.strptime(d, "%Y-%m-%d"), help="Start date (YYYY-MM-DD)")
    parser.add_argument("end_date", type=lambda d: datetime.strptime(d, "%Y-%m-%d"), help="End date (YYYY-MM-DD)")
    parser.add_argument("stations", nargs="+", help="List of stations")
    parser.add_argument("--crx2rnx", required=True, help="Path to CRX2RNX executable")
    parser.add_argument("--gfzrnx", required=True, help="Path to GFZRNX executable")
    args = parser.parse_args()

    download_dir = download_rinex_files(args.start_date, args.end_date, args.stations)
    processed_dir = process_rinex_files(download_dir, args.crx2rnx, "processed_files")
    merged_dir = merge_rinex_files(processed_dir, "merged_files")

    print(f"Final merged files are in: {merged_dir}")

if __name__ == "__main__":
    main()