import torch
import torchvision
from torch.nn import CosineSimilarity
from torchvision.models.feature_extraction import create_feature_extractor
import clip
from PIL import Image
from load_pretrained_models import load_model
from colorthief import ColorThief
import basic_colormath
from scipy.spatial.distance import cosine
#use basic_colormath get_delta_e(rgb_a: Rgb, rgb_b: Rgb) -> float:

device = "cuda" if torch.cuda.is_available() else "cpu"

# shapeModel = load_model("resnet50_trained_on_SIN")
shapePremodel = torchvision.models.resnet50(pretrained=True)
texturePremodel = torchvision.models.resnet50(pretrained=True)
semanticModel, preprocess = clip.load("ViT-B/32", device=device)

return_texture_nodes = {
    "layer1.1.conv1": "layer1"
}
return_shape_nodes = {
    "layer4.2.conv3": "layer4"
}
textureModel = create_feature_extractor(texturePremodel, return_nodes=return_texture_nodes)
shapeModel = create_feature_extractor(shapePremodel, return_nodes=return_shape_nodes)


def compareTwo(im1Path, im2Path):
    """
    Inputs: im1 and im2 strings, filepaths
    Outputs: int that represents score made of a weighted average of the cossine similarities
    """
    im1 = Image.open(im1Path)
    im2 = Image.open(im2Path)

    #preprocessing
    im1CLIP = preprocess(im1).unsqueeze(0).to(device)
    im2CLIP = preprocess(im2).unsqueeze(0).to(device)
    im1_features = semanticModel.encode_image(im1CLIP)
    im2_features = semanticModel.encode_image(im2CLIP)
    cossim = CosineSimilarity(dim=0, eps=1e-6)
    semanticDistance = cossim(torch.flatten(im1_features), torch.flatten(im2_features)).item()*100
    # print(semanticDistance.item())

    #shape
    im1Shape = torch.flatten(shapeModel(im1CLIP)['layer4'])
    im2Shape = torch.flatten(shapeModel(im2CLIP)['layer4'])
    shapeDistance = cossim(im1Shape, im2Shape).item()*100 #get vector from last layer of neural network
    # print(shapeDistance.item())

    #texture
    im1Texture = torch.flatten(textureModel(im1CLIP)['layer1'])
    im2Texture = torch.flatten(textureModel(im2CLIP)['layer1'])
    textureDistance = cossim(im1Texture, im2Texture).item()*100 #get vector from lower layer of neural network
    # print(textureDistance.item())
    
    #color
    color_thief1 = ColorThief(im1Path)
    color_thief2 = ColorThief(im2Path)
    color1 = color_thief1.get_color(quality=1)
    color2 = color_thief2.get_color(quality=1)
    colorDistance =  basic_colormath.get_delta_e(color1, color2)

    output = semanticDistance*0.2 + shapeDistance*0.52 + textureDistance*0.09 + colorDistance*0.18
    output = output/4
    return output

rootPath = "../Downloads/OuiSiOG"
compareTwo(str(rootPath+"/ouisi-nature-002.jpg"),str(rootPath+"/ouisi-nature-005.jpg"))
