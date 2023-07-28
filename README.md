# TraceReq SDK for Python

[![PyPi page link -- version](https://img.shields.io/pypi/v/tracereq-sdk.svg)](https://pypi.python.org/pypi/tracereq-sdk)

This is the Python SDK for [TraceReq](http://tracereq.com/)

---

## Installation

```bash
pip install --upgrade tracereq-sdk
```

## Usage with Flask

```python
import tracereq_sdk

app = Flask(__name__)
tracereq_sdk.init(api_key='xxx-xxx',
    flask_app=app.wsgi_app
)
```

Adding the above any flask service will start tracing requests.
No other additional code is required.

## Supported Frameworks

- [Flask](https://github.com/pallets/flask)

