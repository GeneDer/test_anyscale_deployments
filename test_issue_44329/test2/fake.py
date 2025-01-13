import sys
from faker import Faker
from ray import serve


@serve.deployment
def create_fake_email():
    print("sys.path!!!!!!: ", sys.path)
    return Faker().email()


app = create_fake_email.bind()
