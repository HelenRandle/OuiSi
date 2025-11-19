import torch
import torchvision
import clip
from PIL import Image
from load_pretrained_models import load_model
import basic_colormath
from imagedominantcolor import DominantColor
from scipy.spatial.distance import cosine
#use basic_colormath get_delta_e(rgb_a: Rgb, rgb_b: Rgb) -> float:


shapeModel = load_model("resnet50_trained_on_SIN")
textureModel = torchvision.models.resnet50(pretrained=False)
semanticModel = clip.load() #cosine similarity

device = "cuda" if torch.cuda.is_available() else "cpu"

function compareTwo(im1, im2):
    """
    Inputs: im1 and im2 strings, filepaths
    Outputs:
    """
    im1CLIP = preprocess(Image.open(im1)).unsqueeze(0).to(device)
    im2CLIP = preprocess(Image.open(im2)).unsqueeze(0).to(device)
    semanticDistance = shapeModel(im1CLIP, im2CLIP)

    #TODO: image 1 and 2 need to get evaluated by texture and semantic model
    textureDistance = 1 - cosine(vector1, vector2) #get vector from lower layer of neural network
    shapeDistance = 1 - cosine(vector1, vector2) #get vector from last layer of neural network
    
    color1 = DominantColor(im1)
    color2 = DominantColor(im2)
    colorDistance =  basic_colormath.get_delta_e(color1, color2)
