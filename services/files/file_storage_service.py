import json
import os
from typing import Any, Optional

import aiofiles


class FileStorageService:
  def __init__(self, filepath: str):
    self.filepath = filepath
    os.makedirs(os.path.join(os.curdir, filepath), exist_ok=True)

  def file_exists(self, filename: str) -> bool:
    file_path = os.path.join(self.filepath, filename)

    return os.path.exists(file_path)

  async def save_json(self, filename: str, data: Any) -> None:
    file_path = os.path.join(os.curdir, self.filepath, filename)

    async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
      await file.write(data)

  async def load_json(self, filename: str) -> Optional[Any]:
    if not self.file_exists(filename):
      return None

    file_path = os.path.join(os.curdir, self.filepath, filename)

    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
      return json.loads(await file.read())
