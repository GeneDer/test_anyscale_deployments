from ray import serve


@serve.deployment
class App:
    def __call__(self, request):
        return "Hello World!"

app = App.bind()
