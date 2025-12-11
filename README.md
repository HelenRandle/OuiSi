## Introduction
OuiSi is a game where players arrange similar tiles next to each other based on traits such as color or shape. 
There is no winner to OuiSi, but this game framework opens possibilities for latent-space-related computer vision work to create an AI OuiSi player. 
Our version features an AI OuiSi player that identifies OuiSi matches that are almost as good as a human player on average. 
## Setup
To play this version against our AI, you will need to install `tkinter`, `pillow`, `torch`, `torchvision`, `colorthief`, and `CLIP` (instruction on this github: [https://github.com/openai/CLIP](https://github.com/openai/CLIP))
Update the Pathroot variable in OuiSiGUI to the path to your OuiSi folder
## Troubleshooting
You may run into issues where you get a warning about your tk version being deprecated and your board will display wrong, ensure you have a version of tk installed that is NOT the deprecated system version
