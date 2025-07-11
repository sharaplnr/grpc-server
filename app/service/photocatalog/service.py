from typing import Iterator

import grpc
import datetime
import internal.pb.photocatalog_pb2_grpc as photocatalog_pb2_grpc
import internal.pb.photocatalog_pb2 as photocatalog_pb2
from grpc import ServicerContext
import google.protobuf.timestamp_pb2 as Timestamp
from app.service.photocatalog.mock_repository import MockRepository, PhotoResponseModel, TimeStampModel
from app.service.photocatalog.protocol import Repository


class PhotoCatalogService(photocatalog_pb2_grpc.PhotoCatalogServiceServicer):

    def __init__(self, repository: Repository):
        self._repository = repository

    def Photo(self, request: photocatalog_pb2.IdRequest, context: ServicerContext) -> photocatalog_pb2.PhotoResponse:
        photo = self._repository.get_photo(request.id)
        if not photo:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Photo with id {request.id} not found!")
            return photocatalog_pb2.PhotoResponse()

        response = photocatalog_pb2.PhotoResponse(
            id=photo.id,
            description=photo.description,
            timestamp=photo.timestamp_pb2.Timestamp(
                seconds=photo.timestamp.seconds,
                nanods=photo.timestamp.nanos
            ),
            content=photo.content
        )

        return response

    def AddPhoto(self, request: photocatalog_pb2.PhotoRequest, context: ServicerContext) -> photocatalog_pb2.PhotoResponse:
        photo_response = photocatalog_pb2.PhotoResponse(
            id=request.id,
            description=request.description,
            content=request.content
        )

        now = timestamp_pb2.Timestamp()
        now.FromDateTime(datetime.datetime.now())
        photo_response.timestamp.CopyFrom(now)

        photo_model = PhotoResponseModel(
            id=photo_response.id,
            description=photo_response.description,
            timestamp=TimeStampModel(
                seconds=photo_response.timestamp.seconds,
                nanos=photo_response.timestamp.nanos
            ),
            content=photo_response.content
        )

        self._repository.add_photo(photo_model)

        return photo_response


    def RandomPhotos(self, request: photocatalog_pb2.CountRequest, context: ServicerContext) -> Iterator[photocatalog_pb2.PhotoResponse]:
        for photo in self._repository.get_random_photos(request.count):
            response = photocatalog_pb2.PhotoResponse(
                id=photo.id,
                description=photo.description,
                timestamp=timestamp_pb2.Timestamp(
                    seconds=photo.timestamp.seconds,
                    nanos=photo.timestamp.nanos
                ),
                content=photo.content
            )
            yield response