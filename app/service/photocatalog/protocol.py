from typing import (
    Protocol,
    Iterator
)

from app.service.photocatalog.mock_repository import PhotoResponseModel


class Repository(Protocol):
    def __init__(self):
        self._photos = []

    def add_photo(self, photo: PhotoResponseModel) -> PhotoResponseModel: ...

    def get_photo(self, id: str) -> PhotoResponseModel | None: ...

    def get_random_photos(self, count: int) -> Iterator[PhotoResponseModel]: ...