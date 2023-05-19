# TraceReq SDK for Python

This is the Python SDK for [TraceReq](http://tracereq.com/)

---

## Installation

```bash
pip install --upgrade tracereq
```

## Using with Flask

```python
import tracereq

app = Flask(__name__)
tracereq.init(
    flask_wsgi_app=app.wsgi_app,
    token='auth_token'
)
```

Adding the above in all your flask services will start tracing requests within all the services.

## Integrations

- [Flask](https://github.com/pallets/flask)

## License

Licensed under the MIT license, see [`LICENSE`](LICENSE)
