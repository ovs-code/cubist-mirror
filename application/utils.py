from enum import IntFlag

import cv2
import numpy as np


class Update(IntFlag):
    """Collection of different config-change types
    For communication between UI and application"""
    EXIT = 0
    FG_STYLE = 1
    BACKGROUND = 2
    BG_STYLE = 3
    RESOLUTION = 4
    START = 5
    BG_TYPE = 6


class Background(IntFlag):
    """Different modes of background segmentation"""
    NO_SEGMENTATION = 0
    SAME_STYLE = 1
    DIFFERENT_STYLE = 2

class OutputMode(IntFlag):
    """Different output modes"""
    WINDOW = 0
    FULLSCREEEN = 1
    VIRTUAL_WEBCAM = 2
    VIDEO = 3


# Random background generation
# means and covariance matrix are determined by experimentation
COV = np.array(
    [[13., 12., 13.],
     [12., 12., 13.],
     [13., 13., 15.]]
)
MEANS = np.array([163., 161., 168.])


def random_image(shape, seed=None):
    if seed is not None:
        np.random.seed(seed)
    # `multivariate_normal` seems to be faster than `normal`,
    # results from `normal` would be godd enough
    return np.random.multivariate_normal(MEANS, COV, shape[:2]).astype(np.uint8)


def generate_background(shape, model, seed=None):
    """Generate a styled background based on random noise"""
    noise = random_image(shape, seed)
    data = dict(image=noise)
    return model.infer(data)['output']


def get_video_resolution(path):
    video = cv2.VideoCapture(path)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    video.release()
    return (height, width)
