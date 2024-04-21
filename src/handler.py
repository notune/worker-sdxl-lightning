""" Example handler file. """

import runpod
from diffusers import StableDiffusionXLPipeline, DPMSolverSinglestepScheduler
import torch
import base64
import io
import time

# If your handler runs inference on a model, load the model here.
# You will want models to be loaded into memory before starting serverless.

try:
    pipe = StableDiffusionXLPipeline.from_single_file("/model.safetensors", torch_dtype=torch.float16, variant="fp16")
    pipe.scheduler = DPMSolverSinglestepScheduler.from_config(
        pipe.scheduler.config,
        use_karras_sigmas=True,
    )
    pipe = pipe.to("cuda")
except RuntimeError:
    quit()

def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']
    prompt = job_input['prompt']

    time_start = time.time()
    num_inference_steps = 5
    guidance_scale = 2
    image = pipe(prompt=prompt,
    width=768,
    height=768,
    num_inference_steps=num_inference_steps,
    guidance_scale=guidance_scale).images[0]
    print(f"Time taken: {time.time() - time_start}")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    return base64.b64encode(image_bytes).decode('utf-8')


runpod.serverless.start({"handler": handler})
