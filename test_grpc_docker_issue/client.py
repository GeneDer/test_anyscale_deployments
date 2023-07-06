# Note: `gymnasium` (not `gym`) will be **the** API supported by RLlib from Ray 2.3 on.
try:
    import gymnasium as gym
    gymnasium = True
except Exception:
    import gym
    gymnasium = False

import requests


env = gym.make("CartPole-v1")

for _ in range(5):
    if gymnasium:
        obs, infos = env.reset()
    else:
        obs = env.reset()
    print(f"-> Sending observation {obs}")
    resp = requests.get(
        "http://localhost:8000/", json={"observation": obs.tolist()}
    )
    print(f"<- Received response {resp.json()}")



obs, infos = env.reset()
print(f"-> Sending observation {obs}")
resp = requests.get(
    "http://localhost:8000/", json={"observation": obs.tolist()}
)
print(f"<- Received response {resp.json()}")
