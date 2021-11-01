# Cubist Mirror

A real-time application using style transfer and segmentation.

## Setup

Install requirements

```bash
pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio===0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
pip install numpy opencv-python Pillow pyvirtualcam web.py imageio
```

Download and extract assets.zip into the main folder and images.zip into `static/`. These contain the pretrained models and can be found in the *Releases section of the repository*

## Running the application

The code can be run with `python run.py <command>`, where command is

 - `application` to run the application
 - `video` to stylize a video file
 - `list` to list all available style models

Append `-h / --help` to get detailed usage information.

## Adding styles

Train new models using script provided here.

Insert `.pth` model into `assets/models/pretrained/style_models/`, the style image into `static/images/` and add the new model to `assets/models/defs/style_model.json`.
