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

### Use as a virtual webcam

For Windows and macOS OBS can be used to provide a virtual camera:

 - install [OBS](https://obsproject.com/)
 - launch OBS, click *Start Virtual Camera*, then *Stop Virtual Camera*
 - close OBS, now the virtual camera can be used

For Linux further instructions are available at the [pyvirtualcam package](https://github.com/letmaik/pyvirtualcam).
You might need to adjust `CAM_ID` in `application/config.py`.

After setting up the virtual cam, Select *Start Virtual Webcam* at the launch screen to use it.

## Adding styles

Train new models using script provided here.

Insert `.pth` model into `assets/models/pretrained/style_models/`, the style image into `static/images/` and add the new model to `assets/models/defs/style_model.json`.
