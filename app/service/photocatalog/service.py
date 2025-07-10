from typing import Iterator

import internal.pb.photocatalog_pb2_grpc as photocatalog_pb2_grpc
import internal.pb.photocatalog_pb2 as photocatalog_pb2
from grpc import ServicerContext


class PhotoCatalogService(photocatalog_pb2_grpc.PhotoCatalogServiceServicer):
    def Photo(self, request: photocatalog_pb2.IdRequest, context: ServicerContext) -> photocatalog_pb2.PhotoResponse:
        return photocatalog_pb2.PhotoResponse()

    def AddPhoto(self, request: photocatalog_pb2.PhotoRequest, context: ServicerContext) -> photocatalog_pb2.PhotoResponse:
        return photocatalog_pb2.PhotoResponse()

    def RandomPhotos(self, request: photocatalog_pb2.CountRequest, context: ServicerContext) -> Iterator[photocatalog_pb2.PhotoResponse]:
        for photo in range(request.count):
            yield photocatalog_pb2.PhotoResponse()