import json

import pytest

from .file_storage_service import FileStorageService


@pytest.mark.asyncio
async def test_writing_json_to_file():
  service = FileStorageService("./tests/data")
  data: dict = {"key": "value"}
  filename = "data.json"
  result = await service.save_json(filename, json.dumps(data, indent=2))
  assert result is None


@pytest.mark.asyncio
async def test_read_json_from_file():
  service = FileStorageService("./tests/data")
  filename = "data.json"
  result = await service.load_json(filename)
  assert result == {"key": "value"}


def test_if_file_exists():
  service = FileStorageService("./tests/data")
  filename = "data.json"
  result = service.file_exists(filename)
  assert result is True
