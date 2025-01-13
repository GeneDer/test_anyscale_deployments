import ray
from faker import Faker
from ray import serve


ray.init(address="auto", namespace="example")
serve.start(detached=True, http_options={"host": "0.0.0.0"})

@serve.deployment
def create_fake_email():
    return Faker().email()


app = create_fake_email.bind()

serve.run(app)
