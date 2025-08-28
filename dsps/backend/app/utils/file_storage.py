from pathlib import Path
from typing import Optional
from uuid import uuid4
import shutil


def ensure_dir(path: str) -> Path:
	d = Path(path)
	d.mkdir(parents=True, exist_ok=True)
	return d


def save_bytes(data: bytes, dest_dir: str, filename: Optional[str] = None) -> Path:
	dir_path = ensure_dir(dest_dir)
	name = filename or f"{uuid4().hex}"
	full = dir_path / name
	full.write_bytes(data)
	return full


def save_uploadfile(upload_file, dest_dir: str, extension: Optional[str] = None) -> Path:
	"""
	Save a FastAPI UploadFile to disk under dest_dir with a generated unique name.
	`extension` should include the dot, e.g. ".py".
	"""
	dir_path = ensure_dir(dest_dir)
	ext = extension or ""
	name = f"{uuid4().hex}{ext}"
	full = dir_path / name
	with full.open("wb") as out:
		shutil.copyfileobj(upload_file.file, out)
	upload_file.file.seek(0)
	return full