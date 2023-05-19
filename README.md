# TraceReq SDK for Python

This is the Python SDK for [TraceReq](http://tracereq.com/)

---

## Installation

```bash
pip install --upgrade tracereq
```

## Usage with Flask

```python
import tracereq

app = Flask(__name__)
tracereq.init(
    flask_wsgi_app=app.wsgi_app,
    token='auth_token'
)
```

Adding the above any flask service will start tracing requests.
No other additional code is required.

## Supported Frameworks

- [Flask](https://github.com/pallets/flask)

