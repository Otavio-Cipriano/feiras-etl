from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path


class Transformer(ABC):
    CACHE_MAX_AGE = timedelta(days=365)

    def __init__(self, staged_path, data, cep_service):
        self.data = data
        self.cep_service = cep_service
        self.staged_path = Path(staged_path)

    @abstractmethod
    def transform(self):
        raise NotImplementedError("Extractor must implement the extract method")

    def _get_latest_file(self):

        if not self.staged_path.exists():
            return None

        files = [f for f in self.staged_path.rglob("*") if f.is_file()]

        if not files:
            return None

        return max(files, key=lambda f: f.stat().st_mtime)

    def _is_file_expired(self, file):

        file_time = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc)
        return datetime.now(timezone.utc) - file_time > self.CACHE_MAX_AGE

    def _write_new_raw_data(self, filename, content):
        now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_path = self.raw_path / f"{now}_{filename}"
        with open(file_path, "wb") as f:
            f.write(content)
        return BytesIO(content)

    def _is_file_expired(self, file):
        if not file.exists():
            return True
        file_time = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc)
        return datetime.now(timezone.utc) - file_time > self.CACHE_MAX_AGE

    def _delete_if_expired(self, file):
        if self._is_file_expired(file):
            file.unlink()

    def get_data(self):
        """Return extracted data."""
        return self.data

    def _write_staged_data(self, filename, df):
        self.staged_path.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_path = self.staged_path / f"{now}_{filename}"
        df.to_csv(file_path, index=False)
        return file_path
