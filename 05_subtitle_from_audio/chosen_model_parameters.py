
import torch
from dep_constants import tiny_model, base_model, small_model, medium_model, large_model, large_v2_model

# print("mps available? ", torch.backends.mps.is_available()) #mps is not powerful enough but under development as of 9/2024
# print("mps is built? ", torch.backends.mps.is_built())
# print("mps is built? ", torch.cuda.is_available())
algo_device = "cuda" if torch.cuda.is_available() else "cpu"


# _ CHOOSE AS APPROPRIATE
MODEL = base_model

DEVICE = algo_device # override with a string "cuda", "cpu", etc, or let the script decide for you