#!/usr/bin/env python3

import argparse
import base64
import random
import time

import grpc
import services_pb2
import services_pb2_grpc

IMAGE_PATH = 'Flatirons_Winter_Sunrise_edit_2.jpg'


def doAdd(stub, img, debug=False):
    reply = stub.Add(services_pb2.addMsg(a=5, b=10))
    if debug:
        print("Response is", reply)


def doRawImage(stub, img, debug=False):
    reply = stub.rawImage(services_pb2.rawImageMsg(img=img))
    if debug:
        print("Response is", reply)


def doDotProduct(stub, img, debug=False):
    list_a = [random.random() for _ in range(100)]
    list_b = [random.random() for _ in range(100)]
    reply = stub.dotProduct(services_pb2.dotProductMsg(a=list_a, b=list_b))
    if debug:
        print("Response is", reply)


def doJsonImage(stub, img, debug=False):
    encoded = base64.b64encode(img).decode('utf-8')
    reply = stub.jsonImage(services_pb2.jsonImageMsg(img=encoded))
    if debug:
        print("Response is", reply)


ops = {
    'add': doAdd,
    'rawimage': doRawImage,
    'dotproduct': doDotProduct,
    'jsonimage': doJsonImage,
}

# ---------------------------------------------------------
# Parse command-line arguments
# ---------------------------------------------------------

parser = argparse.ArgumentParser(
    description='gRPC client for measuring server operations'
)
parser.add_argument('host', help='IP address or hostname of the RPC server')
parser.add_argument(
    'cmd',
    type=str.lower,
    choices=list(ops.keys()),
    help='Operation to perform'
)
parser.add_argument('reps', type=int, help='Number of repetitions for measurement')
parser.add_argument('-p', '--port', type=int, default=50051,
                    help='Server port (default: 50051)')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Print the response from the server')
args = parser.parse_args()

# ---------------------------------------------------------
# Connect (one persistent channel, created once)
# ---------------------------------------------------------

addr = f"{args.host}:{args.port}"
print(f"Running {args.reps} reps against {addr}")

channel = grpc.insecure_channel(addr)
stub = services_pb2_grpc.assignmentStub(channel)

# Load the image once, outside the timed region
with open(IMAGE_PATH, 'rb') as f:
    img = f.read()

# Time the requested operation

op = ops[args.cmd]

# One untimed call so channel setup isn't counted
op(stub, img, debug=args.debug)

start = time.perf_counter()
for _ in range(args.reps):
    op(stub, img, debug=args.debug)
delta = ((time.perf_counter() - start) / args.reps) * 1000
print("Took", delta, "ms per operation")
