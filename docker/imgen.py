from diffusers import DiffusionPipeline
import torch

pipeline = DiffusionPipeline.from_pretrained("segmind/small-sd", torch_dtype=torch.float32)
