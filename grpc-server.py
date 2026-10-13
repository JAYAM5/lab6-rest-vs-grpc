#adapted from https://grpc.io/docs/languages/python/basics/
from concurrent import futures
import logging
import math
import time
from PIL import Image
import io
import argparse
import numpy
import base64

import grpc
import services_pb2
import services_pb2_grpc

class assignment(services_pb2_grpc.assignmentServicer):
    """Provides methods that implement functionality of assignment."""

    def Add(self, request, context):
        result = request.a + request.b
        return services_pb2.addReply(sum=result) 

    def rawImage(self,request,context):
        ioBuffer = io.BytesIO(request.img)
        image = Image.open(ioBuffer)

        width= image.size[0]
        height= image.size[1]

        return services_pb2.imageReply(width=width,height=height)

    def dotProduct(self, request,context):
        result = numpy.dot(request.a,request.b)
        return services_pb2.dotProductReply(dotproduct=result)

    def jsonImage(self,request,context):
        
        data = request.img

        img_bytes = base64.b64decode(data)

        ioBuffer = io.BytesIO(img_bytes)
        img = Image.open(ioBuffer)

        width= img.size[0]
        height= img.size[1]

        return services_pb2.jsonImageReply(width=width,height=height)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_assignmentServicer_to_server(
        assignment(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
