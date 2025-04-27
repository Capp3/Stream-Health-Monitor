# Blackmagic Design Webpresentor API Example

## Device health script

This script is used to poll the local BMD Webpresentor for statistics

```python
import json
import requests

url = f'http://${BMD_WEBPRESENTOR_IP}/control/api/v1/livestreams/0'

try:
    # Setting a timeout (in seconds) to avoid indefinite hanging
    response = requests.get(url, timeout=10)
    # Raise an error for bad HTTP status codes
    response.raise_for_status()

    # Process and print the JSON response in a pretty format

    pretty_json = json.dumps(response.json(), indent=4)
    print(pretty_json)
except requests.exceptions.RequestException as e:
    print(f"Error connecting to the API: {e}")
```

### Example Response

```json

```