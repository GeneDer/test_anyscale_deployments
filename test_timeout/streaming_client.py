import requests

prompt = "Tell me a story about dogs."

response = requests.post(f"http://localhost:8000/?prompt={prompt}", stream=True)
response.raise_for_status()
print(response.status_code)
for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
    print("status_code", response.status_code)
    print("chunk", chunk, end="")

    # Dogs are the best.
