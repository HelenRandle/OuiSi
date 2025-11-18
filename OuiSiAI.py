import torch
import torchvision
import clip
from PIL import Image
from load_pretrained_models import load_model
import basic_colormath
from imagedominantcolor import DominantColor
#use basic_colormath get_delta_e(rgb_a: Rgb, rgb_b: Rgb) -> float:


shapeModel = load_model("resnet50_trained_on_SIN")
textureModel = model = torchvision.models.resnet50(pretrained=False)
semanticModel = clip.load() #cosine similarity

