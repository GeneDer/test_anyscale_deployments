import openai

# import aviary.backend.router_application
system = "You are a helpful assistant."
message = "What are some of the highest rated restaurants in San Francisco?"
system = "Given a target sentence construct the underlying meaning representation\nof the input sentence as a single function with attributes and attribute\nvalues. This function should describe the target string accurately and the\nfunction must be one of the following ['inform', 'request', 'give_opinion',\n'confirm', 'verify_attribute', 'suggest', 'request_explanation',\n'recommend', 'request_attribute'].\n\nThe attributes must be one of the following:\n['name', 'exp_release_date', 'release_year', 'developer', 'esrb', 'rating',\n'genres', 'player_perspective', 'has_multiplayer', 'platforms',\n'available_on_steam', 'has_linux_release', 'has_mac_release', 'specifier']\n"
message = "Here is the target sentence:\nDirt: Showdown from 2012 is a sport racing game for the PlayStation, Xbox, PC rated E 10+ (for Everyone 10 and Older). It's not available on Steam, Linux, or Mac."

# Note: not all arguments are currently supported and will be ignored by the backend.
chat_completion = openai.ChatCompletion.create(
    api_base="http://localhost:8000/v1", api_key="NOT A REAL KEY",
    model="meta-llama/Llama-2-7b-chat-hf",
    # model="test_model",
    messages=[{"role": "system", "content": system}, {"role": "user", "content": message}],
    temperature=0.01
)
print(chat_completion)