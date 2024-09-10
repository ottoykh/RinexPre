import requests
import os
import concurrent.futures
from datetime import datetime, timedelta


def download_file(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def download_rinex_files(start_date, end_date, stations, output_dir="downloaded_files"):
    base_url = "https://rinex.geodetic.gov.hk/rinex3/2024/{date}/{station}/1s/{station}00HKG_R_2024{date}{hour}00_01H_01S_MO.crx.gz"

    dates = [(start_date + timedelta(days=i)).strftime('%j') for i in range((end_date - start_date).days + 1)]

    os.makedirs(output_dir, exist_ok=True)
    download_tasks = []

    for date in dates:
        for station in stations:
            for hour in range(0, 24):
                hour_str = f"{hour:02d}"
                url = base_url.format(date=date, station=station, hour=hour_str)
                save_path = os.path.join(output_dir, f"{station}00HKG_R_2024{date}{hour_str}00_01H_01S_MO.crx.gz")
                download_tasks.append((url, save_path))

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(download_file, url, save_path): url for url, save_path in download_tasks}

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as e:
                print(f"{url} generated an exception: {e}")

    return output_dir