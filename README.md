<div align="center">

<h1>SDXL Lightning Worker Template</h1>

A specialized worker template for building custom RunPod Endpoint API workers utilizing the SDXL Lightning model.

</div>

## Setup
Prerequisites: Docker & git installed, an sdxl-lightning model as .safetensors file
1. `git clone https://github.com/notune/worker-sdxl-lightning.git`
2. `cd worker-sdxl-lightning`
3. Add model.safetensors to root directory *(optional: if you named it differently change the line `ADD model.safetensors /` in Dockerfile and `pipe = StableDiffusionXLPipeline.from_single_file("/model.safetensors", torch_dtype=torch.float16, variant="fp16")` in src/handler.py)*
4. `sudo DOCKER_BUILDKIT=1 docker build .`
5. For Docker Hub: Create Repo on https://hub.docker.com/
6. `docker login --username=yourhubusername`
7. Copy image-id from recently built image: `docker images`
8. Tag image: `docker tag <image-id> yourhubusername/sdxll-custom:1.0.0`
9. docker push yourhubusername/sdxll-custom:1.0.0
10. create serverless worker on runpod with container image yourhubusername/sdxll-custom:1.0.0

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
