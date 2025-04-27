# Vimeo Stream info examples

## Retrieve and analyse a HLS stream via API

This script uses the vimeo API to get a HLS playback address with authentication and returns a JSON with the m3u8 file link. This link is then passed to FFPROBE for reading and produces a JSON output

```python
mport vimeo
import json
import subprocess

url = f'https://api.vimeo.com/me/live_events/${VIMEO_STREAM_ID}/m3u8_playback'

client = vimeo.VimeoClient(
    token=${VIMEO_API_TOKEN},
    key=${VIMEO_API_KEY},
    secret=${VIMEO_API_SECRET}
)

# Fetch response from Vimeo API
response = client.get(url)

# Check for successful response
if response.status_code != 200:
    print(f"Error: Unable to fetch video data (Status Code: {response.status_code})")
    exit(1)

# Parse response data
response_data = response.json()
print("Vimeo API Response:")
print(json.dumps(response_data, indent=4))  # Pretty-print response

# Extract M3U8 URL
video_url = response_data.get("m3u8_playback_url")
if not video_url:
    print("Error: No playback URL found in response")
    exit(1)

# Construct FFPROBE command
ffprobe_command = [
    "ffprobe",
    "-v", "quiet",  # Suppress unnecessary logs
    "-print_format", "json",  # Output format JSON
    "-show_format",
    "-pretty",
    "-show_streams",
    video_url
]

# Execute FFPROBE command and capture output
try:
    result = subprocess.run(ffprobe_command, capture_output=True, text=True, check=True)
    ffprobe_output = result.stdout
    print("\nFFPROBE JSON Output:")
    print(json.dumps(json.loads(ffprobe_output), indent=4))  # Pretty-print FFPROBE output
except subprocess.CalledProcessError as e:
    print(f"Error executing FFPROBE: {e.stderr}")
    exit(1)
```

### Script Output

```json

```