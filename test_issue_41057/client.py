import requests


url = "http://0.0.0.0:8000/app"
text_chunk = [str(i) for i in range(5)]


try:
    resp = requests.get(url, json={"items": text_chunk}, timeout=1)
    print("timeout = 1, before client disconnects", resp.text)
except requests.exceptions.ConnectionError:
    print("timeout = 1, client disconnects")

try:
    text_chunk = [str(i) for i in range(5, 8)]
    resp = requests.post(url, json={"items": text_chunk}, timeout=0.005)
    print("timeout = 0.005, before client disconnects", resp.text)
except requests.exceptions.ReadTimeout:
    print("timeout = 0.005, client ReadTimeout")
except requests.exceptions.ConnectionError:
    print("timeout = 0.005, client ConnectionError")

text_chunk = [str(i) for i in range(8, 10)]
resp = requests.post(url, json={"items": text_chunk}, timeout=None)
print("timeout = None, after client disconnects", resp.text)
