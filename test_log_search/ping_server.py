import requests
import time


# Service specific config
base_url = "https://gene-test-service-reconfigure-bxauk.cld-kvedzwag2qa8i5bj.s.anyscaleuserdata.com/app"
token = "PmgpJ_hd1iL84YeqZk7ohW7OM9Xd6-GJzqI0NEe-d_4"

# Requests config
path = "/"
full_url = f"{base_url}{path}"
headers = {"Authorization": f"Bearer {token}"}

while True:
    resp = requests.get(full_url, headers=headers)

    print(resp.text)
    time.sleep(1)
    