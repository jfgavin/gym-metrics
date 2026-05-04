"""Poll PureGym live person count every POLL_INTERVAL_SECONDS and append to a CSV.

Required env vars:
  PUREGYM_EMAIL   - account email
  PUREGYM_PIN     - numeric PIN

Optional env vars:
  PUREGYM_GYM_ID          - integer gym ID (defaults to your home gym)
  DATA_FILE               - output CSV path (default: gym_counts.csv)
  POLL_INTERVAL_SECONDS   - seconds between polls (default: 300)
"""

import csv
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from gymtools.puregym_api import PureGymClient


def main() -> None:
    email = os.environ["PUREGYM_EMAIL"]
    pin = os.environ["PUREGYM_PIN"]
    raw_gym_id = os.getenv("PUREGYM_GYM_ID")
    data_file = Path(os.getenv("DATA_FILE", "gym_counts.csv"))
    interval = int(os.getenv("POLL_INTERVAL_SECONDS", 300))

    client = PureGymClient(email, pin)

    if raw_gym_id is None:
        gym_id = client.get_home_gym_id()
        print(f"Using home gym ID: {gym_id}")
    else:
        gym_id = int(raw_gym_id)

    write_header = not data_file.exists()
    with open(data_file, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp", "people_in_gym"])

        while True:
            try:
                count = client.get_people_in_gym(gym_id)
                ts = datetime.now(timezone.utc).isoformat()
                writer.writerow([ts, count])
                f.flush()
                print(f"{ts}  {count} people")
            except Exception as e:
                print(f"Error fetching count: {e}")

            time.sleep(interval)


if __name__ == "__main__":
    main()
