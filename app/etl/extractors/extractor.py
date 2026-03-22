from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path


class Extractor(ABC):
    CACHE_MAX_AGE = timedelta(days=365)

    def __init__(self, base_url=None):
        self.base_url = base_url
        self.data = None
        self.raw_path = Path("app/data/raw")

    @abstractmethod
    def extract(self):
        raise NotImplementedError("Extractor must implement the extract method")

    def _get_latest_file(self):

        if not self.raw_path.exists():
            return None

        files = [f for f in self.raw_path.rglob("*") if f.is_file()]

        if not files:
            return None

        return max(files, key=lambda f: f.stat().st_mtime)

    def _is_file_expired(self, file):

        file_time = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc)
        return datetime.now(timezone.utc) - file_time > self.CACHE_MAX_AGE

    def _write_new_raw_data(self, folder, filename, content):
        now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_path = self.raw_path / folder / f"{now}_{filename}"
        with open(file_path, "wb") as f:
            f.write(content)
        return BytesIO(content)

    def validate(self):
        """Validate extracted data."""
        return self.data is not None

    def get_data(self):
        """Return extracted data."""
        return self.data
