import csv
import fitdecode
from itertools import chain
from pathlib import Path
import typer


def main(p: Path):
    fit_files = p.glob("*.fit")
    records = []
    for fit_file in fit_files:
        with fitdecode.FitReader(fit_file) as fit:
            for frame in fit:
                if (
                    isinstance(frame, fitdecode.FitDataMessage)
                    and frame.name == "session"
                ):
                    records.append(
                        {
                            field.name: f"{field.value} {field.units}"
                            for field in frame.fields
                        }
                    )
    headers = set(chain.from_iterable(record.keys() for record in records))
    with open(p / "all.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, headers)
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    typer.run(main)
