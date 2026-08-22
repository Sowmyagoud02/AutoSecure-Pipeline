from pathlib import Path
from uuid import uuid4
import pandas as pd

from fastapi import UploadFile


ALLOWED_EXTENSIONS = {".csv", ".xlsx"}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class FileValidationError(Exception):
    pass


def validate_file_type(filename: str) -> str:
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise FileValidationError(
            "Only CSV and XLSX files are allowed."
        )

    return extension


def generate_stored_filename(original_filename: str) -> str:
    extension = Path(original_filename).suffix.lower()

    return f"{uuid4().hex}{extension}"

UPLOAD_DIR = Path("backend/storage/uploads")


async def save_uploaded_file(
    file: UploadFile,
    stored_filename: str,
) -> tuple[Path, int]:

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = UPLOAD_DIR / stored_filename

    total_size = 0

    with destination.open("wb") as output:

        while chunk := await file.read(1024 * 1024):

            total_size += len(chunk)

            if total_size > MAX_FILE_SIZE:
                destination.unlink(missing_ok=True)

                raise FileValidationError(
                    "File size exceeds the 10 MB limit."
                )

            output.write(chunk)

    return destination, total_size


def inspect_dataset(
    file_path: Path,
    extension: str,
) -> dict:

    if extension == ".csv":
        dataframe = pd.read_csv(file_path)

    elif extension == ".xlsx":
        dataframe = pd.read_excel(file_path)

    else:
        raise FileValidationError(
            "Unsupported file format."
        )

    return {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "column_names": dataframe.columns.tolist(),
        "missing_values": int(
            dataframe.isnull().sum().sum()
        ),
        "duplicate_rows": int(
            dataframe.duplicated().sum()
        ),
    }