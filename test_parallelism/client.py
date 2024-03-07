import time
import requests
import concurrent.futures


def send_request(blob):
    s = time.time()
    resp = requests.post(f"http://127.0.0.1:8000/translate", json={"audio": blob})
    print(resp.json())
    return time.time() - s


blob = "foobar"
print(send_request(blob))
print(send_request(blob))
print(send_request(blob))
print(send_request(blob))

time.sleep(3)
print("TEST")
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []
    for i in range(50):
        results.append(executor.submit(send_request, blob))
    print("RESULTS")
    for future in concurrent.futures.as_completed(results):
        result = future.result()
        print(result)
