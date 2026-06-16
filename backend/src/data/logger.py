import csv
from pathlib import Path
from dataclasses import asdict

from src.data.study_log import StudyLog
from src.data.validator import validate_study_log


PATH = Path("data/raw/study_logs.csv")


def save_study_log(log: StudyLog) -> None:

    if not validate_study_log(log):
        raise ValueError("Invalid StudyLog data.")

    PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    log_dict = asdict(log)

    with open(
        PATH,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=log_dict.keys()
        )

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(log_dict)