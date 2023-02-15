from diffusers import StableDiffusionPipeline
import torch
from transformers import pipeline


def get_stable_diffusion_pipe():
    if torch.cuda.is_available():
        pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)
        pipe.to("cuda")
        # Below may not be needed on Graphics cards with more than 8 GB of memory
        pipe.enable_xformers_memory_efficient_attention()
        pipe.enable_attention_slicing()
        pipe.enable_sequential_cpu_offload()
    else:
        pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1")
    return pipe


def get_summarizer_pipe(device=0):
    if not torch.cuda.is_available():
        device = -1
    pipe = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
    return pipe
