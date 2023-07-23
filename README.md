# TraceReq SDK for Python

This is the Python SDK for [TraceReq](http://tracereq.com/)

---

## Installation

```bash
pip install --upgrade tracereq-sdk
```

## Usage with Flask

```python
import tracereq

app = Flask(__name__)
tracereq.init(api_key='xxx-xxx',
    flask_app=app.wsgi_app
)
```

Adding the above any flask service will start tracing requests.
No other additional code is required.

## Supported Frameworks

- [Flask](https://github.com/pallets/flask)

