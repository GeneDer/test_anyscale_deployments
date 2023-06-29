import ray
from utils import test
import os
import sys

print(f"1: current dir: {os.getcwd()}, sys.path: {sys.path}")
test.hello()

@ray.remote
def foo():
    print(f"2: current dir: {os.getcwd()}, sys.path: {sys.path}")
    test.hello()


ray.get(foo.remote())
