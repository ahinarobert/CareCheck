import argparse
from unittest.mock import patch
from datetime import datetime

import tools
from dry_run import run_dry_check


def run_for_date(fake_date: str):
    fake_now = datetime.strptime(fake_date, "%Y-%m-%d")
    with patch.object(tools, "_today", return_value=fake_now):
        print(f"\nSimulating CareCheck run on: {fake_date}\n")
        run_dry_check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", required=True)
    args = parser.parse_args()
    run_for_date(args.day)