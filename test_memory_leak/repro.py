# File name: repro.py

from ray import serve

@serve.deployment
def f():
    return "hi"

app = f.bind()
