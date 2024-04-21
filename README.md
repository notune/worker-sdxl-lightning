<div align="center">

<h1>SDXL Lightning Worker Template</h1>

A specialized worker template for building custom RunPod Endpoint API workers utilizing the SDXL Lightning model.

</div>

## Example Request

```python
import requests
import base64
from PIL import Image
import io

url = "https://api.runpod.ai/v2/<YOUR_RUNPOD_ID>/runsync"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer <YOUR_TOKEN_HERE>"
}
data = {
    "input": {
        "prompt": "a cute 3d animated cat, pixar style"
    }
}

response = requests.post(url, headers=headers, json=data)

# Check if the response is successful
if response.status_code == 200:
    response_data = response.json()
    if response_data['status'] == 'COMPLETED':
        # Decode the base64 image data
        base64_string = response_data['output']
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        image.show()  # Display the image
        image.save("output_image.png")  # Save the image as a PNG file
    else:
        print("Request was not completed successfully.")
else:
    print(f"Failed to get a valid response. Status code: {response.status_code}")
```
